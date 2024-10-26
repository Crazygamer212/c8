import subprocess
import threading
import os
import signal

# Global variable to keep track of the beep process
_beep_process = None

def startBeep(frequency=440):
    global _beep_process

    # ALSA speaker-test command with sine wave
    def beep():
        global _beep_process
        _beep_process = subprocess.Popen(
            ["speaker-test", "--frequency", str(frequency), "--test", "sine"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    # Start the beep in a new thread to allow stopping
    threading.Thread(target=beep, daemon=True).start()

def endBeep():
    global _beep_process
    if _beep_process:
        os.kill(_beep_process.pid, signal.SIGKILL)  # Forcefully kill the beep
        _beep_process = None

# Example usage:
# startBeep(1000)  # Starts a beep at 1000 Hz
# endBeep()  # Stops the beep


if __name__ == "__main__":
    while True:
        input("toPlay:")
        startBeep(333)
        input("toStop:")
        endBeep()