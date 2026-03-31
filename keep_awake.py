"""
keep_awake.py
Prevents Windows from sleeping using SetThreadExecutionState — the same
method used by video players and presentation apps. No mouse tricks needed.

Usage:
  python keep_awake.py                # keeps screen + system awake until Ctrl+C
  python keep_awake.py --system-only  # allow screen to dim, but prevent sleep
"""

import ctypes
import time
import argparse

# Windows execution state flags
ES_CONTINUOUS       = 0x80000000  # keep state until explicitly cleared
ES_SYSTEM_REQUIRED  = 0x00000001  # prevent system sleep
ES_DISPLAY_REQUIRED = 0x00000002  # prevent screen from turning off

def set_awake(keep_display_on=True):
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    if keep_display_on:
        flags |= ES_DISPLAY_REQUIRED
    result = ctypes.windll.kernel32.SetThreadExecutionState(flags)
    if result == 0:
        print("[keep_awake] WARNING: SetThreadExecutionState failed. Try running as administrator.")
    return result != 0

def clear_awake():
    """Release the hold — lets Windows sleep normally again."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def main():
    parser = argparse.ArgumentParser(description="Prevent Windows from sleeping.")
    parser.add_argument("--system-only", action="store_true",
                        help="Prevent sleep but allow screen to dim/turn off")
    args = parser.parse_args()

    keep_display = not args.system_only
    mode = "screen + system" if keep_display else "system only (screen may dim)"

    if set_awake(keep_display_on=keep_display):
        print(f"[keep_awake] Active — blocking sleep ({mode}). Press Ctrl+C to stop.")
    else:
        print("[keep_awake] Could not set execution state. Exiting.")
        return

    try:
        while True:
            time.sleep(60)  # just keeps the process alive; Windows does the rest
    except KeyboardInterrupt:
        pass
    finally:
        clear_awake()
        print("\n[keep_awake] Released. Windows will sleep normally again.")

if __name__ == "__main__":
    main()