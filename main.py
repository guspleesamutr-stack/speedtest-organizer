# SPEEDTEST ORGANIZER V5.4 FINAL (FULL COMBINED)


# =========================================================
# SPEEDTEST ORGANIZER V5.4 FINAL
# =========================================================
#
# REQUIRE:
# py -3.12 -m pip install customtkinter tkinterdnd2 pillow
#
# RUN:
# py -3.12 V5.4.py
#
# =========================================================

# Standard Library
import os
import shutil

# Third-party
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

# Local
from core.constants import *
from core.folder import get_mesh_folder


# =========================================================
# CONFIG
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# APP
# =========================================================

class SpeedtestOrganizer(TkinterDnD.Tk):

    def __init__(self):

        super().__init__()

        self.title("Speedtest Organizer V5.4 FINAL")
        self.geometry("1700x950")
        self.minsize(1280, 720)

        self.root_folder = ""

        self.last_batch = []

        self.near_files = []
        self.normal_files = []
        self.worst_files = []

        self.session_locked = False

        self.build_ui()

        self.update_all_previews()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self, height=60)

        top.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        top.grid_columnconfigure(0, weight=1)

        self.root_label = ctk.CTkLabel(
            top,
            text="No Root Folder Selected",
            font=("Arial", 18, "bold")
        )

        self.root_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20
        )

        root_btn = ctk.CTkButton(
            top,
            text="Select Root Folder",
            width=180,
            height=40,
            command=self.select_root_folder
        )

        root_btn.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        left = ctk.CTkFrame(self, width=360)

        left.grid(
            row=1,
            column=0,
            sticky="ns",
            padx=(10, 5),
            pady=(0, 10)
        )

        left.grid_propagate(False)

        title = ctk.CTkLabel(
            left,
            text="CONTROL PANEL",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=(15, 10))

        self.control_scroll = ctk.CTkScrollableFrame(
            left,
            width=320
        )

        self.control_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.tabs = ctk.CTkTabview(
            self.control_scroll,
            width=300
        )

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.sa_tab = self.tabs.add("Standalone")
        self.mesh_tab = self.tabs.add("Mesh")

        self.build_standalone_tab()
        self.build_mesh_tab()

        self.session_label = ctk.CTkLabel(
            left,
            text="SESSION UNLOCKED",
            font=("Arial", 18, "bold"),
            text_color="orange"
        )

        self.session_label.pack(
            pady=(5, 5)
        )

        self.lock_btn = ctk.CTkButton(
            left,
            text="LOCK SESSION",
            height=42,
            command=self.toggle_session
        )

        self.lock_btn.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        right = ctk.CTkFrame(self)

        right.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=(0, 10)
        )

        right.grid_columnconfigure(0, weight=1)
        right.grid_columnconfigure(1, weight=1)
        right.grid_columnconfigure(2, weight=1)

        right.grid_rowconfigure(0, weight=1)

        self.create_zone(right, "NEAR (0m)", 0, "green")
        self.create_zone(right, "NORMAL (5m)", 1, "orange")
        self.create_zone(right, "WORST (10m)", 2, "red")

    # =====================================================
    # CONTROL
    # =====================================================

    def create_control(
        self,
        parent,
        title,
        values,
        variable,
        command=None
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=8
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 14, "bold")
        )

        label.pack(anchor="w", pady=(0,5))

        combo = ctk.CTkComboBox(
            frame,
            values=values,
            variable=variable,
            height=38,
            command=command
        )

        combo.pack(fill="x")

        return combo

    # =====================================================
    # STANDALONE
    # =====================================================

    def build_standalone_tab(self):

        self.sa_band = ctk.StringVar(value="5GHz")
        self.sa_channel = ctk.StringVar(value="")
        self.sa_device_type = ctk.StringVar(value="Laptop")
        self.sa_device_name = ctk.StringVar(value="Laptop wifi7")
        self.sa_other_device = ctk.StringVar()

        self.sa_band_combo = self.create_control(
            self.sa_tab,
            "Band",
            ["2.4GHz", "5GHz", "MLO"],
            self.sa_band,
            self.sa_band_changed
        )

        self.sa_channel_combo = self.create_control(
            self.sa_tab,
            "Channel",
            ["", "36", "64", "100"],
            self.sa_channel,
            lambda e: self.update_all_previews()
        )

        self.sa_device_type_combo = self.create_control(
            self.sa_tab,
            "Device Type",
            ["Laptop", "Mobile"],
            self.sa_device_type,
            self.sa_device_type_changed
        )

        self.sa_device_combo = self.create_control(
            self.sa_tab,
            "Device Name",
            LAPTOPS,
            self.sa_device_name,
            lambda e: self.update_all_previews()
        )

        self.sa_other_entry = ctk.CTkEntry(
            self.sa_tab,
            placeholder_text="Custom Device Name",
            textvariable=self.sa_other_device,
            height=38
        )

        self.sa_other_entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.sa_other_entry.bind(
            "<KeyRelease>",
            lambda e: self.update_all_previews()
        )

    # =====================================================
    # MESH
    # =====================================================

    def build_mesh_tab(self):

        self.mesh_topology = ctk.StringVar(value="Daisy Chain")
        self.mesh_backhaul = ctk.StringVar(value=BACKHAULS[0])
        self.mesh_router = ctk.StringVar(value="Main")

        self.mesh_test_type = ctk.StringVar(value="WiFi")

        self.mesh_band = ctk.StringVar(value="5GHz")
        self.mesh_channel = ctk.StringVar(value="")

        self.mesh_lan_type = ctk.StringVar(
            value="LAN 1G Performance"
        )

        self.mesh_device_type = ctk.StringVar(value="Laptop")
        self.mesh_device_name = ctk.StringVar(value="Laptop wifi7")
        self.mesh_other_device = ctk.StringVar()

        self.create_control(
            self.mesh_tab,
            "Topology",
            ["Daisy Chain", "Star"],
            self.mesh_topology,
            lambda e: self.update_all_previews()
        )

        self.create_control(
            self.mesh_tab,
            "Backhaul",
            BACKHAULS,
            self.mesh_backhaul,
            lambda e: self.update_all_previews()
        )

        self.create_control(
            self.mesh_tab,
            "Router",
            ["Main", "AP1", "AP2"],
            self.mesh_router,
            lambda e: self.update_all_previews()
        )

        self.create_control(
            self.mesh_tab,
            "Test Type",
            ["WiFi", "LAN"],
            self.mesh_test_type,
            self.mesh_test_type_changed
        )

        self.mesh_band_combo = self.create_control(
            self.mesh_tab,
            "Band",
            ["2.4GHz", "5GHz", "MLO"],
            self.mesh_band,
            self.mesh_band_changed
        )

        self.mesh_channel_combo = self.create_control(
            self.mesh_tab,
            "Channel",
            ["", "36", "64", "100"],
            self.mesh_channel,
            lambda e: self.update_all_previews()
        )

        self.mesh_lan_combo = self.create_control(
            self.mesh_tab,
            "LAN Type",
            [
                "LAN 1G Performance",
                "LAN 2.5G Performance"
            ],
            self.mesh_lan_type,
            lambda e: self.update_all_previews()
        )

        self.mesh_lan_combo.pack_forget()

        self.mesh_device_type_combo = self.create_control(
            self.mesh_tab,
            "Device Type",
            ["Laptop", "Mobile"],
            self.mesh_device_type,
            self.mesh_device_type_changed
        )

        self.mesh_device_combo = self.create_control(
            self.mesh_tab,
            "Device Name",
            LAPTOPS,
            self.mesh_device_name,
            lambda e: self.update_all_previews()
        )

        self.mesh_other_entry = ctk.CTkEntry(
            self.mesh_tab,
            placeholder_text="Custom Device Name",
            textvariable=self.mesh_other_device,
            height=38
        )

        self.mesh_other_entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.mesh_other_entry.bind(
            "<KeyRelease>",
            lambda e: self.update_all_previews()
        )

    # =====================================================
    # TEST TYPE
    # =====================================================

    def mesh_test_type_changed(self, value):

        if value == "LAN":

            self.mesh_lan_combo.pack(
                fill="x",
                padx=10,
                pady=8
            )

        else:

            self.mesh_lan_combo.pack_forget()

        self.update_all_previews()

    # =====================================================
    # ZONE
    # =====================================================

    def create_zone(self, parent, title, column, color):
        pass

    # =====================================================
    # CHANNEL
    # =====================================================

    def sa_band_changed(self, value):

        if value == "2.4GHz":

            self.sa_channel_combo.configure(
                values=[
                    "",
                    "1", "2", "3", "4", "5",
                    "6", "7", "8", "9", "10",
                    "11", "12", "13"
                ]
            )

        elif value == "5GHz":

            self.sa_channel_combo.configure(
                values=[
                    "",
                    "36",
                    "64",
                    "100"
                ]
            )

        else:

            self.sa_channel_combo.configure(
                values=[""]
            )

        self.sa_channel.set("")

        self.update_all_previews()


    def mesh_band_changed(self, value):

        if value == "2.4GHz":

            self.mesh_channel_combo.configure(
                values=[
                    "",
                    "1", "2", "3", "4", "5",
                    "6", "7", "8", "9", "10",
                    "11", "12", "13"
                ]
            )

        elif value == "5GHz":

            self.mesh_channel_combo.configure(
                values=[
                    "",
                    "36",
                    "64",
                    "100"
                ]
            )
    
        else:

            self.mesh_channel_combo.configure(
                values=[""]
            )

        self.mesh_channel.set("")

        self.update_all_previews()

    # =====================================================
    # DEVICE TYPE
    # =====================================================

    def sa_device_type_changed(self, value):

        if value == "Laptop":

            self.sa_device_combo.configure(
                values=LAPTOPS
            )

            self.sa_device_name.set(
                LAPTOPS[0]
            )

        else:

            self.sa_device_combo.configure(
                values=MOBILES
            )

            self.sa_device_name.set(
                MOBILES[0]
            )

        self.update_all_previews()


    def mesh_device_type_changed(self, value):

        if value == "Laptop":

            self.mesh_device_combo.configure(
                values=LAPTOPS
            )

            self.mesh_device_name.set(
                LAPTOPS[0]
            )

        else:

            self.mesh_device_combo.configure(
                values=MOBILES
            )

            self.mesh_device_name.set(
                MOBILES[0]
            )

        self.update_all_previews()

    # =====================================================
    # ROOT
    # =====================================================

    def select_root_folder(self):
        pass

    # =====================================================
    # SESSION
    # =====================================================

    def toggle_session(self):
        pass

    # =====================================================
    # PREVIEW
    # =====================================================

    def update_all_previews(self):
        pass

    # =====================================================
    # FILENAME
    # =====================================================

    def build_filename(self, distance):

        current = self.tabs.get()

        if current == "Standalone":

            device = self.sa_device_name.get()

            if device == "Other":

                custom = self.sa_other_device.get().strip()

                if custom:
                    device = custom

            filename = (
                f"SA_"
                f"{distance}_"
                f"{self.sa_band.get()}_"
                f"{device}"
            )

            if self.sa_channel.get():

                filename += (
                    f"_CH{self.sa_channel.get()}"
                )

            folder = "00. Standalone"

        else:

            topology = (
                "DC"
                if self.mesh_topology.get() == "Daisy Chain"
                else "Star"
            )

            folder = get_mesh_folder(
                topology,
                backhaul
            )

            if self.mesh_test_type.get() == "WiFi":

                device = self.mesh_device_name.get()

                if device == "Other":

                    custom = self.mesh_other_device.get().strip()

                    if custom:
                        device = custom

                filename = (
                    f"Mesh_"
                    f"{topology}_"
                    f"{backhaul}_"
                    f"{router}_"
                    f"{distance}_"
                    f"{self.mesh_band.get()}_"
                    f"{device}"
                )

                if self.mesh_channel.get():

                    filename += (
                        f"_CH{self.mesh_channel.get()}"
                    )

            else:

                filename = (
                    f"Mesh_"
                    f"{topology}_"
                    f"{backhaul}_"
                    f"{router}_"
                    f"{self.mesh_lan_type.get()}"
                )

        return folder, filename

    # =====================================================
    # ZONE
    # =====================================================

    def create_zone(self, parent, title, column, color):

        zone = ctk.CTkFrame(parent)

        zone.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8
        )

        zone.grid_rowconfigure(1, weight=1)
        zone.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            zone,
            text=title,
            font=("Arial", 22, "bold"),
            text_color=color
        )

        label.grid(
            row=0,
            column=0,
            pady=(10,5)
        )

        drop = ctk.CTkTextbox(
            zone,
            font=("Arial", 14),
            wrap="word"
        )

        drop.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )
        
        thumb_label = ctk.CTkLabel(
            zone,
            text=""
        )

        thumb_label.grid(
            row=1,
            column=0,
            sticky="se",
            padx=15,
            pady=15
        )

        drop.insert(
            "end",
            "\nDROP IMAGE HERE"
        )

        preview = ctk.CTkTextbox(
            zone,
            height=95,
            font=("Consolas", 11),
            wrap="word"
        )

        preview.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0,5)
        )

        action = ctk.CTkFrame(
            zone,
            fg_color="transparent"
        )

        action.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0,10)
        )

        action.grid_columnconfigure((0,1,2,3), weight=1)

        select_btn = ctk.CTkButton(
            action,
            text="Select",
            height=36,
            command=lambda z=("0m" if title == "NEAR (0m)" else "5m" if title=="NORMAL (5m)" else "10m"):
            self.select_images(z)
        )

        select_btn.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=3
        )

        clear_btn = ctk.CTkButton(
            action,
            text="Clear",
            height=36,
            command=lambda z=("0m" if title == "NEAR (0m)" else "5m" if title=="NORMAL (5m)" else "10m"):
            self.clear_zone(z)
        )

        clear_btn.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=3
        )

        copy_btn = ctk.CTkButton(
            action,
            text="Copy",
            height=36,
            command=lambda z=("0m" if title == "NEAR (0m)" else "5m" if title=="NORMAL (5m)" else "10m"):
            self.copy_zone(z)
        )

        copy_btn.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=3
        )

        undo_btn = ctk.CTkButton(
            action,
            text="Undo",
            height=36,
            command=self.undo_last
        )

        undo_btn.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=3
        )

        drop.drop_target_register(DND_FILES)

        drop.dnd_bind(
            "<<Drop>>",
            lambda e:
            self.drop_files(
                e,
                "0m" if title == "NEAR (0m)" else
                "5m" if title == "NORMAL (5m)" else
                "10m"
            )
        )

        if title == "NEAR (0m)":

            self.near_drop = drop
            self.near_preview = preview
            self.near_thumb = thumb_label

        elif title == "NORMAL (5m)":

            self.normal_drop = drop
            self.normal_preview = preview
            self.normal_thumb = thumb_label

        else:

            self.worst_drop = drop
            self.worst_preview = preview
            self.worst_thumb = thumb_label

    # =====================================================
    # FILES
    # =====================================================

    def select_images(self, zone):

        files = filedialog.askopenfilenames(
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png")
            ]
        )

        if not files:
            return

        self.assign_files(zone, list(files))

    def drop_files(self, event, zone):

        files = self.tk.splitlist(event.data)

        self.assign_files(zone, list(files))

    def assign_files(self, zone, files):

        if zone == "0m":

            self.near_files = files
            self.refresh_drop(
                self.near_drop,
                files
            )

        elif zone == "5m":

            self.normal_files = files
            self.refresh_drop(
                self.normal_drop,
                files
            )

        else:

            self.worst_files = files
            self.refresh_drop(
                self.worst_drop,
                files
            )
            
        self.update_thumbnail(
            zone,
            files
            )

        self.update_all_previews()

    def refresh_drop(self, widget, files):

        widget.delete("1.0", "end")

        for file in files:

            widget.insert(
                "end",
                os.path.basename(file) + "\n"
            )

    def clear_zone(self, zone):

        if zone == "0m":

            self.near_files = []

            self.near_drop.delete("1.0", "end")
            self.near_drop.insert("end","\nDROP IMAGE HERE")

            self.near_thumb.configure(
                image=None,
                text=""
            )

        elif zone == "5m":

            self.normal_files = []

            self.normal_drop.delete("1.0", "end")
            self.normal_drop.insert("end","\nDROP IMAGE HERE")

            self.normal_thumb.configure(
                image=None,
                text=""
            )

        else:

            self.worst_files = []

            self.worst_drop.delete("1.0", "end")
            self.worst_drop.insert("end","\nDROP IMAGE HERE")

            self.worst_thumb.configure(
                image=None,
                text=""
            )

        self.update_all_previews()

    # =====================================================
    # PREVIEW
    # =====================================================

    def update_all_previews(self):

        self.update_preview_box(
            self.near_preview,
            "Near(0m)"
        )

        self.update_preview_box(
            self.normal_preview,
            "Normal(5m)"
        )

        self.update_preview_box(
            self.worst_preview,
            "Worst(10m)"
        )

    def update_preview_box(self, widget, distance):

        folder, filename = self.build_filename(distance)

        widget.delete("1.0", "end")

        widget.insert(
            "end",
            f"{folder}\\\n"
        )

        widget.insert(
            "end",
            f"{filename}.jpg"
        )
    # =====================================================
