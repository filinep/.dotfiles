# modified commands
alias grep='grep --color=auto'
alias more='less'
alias mkdir='mkdir -p -v'
alias ping='ping -c 5'
alias nano='nano -c'
alias ps='ps -elf'
alias ls='ls -hF --color=always'

alias chat='urxvt -e weechat'
alias calc='python2 -i -c "from math import *"'

# Get color support for 'less'
export LESS="--RAW-CONTROL-CHARS"

# Use colors for less, man, etc.
. ~/.dotfiles/bash/.LESS_TERMCAP

shopt -s autocd

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
EDITOR=emacs
PAGER=less

export BROWSER
export EDITOR
export PAGER

# Python stuff
export PYTHONDOCS=/usr/share/doc/python2/html/

# Java stuff
export java7=/usr/lib/jvm/java-7-openjdk
export java6=~/local/jdk1.6.0_34
export java8=~/local/jdk1.8.0
export currentjava=$java7
export JAVA_HOME=$currentjava/jre
export _JAVA_AWT_WM_NONREPARENTING=1
export SCALA_HOME=/usr/share/scala

export PATH=$currentjava/bin:~/local/bin:$(ruby -rubygems -e "puts Gem.user_dir")/bin:$PATH:~/local/android-sdk-linux/tools

clear
~/.dotfiles/bash/space_invaders
