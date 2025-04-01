import argparse
import distutils
import errno
import os
import random
import shutil
import string
import subprocess
import time

STOP_BITNAMI = ['/opt/bitnami/ctlscript.sh', 'stop', 'apache']
START_BITNAMI = ['/opt/bitnami/ctlscript.sh', 'start', 'apache']

def process_settings():
    parser = argparse.ArgumentParser(
        prog='deployer',
        description='Utility for setting up a bitnami instance'
    )
    parser.add_argument('-c', '--certificate', help='ARN for the SSL certificate in ACM', required=True)
    parser.add_argument('-r', '--repo', help='Git repository (.git path) for the htdocs contents', required=True)
    parser.add_argument('-t', '--htdocs', help='Root directory for htdocs', required=True)
    return parser.parse_args()

def execute_command(cmd, cwd=None, capture_output=False):
    print(' '.join(cmd))
    if len(cmd) > 0:
        return subprocess.run(cmd, cwd=cwd, capture_output=capture_output)

def create_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)

def find_first_subfolder(folder):
    with os.scandir(folder) as it:
        for entry in it:
            if not entry.name.startswith('.') and not entry.is_file():
                return entry.name
    return None

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

settings = process_settings()

print('Stopping Bitnami...')
execute_command(STOP_BITNAMI)

# download latest site code
print('Downloading htdocs from git...')
create_directory('tmp')
clear_directory('tmp')
execute_command(['git', 'clone', settings.repo], 'tmp')

# copy site code to htdocs
print('Copying to htdocs folder...')
repo_folder = find_first_subfolder('tmp')
print(repo_folder)
clear_directory(settings.htdocs)
shutil.copytree(os.getcwd() + '/tmp/' + repo_folder, settings.htdocs, dirs_exist_ok=True)
clear_directory('tmp')

# download SSL certificate
# TODO

# deploy SSL certificate
# TODO

time.sleep(5) # wait for Bitnami to be ready to restart

print('Starting Bitnami...')
execute_command(START_BITNAMI)
