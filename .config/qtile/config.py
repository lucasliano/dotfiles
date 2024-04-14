# Sacado de: https://github.com/david35mm/.files/tree/main/.config/qtile

# Requirements:
# rofi (https://github.com/davatorium/rofi/blob/next/INSTALL.md)
# konsole/alacritty
# btm (https://github.com/ClementTsang/bottom)
# pavucontrol (volumen)
# brightnessctl (brillo) - Dar permisos: sudo chmod +s $(which brightnessctl)
# flameshot (screenshot)
# picom (transparencia)
# dunst (notificaciones)
# udiskie (auto montar USB)

# psutil


import os
import shutil
import socket
import subprocess
from libqtile import bar
from libqtile import hook
from libqtile import layout
from libqtile import qtile
from libqtile import widget
from libqtile.config import EzClick as Click
from libqtile.config import EzDrag as Drag
from libqtile.config import EzKey as Key
from libqtile.config import Group
from libqtile.config import Match
from libqtile.config import Screen
from libqtile.lazy import lazy


# Teclas importantes:
#   M-<Space>:  Lock
#   M-C-r:      Reiniciar Qtile
#   M-C-q:      Logout
#   M-i:        Abrir internet
#   M-c:        Abrir code
#   M-o:        Abrir Obsidian
#   M-e:        Abrir archivos

mod = "mod4"
my_term = "alacritty" 
my_browser = 'firefox' #"brave-browser"
my_file_manager = "nautilus"
my_markdown = "obsidian"
my_ide = "code"
my_chat = 'discord'

