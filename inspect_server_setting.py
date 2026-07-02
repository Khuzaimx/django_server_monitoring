import paramiko
import sys

def run_ssh_command(ssh, cmd):
    print(f"\nRunning: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    exit_status = stdout.channel.recv_exit_status()
    print(f"Exit status: {exit_status}")
    if out:
        print("Stdout:", out)
    if err:
        print("Stderr:", err)
    return exit_status == 0

def main():
   

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password, timeout=15)
        print("Connected successfully!")

        print("\n--- Listing directories and files under letsencrypt ---")
        run_ssh_command(ssh, "ls -la /etc/letsencrypt/")
        run_ssh_command(ssh, "ls -la /etc/letsencrypt/live/")
        run_ssh_command(ssh, "ls -la /etc/letsencrypt/archive/")
        run_ssh_command(ssh, "ls -la /etc/letsencrypt/live/psycheversity.com/")
        
        # Test if we can read the file as root on host
        run_ssh_command(ssh, "head -n 2 /etc/letsencrypt/live/psycheversity.com/fullchain.pem")

        # Test if docker can read it inside a test container
        run_ssh_command(ssh, "docker run --rm -v /etc/letsencrypt:/etc/letsencrypt:ro alpine head -n 2 /etc/letsencrypt/live/psycheversity.com/fullchain.pem")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
