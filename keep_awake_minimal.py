import ctypes
import time

# Windows execution state flags
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

# Keep PC awake
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
print("[keep_awake] Active. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print("\n[keep_awake] Released.")