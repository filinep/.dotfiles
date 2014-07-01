from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy
from libqtile.widget import base
from libqtile import layout, bar, widget, drawer#, obj

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
    # MonadTall layout
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "k", lazy.layout.down()),
    Key([alt], "Tab", lazy.layout.down()),
    Key([mod, shft], "h", lazy.layout.swap_left()),
    Key([mod, shft], "l", lazy.layout.swap_right()),
    Key([mod, shft], "j", lazy.layout.shuffle_down()),
    Key([mod, shft], "k", lazy.layout.shuffle_up()),
    Key([mod, ctrl], "h", lazy.layout.normalize()),
    Key([mod, ctrl], "l", lazy.layout.maximize()),
    Key([mod, ctrl], "j", lazy.layout.grow()),
    Key([mod, ctrl], "k", lazy.layout.shrink()),
    Key([mod, shft], "space", lazy.layout.flip()),

    Key([mod], "f", lazy.window.toggle_floating()),

    # Session
    #Key([mod, ctrl], 'l', lazy.spawn('gnome-screensaver-command -l')),
    #Key([mod, ctrl], 'q', lazy.spawn('gnome-session-quit --logout --no-prompt')),
    #Key([mod, shft, 'control'], 'q', lazy.spawn('gnome-session-quit --power-off')),

    # Shortcuts
    Key([], 'F1', lazy.screen.togglegroup('terminal')),
    Key([mod], "Return", lazy.spawn("urxvt -e screen")),

    # Toggle between different layouts as defined below
    Key([mod, alt], "Tab", lazy.nextlayout()),

    Key([mod], "Prior", lazy.screen.prevgroup()),
    Key([mod], "Next", lazy.screen.nextgroup()),
    
    Key([alt], "F4", lazy.window.kill()), # Close window
    Key([mod, ctrl], "r", lazy.restart()), # Reload qtile settings
    Key([mod], "space", lazy.spawncmd('run')), # open program
    Key([mod], "F12", lazy.window.toggle_fullscreen()),
]

"""
! black dark/light
URxvt*color0: #2e3436
URxvt*color8: #6e706b

! red dark/light
URxvt*color1: #cc0000
URxvt*color9: #ef2929

! green dark/light
URxvt*color2: #4e9a06
URxvt*color10: #8ae234

! yellow dark/light
URxvt*color3: #edd400
URxvt*color11: #fce94f

! blue dark/light
URxvt*color4: #3465a4
URxvt*color12: #729fcf

! magenta dark/light
URxvt*color5: #92659a
URxvt*color13: #c19fbe

! cyan dark/light
URxvt*color6: #07c7ca
URxvt*color14: #63e9e9

! white dark/light
URxvt*color7: #d3d7cf
URxvt*color15: #eeeeec
"""

default_data = dict(
    foreground="00ccff",
    font="DejaVu Sans"
)

groups = [
    Group("home", matches=[Match(wm_class=["Firefox"])]),
    Group("editor", matches=[Match(wm_class=["Emacs"])]),
    Group("terminal", matches=[Match(title=["Terminal"])]),
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


from libqtile import command, confreader, drawer, hook, configurable, window
import gobject

class MyGap(command.CommandObject, configurable.Configurable):
    defaults = [
        ("background", "#00FF00", "Background colour."),
        ("opacity",  1, "Bar window opacity.")
    ]
    
    def __init__(self, **config):
        configurable.Configurable.__init__(self, **config)
        self.qtile = None
        self.screen = None
        self.add_defaults(MyGap.defaults)
        self.size = 12

    def _configure(self, qtile, screen):
        self.qtile = qtile
        self.screen = screen
        
        self.window = window.Internal.create(
            self.qtile,
            self.x, self.y, self.width, self.height,
            self.opacity
        )

        self.drawer = drawer.Drawer(
            self.qtile,
            self.window.window.wid,
            self.width,self.height
        )
        self.drawer.clear(self.background)

        self.window.handle_Expose = self.handle_Expose
        self.window.handle_ButtonPress = self.handle_ButtonPress
        self.window.handle_ButtonRelease = self.handle_ButtonRelease
        qtile.windowMap[self.window.window.wid] = self.window
        self.window.unhide()

        # FIXME: These should be targeted better.
        hook.subscribe.setgroup(self.draw)
        hook.subscribe.changegroup(self.draw)

    @property
    def x(self):
        return 100

    @property
    def y(self):
        return 100

    @property
    def width(self):
        return 100

    @property
    def height(self):
        return 100

    def geometry(self):
        return (self.x, self.y, self.width, self.height)

    def _items(self, name):
        if name == "screen":
            return (True, None)

    def _select(self, name, sel):
        if name == "screen":
            return self.screen

    @property
    def position(self):
        for i in ["top", "bottom", "left", "right"]:
            if getattr(self.screen, i) is self:
                return i

    def info(self):
        return dict(
            width=self.width,
            position=self.position,
            window=self.window.window.wid
        )

    def cmd_info(self):
        return self.info()

    def handle_Expose(self, e):
        self.draw()

    def handle_ButtonPress(self, e):
        pass

    def handle_ButtonRelease(self, e):
        pass

    def widget_grab_keyboard(self, widget):
        '''self.window.handle_KeyPress = widget.handle_KeyPress
        self.saved_focus = self.qtile.currentWindow
        self.window.window.set_input_focus()'''
        pass

    def widget_ungrab_keyboard(self):
        pass
        '''del self.window.handle_KeyPress
        if not self.saved_focus is None:
            self.saved_focus.window.set_input_focus()'''

    def draw(self):
        self.opacity -= 0.01
        self.window.setOpacity(self.opacity)
        self.drawer.clear((0,1,1))
        self.drawer.draw(0, 100)
        print self.opacity

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
            ], 28, background="333333"#, "#202020", "#5a5a5a"]#"000000", #background="1D1D1D",
        ),
        #bottom=MyGap()
        # bottom=bar.Bar(
        #     [
        #         widget.Systray(
        #             **default_data
        #         ),
        #     ], 28, background="000000"
        # )
    ),
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
    subprocess.Popen(['urxvt', '-e', 'screen'])

