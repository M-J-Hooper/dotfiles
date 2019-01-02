# Register aliases
alias ll='ls -lah'
alias pls='sudo $(history -p !!)'
alias vi=vim
alias grep='grep --color'
alias at='tmux a'
alias k='kubectl'
alias g='gcloud'
alias fixssh='eval $(tmux showenv -s SSH_AUTH_SOCK)'

# Very secret stuff
[ -f ~/.bashsecrets ] && . ~/.bashsecrets

# Bash autocompletion
[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion

#Styling
export PS1='[\u \w$(git branch 2>/dev/null | sed -n "s/* \(.*\)/\ (\1\)/p")]$ '

# Environment
export PATH=$PATH:/usr/local/go/bin
