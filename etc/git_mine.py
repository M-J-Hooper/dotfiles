import os
import re
import git
import hashlib
import time
from datetime import datetime

l = r = '---'
pattern = re.compile(r'^0000')
repo = git.Repo('.')
c = repo.head.commit

# Without this, post-commit hook loops forever
if pattern.match(c.hexsha):
    exit('Nothing to do...')

config = repo.config_reader()
name = config.get_value('user', 'name')
email = config.get_value('user', 'email')
author = f'{c.author.name} <{c.author.email}>'
committer = f'{name} <{email}>'

# Avoid messing with other people's commits when rebasing
if author != committer:
    exit('Not mine...')

# This is pretty shady but lets post-commit hook work in rebases...
cherry = './.git/CHERRY_PICK_HEAD'
if os.path.isfile(cherry):
    os.remove(cherry)

author_offset = int(c.author_tz_offset / -3600)
committer_offset = int(datetime.now().astimezone().utcoffset().total_seconds() / 3600)

t_start = datetime.now().timestamp()
t_author = int(c.authored_datetime.timestamp())
t_commit = int(t_start) + 1

# Template for `git cat-file commit HEAD` output of hypothetical commit
template = f'tree {c.tree.hexsha}'
for parent in c.parents:
    template += f'\nparent {parent.hexsha}'

template += f'\nauthor {author} {t_author} {author_offset:+03d}00'
template += f'\ncommitter {committer} {{}} {committer_offset:+03d}00'
template += f'\n\n{{}}\n'

# Avoid duplicating footer
msg = new_msg = re.sub(f'{l}\\d+{r}', '', c.message).strip()

n = 0
sha = 'TBD'
while not pattern.match(sha):
    n += 1
    if n % 100000 == 0:
        # Make sure commit timestamp is in the future
        t_commit = int(datetime.now().timestamp()) + 1
        print(f'Attempt {n} to commit at {t_commit}: {sha}')

    # Construct cat-file output from template including footer
    new_msg = f'{msg}\n\n{l}{n}{r}'
    cat_file = template.format(t_commit, new_msg)

    # Add NUL-terminated header
    byte_len = len(cat_file.encode())
    sha_input = f'commit {byte_len}\0{cat_file}'

    # Predict hash of future commit
    sha = hashlib.sha1(sha_input.encode()).hexdigest()


print(f'\n{l}{n}{r}> {sha}\n')

dt = datetime.now().timestamp() - t_start
if dt > 0.01:
    print(f'Took {dt:.2f}s (~{n/dt:.0f}/s)')

print(f'Waiting to commit at {t_commit}...')
while datetime.now().timestamp() < t_commit:
    time.sleep(0.01)

# Amend existing commit with new message to update the hash
repo.git.commit(m=new_msg, amend=True, n=True)
print('Done!')
