#setxkbmap -option ctrl:nocaps
#exec gnome-session
#exec awesome
#exec openbox-session

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

if [ -s ~/.Xmodmap ]; then
    xmodmap ~/.Xmodmap
fi

xsetroot -cursor_name left_ptr
[[ -f ~/.Xresources ]] && xrdb -merge ~/.Xresources

numlockx &

XDG_CURRENT_SESSION=qtile exec qtile
