import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "includes": ["os", "customtkinter", "tkinter", "PIL", "minecraft_launcher_lib", "subprocess", "threading", "configparser", "uuid", "requests", "zipfile", "time"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if (sys.platform == "win32"):
    base = "Win32GUI"    # Tells the build script to hide the console.

setup(
    name="Astro Launcher",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=[Executable("launcher.py", base=base, icon="assets/icon.ico")],)