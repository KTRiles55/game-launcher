import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ctypes import windll, byref, sizeof, c_int


class Launcher(tb.Toplevel):
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("")
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.iconbitmap("empty.ico")

# Applying the custom window attribute for the border color
        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x5e3d49  # Dark purple color
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

        # Widgets
        self.menu = Menu(self)

        # Run program
        self.mainloop()


class Menu(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widget()

    def create_widget(self):
        style = tb.Style()
        style2 = tb.Style()
        style2.configure("TNotebook.Tab", font=("Unispace", "18", "bold"))
        style.configure("custom.TNotebook", padding=[0,0], tabmargins=[0,0,0,0], tabposition="nsew")
        notebook = tb.Notebook(self, style="custom.TNotebook")

        # Tabs
        home_tab = tb.Frame(notebook)
        library_tab = tb.Frame(notebook)
        store_tab = tb.Frame(notebook)
        account_tab = tb.Frame(notebook)

        # Adding Tabs
        notebook.add(home_tab, text="Home")
        notebook.add(library_tab, text="Library")
        notebook.add(store_tab, text="Store")
        notebook.add(account_tab, text="Account")

        notebook.pack(expand=True, fill=BOTH)

        # Tab Labels
        home_label = tb.Label(home_tab)
        home_label.pack(pady=20)
        library_label = tb.Label(library_tab)
        library_label.pack(pady=20)
        store_label = tb.Label(store_tab)
        store_label.pack(pady=20)
        account_label = tb.Label(account_tab)
        account_label.pack(pady=20)


if __name__ == "__main__":
    app = Launcher((1400,900))
    app.mainloop()
