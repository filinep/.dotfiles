# modified commands
alias grep='grep --color=auto'
alias more='less'
alias mkdir='mkdir -p -v'
alias ping='ping -c 5'
alias nano='nano -w -c'
alias ps='ps -elf'
alias ls='ls -hF --color=always'

alias openports='netstat --all --numeric --programs --inet --inet6'

alias em='emacsclient -c -nw'
alias emacs='emacsclient -c'
alias calc='python2 -i -c "from math import *; from matplotlib import pyplot as plot; from scipy import *"'
#alias ssh='TERM=xterm
if [ -f ~/.config/.alias ]; then
    . ~/.config/.alias
fi

# Get color support for 'less'
export LESS="--RAW-CONTROL-CHARS"

# Use colors for less, man, etc.
. ~/.dotfiles/bash/.LESS_TERMCAP

# safety features
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -I'
alias ln='ln -i'
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'

shopt -s autocd

[ -n "$TMUX" ] && export TERM=screen-256color || TERM=rxvt-unicode

case $TERM in
    screen*)
        # This is the escape sequence ESC k ESC \
        SCREENTITLE='\[\ek\w\e\\\]'
        ;;
    *)
        SCREENTITLE=''
        ;;
esac

PS1="${SCREENTITLE}\[\e[01;33m\]|\$(if [[ \$? == 0 ]]; then echo \"\[\e[01;32m\]\342\234\223\"; else echo \"\[\e[01;31m\]\342\234\227\"; fi) \[\e[01;34m\]\w \[\e[01;33m\]>>\[\e[00m\] "

export HISTCONTROL=erasedups 
export HISTSIZE=4096

if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

complete -cf sudo
complete -cf man

if [ -n "$DISPLAY" ]; then
    BROWSER=firefox
else
    BROWSER=links
fi
ALTERNATE_EDITOR=""

export BROWSER
export EDITOR=emacs
export PAGER=less

# Java stuff
export _JAVA_AWT_WM_NONREPARENTING=1
export QT_QPA_PLATFORMTHEME=gtk2
export QT_STYLE_OVERRIDE=GTK+
export APPENGINE_SDK_HOME=/opt/google-appengine-java
export PATH=~/local/bin:$PATH:/opt/google-appengine-java/bin

if [ -f ~/.proxy ]; then
    . ~/.proxy
fi

unset SSH_ASKPASS

clear
~/.dotfiles/bash/space_invaders

