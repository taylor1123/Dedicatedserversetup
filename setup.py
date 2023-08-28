from cx_Freeze import setup, Executable

setup(
    name="YourAppName",
    version="0.1",
    description="dedicated server set up",
    executables=[Executable("main.py")]
)
