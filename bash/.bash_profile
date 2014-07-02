if [ -z "$TMUX" ]; then
    setleds -D +num
    eval `keychain --eval id_rsa`
else
    . ~/.bashrc
fi
