if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

if [ -s ~/.Xmodmap ]; then
    xmodmap ~/.Xmodmap
fi

hsetroot -center ~/.dotfiles/X/background.jpg -flipv -add "#00000000" -add "#6f6f6fff" -gradient 180 -blur 50
xsetroot -cursor_name left_ptr
[[ -f ~/.Xresources ]] && xrdb -merge ~/.Xresources

numlockx &

XDG_CURRENT_SESSION=qtile exec dbus-launch qtile
#XDG_CURRENT_SESSION=qtile exec x11trace /usr/bin/qtile -c ~/.config/qtile/config.py > ~/qtile-xtrace.log
