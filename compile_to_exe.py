import subprocess
import sys
import os
import shutil  # Add this line to import the shutil module

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
        
        # Delete the build folder
        build_dir = os.path.join(os.path.dirname(spec_path), 'build')
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
            print("Build folder deleted.")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")

if __name__ == "__main__":
    spec_path = "CastToTv.spec"  # Path to your .spec file
    compile_to_exe(spec_path)
