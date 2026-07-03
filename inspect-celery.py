import paramiko
import sys

def run_ssh_command(ssh, cmd):
    print(f"\nExecuting: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    
    print("=== STDOUT ===")
    print(out.strip() if out.strip() else "(Empty)")
    print("=== STDERR ===")
    print(err.strip() if err.strip() else "(Empty)")
    return out, err

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    hostname = " "
    username = " "
    password = " "
    remote_base = " "

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to remote VM {hostname}...")
        ssh.connect(hostname, username=username, password=password, timeout=15)
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    try:
        # Check Celery Beat logs
        print("\n=== Celery Beat Logs ===")
        run_ssh_command(ssh, f"cd {remote_base} && docker compose logs --tail=200 celery_beat")

        # Check Celery Worker logs
        print("\n=== Celery Worker Logs ===")
        run_ssh_command(ssh, f"cd {remote_base} && docker compose logs --tail=200 celery_worker")

    finally:
        ssh.close()

if __name__ == "__main__":
    main()