mouse = [
    Drag("M-1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag("M-3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click("M-2",
          lazy.window.bring_to_front()),
]

keys = [
    # System
    Key("M-C-r",
        lazy.restart(),
        desc="Restart Qtile"),
    Key("M-C-q",
        lazy.shutdown(),
        desc="Quit Qtile"),
    Key("M-<Space>",
        lazy.spawn("systemctl suspend"),
        desc="Bloquea la pantalla"),
    Key("M-p",
        lazy.widget["keyboardlayout"].next_keyboard(),
        desc="Cambia el teclado entre US y LATAM"),

    # Layout
    Key("M-q", 
        lazy.next_screen(),
        desc="Next Screen"),
    Key("M-S-j",
        lazy.layout.shuffle_up(),
        desc="Swap with previous window"),
    Key("M-S-k",
        lazy.layout.shuffle_down(),
        desc="Swap with next window"),
    Key("M-j",
        lazy.group.prev_window(),
        desc="Focus previous window"),
    Key("M-k",
        lazy.group.next_window(),
        desc="Focus next window"),
    Key("M-s",
        lazy.window.toggle_fullscreen(),
        desc="Fullscreen toogle"),
    Key("M-w",
        lazy.window.kill(),
        desc="Close the window"),
    Key("M-f",
        lazy.window.toggle_floating(),
        desc="Floating toggle"),
    Key("M-S-f",
        lazy.layout.flip(),
        desc="Flip master pane side"),
    Key("M-S-h",
        lazy.layout.shrink(),
        desc="Shrink window size"),
    Key("M-S-l",
        lazy.layout.grow(),
        desc="Expand window size"),
    Key("M-S-n",
        lazy.layout.reset(),
        desc="Normalize all windows size"),
    Key("M-<Tab>",
        lazy.next_layout(),
        desc="Cycle through layouts"),
    Key("M-h",
        lazy.layout.shrink_main(),
        desc="Shrink master pane width"),
    Key("M-l",
        lazy.layout.grow_main(),
        desc="Grow master pane width"),
    Key("M-n",
        lazy.layout.normalize(),
        desc="Normalize all slave windows size"),
    Key("M-<comma>",
        lazy.prev_screen(),
        desc="Focus the previous screen"),
    Key("M-<period>",
        lazy.next_screen(),
        desc="Focus the next screen"),

    # Volumen
    Key("<XF86AudioLowerVolume>",
        lazy.spawn("amixer -D pulse sset Master 2%-"),
        desc="Decrease the volume"),
    Key("<XF86AudioMute>",
        lazy.spawn("amixer -D pulse sset Master toggle"),
        desc="Mute toggle"),
    Key("<XF86AudioRaiseVolume>",
        lazy.spawn("amixer -D pulse sset Master 2%+"),
        desc="Increase the volume"),


    # TODO: Buscar alguna forma de mejorarlo.
     Key("<XF86MonBrightnessDown>",
         lazy.spawn("brightnessctl set 10%-"),
         desc="Decrease the brightness"),
     Key("<XF86MonBrightnessUp>",
         lazy.spawn("brightnessctl set 10%+"),
         desc="Increase the brightness"),

    # Apps
    Key("M-r",
        lazy.spawn("rofi -show drun"),
        desc="Run the application launcher"),
    Key("A-<Tab>",
        lazy.spawn("rofi -show window"),
        desc="Open the window switcher"),
    Key("M-S-s",
        lazy.spawn("flameshot gui"),
        desc="Screenshot"),
    Key("M-<Return>",
        lazy.spawn(my_term),
        desc="Launch " + my_term),
    Key("M-i",
        lazy.spawn(my_browser),
        desc="Launch " + my_browser),
    Key("M-e",
        lazy.spawn(my_file_manager),
        desc="Launch " + my_file_manager),
    Key("M-o",
        lazy.spawn(my_markdown),
        desc="Launch " + my_markdown),
    Key("M-c",
        lazy.spawn(my_ide),
        desc="Launch " + my_ide),
    Key("M-d",
        lazy.spawn(my_chat),
        desc="Launch " + my_chat),
]

groups = [
    Group("web",
          layout="max",
          matches=[
              Match(wm_class=[my_browser]),
          ]),
    Group("dev",
          layout="monadtall",
          matches=[
              Match(wm_class=[my_ide]),
          ]),
    Group("sys",
          layout="monadtall",
          ),
    Group("doc",
          layout="monadtall",
          matches=[
              Match(wm_class=[my_markdown]),
          ]),
    Group("chat",
          layout="max",
          matches=[
              Match(wm_class=["discord"]),
          ]),
    Group("media",
          layout="max",
          matches=[
              Match(wm_class=["vlc"]),
          ]),
]

for k, group in zip(["1", "2", "3", "4", "5", "6"], groups):
  keys.append(Key("M-" + (k), lazy.group[group.name].toscreen()))
  keys.append(Key("M-S-" + (k), lazy.window.togroup(group.name)))

colours = [
    ["#1f2329", "#1f2329"],  # Background
    ["#dcdcdc", "#dcdcdc"],  # Foreground
    ["#535965", "#535965"],  # Not Focused (Grey)
    ["#e55561", "#e55561"],
    ["#8ebd6b", "#8ebd6b"],
    ["#e2b86b", "#e2b86b"],
    ["#4fa6ed", "#4fa6ed"],  # Focused (Lightblue)
    ["#bf68d9", "#bf68d9"],
    ["#48b0bd", "#48b0bd"],
]

layout_theme = {
    "border_focus": colours[6],
    "border_normal": colours[2],
    "margin": 20,
    "border_width": 2,
}

layouts = [
    # layout.Bsp(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Stack(stacks=2, **layout_theme),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Slice(**layout_theme),


    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.Stack(num_stacks=2),
]

prompt = f"{os.environ['USER']}@{socket.gethostname()}: "

widget_defaults = dict(background=colours[0],
                       foreground=colours[1],
                       font="Roboto Nerd Font Regular",
                       fontsize=12,
                       padding=1)

extension_defaults = widget_defaults.copy()

widgets = [
    widget.Sep(
        foreground=colours[0],
        linewidth=4),
    widget.Image(
        filename="~/.config/qtile/py.png",
        mouse_callbacks=({
            "Button1": lambda: qtile.cmd_spawn("rofi -show drun"),
            "Button3": lambda: qtile.cmd_spawn("rofi -show run"),
        }),
        scale=True),
    widget.KeyboardLayout(
        configured_keyboards=['latam','us'],
        foreground=colours[6],
        fontsize=10,),

    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.GroupBox(
        active=colours[4],      # Green
        inactive=colours[6],    # Blue

        highlight_method="line",
        highlight_color = ['2d2d2d', '282828'],
        borderwidth = 1,

        # In use screen
        this_current_screen_border=colours[7],  # Purple
        this_screen_border=colours[7],          # Purple

        # 2nd screens
        other_current_screen_border=colours[3], # Gray
        other_screen_border=colours[3], # Gray
        # other_current_screen_border="#ffa500", #RED
        # other_screen_border="#ffa500",  # ORANGE
       

        urgent_border=colours[3],
        urgent_text=colours[3],
        disable_drag=True,
        invert_mouse_wheel=True,
        margin=2,
        padding=0,
        rounded=True,
        urgent_alert_method="text"),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.CurrentLayout(
        foreground=colours[7],
        font="Roboto Nerd Font Bold"),

    widget.Cmus(
        noplay_color=colours[2],
        play_color=colours[1]),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.WindowName(
        max_chars=75),
        
    widget.CPU(
        foreground=colours[3],
        format="🖥️ {load_percent}%",
        mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e btm"),
        },
        update_interval=1.0),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.MemoryGraph(
        foreground=colours[4],
        border_color=colours[0], # Same as background
        fill_color=colours[4],
        graph_color=colours[4],
        line_width=1,
        type='line',
        mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e btm"),
        },
        update_interval=1.0),    
    widget.Memory(
        foreground=colours[4],
        format=" {MemUsed:.0f} MB",
        mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e btm"),
        },
        update_interval=1.0),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.NetGraph(
        foreground=colours[5],
        border_color=colours[0], # Same as background
        fill_color=colours[5],
        graph_color=colours[5],
        line_width=1,
        bandwidth_type='down',
        type='line',
        # type=,
        mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn("gnome-control-center"),
        },),
    widget.Net(
        foreground = colours[5],
        format = " ⬇️{down} ⬆️{up} 📡",
        ),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.PulseVolume(
        foreground=colours[6],
        fmt="🔈 {}",
        update_interval=0.1,
        volume_app="pavucontrol",
        step=5),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Battery(
        foreground=colours[7],
        format="{char} {percent:2.0%}",
        charge_char="⚡ ",
        discharge_char="🔋 ",
        empty_char="🪫 ",
        full_char="🔌 ",
        unknown_char="? ",
        low_foreground=colours[3],
        low_percentage=0.15,
        show_short_text=False,
        notify_below=15,
        update_interval=10),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Clock(
        foreground=colours[8],
        format="📅 %a %b %d  %I:%M %P"),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Systray(
        icon_size=14,
        padding=4),
]


