import os
import shutil
from datetime import datetime

def ensure_backup_dir(backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def rotate_backups(backup_dir, num_backups_to_keep, extension):
    backups = sorted(
        [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.lower().endswith(extension.lower())],
        key=lambda x: os.path.getmtime(x),
        reverse=True
    )
    if len(backups) > num_backups_to_keep:
        for old_backup in backups[num_backups_to_keep:]:
            os.remove(old_backup)

def create_backup(monitored_file, backup_dir):
    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%Mm%Ss")
    filename = os.path.basename(monitored_file)
    name, ext = os.path.splitext(filename)
    backup_file = f"{name}_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_file)
    shutil.copy2(monitored_file, backup_path)
    return backup_path
