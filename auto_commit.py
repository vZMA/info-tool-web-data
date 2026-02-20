import os, time, subprocess, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.system('git pull')
os.system('git add -A')

def generate_commit_message():
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    output = result.stdout

    added = []
    modified = []
    deleted = []
    renamed = []

    for line in output.splitlines():
        if line.startswith('A '):
            added.append(line[3:])
        elif line.startswith('M '):
            modified.append(line[3:])
        elif line.startswith('D '):
            deleted.append(line[3:])
        elif line.startswith('R '):
            match = re.match(r'R\s+(.+?)\s+->\s+(.+)', line)
            if match:
                renamed.append(f'{match.group(1)}->{match.group(2)}')


    message_parts = []
    if added:
        message_parts.append(f"Added {', '.join(added)}")
    if modified:
        message_parts.append(f"Modified {', '.join(modified)}")
    if deleted:
        message_parts.append(f"Deleted: {', '.join(deleted)}")
    if renamed:
        message_parts.append(f"Renamed: {', '.join(renamed)}")

    out = '. '.join(message_parts) if message_parts else 'No changes to commit'

    return out.replace('\"', '\'')

commit_message = input('Manual commit message: ')
if len(commit_message) == 0:
    commit_message = generate_commit_message() 

os.system('git commit -m \"' + commit_message + '\"')
os.system('git push origin main')