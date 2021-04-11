import os
import re
import git
import hashlib
import time
from datetime import datetime

pattern = re.compile(r'^0000')
repo = git.Repo('.')
c = repo.head.commit

# Without this, post-commit hook loops forever
if pattern.match(c.hexsha):
    exit('Nothing to do...')

# This is pretty shady but lets post-commit hook work in rebases...
cherry = './.git/CHERRY_PICK_HEAD'
if os.path.isfile(cherry):
    os.remove(cherry)

msg = re.sub(r'\n\n\(\d+\)', '', repo.head.commit.message)

config = repo.config_reader()
name = config.get_value('user', 'name')
email = config.get_value('user', 'email')
author = f'{c.author.name} <{c.author.email}>'
committer = f'{name} <{email}>'

author_offset = int(c.author_tz_offset / -3600)
committer_offset = int(time.altzone / -3600)

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

n = 0
sha = 'TBD'
new_msg = 'TLDR'
while not pattern.match(sha):
    n += 1
    new_msg = f'{msg}\n({n})'

    # Construct cat-file output from template
    cat_file = template.format(t_commit, new_msg)

    # Add NUL-terminated header
    byte_len = len(cat_file.encode('utf-8'))
    input = f'commit {byte_len}\0{cat_file}'

    # Predict hash of future commit
    sha = hashlib.sha1(input.encode('utf-8')).hexdigest()

    # Periodically update future commit timestamp
    if n % 100000 == 0:
        t_commit = int(datetime.now().timestamp()) + 1
        print(f'Attempt {n} to commit at {t_commit}: {sha}')

dt = datetime.now().timestamp() - t_start
print(f'\nFound {sha} after {n} attempts')
print(f'Took {dt:.2f}s (~{n/dt:.0f}/s)')

print(f'Waiting to commit at {t_commit}...')
while datetime.now().timestamp() < t_commit:
    time.sleep(0.01)   

# Amend existing commit to use mined hash
repo.git.commit(m=new_msg, amend=True, n=True)
print('Done!')