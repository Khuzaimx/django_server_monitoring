import paramiko
import os
import sys

def main():
    local_path = r"c:\Users\elmir\Desktop\experiment\psych_experiment_platform\backend\groups\serializers.py"
    remote_path = "/home/sj/psych_experiment_platform/backend/groups/serializers.py"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to VM...")
    ssh.connect( )

    sftp = ssh.open_sftp()
    print(f"Uploading {local_path} -> {remote_path}...")
    sftp.put(local_path, remote_path)
    sftp.close()

    print("Restarting backend container to apply serializer changes...")
    stdin, stdout, stderr = ssh.exec_command("cd /home/sj/psych_experiment_platform && docker compose restart backend")
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))

    ssh.close()
    print("Serializer synced and backend container restarted successfully!")

if __name__ == "__main__":
    main()
