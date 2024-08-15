import sys
import platform

def is_windows_platform():
    return platform.system() == "Windows"

def is_posix_platform():
    return platform.system() in ["Darwin", "Linux"]