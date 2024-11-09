import requests
import tkinter as tk
from tkinter import ttk, messagebox
import winsound
import json
import os
import xml.etree.ElementTree as ET

# Default configuration
CONFIG_PATH = "C:/GitHubRepos/MyPythonScripts/CastToTV/config.json"
DEFAULT_CONFIG = {
    "roku_ip": "192.168.1.207",
    "sound_effect_path": "C:/GitHubRepos/MyPythonScripts/CastToTV/269504__michorvath__button-click.wav"
}

# Load configuration
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
else:
    config = DEFAULT_CONFIG

ROKU_TV_IP = config["roku_ip"]
SOUND_EFFECT_PATH = config["sound_effect_path"]

def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def send_text_to_roku(text):
    for char in text:
        if char.isalnum():
            send_roku_command(f'keypress/Lit_{char}')
        elif char == ' ':
            send_roku_command('keypress/Lit_%20')
        # Add more special character handling as needed

def send_roku_command(command):
    winsound.PlaySound(SOUND_EFFECT_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)  # Play custom sound effect
    roku_url = f"http://{ROKU_TV_IP}:8060/{command}"
    try:
        response = requests.post(roku_url, timeout=5)  # Add a timeout to the request
        response.raise_for_status()
        print(f"Successfully sent command: {command}")
    except requests.RequestException as e:
        print(f"Failed to send command: {command}. Error: {e}, most likely because the Roku TV is loading app content.")


def get_installed_apps():
    roku_url = f"http://{ROKU_TV_IP}:8060/query/apps"
    try:
        response = requests.get(roku_url, timeout=5)  # Add a timeout to the request
        response.raise_for_status()
        apps_xml = response.content
        root = ET.fromstring(apps_xml)
        apps = [(app.text, app.attrib['id']) for app in root.findall('app')]
        print("Installed Apps:")
        for app_name, app_id in apps:
            print(f"{app_name} (ID: {app_id})")
        messagebox.showinfo("Installed Apps", "\n".join([f"{app_name} (ID: {app_id})" for app_name, app_id in apps]))
    except requests.RequestException as e:
        print(f"Failed to retrieve apps. Error: {e}")
        messagebox.showerror("Error", f"Failed to retrieve apps. Error: {e}")

