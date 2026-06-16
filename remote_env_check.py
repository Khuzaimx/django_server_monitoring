import paramiko
import sys

def main():
    hostname = "50...."
    username = "s....."
    password = "9......"
    remote_base = "/home/..."

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password, timeout=15)
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    try:
        stdin, stdout, stderr = ssh.exec_command(f"cat {remote_base}/.env")
        print("=== REMOTE .ENV ===")
        print(stdout.read().decode('utf-8'))
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
