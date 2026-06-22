import paramiko
import sys
import os
import subprocess

def get_git_commits():
    try:
        res = subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True, check=True)
        return int(res.stdout.strip())
    except Exception:
        return "Unknown"

def count_lines_of_code(directory, extensions):
    total_lines = 0
    total_files = 0
    for root, dirs, files in os.walk(directory):
        if any(exclude in root for exclude in [".git", "node_modules", "venv", ".venv", "dist", "build", "staticfiles", "__pycache__"]):
            continue
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                total_files += 1
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    pass
    return total_files, total_lines

def query_remote_database():
    hostname = "50"
    username = "sj"
    password = ""
    remote_base = "/home"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password, timeout=15)
    except Exception as e:
        print(f"SSH Connection failed: {e}")
        return {}

    python_inspect_code = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from activities.models import Submission, Activity
from questionnaires.models import ResponseSet
from groups.models import Group

User = get_user_model()
print(f"USERS_COUNT:{User.objects.count()}")
print(f"SUBMISSIONS_COUNT:{Submission.objects.count()}")
print(f"RESPONSESETS_COUNT:{ResponseSet.objects.count()}")
print(f"GROUPS_COUNT:{Group.objects.count()}")
print(f"ACTIVITIES_COUNT:{Activity.objects.count()}")
"""

    try:
        sftp = ssh.open_sftp()
        with sftp.file(f"{remote_base}/backend/inspect_metrics_temp.py", "w") as f:
            f.write(python_inspect_code)
        sftp.close()

        cmd_run = f"cd {remote_base} && docker compose exec -T backend python inspect_metrics_temp.py"
        stdin, stdout, stderr = ssh.exec_command(cmd_run)
        
        out = stdout.read().decode('utf-8', errors='ignore')
        ssh.exec_command(f"rm {remote_base}/backend/inspect_metrics_temp.py")
        
        results = {}
        for line in out.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                results[k.strip()] = int(v.strip())
        return results
    finally:
        ssh.close()

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    print("Analyzing codebase metrics...")
    
    local_base = r"c:\Users\elmir\Desktop\experiment\psych_experiment_platform"
    
    # 1. Commits count
    commits = get_git_commits()
    
    # 2. LOC Backend (Python)
    py_files, py_loc = count_lines_of_code(os.path.join(local_base, "backend"), [".py"])
    
    # 3. LOC Frontend (TSX, TS, CSS)
    fe_files, fe_loc = count_lines_of_code(os.path.join(local_base, "frontend", "src"), [".ts", ".tsx", ".css"])
    
    # 4. Query DB
    print("Connecting to VM Database...")
    db_metrics = query_remote_database()
    
    print("\n================ PROJECT METRICS ================")
    print(f"Total Git Commits: {commits}")
    print(f"Backend Python Files: {py_files} | Total LOC: {py_loc}")
    print(f"Frontend TS/TSX/CSS Files: {fe_files} | Total LOC: {fe_loc}")
    print("\n=== Remote VM Database Counts ===")
    for k, v in db_metrics.items():
        print(f"{k}: {v}")
    print("=================================================")

if __name__ == "__main__":
    main()
