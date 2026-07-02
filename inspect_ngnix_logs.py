import paramiko
import sys

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

   

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password, timeout=15)
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    try:
        print("\n--- Fetching Nginx Container Logs (Last 100 lines) ---")
        stdin, stdout, stderr = ssh.exec_command(f"cd {remote_base} && docker compose logs nginx --tail=100")
        print(stdout.read().decode('utf-8', errors='replace'))
        print(stderr.read().decode('utf-8', errors='replace'))

    finally:
        ssh.close()

if __name__ == '__main__':
    main()
