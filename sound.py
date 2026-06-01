import os, subprocess

# Thanks to Brandon Morris and HaelDB for the sound.
# https://opengameart.org/content/completion-sound
audio_path = os.path.join(os.path.dirname(__file__), "complete.oga")
# alternative:
# "/usr/share/sounds/freedesktop/stereo/complete.oga"

def play_finish_sound():
    try:
        subprocess.Popen(["paplay", audio_path])
    except FileNotFoundError:
        print("Could not find paplay. Install it with:\nsudo apt install pulseaudio-utils")
