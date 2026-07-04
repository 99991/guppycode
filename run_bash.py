import os
import config
import subprocess
import truncate

nvidia_args = """
--device /dev/nvidia0
--device /dev/nvidiactl
--device /dev/nvidia-modeset
--device /dev/nvidia-uvm
--device /dev/nvidia-uvm-tools
-v /usr/bin/nvcc:/usr/bin/nvcc:ro
-v /usr/lib/nsight-compute:/usr/lib/nsight-compute:ro
-v /usr/lib/x86_64-linux-gnu/nsight-compute:/usr/lib/x86_64-linux-gnu/nsight-compute:ro
-v /usr/bin/cudafe++:/usr/bin/cudafe++:ro
-v /usr/bin/ptxas:/usr/bin/ptxas:ro
-v /usr/bin/fatbinary:/usr/bin/fatbinary:ro
-v /usr/bin/nvlink:/usr/bin/nvlink:ro
-v /usr/bin/cuobjdump:/usr/bin/cuobjdump:ro
-v /usr/bin/nvprune:/usr/bin/nvprune:ro
-v /usr/bin/nvdisasm:/usr/bin/nvdisasm:ro
-v /usr/bin/gcc-12:/usr/bin/gcc-12:ro
-v /usr/bin/g++-12:/usr/bin/g++-12:ro
-v /usr/lib/gcc:/usr/lib/gcc:ro
-v /usr/include/c++/12:/usr/include/c++/12:ro
-v /usr/include/x86_64-linux-gnu/c++/12:/usr/include/x86_64-linux-gnu/c++/12:ro
-v /usr/lib/nvidia-cuda-toolkit:/usr/lib/nvidia-cuda-toolkit:ro
-v /usr/lib/cuda:/usr/lib/cuda:ro
-v /usr/include:/usr/include:ro
-v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi:ro
-v /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:ro
-v /lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu:ro
-e CUDA_HOME=/usr/lib/cuda
-e PATH=/home/testuser/testenv/bin:/usr/lib/nsight-compute:/usr/lib/nvidia-cuda-toolkit/bin:/usr/lib/cuda/bin:/usr/bin
-e LD_LIBRARY_PATH=/usr/lib/cuda/lib64:/usr/lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu
""".strip().split()

def run_bash(command_str: str) -> str:
    command = []

    if not config.args.dangerous_no_sandbox:
        current_directory = os.getcwd()

        sandboxing_args = [
            "--security-opt", "no-new-privileges",
            "--cap-drop=ALL",
            "--memory", "8192m",
            "--memory-swap", "8192m",
            "--cpus=1",
        ]

        if config.args.no_network:
            sandboxing_args.append("--network=none")

        command = [
            "docker",
            "run",
            "--rm",
            "--volume", current_directory + ":/work",
            "-w", "/work",
        ]

        command += sandboxing_args

        if config.args.nvidia:
            command += nvidia_args

        if config.args.docker_arg:
            command += config.args.docker_arg

        command.append(config.args.docker_image)

    command += ["bash", "-c", command_str]

    try:
        result = subprocess.run(command, capture_output=True, timeout=config.args.timeout)
    except subprocess.TimeoutExpired as e:
        return f"ERROR: Command {command} took longer than allowed maximum time of {config.args.timeout} seconds and has been canceled."

    lines_to_remove = [
        "bash: cannot set terminal process group (-1): Inappropriate ioctl for device",
        "bash: no job control in this shell",
    ]

    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")

    lines = (stdout + stderr).split("\n")

    lines = [line for line in lines if line not in lines_to_remove]

    output = "\n".join(lines)

    if result.returncode != 0:
        output = f"[ERROR: exit code {result.returncode} for `{command_str}`]\n" + output

    return truncate.truncate(output)

def test():
    assert run_bash("echo foo") == "foo\n"

if __name__ == "__main__":
    test()
