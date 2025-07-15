import customtkinter as ctk
from jobseeker import JobSeekerUI
from employer import EmployerUI
from members import MembersUI
from utils import clear_frame
import tkinter as tk

class JobPortalApp:
    def __init__(self, root):
        #initial setup of app and window parameters
        self.root = root
        self.root.title("JobSync")  # set window title
        self.root.geometry("1280x720")  # set window size
        self.root.minsize(800, 650)  # minimum size limit

        #create different UI classes
        self.jobseeker_ui = JobSeekerUI(root, self.main_menu)
        self.employer_ui = EmployerUI(root, self.main_menu)
        self.credits_ui = MembersUI(root, self.main_menu)

        #call the main menu at start
        self.main_menu()

    def main_menu(self):
        #clear previous content from root
        clear_frame(self.root)

        # -------------------------------------------------------
        # HEADER SECTION
        # -------------------------------------------------------
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=60)
        header_frame.pack(side=tk.TOP, fill="x")

        #this is the header label
        header_label = ctk.CTkLabel(
            header_frame,
            text="JobSync: Job Portal Application",
            font=("Helvetica", 20, "bold"),
            fg_color="#444444",
            text_color="white"
        )
        header_label.pack(pady=15)

        # -------------------------------------------------------
        # MAIN MENU CONTENT
        # -------------------------------------------------------
        #create a description label
        ctk.CTkLabel(
            self.root,
            text="Job Portal para sa mga katulad kong walang trabaho",
            font=("Arial", 24, "italic")
        ).pack(pady=20)

        #set uniform dimensions for buttons
        uniform_width = 300
        uniform_height = 60

        #job search button setup
        job_search_button = ctk.CTkButton(
            self.root,
            text="Job Search",
            command=self.jobseeker_ui.jobseeker_login_page,
            fg_color="#2173b3",
            hover_color="#1a5a8e",
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            width=uniform_width,
            height=uniform_height
        )
        job_search_button.pack(pady=10)

        #employer portal button setup
        employer_portal_button = ctk.CTkButton(
            self.root,
            text="Employer Portal",
            command=self.employer_ui.employer_login_page,
            fg_color="#c65d14",
            hover_color="#9c460f",
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            width=uniform_width,
            height=uniform_height
        )
        employer_portal_button.pack(pady=10)

        #exit button to quit the app
        exit_button = ctk.CTkButton(
            self.root,
            text="Exit",
            command=self.root.quit,
            fg_color="#841e1e",
            hover_color="#641616",
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            width=uniform_width,
            height=uniform_height
        )
        exit_button.pack(pady=10)

        # -------------------------------------------------------
        # FOOTER SECTION
        # -------------------------------------------------------
        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")

        #footer label with credits info
        link_label = ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        )
        link_label.pack(side=tk.LEFT, padx=10, pady=5)
        #right click on label will show the members page (credits)
        link_label.bind("<Button-3>", lambda event: self.credits_ui.members_page())

if __name__ == "__main__":
    #init the main tkinter custom window
    root = ctk.CTk()
    app = JobPortalApp(root)
    root.mainloop()  #run the main loop