def create_gui():
    root = tk.Tk()
    root.title("Roku Remote Control")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=5)
    style.configure("Symbol.TButton", font=("Helvetica", 20), padding=5)
    style.configure("TFrame", padding=10)
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("Red.TButton", font=("Helvetica", 20), background="red", foreground="black")  # Add this line to configure the red button style

    def on_key_press(event):
        key_mapping = {
            'Up': 'keypress/Up',
            'Down': 'keypress/Down',
            'Left': 'keypress/Left',
            'Right': 'keypress/Right',
            'Return': 'keypress/Select',
            'space': 'keypress/Play',
            'plus': 'keypress/VolumeUp',
            'minus': 'keypress/VolumeDown',
            'BackSpace': 'keypress/Back'  # Add this line for backspace key
        }
        if event.keysym in key_mapping:
            send_roku_command(key_mapping[event.keysym])

    def set_ip():
        def save_ip():
            global ROKU_TV_IP
            ROKU_TV_IP = ip_entry.get()
            config["roku_ip"] = ROKU_TV_IP
            save_config()
            ip_window.destroy()

        ip_window = tk.Toplevel(root)
        ip_window.title("Set Roku IP Address")
        tk.Label(ip_window, text="Enter Roku TV IP Address:\nHome -> Settings -> Network -> About -> IP address").pack(pady=5)
        ip_entry = tk.Entry(ip_window)
        ip_entry.pack(pady=5)
        ip_entry.insert(0, ROKU_TV_IP)
        tk.Button(ip_window, text="Save", command=save_ip).pack(pady=5)

    root.bind('<KeyPress>', on_key_press)

    # Frame for IP, Power, and Apps buttons
    top_frame = ttk.LabelFrame(root, text="Settings")
    top_frame.pack(fill='x', padx=10, pady=10)

    # IP button at the top left
    ip_button = ttk.Button(top_frame, text='Set IP', command=set_ip)
    ip_button.pack(side='left', padx=5, pady=5)

    # Power button at the top right
    power_button = ttk.Button(top_frame, text='⏻', command=lambda: send_roku_command('keypress/Power'), style="Red.TButton", width=5)
    power_button.pack(side='right', padx=5, pady=5)

    # Apps button at the top center
    apps_button = ttk.Button(top_frame, text='Show Apps', command=get_installed_apps)
    apps_button.pack(side='left', padx=10, pady=5)

    # Add YouTube URL button
    btn_youtube_url = ttk.Button(top_frame, text='Send Text', command=lambda: open_youtube_video(root))
    btn_youtube_url.pack(side='left', padx=5, pady=5)

    # Navigation and Volume frames
    nav_vol_frame = ttk.Frame(root)
    nav_vol_frame.pack(pady=10, fill="x")

    # Navigation buttons
    nav_frame = ttk.LabelFrame(nav_vol_frame, text="Navigation")
    nav_frame.pack(side='left', padx=10, pady=10)

    btn_up = ttk.Button(nav_frame, text='↑', command=lambda: send_roku_command('keypress/Up'), style="Symbol.TButton", width=5)
    btn_up.grid(row=0, column=1, pady=5)

    btn_left = ttk.Button(nav_frame, text='←', command=lambda: send_roku_command('keypress/Left'), style="Symbol.TButton", width=5)
    btn_left.grid(row=1, column=0, padx=5)

    btn_ok = ttk.Button(nav_frame, text='OK', command=lambda: send_roku_command('keypress/Select'))
    btn_ok.grid(row=1, column=1, padx=5)

    btn_right = ttk.Button(nav_frame, text='→', command=lambda: send_roku_command('keypress/Right'), style="Symbol.TButton", width=5)
    btn_right.grid(row=1, column=2, padx=5)

    btn_down = ttk.Button(nav_frame, text='↓', command=lambda: send_roku_command('keypress/Down'), style="Symbol.TButton", width=5)
    btn_down.grid(row=2, column=1, pady=5)

    # Volume buttons
    vol_frame = ttk.LabelFrame(nav_vol_frame, text="Volume")
    vol_frame.pack(side='left', padx=10, pady=10)

    btn_vol_up = ttk.Button(vol_frame, text='🔊', command=lambda: send_roku_command('keypress/VolumeUp'), style="Symbol.TButton", width=5)
    btn_vol_up.grid(row=0, column=0, padx=5, pady=5)

    btn_vol_down = ttk.Button(vol_frame, text='🔉', command=lambda: send_roku_command('keypress/VolumeDown'), style="Symbol.TButton", width=5)
    btn_vol_down.grid(row=1, column=0, padx=5, pady=5)

    btn_mute = ttk.Button(vol_frame, text='🔇', command=lambda: send_roku_command('keypress/VolumeMute'), style="Symbol.TButton", width=5)
    btn_mute.grid(row=0, column=1, padx=5, pady=5)

    # Controls and Channels frames
    ctrl_ch_frame = ttk.Frame(root)
    ctrl_ch_frame.pack(pady=10, fill="x")

    # Control buttons
    ctrl_frame = ttk.LabelFrame(ctrl_ch_frame, text="Controls")
    ctrl_frame.pack(side='left', padx=10, pady=10)

    btn_back = ttk.Button(ctrl_frame, text='↩', command=lambda: send_roku_command('keypress/Back'), style="Symbol.TButton", width=5)
    btn_back.grid(row=0, column=0, padx=5, pady=5)

    btn_home = ttk.Button(ctrl_frame, text='🏠', command=lambda: send_roku_command('keypress/Home'), style="Symbol.TButton", width=5)
    btn_home.grid(row=0, column=1, padx=5, pady=5)

    btn_play_pause = ttk.Button(ctrl_frame, text='⏯', command=lambda: send_roku_command('keypress/Play'), style="Symbol.TButton", width=5)
    btn_play_pause.grid(row=0, column=2, padx=5, pady=5)

    btn_rewind = ttk.Button(ctrl_frame, text='⏪', command=lambda: send_roku_command('keypress/Rev'), style="Symbol.TButton", width=5)
    btn_rewind.grid(row=1, column=0, padx=5, pady=5)

    btn_fast_forward = ttk.Button(ctrl_frame, text='⏩', command=lambda: send_roku_command('keypress/Fwd'), style="Symbol.TButton", width=5)
    btn_fast_forward.grid(row=1, column=2, padx=5, pady=5)

    # Channel buttons
    ch_frame = ttk.LabelFrame(ctrl_ch_frame, text="Channels")
    ch_frame.pack(side='left', padx=50, pady=10) 

    btn_ch_up = ttk.Button(ch_frame, text='🔼', command=lambda: send_roku_command('keypress/ChannelUp'), style="Symbol.TButton", width=5)
    btn_ch_up.grid(row=0, column=0, padx=5, pady=5)

    btn_ch_down = ttk.Button(ch_frame, text='🔽', command=lambda: send_roku_command('keypress/ChannelDown'), style="Symbol.TButton", width=5)
    btn_ch_down.grid(row=1, column=0, padx=5, pady=5)

    # Input buttons
    input_frame = ttk.LabelFrame(root, text="Inputs")
    input_frame.pack(pady=10, fill="x")

    btn_hdmi1 = ttk.Button(input_frame, text='HDMI 1', command=lambda: send_roku_command('keypress/InputHDMI1'))
    btn_hdmi1.grid(row=0, column=0, padx=5, pady=5)

    btn_hdmi2 = ttk.Button(input_frame, text='Xbox', command=lambda: send_roku_command('keypress/InputHDMI2'))
    btn_hdmi2.grid(row=0, column=1, padx=5, pady=5)

    btn_hdmi3 = ttk.Button(input_frame, text='HDMI 3', command=lambda: send_roku_command('keypress/InputHDMI3'))
    btn_hdmi3.grid(row=0, column=2, padx=5, pady=5)

    btn_switch = ttk.Button(input_frame, text='Nintendo Switch', command=lambda: send_roku_command('keypress/InputHDMI3'))
    btn_switch.grid(row=0, column=3, padx=5, pady=5)

    btn_av = ttk.Button(input_frame, text='AV', command=lambda: send_roku_command('keypress/InputAV1'))
    btn_av.grid(row=0, column=4, padx=5, pady=5)

    # App buttons
    app_frame = ttk.LabelFrame(root, text="Apps")
    app_frame.pack(pady=10, fill="x")

    app_colors = {
        'Netflix': '#E50914',
        'YouTube': '#FF0000',
        'Hulu': '#1CE783',
        'Disney+': '#113CCF',
        'Prime Video': '#00A8E1',
        'FOX LOCAL: Free Live News': '#003366',
        'Dropout': '#FFD700',
        'Paramount Plus': '#0060A9',
        'Peacock TV': '#000000',
        'Apple TV': '#000000',
        'Max': '#0033A0',
        'Pluto TV - Watch Free TV': '#000000',
        'Tubi - Free Movies & TV': '#E50914',
        'Fawesome - Free Movies and TV Shows': '#FF0000',
        'Crunchyroll': '#F47521',
        'Plex - Free Movies & TV': '#E5A00D',
        'AMC+': '#000000',
        'Spotify Music': '#1DB954',
        'The Roku Channel': '#6A0DAD'
    }

    apps = [
        ('Netflix', 'launch/12'),
        ('YouTube', 'launch/837'),
        ('Hulu', 'launch/2285'),
        ('Disney+', 'launch/291097'),
        ('Prime Video', 'launch/13'),
        ('FOX LOCAL: Free Live News', 'launch/711586'),
        ('Dropout', 'launch/253232'),
        ('Paramount Plus', 'launch/31440'),
        ('Peacock TV', 'launch/593099'),
        ('Apple TV', 'launch/551012'),
        ('Max', 'launch/61322'),
        ('Pluto TV - Watch Free TV', 'launch/74519'),
        ('Tubi - Free Movies & TV', 'launch/41468'),
        ('Fawesome - Free Movies and TV Shows', 'launch/48630'),
        ('Crunchyroll', 'launch/2595'),
        ('Plex - Free Movies & TV', 'launch/13535'),
        ('AMC+', 'launch/636527'),
        ('Spotify Music', 'launch/22297'),
        ('The Roku Channel', 'launch/151908')
    ]

    for i, (text, command) in enumerate(apps):
        button = ttk.Button(app_frame, text=text, width=15, command=lambda cmd=command: send_roku_command(cmd))
        button.grid(row=i // 4, column=i % 4, padx=5, pady=5)  # Adjust row and column to accommodate new button
        button.configure(style=f"{text}.TButton")
        style.configure(f"{text}.TButton", background=app_colors.get(text, '#FFFFFF'), foreground=app_colors.get(text, '#FFFFFF'))  # Set text color to match border color

    # Update the window size to fit all widgets
    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")

    root.mainloop()

def open_youtube_video(root):
    def play_video():
        url = url_entry.get()
        video_id = url.split('v=')[-1]
        send_roku_command(f'launch/837?contentID={video_id}')
        url_window.destroy()

    url_window = tk.Toplevel(root)
    url_window.title("Open YouTube Video")
    tk.Label(url_window, text="Enter text").pack(pady=5)
    url_entry = tk.Entry(url_window)
    url_entry.pack(pady=5)
    tk.Button(url_window, text="Open Youtube URL", command=play_video).pack(pady=5)
    tk.Button(url_window, text="Send Text", command=lambda: send_text_to_roku(url_entry.get())).pack(pady=5)

if __name__ == "__main__":
    create_gui()
