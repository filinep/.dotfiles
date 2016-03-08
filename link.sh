#!/usr/bin/bash

link() {
    rm -rf $2 && ln -s ~/.dotfiles/$1 $2
}

# Bash
link bash/.bashrc ~/.bashrc
link bash/.bash_profile ~/.bash_profile

# Screen
# link screen/.screenrc ~/.screenrc

# Tmux
link tmux/.tmux.conf ~/.tmux.conf

# Nano
link nano/.nanorc ~/.nanorc

# Qtile
link qtile ~/.config/qtile

# X stuff
link X/.Xresources ~/.Xresources
link X/.Xmodmap ~/.Xmodmap
link X/.xinitrc ~/.xinitrc

# GTK
link gtk/.gtkrc-2.0 ~/.gtkrc-2.0
link gtk/settings.ini ~/.config/gtk-3.0/settings.ini
