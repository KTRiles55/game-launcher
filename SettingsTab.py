import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import ImageTk, Image 
from ttkbootstrap import Style

class SettingsTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Define the controller options and their default settings
        self.controller_options = {
            "Xbox 360": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Vibration": ["Off", "On"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button A": ["Jump", "Attack", "Interact"],
                "Button B": ["Crouch", "Reload", "Dodge"],
                "Button X": ["Inventory", "Special Ability", "Map"],
                "Button Y": ["Use Item", "Melee", "Sprint"]
            },
            "Xbox One": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Vibration": ["Off", "On"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button A": ["Jump", "Attack", "Interact"],
                "Button B": ["Crouch", "Reload", "Dodge"],
                "Button X": ["Inventory", "Special Ability", "Map"],
                "Button Y": ["Use Item", "Melee", "Sprint"]
            },
            "PlayStation 4": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Vibration": ["Off", "On"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button X": ["Jump", "Attack", "Interact"],
                "Button Circle": ["Crouch", "Reload", "Dodge"],
                "Button Square": ["Inventory", "Special Ability", "Map"],
                "Button Triangle": ["Use Item", "Melee", "Sprint"]
            },
            "PlayStation 5": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Vibration": ["Off", "On"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button X": ["Jump", "Attack", "Interact"],
                "Button Circle": ["Crouch", "Reload", "Dodge"],
                "Button Square": ["Inventory", "Special Ability", "Map"],
                "Button Triangle": ["Use Item", "Melee", "Sprint"]
            },
            "Nintendo Switch": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Vibration": ["Off", "On"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button A": ["Jump", "Attack", "Interact"],
                "Button B": ["Crouch", "Reload", "Dodge"],
                "Button X": ["Inventory", "Special Ability", "Map"],
                "Button Y": ["Use Item", "Melee", "Sprint"]
            },
            "GameCube": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Vibration": ["Off", "On"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button A": ["Jump", "Attack", "Interact"],
                "Button B": ["Crouch", "Reload", "Dodge"],
                "Button X": ["Inventory", "Special Ability", "Map"],
                "Button Y": ["Use Item", "Melee", "Sprint"]
            },
            "Mouse": {
                "Sensitivity": ["Low", "Medium", "High"],
                "Invert Y-axis": ["Off", "On"],
                "Invert X-axis": ["Off", "On"],
                "Button Left": ["Primary Weapon", "Fire", "Use"],
                "Button Right": ["Secondary Weapon", "Zoom", "Grenade"],
                "Button Middle": ["Reload", "Melee", "Special Ability"]
            }
        }

        # Create the main frame for the sub tabs
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Create the sub tabs
        self.sub_tabs = ttk.Notebook(self.main_frame)
        self.controller_tab = ttk.Frame(self.sub_tabs)
        self.account_tab = ttk.Frame(self.sub_tabs)
        self.close_app_tab = ttk.Frame(self.sub_tabs)
        self.sub_tabs.add(self.controller_tab, text="Select Controller")
        self.sub_tabs.add(self.account_tab, text="Select Account Setting")
        self.sub_tabs.add(self.close_app_tab, text="Close App")
        self.sub_tabs.pack(expand=True, fill="both")

        # Create the controller dropdown
        self.controller_label = ttk.Label(self.controller_tab, text="Select Controller:")
        self.controller_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.controller_var = tk.StringVar()
        self.controller_var.set("Xbox One")  # Default controller selection
        self.controller_dropdown = ttk.Combobox(self.controller_tab, textvariable=self.controller_var, values=list(self.controller_options.keys()))
        self.controller_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Bind the controller dropdown selection to update the settings
        self.controller_dropdown.bind("<<ComboboxSelected>>", self.update_controller_settings)

        # Create the settings frame for controller settings
        self.controller_settings_frame = ttk.LabelFrame(self.controller_tab, text="Controller Settings")
        self.controller_settings_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create the apply button for controller settings
        self.apply_button = ttk.Button(self.controller_tab, text="Apply Controller Settings", command=self.apply_controller_settings)
        self.apply_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Update the controller settings
        self.update_controller_settings()

        # Create the account dropdown
        self.account_label = ttk.Label(self.account_tab, text="Select Account Setting:")
        self.account_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.account_var = tk.StringVar()
        self.account_var.set("Manage")  # Default account setting selection
        self.account_dropdown = ttk.Combobox(self.account_tab, textvariable=self.account_var, values=["Manage", "Privacy", "Data Management"])
        self.account_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Bind the account dropdown selection to update the account settings
        self.account_dropdown.bind("<<ComboboxSelected>>", self.update_account_settings)

        # Create the account settings frame
        self.account_settings_frame = ttk.LabelFrame(self.account_tab, text="Account Settings")
        self.account_settings_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Update the account settings
        self.update_account_settings()

        # Create the close app button
        self.close_app_button = ttk.Button(self.close_app_tab, text="Close App", command=confirm_close_app)
        self.close_app_button.pack(padx=10, pady=10)

    def update_account_settings(self, event=None):
        selected_setting = self.account_var.get()

        # Clear existing account settings
        for widget in self.account_settings_frame.winfo_children():
            widget.destroy()

        # Create buttons for selected account setting
        if selected_setting == "Manage":
            options = ["Change Username", "Change Password", "Delete Account"]
        elif selected_setting == "Privacy":
            options = ["Toggle Privacy Settings", "Manage Blocked Users", "Clear Browsing Data"]
        elif selected_setting == "Data Management":
            options = ["Download Data", "Manage Cloud Storage", "Clear Local Data"]

        # Populate the account settings frame with options
        for index, option in enumerate(options):
            button = ttk.Button(self.account_settings_frame, text=option, command=lambda option=option: self.handle_account_option(option))
            button.grid(row=index, column=0, padx=5, pady=5, sticky="w")

    def handle_account_option(self, option):
        messagebox.showinfo("Account Setting Selected", f"You clicked on: {option}")

    def update_controller_settings(self, event=None):
        selected_controller = self.controller_var.get()

        # Clear existing settings
        for widget in self.controller_settings_frame.winfo_children():
            widget.destroy()

        # Create labels and dropdowns for each setting
        row = 0
        for setting, options in self.controller_options[selected_controller].items():
            label = ttk.Label(self.controller_settings_frame, text=setting + ":")
            label.grid(row=row, column=0, padx=5, pady=5)
            dropdown_var = tk.StringVar()
            dropdown = ttk.Combobox(self.controller_settings_frame, textvariable=dropdown_var, state="readonly", values=options)
            dropdown.grid(row=row, column=1, padx=5, pady=5)
            dropdown_var.set(options[0])  # Default option
            row += 1

    def apply_controller_settings(self):
        confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to apply controller settings?")
        if confirmation:
            selected_controller = self.controller_var.get()
            messagebox.showinfo("Settings Applied", f"Controller settings for {selected_controller} applied successfully.")

def create_settings_window():
    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_tab = SettingsTab(settings_window)
    settings_tab.pack(expand=True, fill="both")
    
    # Add close button to close the window
    close_button = ttk.Button(settings_window, text="Close", command=settings_window.destroy)
    close_button.pack()

def confirm_close_app():
    confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to close the application?")
    if confirmation:
        exit()

def main():
    global root
    root = tk.Tk()
    root.title("Main Window")

    settings_button = ttk.Button(root, text="Open Settings", command=create_settings_window)
    settings_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
