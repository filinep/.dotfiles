#!/usr/bin/bash

link() {
    rm -rf $2 && ln -s ~/.dotfiles/$1 $2
}

# Bash
link bash/.bashrc ~/.bashrc
link bash/.bash_profile ~/.bash_profile

# Screen
link screen/.screenrc ~/.screenrc

# Qtile
link qtile ~/.config/qtile

# X stuff
link X/.Xresources ~/.Xresources
link X/.Xmodmap ~/.Xmodmap

# GTK
link gtk/.gtkrc-2.0 ~/.gtkrc-2.0

