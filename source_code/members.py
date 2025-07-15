import tkinter as tk
import customtkinter as ctk
from PIL import Image
from utils import clear_frame


class MembersUI:
    def __init__(self, root, main_menu_callback):
        self.root = root
        self.main_menu_callback = main_menu_callback  # init main menu callback

    def members_page(self):
        clear_frame(self.root)  # clear the frame for refresh
        self.root.configure(bg="#000000")  # set bg to black

        main_frame = ctk.CTkFrame(self.root, fg_color="#1b1b1b", corner_radius=0)
        main_frame.pack(fill="both", expand=True)

        # title label
        title_label = ctk.CTkLabel(
            main_frame,
            text="Group 10",
            font=("Rockwell", 36, "bold"),
            text_color="#EC7A01",
            fg_color="transparent"
        )
        title_label.pack(pady=(20, 10))

        # subtitle label
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="CCCS105 Information Management 1",   
            font=("Arial", 20),
            text_color="white",
            fg_color="transparent"
        ) 
        subtitle_label.pack(pady=(0, 20))

        # back button section
        back_button = ctk.CTkButton(
            main_frame,
            text="Back to Main Menu",
            command=self.main_menu_callback,
            fg_color="#EC7A01",
            hover_color="#D96C00"
        )
        back_button.pack(side=tk.BOTTOM, pady=(0, 20))

        content_frame = ctk.CTkFrame(main_frame, fg_color="#1b1b1b", corner_radius=10)
        content_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # group members section
        members_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        members_section.pack(pady=10, fill="x")

        group_title = ctk.CTkLabel(
            members_section,
            text="Group Members",
            font=("Arial", 24, "bold"),
            text_color="#EC7A01",
            fg_color="transparent"
        )
        group_title.pack(pady=(10, 1))

        members_frame = ctk.CTkFrame(members_section, fg_color="transparent")
        members_frame.pack(pady=(5, 2), padx=20, fill="x")

        members = [
            {"name": "Member 1 Name", "role": "Role ko daw haha", "image": "images/image1.jpg"},
            {"name": "Member 2 Name", "role": "Role model", "image": "images/image2.jpg"},
            {"name": "Member 3 Name", "role": "Rolling in the deep", "image": "images/image3.jpg"}
        ]

        for member in members:
            member_frame = ctk.CTkFrame(members_frame, fg_color="#1b1b1b", corner_radius=10)
            member_frame.pack(side=tk.LEFT, padx=15, pady=(5, 3), expand=True)

            try:
                image = Image.open(member["image"]).resize((150, 150))  # open and resize the image
                member_ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(150, 150))
                image_label = ctk.CTkLabel(member_frame, image=member_ctk_image, text="")
                image_label.pack(pady=(10, 5))
            except Exception:
                # if image fails to load, show fallback text
                ctk.CTkLabel(
                    member_frame,
                    text="HAHA alam na",
                    font=("Arial", 14),
                    text_color="white",
                    fg_color="transparent"
                ).pack(pady=(10, 5))

            # member name
            ctk.CTkLabel(
                member_frame,
                text=member["name"],
                font=("Arial", 16, "bold"),
                text_color="white",
                fg_color="transparent"
            ).pack(pady=(5, 1))

            # member role
            ctk.CTkLabel(
                member_frame,
                text=member["role"],
                font=("Arial", 14),
                text_color="white",
                fg_color="transparent"
            ).pack(pady=(1, 5))

        # instructor section
        instructor_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        instructor_section.pack(pady=(10, 5), fill="x")

        instructor_title = ctk.CTkLabel(
            instructor_section,
            text="Instructor",
            font=("Arial", 24, "bold"),
            text_color="#EC7A01",
            fg_color="transparent"
        )
        instructor_title.pack(pady=(7, 5))

        instructor_frame = ctk.CTkFrame(instructor_section, fg_color="#1b1b1b", corner_radius=10)
        instructor_frame.pack(pady=(10, 5))

        # instructor name
        ctk.CTkLabel(
            instructor_frame,
            text="Instructor Name",
            font=("Arial", 16, "bold"),
            text_color="white",
            fg_color="transparent"
        ).pack(pady=(5, 1))
        # instructor role
        ctk.CTkLabel(
            instructor_frame,
            text="Course Instructor",
            font=("Arial", 14),
            text_color="white",
            fg_color="transparent"
        ).pack(pady=(1, 5))
