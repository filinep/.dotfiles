if [ -z "$TMUX" ]; then
    setleds -D +num
    eval `keychain --eval --agents ssh id_rsa google_compute_engine`
else
    . ~/.bashrc
fi
