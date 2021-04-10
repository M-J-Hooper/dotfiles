import re
import git
import hashlib
import time
from datetime import datetime

repo = git.Repo('.')

c = repo.head.commit

msg = repo.head.commit.message
base = 'tree ' + c.tree.hexsha
base += '\nparent ' + c.parents[0].hexsha

dt = 5
now = int(datetime.now().timestamp())
then = now + dt
n = 0
sha = ''
new_msg = ''
while not sha.startswith('0000'):
    new_msg = msg + '\n' + str(n)

    cat = base + '\nauthor Matt Hooper <mattt.hoooper@gmail.com> ' + str(int(c.authored_datetime.timestamp())) + ' +0100'
    cat += '\ncommitter Matt Hooper <mattt.hoooper@gmail.com> ' + str(then) + ' +0100'
    cat += '\n\n' + new_msg + '\n'

    bs = len(cat.encode('utf-8'))
    ss = 'commit ' + str(bs) + '\0' + cat

    sha = hashlib.sha1(ss.encode('utf-8')).hexdigest()
    n += 1
    if n % 1000 == 0:
        print(n)

print(now, then, sha, new_msg)

while datetime.now().timestamp() < then:
    time.sleep(0.01)   

repo.git.commit(m=new_msg, amend=True)

# # Amend the head commit in the loop
# # Dumb approach which is too slow due to Git IO
# n = 0
# while not repo.head.commit.hexsha.startswith('00'):
#     new_message = re.sub(r'(\n\n\d+)?$', '\n\n' + str(n), repo.head.commit.message, count=1)
#     repo.git.commit(m=new_message, amend=True)
#     n += 1