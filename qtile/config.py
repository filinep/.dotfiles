# -*- coding: utf-8 -*-
from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy
from libqtile.widget import base
from libqtile import layout, bar, widget, drawer, hook, dgroups

import shlex, os

################################################################################
## Global
################################################################################
def log(s):
    screens[0].qtile.log.error(s)

term = 'urxvt -e bash -c "tmux -q has-session && exec tmux attach-session -d || exec tmux new-session"'
main = None
auto_fullscreen = True

def detect_screens(qtile):
    """
    Detect if a new screen is plugged and reconfigure/restart qtile
    """

    def setup_monitors(action=None, device=None):
        """
        Add 1 group per screen
        """

        if action == "change":
            # setup monitors with xrandr
            # call("setup_screens")
            lazy.restart()

        nbr_screens = len(qtile.conn.pseudoscreens)
        for i in xrange(0, nbr_screens-1):
            groups.append(Group('h%sx' % (i+5), persist=False))
    setup_monitors()

    import pyudev

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('drm')
    monitor.enable_receiving()

    # observe if the monitors change and reset monitors config
    observer = pyudev.MonitorObserver(monitor, setup_monitors)
    observer.start()

@hook.subscribe.startup
def runner():
    import subprocess
    subprocess.Popen(shlex.split(term))


################################################################################
## Groups
################################################################################
dgroups_app_rules = []

groups = [
    Group('', matches=[Match(wm_class=['Firefox'])], exclusive=True),
    Group('', matches=[Match(wm_class=['Emacs'])], exclusive=True),
    Group('', matches=[Match(title=['Terminal'])], exclusive=True),
    Group('', matches=[Match(title=['calibre-gui'], wm_class=['libprs500'])], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(wm_class=['lyx', 'Lyx'])], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(title=['Mozilla Thunderbird'])], persist=False, init=False),
    Group('', matches=[Match(title=['Kodi', 'VLC media player', 'FCEUX 2.2.2'], wm_class=['vlc', 'Vlc'])], exclusive=True, persist=False, init=False),
    Group('', matches=[
        Match(role=['gimp-toolbox']),
        Match(role=['gimp-dock']),
        Match(title=['GNU Image Manipulation Program'])
    ], layout='gimp', persist=False, init=False),
    Group('', matches=[Match(wm_class=['Nautilus'])], persist=False, init=False),
    Group('', persist=False, init=False),
    #Group('', matches=[Match(wm_class=['Xchat'])]),
]


################################################################################
## Keys
################################################################################
mod = 'mod4'
alt = 'mod1'
ctrl = 'control'
shft = 'shift'

keys = [
    Key([mod, ctrl], 'Left', lazy.layout.toggle_split()),
    Key([mod, ctrl], 'Right', lazy.layout.client_to_next()),
    Key([mod, ctrl], 'Down', lazy.layout.down()),
    Key([mod, ctrl], 'Up', lazy.layout.rotate()),
    Key([alt], 'Tab', lazy.layout.next()),
    Key([mod], 'f', lazy.window.toggle_floating()),
    Key([mod], 'Tab', lazy.next_screen()),
    Key([mod, ctrl], 'q', lazy.shutdown()),
    Key([], 'F1', lazy.screen[0].togglegroup('')),
    Key([mod], 'Return', lazy.spawn(term)),
    Key([mod, shft], 'Tab', lazy.next_layout()),
    Key([mod, alt], 'Tab', lazy.screen.next_group()),
    Key([mod], 'Prior', lazy.screen.prev_group()),
    Key([mod], 'Next', lazy.screen.next_group()),
    Key([alt], 'F4', lazy.window.kill()),
    Key([mod, ctrl], 'r', lazy.restart()),
    Key([mod], 'space', lazy.spawncmd('run')),
    Key([mod, ctrl], 'f', lazy.window.toggle_fullscreen()),
    Key([alt], 'grave', lazy.window.bring_to_front()),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('sudo /home/filipe/local/bin/backlight dec')),
    Key([], 'XF86MonBrightnessUp', lazy.spawn('sudo /home/filipe/local/bin/backlight inc')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer set Master playback 5-')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer set Master playback 5+')),
    Key([], 'XF86AudioMute', lazy.spawn('amixer set Master toggle')),
    Key([mod], 'z', lazy.window.togroup()),
    Key([mod], 'b', lazy.spawn('bash -c "/home/filipe/local/bin/backlight_off"')),
]

dgroups_key_binder = dgroups.simple_key_binder(mod)
# for index, grp in enumerate(groups):
#     keys.extend([
#         Key([mod], str(index+1), lazy.group[grp.name].toscreen()), # switch to group
#         Key([mod, ctrl], str(index+1), lazy.window.togroup(grp.name)), # send to group
#     ])


