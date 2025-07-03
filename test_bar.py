import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

CONFIG_FILE = "config.json"

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        
        self.tooltip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify='left',
                         background='#2d2d2d', foreground='white',
                         relief='flat', borderwidth=0,
                         font=('Segoe UI', 9),
                         padx=8, pady=4)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "build_config": "Debug",
            "auto_build": False,
            "default_device": "iPhone 15",
            "device_ip": "",
            "simulator_path": "",
            "build_input_dir": "",
            "build_output_dir": ""
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def build_action():
    folder_path = filedialog.askdirectory(title="Select Project Folder")
    if folder_path:
        print(f"Building project in: {folder_path}")
        # Add your build logic here using the selected folder
    else:
        print("Build cancelled - no folder selected")

def run_simulator():
    print("Run Simulator button clicked")
    # Add your simulator logic here

def run_device():
    print("Run Device button clicked")
    # Add your device logic here

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("450x550")
    settings_window.configure(bg='#f0f0f0')
    settings_window.resizable(False, False)
    settings_window.transient(root)
    settings_window.grab_set()
    
    settings_window.geometry("+%d+%d" % (root.winfo_rootx() + 50, root.winfo_rooty() + 50))
    
    main_frame = tk.Frame(settings_window, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    title_label = tk.Label(main_frame, text="Settings", font=('Segoe UI', 14, 'bold'), 
                          bg='#f0f0f0', fg='#333333')
    title_label.pack(pady=(0, 20))

    # Build Settings Frame
    build_frame = tk.LabelFrame(main_frame, text="Build Settings", font=('Segoe UI', 10),
                               bg='#f0f0f0', fg='#333333')
    build_frame.pack(fill=tk.X, pady=(0, 15))

    tk.Label(build_frame, text="Build Configuration:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(anchor='w')
    config_combo = ttk.Combobox(build_frame, values=["Debug", "Release", "Testing"], state="readonly")
    config_combo.pack(fill=tk.X, pady=3)

    auto_build_var = tk.BooleanVar()
    auto_build_check = tk.Checkbutton(build_frame, text="Auto-build on file changes",
                                     variable=auto_build_var, bg='#f0f0f0',
                                     font=('Segoe UI', 9))
    auto_build_check.pack(anchor='w', pady=(0, 5))

    # New build input/output directories
    def dir_picker(entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)

    tk.Label(build_frame, text="Build Input Directory:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(anchor='w')
    build_input_frame = tk.Frame(build_frame, bg='#f0f0f0')
    build_input_frame.pack(fill=tk.X, pady=2)
    build_input_entry = tk.Entry(build_input_frame)
    build_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    build_input_btn = ttk.Button(build_input_frame, text="Browse", width=8, command=lambda: dir_picker(build_input_entry))
    build_input_btn.pack(side=tk.LEFT, padx=5)

    tk.Label(build_frame, text="Build Output Directory:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(anchor='w')
    build_output_frame = tk.Frame(build_frame, bg='#f0f0f0')
    build_output_frame.pack(fill=tk.X, pady=2)
    build_output_entry = tk.Entry(build_output_frame)
    build_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    build_output_btn = ttk.Button(build_output_frame, text="Browse", width=8, command=lambda: dir_picker(build_output_entry))
    build_output_btn.pack(side=tk.LEFT, padx=5)

    # Simulator Settings Frame
    sim_frame = tk.LabelFrame(main_frame, text="Simulator Settings", font=('Segoe UI', 10),
                             bg='#f0f0f0', fg='#333333')
    sim_frame.pack(fill=tk.X, pady=(0, 15))

    tk.Label(sim_frame, text="Default Device:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(anchor='w')
    device_combo = ttk.Combobox(sim_frame,
                                values=["iPhone 15", "iPhone 15 Pro", "iPad", "Android Phone"],
                                state="readonly")
    device_combo.pack(fill=tk.X, pady=3)

    # Default Device IP
    tk.Label(sim_frame, text="Default Device IP:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(anchor='w')
    device_ip_entry = tk.Entry(sim_frame)
    device_ip_entry.pack(fill=tk.X, pady=3)

    # Simulator executable path with file picker
    def file_picker(entry_widget):
        file = filedialog.askopenfilename(title="Select Simulator Executable")
        if file:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file)

    tk.Label(sim_frame, text="Simulator Executable Path:", bg='#f0f0f0', font=('Segoe UI', 9)).pack(anchor='w')
    sim_path_frame = tk.Frame(sim_frame, bg='#f0f0f0')
    sim_path_frame.pack(fill=tk.X, pady=2)
    sim_path_entry = tk.Entry(sim_path_frame)
    sim_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    sim_path_btn = ttk.Button(sim_path_frame, text="Browse", width=8, command=lambda: file_picker(sim_path_entry))
    sim_path_btn.pack(side=tk.LEFT, padx=5)

    # Load existing config into settings
    config = load_config()
    config_combo.set(config.get("build_config", "Debug"))
    auto_build_var.set(config.get("auto_build", False))
    device_combo.set(config.get("default_device", "iPhone 15"))
    device_ip_entry.insert(0, config.get("device_ip", ""))
    sim_path_entry.insert(0, config.get("simulator_path", ""))
    build_input_entry.insert(0, config.get("build_input_dir", ""))
    build_output_entry.insert(0, config.get("build_output_dir", ""))

    button_frame = tk.Frame(main_frame, bg='#f0f0f0')
    button_frame.pack(fill=tk.X, pady=(20, 0))

    def save_settings():
        new_config = {
            "build_config": config_combo.get(),
            "auto_build": auto_build_var.get(),
            "default_device": device_combo.get(),
            "device_ip": device_ip_entry.get(),
            "simulator_path": sim_path_entry.get(),
            "build_input_dir": build_input_entry.get(),
            "build_output_dir": build_output_entry.get()
        }
        save_config(new_config)
        print(f"Settings saved: {new_config}")
        messagebox.showinfo("Settings", "Settings saved successfully!")
        settings_window.destroy()

    def cancel_settings():
        settings_window.destroy()

    cancel_btn = ttk.Button(button_frame, text="Cancel", command=cancel_settings)
    cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))

    save_btn = ttk.Button(button_frame, text="Save", command=save_settings)
    save_btn.pack(side=tk.RIGHT)

# Create main window
root = tk.Tk()
root.title("Device Controls")
root.geometry("210x42")
root.configure(bg='#f0f0f0')
root.resizable(False, False)

# Configure style
style = ttk.Style()
style.theme_use('clam')

# Make buttons square and uniform sized
BUTTON_SIZE = 60
style.configure('Modern.TButton',
                font=('Segoe UI', 16),
                padding=2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                relief='flat')

style.map('Modern.TButton',
          background=[('active', '#e8e8e8'),
                      ('pressed', '#d0d0d0')])

main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(main_frame, bg='#ffffff')
button_frame.pack(fill=tk.X)

def make_square_button(parent, text, command):
    btn = ttk.Button(parent, text=text, command=command, style='Modern.TButton')
    btn.config(width=4, padding=2)
    btn.pack(side=tk.LEFT)
    return btn

build_btn = make_square_button(button_frame, "🔨", build_action)
ToolTip(build_btn, "Build Project")

simulator_btn = make_square_button(button_frame, "▶", run_simulator)
ToolTip(simulator_btn, "Run Simulator")

device_btn = make_square_button(button_frame, "🔗", run_device)
ToolTip(device_btn, "Run on Device")

settings_btn = make_square_button(button_frame, "⚙️", open_settings)
ToolTip(settings_btn, "Settings")

# Load config and print on startup (optional)
config = load_config()
print("Loaded config on startup:", config)

if __name__ == "__main__":
    root.mainloop()
