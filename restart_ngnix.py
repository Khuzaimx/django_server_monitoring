import paramiko
import sys

def main():
    hostname = ""
    username = ""
    password = "9"
    remote_base = "/home/"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to remote VM {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=15)
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    print("\n--- Restarting nginx container ---")
    cmd_nginx = f"cd {remote_base} && docker compose restart nginx"
    stdin, stdout, stderr = ssh.exec_command(cmd_nginx)
    print("=== nginx restart stdout ===")
    print(stdout.read().decode('utf-8', errors='ignore'))
    print("=== nginx restart stderr ===")
    print(stderr.read().decode('utf-8', errors='ignore'))

    ssh.close()

if __name__ == '__main__':
    main()