reduced_widgets = [
    widget.Sep(
        foreground=colours[0],
        linewidth=4),
    widget.Image(
        filename="~/.config/qtile/py.png",
        mouse_callbacks=({
            "Button1": lambda: qtile.cmd_spawn("rofi -show drun"),
            "Button3": lambda: qtile.cmd_spawn("rofi -show run"),
        }),
        scale=True),
    widget.KeyboardLayout(
        configured_keyboards=['latam','us'],
        foreground=colours[6],
        fontsize=10,),

    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.GroupBox(
        active=colours[4],      # Green
        inactive=colours[6],    # Blue

        highlight_method="line",
        highlight_color = ['2d2d2d', '282828'],
        borderwidth = 3,

        # In use screen
        this_current_screen_border=colours[3],  # Purple
        this_screen_border=colours[3],          # Purple

        # 2nd screens
        other_current_screen_border=colours[7], # Gray
        other_screen_border=colours[7], # Gray       

        urgent_border=colours[3],
        urgent_text=colours[3],
        disable_drag=True,
        invert_mouse_wheel=True,
        margin=2,
        padding=0,
        rounded=True,
        urgent_alert_method="text"),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.CurrentLayout(
        foreground=colours[7],
        font="Roboto Nerd Font Bold"),

    widget.Cmus(
        noplay_color=colours[2],
        play_color=colours[1]),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.WindowName(
        max_chars=75),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
    widget.Clock(
        foreground=colours[8],
        format="📅 %a %b %d  %I:%M %P")
]

