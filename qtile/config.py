from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy
from libqtile.widget import base
from libqtile import layout, bar, widget, drawer, hook

mod = "mod4"
alt = "mod1"
ctrl = "control"
shft = "shift"

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
#         qt.mapKey(Key(["control"], "g", lazy.spawn("true"))) # this is a decent no-op, could be better
#         qt.grabKeys()
#     return sm_closure

# sm = [ Key([], "b", some_action()) ]

# keys = [ Key(["control"], "t", lazy.function(make_submap(sm))) ]

keys = [
    Key([mod, ctrl], "Left", lazy.layout.toggle_split()),
    Key([mod, ctrl], "Right", lazy.layout.client_to_next()),
    Key([mod, ctrl], "Down", lazy.layout.down()),
    Key([mod, ctrl], "Up", lazy.layout.rotate()),

    Key([alt], "Tab", lazy.layout.next()),

    Key([mod], "f", lazy.window.toggle_floating()),

    Key([mod], "Tab", lazy.to_next_screen()),

    # Session
    #Key([mod, ctrl], 'l', lazy.spawn('gnome-screensaver-command -l')),
    Key([mod, ctrl], 'q', lazy.shutdown()),
    #Key([mod, shft, 'control'], 'q', lazy.spawn('gnome-session-quit --power-off')),

    # Shortcuts
    Key([], 'F1', lazy.screen[0].togglegroup('terminal')),
    Key([mod], "Return", lazy.spawn("urxvt -e tmux")),

    # Toggle between different layouts as defined below
    Key([mod, alt], "Tab", lazy.nextlayout()),

    Key([mod], "Prior", lazy.screen.prevgroup()),
    Key([mod], "Next", lazy.screen.nextgroup()),
    
    Key([alt], "F4", lazy.window.kill()), # Close window
    Key([mod, ctrl], "r", lazy.restart()), # Reload qtile settings
    Key([mod], "space", lazy.spawncmd('run')), # open program
    Key([mod], "F12", lazy.window.toggle_fullscreen()),
]

default_data = dict(
    foreground="00ccff",
    font="DejaVu Sans"
)

groups = [
    Group("home", matches=[Match(wm_class=["Firefox"])], screen_affinity=1),
    Group("editor", matches=[Match(wm_class=["Emacs"])], screen_affinity=0),
    Group("terminal", matches=[Match(title=["Terminal"])], screen_affinity=1),
    Group("other")
]

for index, grp in enumerate(groups):
    keys.extend([
        Key([mod], str(index+1), lazy.group[grp.name].toscreen()), # switch to group
        Key([mod, ctrl], str(index+1), lazy.window.togroup(grp.name)), # send to group
    ])

dgroups_key_binder = None
dgroups_app_rules = []

border = dict(
    border_normal='#000000',
    border_focus='#edd400',
    border_width=1,
)

layouts = [
    layout.Max(),
    layout.MonadTall(ratio=0.8),
    layout.Stack(**border)
]

class CloseWindow(base._TextBox):
    def __init__(self, **config):
        base._TextBox.__init__(self, text='x', width=bar.CALCULATED, **config)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)

    def button_press(self, x, y, button):
        if button == 1:
            self.qtile.currentWindow.kill()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    invert_mouse_wheel=True,
                    borderwidth=1, 
                    active='00ccff', 
                    inactive='0055aa', 
                    this_current_screen_border='000000', 
                    fontsize=12, 
                    highlight_method='block',
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
                    '%a %d %b %H:%M', fontsize=14, **default_data
                ),
                #DrawerWidget()
            ], 28, background="333333"
        )
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    invert_mouse_wheel=True,
                    borderwidth=1, 
                    active='00ccff', 
                    inactive='0055aa', 
                    this_current_screen_border='000000', 
                    fontsize=12, 
                    highlight_method='block',
                    **default_data
                )
            ], 28, background="333333"
        )
    )
]

main = None
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False

floating_layout = layout.Floating(auto_float_types=[
    "notification",
    "toolbar",
    "splash",
    "dialog",
    "utility"
])

mouse = [
    Drag(
        [mod], "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod], "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click(
        [mod], "Button2",
        lazy.window.bring_to_front()
    ),
]

auto_fullscreen = True

@hook.subscribe.startup          
def runner():
    import subprocess
    subprocess.Popen(['urxvt', '-e', 'tmux'])

