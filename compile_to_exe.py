import subprocess
import sys
import os

def compile_to_exe(spec_path):
    if not os.path.exists(spec_path):
        print(f"Error: The spec file {spec_path} does not exist.")
        return

    command = [
        sys.executable, '-m', 'PyInstaller',
        spec_path
    ]

    try:
        subprocess.run(command, check=True)
        print("Compilation successful. The executable is located in the 'dist' directory.")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")

if __name__ == "__main__":
    spec_path = "CastToTv.spec"  # Path to your .spec file
    compile_to_exe(spec_path)