def status_bar(widget_list):
  return bar.Bar(widget_list, 20, opacity=0.85)

def random_wallpaper():
    return '/home/lucas/Pictures/wallpapers/'+'gruvbox_style.png'#'house.png' #'pixel_art.png'



# How to solve monitor being duplicated?:
# xrandr --output HDMI-1-0 --mode 1920x1080 --noprimary --left-of eDP-1


# How I'm setting up the dual monitor thing:
# I want the big monitor to have the widgets, but if i only have the 
# notebook connected, then that monitor should have them
screens = [
    # Primary Monitor (eDP-1 Notebook)
    Screen(
        top=status_bar(widgets),
        wallpaper='/home/lucas/Pictures/wallpapers/'+'gruvbox_style.png',
        wallpaper_mode="stretch",
    ),
]

# Now we check if we have more than one monitor.
connected_monitors = (subprocess.run(
    "xrandr | busybox grep 'connected' | busybox cut -d' ' -f2",
    check=True,
    shell=True,
    stdout=subprocess.PIPE,
).stdout.decode("UTF-8").split("\n")[:-1].count("connected"))

# In which case, we rearrenge the screens list
if connected_monitors == 2:
    screens = [
        # Primary Monitor (eDP-1 Notebook)
        Screen(
            top=status_bar(reduced_widgets),
            wallpaper='/home/lucas/Pictures/wallpapers/'+'house.png',
            wallpaper_mode="stretch",
        ),

        # Secondary Monitor (HDMI-1-0)
        Screen(
            top=status_bar(widgets),
            wallpaper='/home/lucas/Pictures/wallpapers/'+'gruvbox_style.png',
            wallpaper_mode="stretch",
        ),
    ]

auto_fullscreen = True
auto_minimize = True
bring_front_click = False
cursor_warp = False
dgroups_app_rules = []
dgroups_key_binder = None
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title="Authentication"),
        Match(title="branchdialog"),
        Match(title="Chat"),
        Match(title="pinentry"),
        Match(title="Polls"),
        Match(wm_class="Arandr"),
        Match(wm_class="Blueman-adapters"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="confirm"),
        Match(wm_class="confirmreset"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="Gnome-screenshot"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="notification"),
        Match(wm_class="Pavucontrol"),
        Match(wm_class="splash"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="toolbar"),
    ])
focus_on_window_activation = "smart"
follow_mouse_focus = False
reconfigure_screens = True

# pylint: disable=consider-using-with
@hook.subscribe.restart
def delete_cache():
    shutil.rmtree(os.path.expanduser("~/.config/qtile/__pycache__"))

@hook.subscribe.shutdown
def stop_apps():
    delete_cache()
    # Algo que quieras correr cuando se apaga Qtile
    qtile.cmd_spawn(["killall", "dunst", "picom", "udiskie"])

@hook.subscribe.startup_once
def start_apps():
    # Algo que quieras ejecutar cuando bootea Qtile
    qtile.cmd_spawn(["picom", "-b"])
    qtile.cmd_spawn(["dunst"])
    qtile.cmd_spawn(["udiskie", "-asn", "-f", "pcmanfm-qt"])

wmname = "LG3D"
