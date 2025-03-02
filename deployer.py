import argparse
import subprocess

STOP_BITNAMI = ['/opt/bitnami/ctlscript.sh', 'stop', 'apache']
START_BITNAMI = ['/opt/bitnami/ctlscript.sh', 'start', 'apache']

def process_settings():
    parser = argparse.ArgumentParser(
        prog='deployer',
        description='Utility for setting up a bitnami instance'
    )
    parser.add_argument('-c', '--certificate', help='S3 Bucket path for the SSL certificate', required=True)
    parser.add_argument('-r', '--repo', help='Git repository for the htdocs contents', required=True)
    return parser.parse_args()

def execute_command(cmd):
    return subprocess.run(cmd)

settings = process_settings()

print('Stopping Bitnami...')
execute_command(STOP_BITNAMI)

# download latest site code

# copy site code to htdocs

# download SSL certificate

# deploy SSL certificate

print('Starting Bitnami...')
execute_command(START_BITNAMI)
