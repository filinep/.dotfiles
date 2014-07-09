# -*- coding: utf-8 -*-
from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy
from libqtile.widget import base
from libqtile import layout, bar, widget, drawer, hook

import shlex

################################################################################
## Global
################################################################################
def log(s):
    screens[0].qtile.log.error(s)

term = 'urxvt -e bash -c "tmux -q has-session && exec tmux attach-session -d || exec tmux new-session"'
main = None
auto_fullscreen = True

@hook.subscribe.startup
def runner():
    import subprocess
    subprocess.Popen(shlex.split(term))


################################################################################
## Groups
################################################################################
dgroups_key_binder = None
dgroups_app_rules = []

groups = [
    Group('', matches=[Match(wm_class=['Firefox'])]),
    Group('', matches=[Match(wm_class=['Emacs'])]),
    Group('', matches=[Match(title=['Terminal'])]),
    Group('', matches=[Match(wm_class=['Xchat'])]),
    Group('')
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
    Key([mod], 'Tab', lazy.to_next_screen()),
    Key([mod, ctrl], 'q', lazy.shutdown()),
    Key([], 'F1', lazy.screen[0].togglegroup('')),
    Key([mod], 'Return', lazy.spawn(term)),
    Key([mod, alt], 'Tab', lazy.nextlayout()),
    Key([mod], 'Prior', lazy.screen.prevgroup()),
    Key([mod], 'Next', lazy.screen.nextgroup()),
    Key([alt], 'F4', lazy.window.kill()),
    Key([mod, ctrl], 'r', lazy.restart()),
    Key([mod], 'space', lazy.spawncmd('run')),
    Key([mod], 'F12', lazy.window.toggle_fullscreen()),
]

for index, grp in enumerate(groups):
    keys.extend([
        Key([mod], str(index+1), lazy.group[grp.name].toscreen()), # switch to group
        Key([mod, ctrl], str(index+1), lazy.window.togroup(grp.name)), # send to group
    ])


################################################################################
## Layouts
################################################################################
layouts = [
    layout.Max(),
    layout.Stack(),
]

floating_layout = layout.Floating(auto_float_types=[
    'notification',
    'toolbar',
    'splash',
    'dialog',
    'utility'
], max_border_width=1, fullscreen_border_width=1)


################################################################################
## Screens + Widgets
################################################################################
class CloseWindow(base._TextBox):
    def __init__(self, **config):
        base._TextBox.__init__(self, text='x', width=bar.CALCULATED, **config)

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
                    invert_mouse_wheel=True,
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
                ),
                widget.Volume(
                    theme_path='/home/filipe/.config/qtile/', **default_data
                ), 
                widget.Clock(
                    '%a %d %b %H:%M', fontsize=15, **default_data
                )
            ], 28, background='#2e3436'
        )
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    invert_mouse_wheel=True,
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
                )
            ], 28, background='#2e3436'
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