################################################################################
## Layouts
################################################################################
border_args = dict(
    border_width=1,
    border_focus='#00ccff',
    border_normal='#0055aa'
)

layouts = [
    layout.Max(margin=1, **border_args),
    layout.Stack(margin=1, **border_args),
    layout.Slice(side='left', width=192, name='gimp', role='gimp-toolbox',
         fallback=layout.Slice(side='right', width=256, role='gimp-dock',
         fallback=layout.Tile(**border_args), **border_args)
    ),
]

floating_layout = layout.Floating(auto_float_types=[
    'notification',
    'toolbar',
    'splash',
    'dialog',
    'utility'
], max_border_width=1, fullscreen_border_width=1, **border_args)


################################################################################
## Screens + Widgets
################################################################################
class CloseWindow(base._TextBox):
    def __init__(self, **config):
        base._TextBox.__init__(self, text='X', width=bar.CALCULATED, **config)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)

    def button_press(self, x, y, button):
        if button == 1:
            self.qtile.currentWindow.kill()

default_data = dict(
    foreground='#00ccff',
    font='FontAwesome'
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    invert_mouse_wheel=False,
                    active='#00ccff', 
                    inactive='#0055aa', 
                    this_current_screen_border='#0077aa', 
                    other_screen_border='#555555', 
                    this_screen_border='#202020', 
                    fontsize=18, 
                    highlight_method='block',
                    urgent_alert_method='text',
                    **default_data
                ),
                widget.Sep(),
                widget.WindowName(
                    width=bar.STRETCH, fontsize=14, **default_data
                ),
                widget.Prompt(
                    fontsize=14, **default_data
                ),
                widget.Notify(
                    fontsize=14, **default_data
                ),
                widget.Sep(),
                CloseWindow(fontsize=14, **default_data),
                widget.Sep(),
                widget.Systray(
                    **default_data
                )
            ] + ([
                widget.BatteryIcon(theme_path='/home/filipe/.config/qtile/battery/', **default_data)
            ] if os.listdir('/sys/class/power_supply') else []) + [
                widget.Volume(
                    theme_path='/home/filipe/.config/qtile/audio/', **default_data
                ),
                widget.Clock(
                    format='%a %d %b %H:%M', fontsize=15, **default_data
                )
            ], 28, background='#2e3441'
        )
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    invert_mouse_wheel=False,
                    active='#00ccff', 
                    inactive='#0055aa', 
                    this_current_screen_border='#0077aa', 
                    other_screen_border='#555555', 
                    this_screen_border='#202020', 
                    fontsize=18, 
                    highlight_method='block',
                    urgent_alert_method='text',
                    **default_data
                ),
                widget.Sep(),
                widget.WindowName(
                    width=bar.STRETCH, fontsize=14, **default_data
                ),
                widget.Sep(),
                CloseWindow(fontsize=14, **default_data),
            ], 28, background='#2e3441'
        )
    )
]


################################################################################
## Mouse
################################################################################
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False

mouse = [
    Drag(
        [mod], 'Button1',
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod], 'Button3',
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click(
        [mod], 'Button2',
        lazy.window.bring_to_front()
    ),
]


################################################################################
## Follow window focus
################################################################################
follow_focus = True
border_normal = '#000000'
border_focus = '#00ccff'
border_width = 1

@hook.subscribe.client_focus
def fake_single_window_focus(win):
    if hasattr(screens[0].qtile, 'follow_focus'): # in case we're using official qtile
        for s in screens:
            if s.group:
                for i in s.group.windows:
                    i.place(i.x, i.y, i.width, i.height, border_width, None)
    if hasattr(win, 'floating') and win.floating: # make floaties auto come to the front
        win.cmd_bring_to_front()


################################################################################
## Todo
################################################################################
# def make_submap(sm):
#     def sm_closure(qt):
#         class ReplaceMap(dict):
#             def get(self, k, d=None):
#                 rv = dict.get(self, k, d)
#                 qt.keyMap = qt.old_keymap
#                 del qt.old_keymap
#                 qt.grabKeys()
#                 return rv
#         if not hasattr(qt, 'old_keymap'):
#             qt.old_keymap = qt.keyMap
#         qt.keyMap = ReplaceMap()
#         for i in sm:
#             qt.mapKey(i)
#         qt.mapKey(Key(['control'], 'g', lazy.spawn('true'))) # this is a decent no-op, could be better
#         qt.grabKeys()
#     return sm_closure

# sm = [ Key([], 'b', some_action()) ]

# keys = [ Key(['control'], 't', lazy.function(make_submap(sm))) ]