# THUMBNAIL
# =====================================================

    def update_thumbnail(self, zone, files):

        if zone == "0m":

            thumb_widget = self.near_thumb

        elif zone == "5m":

            thumb_widget = self.normal_thumb

        else:

           thumb_widget = self.worst_thumb

        # CLEAR THUMBNAIL
        thumb_widget.configure(
            image=None,
            text=""
        )

        if not files:
            return

        try:

            image = Image.open(files[0])

            image.thumbnail((180, 100))

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            thumb_widget.configure(
                image=ctk_image,
                text=""
            )

            thumb_widget.image = ctk_image

        except Exception as e:

            print(e)


    # =====================================================
    # COPY
    # =====================================================

    def copy_zone(self, zone):

        if not self.root_folder:

            messagebox.showerror(
                "Error",
                "Please select root folder"
            )
            return

        if zone == "0m":

            files = self.near_files
            distance = "Near(0m)"

        elif zone == "5m":

            files = self.normal_files
            distance = "Normal(5m)"

        else:

            files = self.worst_files
            distance = "Worst(10m)"

        if not files:

            messagebox.showwarning(
                "Empty",
                "No image selected"
            )
            return

        folder, filename = self.build_filename(distance)

        dst_folder = os.path.join(
            self.root_folder,
            folder
        )

        os.makedirs(
            dst_folder,
            exist_ok=True
        )

        self.last_batch = []

        for index, src in enumerate(files):

            ext = os.path.splitext(src)[1]

            name = filename

            if len(files) > 1:

                name += f"_{index+1}"

            final = os.path.join(
                dst_folder,
                name + ext
            )

            shutil.copy2(src, final)

            self.last_batch.append(final)

        messagebox.showinfo(
            "Success",
            f"Copied {len(files)} file(s)"
        )

    # =====================================================
    # ROOT
    # =====================================================

    def select_root_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.root_folder = folder

            self.root_label.configure(
                text=folder
            )

    # =====================================================
    # SESSION
    # =====================================================

    def toggle_session(self):

        self.session_locked = (
            not self.session_locked
        )

        if self.session_locked:

            self.session_label.configure(
                text="SESSION LOCKED",
                text_color="green"
            )

            self.lock_btn.configure(
                text="UNLOCK SESSION"
            )

        else:

            self.session_label.configure(
                text="SESSION UNLOCKED",
                text_color="orange"
            )

            self.lock_btn.configure(
                text="LOCK SESSION"
            )

    # =====================================================
    # UNDO
    # =====================================================

    def undo_last(self):

        deleted = 0

        for file in self.last_batch:

            if os.path.exists(file):

                os.remove(file)

                deleted += 1

        self.last_batch = []

        messagebox.showinfo(
            "Undo",
            f"Removed {deleted} file(s)"
        )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app = SpeedtestOrganizer()

    app.mainloop()
# เหลือแค่ functions ด้านล่างบางส่วนที่คุณมีอยู่แล้วจาก version ก่อนหน้า เช่น create_zone / copy / clear / undo / preview ให้นำมาวางต่อท้ายได้เลยครับ
