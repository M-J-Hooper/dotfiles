import re
import git
import hashlib
import time
from datetime import datetime

repo = git.Repo('.')
c = repo.head.commit

offset = int(c.author_tz_offset / -3600)
tz = f'{offset:+03d}00'

base = f'tree {c.tree.hexsha}'
base += f'\nparent {c.parents[0].hexsha}'

msg = repo.head.commit.message
actor = f'{c.author.name} <{c.author.email}>'

t_start = int(datetime.now().timestamp())
t_author = int(c.authored_datetime.timestamp())
t_commit = t_start + 1
n = 0
sha = ''
new_msg = ''
ss = ''
while not sha.startswith('0000'):
    n += 1
    new_msg = f'{msg}\n{n}'

    cat = base + f'\nauthor {actor} {t_author} {tz}'
    cat += f'\ncommitter {actor} {t_commit} {tz}'
    cat += f'\n\n{new_msg}\n'

    bs = len(cat.encode('utf-8'))
    ss = f'commit {bs}\0{cat}'

    sha = hashlib.sha1(ss.encode('utf-8')).hexdigest()
    if n % 1000 == 0:
        t_commit = int(datetime.now().timestamp()) + 1
        print(f'Attempt {n} to commit at {t_commit}')

print(t_author, t_commit, sha, ss)

while datetime.now().timestamp() < t_commit:
    time.sleep(0.01)   

repo.git.commit(m=new_msg, amend=True)

# # Amend the head commit in the loop
# # Dumb approach which is too slow due to Git IO
# n = 0
# while not repo.head.commit.hexsha.startswith('00'):
#     new_message = re.sub(r'(\n\n\d+)?$', '\n\n' + str(n), repo.head.commit.message, count=1)
#     repo.git.commit(m=new_message, amend=True)
#     n += 1