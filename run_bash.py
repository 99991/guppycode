import os
import config
import subprocess
import shlex
import truncate

nvidia_args_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvidia.txt")

if config.args.nvidia_args:
    nvidia_args_path = config.args.nvidia_args

with open(nvidia_args_path) as f:
    nvidia_args = []
    for line in f:
        if line.strip():
            nvidia_args.extend(line.strip().split(maxsplit=1))

if config.args.remote:
    if not config.args.sshkey:
        print("--remote requires --sshkey <path>")
        exit(1)

    if not config.args.directory:
        print("--remote requires --directory <path>")
        exit(1)

    try:
        import paramiko
    except ImportError:
        print("--remote requires\n\n\tpip install paramiko")
        exit(1)

    username, host = config.args.remote.split("@")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(
        host,
        username=username,
        key_filename=config.args.sshkey,
        allow_agent=False,
        look_for_keys=False,
    )

def run_bash(command_str: str, limit: bool=True) -> str:
    command = []

    if not config.args.dangerous_no_sandbox:
        directory = config.args.directory if config.args.directory else os.getcwd()

        sandboxing_args = [
            "--security-opt", "no-new-privileges",
            "--cap-drop=ALL",
            "--memory", config.args.memory,
            "--memory-swap", config.args.memory,
            f"--cpus={config.args.cpus}",
        ]

        if config.args.no_network:
            sandboxing_args.append("--network=none")

        command = [
            "docker",
            "run",
            "--rm",
            "--volume", directory + ":/work",
            "-w", "/work",
        ]

        command += sandboxing_args

        if config.args.nvidia:
            command += nvidia_args

        if config.args.docker_arg:
            for arg in config.args.docker_arg:
                command += shlex.split(arg)

        command.append(config.args.docker_image)

    command += ["bash", "-c", command_str]

    if config.args.remote:
        command = " ".join(shlex.quote(arg) for arg in command)
        stdin, stdout, stderr = client.exec_command(command, timeout=config.args.timeout)
        stdin.close()

        stdout_text = stdout.read().decode("utf-8", errors="replace")
        stderr_text = stderr.read().decode("utf-8", errors="replace")

        returncode = stdout.channel.recv_exit_status()
    else:
        try:
            result = subprocess.run(command, capture_output=True, timeout=config.args.timeout)
            stdout_text = result.stdout.decode("utf-8", errors="replace")
            stderr_text = result.stderr.decode("utf-8", errors="replace")
            returncode = result.returncode
        except subprocess.TimeoutExpired as e:
            return f"ERROR: Command {command} took longer than allowed maximum time of {config.args.timeout} seconds and has been canceled."

    lines_to_remove = [
        "bash: cannot set terminal process group (-1): Inappropriate ioctl for device",
        "bash: no job control in this shell",
    ]

    lines = (stdout_text + stderr_text).split("\n")

    lines = [line for line in lines if line not in lines_to_remove]

    output = "\n".join(lines)

    if returncode != 0:
        output = f"[ERROR: exit code {returncode} for `{command_str}`]\n" + output

    return truncate.truncate(output) if limit else output

def test():
    assert run_bash("echo foo") == "foo\n"

if __name__ == "__main__":
    test()
