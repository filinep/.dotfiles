# -*- coding: utf-8 -*-
from libqtile.config import Key, Screen, Group, Match, Drag, Click, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile.widget import base
from libqtile import layout, bar, widget, drawer, hook, dgroups
from libqtile.log_utils import logger

import ConfigParser
import os, requests

################################################################################
## Colours
################################################################################
foreground = '#00ccff'
background = '#2e3441'
border_focus = '#00ccff'
border_normal = '#0055aa'
active = '#00ccff'
inactive = '#0055aa'
this_current_screen_border = '#0077aa'
other_screen_border = '#555555'
this_screen_border = '#202020'

################################################################################
## Global
################################################################################
config = ConfigParser.RawConfigParser()
config.read('/home/filipe/.config/.vars')

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
dgroups_app_rules = []

groups = [
    Group('', matches=[Match(wm_class=['Firefox'])], exclusive=True),
    Group('', matches=[Match(wm_class=['Emacs'])], exclusive=True),
    Group('', matches=[Match(title=['Terminal'])], exclusive=True),
    Group('', matches=[Match(title=['calibre-gui'], wm_class=['libprs500'])], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(wm_class=['lyx', 'Lyx'])], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(wm_class=['evince', 'Evince'])], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(title=['Zeal'])], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(title=['Kodi', 'VLC media player', 'FCEUX 2.2.2'], wm_class=['vlc', 'Vlc'])], exclusive=True, persist=False, init=False),
    Group('', matches=[
        Match(role=['gimp-toolbox']),
        Match(role=['gimp-dock']),
        Match(title=['GNU Image Manipulation Program'])
    ], exclusive=True, persist=False, init=False),
    Group('', matches=[Match(wm_class=['Nautilus'])], exclusive=True, persist=False, init=False),
    Group('', persist=False, init=False),
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
    Key([mod], 'Prior', lazy.screen.prev_group()),
    Key([mod], 'Next', lazy.screen.next_group()),
    Key([alt], 'F4', lazy.window.kill()),
    Key([mod, ctrl], 'r', lazy.restart()),
    Key([mod], 'space', lazy.spawncmd('run')),
    Key([mod, ctrl], 'f', lazy.window.toggle_fullscreen()),
    Key([alt], 'grave', lazy.window.bring_to_front()),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('sudo /home/filipe/local/bin/backlight dec')),
    Key([], 'XF86MonBrightnessUp', lazy.spawn('sudo /home/filipe/local/bin/backlight inc')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('sh -c "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 -5%"')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('sh -c "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 +5%"')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute 0 toggle')),
    Key([mod], 'z', lazy.window.togroup()),
    Key([mod], 'b', lazy.spawn('bash -c "/home/filipe/local/bin/backlight_off"')),
    Key([mod, alt], "Down", lazy.layout.down()),
    Key([mod, alt], "Up", lazy.layout.up()),
    Key([mod, alt], "Left", lazy.layout.client_to_next()),
    Key([mod, alt], "Right", lazy.layout.client_to_previous()),
]

dgroups_key_binder = dgroups.simple_key_binder(mod)

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
    layout.Stack(margin=1, **border_args)
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

class Bitcoin(base.ThreadedPollText):
    orientations = base.ORIENTATION_HORIZONTAL

    keyid = config.get('LUNO', 'KEY')
    secret = config.get('LUNO', 'SECRET')

    ticker_url  = "https://api.mybitx.com/api/1/tickers"
    balance_url = "https://api.mybitx.com/api/1/balance"

    defaults = [
        ('update_interval', 60, 'The update interval.'),
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(Bitcoin.defaults)

    def draw(self):
        base.ThreadedPollText.draw(self)

    def poll(self):
        try:
            tickers = requests.get(self.ticker_url).json()
            ask_xbt = [float(i['last_trade']) for i in tickers['tickers'] if i['pair'] == 'XBTZAR'][0]

            balances = requests.get(self.balance_url, auth=(self.keyid, self.secret)).json()['balance']
            xbt = sum([float(i['balance']) for i in balances if i['asset'] == 'XBT'])
            zar = sum([float(i['balance']) for i in balances if i['asset'] == 'ZAR'])
            bch = sum([float(i['balance']) for i in balances if i['asset'] == 'BCH'])
            eth = sum([float(i['balance']) for i in balances if i['asset'] == 'ETH'])

            return "ETH: %.4f, BCH: %.2f, XBT: %.6f, ZAR: %.2f, Price: %.0f" % (eth, bch, xbt, xbt*ask_xbt + zar, ask_xbt)
        except Exception as e:
            return str(e)[:50]

widget_defaults = dict(
    foreground=foreground,
    font='FontAwesome',
    fontsize=14
)

def groupbox(): return widget.GroupBox(
        invert_mouse_wheel=False,
        active=active, 
        inactive=inactive, 
        this_current_screen_border=this_current_screen_border, 
        other_screen_border=other_screen_border, 
        this_screen_border=this_screen_border, 
        fontsize=18, 
        highlight_method='block',
        urgent_alert_method='text'
)

def sep(): return widget.Sep()

def battery(): return [
        widget.BatteryIcon(theme_path='/home/filipe/.config/qtile/battery/')
] if os.listdir('/sys/class/power_supply') else []

screens = [
    Screen(
        top=bar.Bar(
            [
                groupbox(),
                sep(),
                widget.WindowName(width=bar.STRETCH),
                widget.Prompt(),
                widget.Notify(),
                sep(),
                Bitcoin(),
                sep(),
                CloseWindow(),
                sep(),
                widget.Systray()
            ] + battery() + [
                widget.Volume(theme_path='/home/filipe/.config/qtile/audio/'),
                widget.Clock(format='%a %d %b %H:%M')
            ], 28, background='#2e3441'
        )
    ),
    Screen(
        top=bar.Bar(
            [
                groupbox(),
                sep(),
                widget.WindowName(width=bar.STRETCH),
                sep(),
                CloseWindow()
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
