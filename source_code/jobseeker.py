import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection
from utils import clear_frame

class JobSeekerUI:
    # init: setting up the class
    def __init__(self, root, switch_to_main_menu):
        self.root = root
        self.switch_to_main_menu = switch_to_main_menu
        self.current_username = None
        self.current_user_id = None 
        self.temp_username = None
        self.temp_password = None
        self.job_results = {}
        self.app_records = {}

    # sets current username
    def set_current_username(self, username):
        self.current_username = username


    """===================================================================================================================================================================================="""

    # jobseeker login page ui
    def jobseeker_login_page(self):
        clear_frame(self.root)
        
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        title_label = ctk.CTkLabel(
            header_frame,
            text="Job Seeker",
            font=("Arial", 30),
            fg_color="#444444",
            text_color="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")
        ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(footer_frame, text="Back", command=self.switch_to_main_menu).pack(side=tk.RIGHT, padx=5, pady=5)
        
        form_frame = ctk.CTkFrame(self.root, fg_color="#646463", width=400, height=285, corner_radius=10)
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False) 

        ctk.CTkLabel(form_frame, text="Log In", font=("Arial", 30), anchor="w").pack(padx=30, pady=(30, 15), anchor="w")
        username_entry = ctk.CTkEntry(form_frame, width=350, height=50, placeholder_text="   Username")
        username_entry.pack(pady=(5,10), padx=15)
        password_entry = ctk.CTkEntry(form_frame, width=350, height=50, show="*", placeholder_text="   Password", )
        password_entry.pack(pady=10, padx=15)
        login_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)

        # try log in
        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT u.*, j.name 
                FROM users u
                JOIN jobseekers j ON u.id = j.user_id
                WHERE u.username = %s AND u.password = %s AND u.role = %s
            """
            cursor.execute(query, (username, password, "jobseeker"))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                self.current_username = username
                self.current_user_id = user['id']
                messagebox.showinfo("Login Success", f"Welcome, {user['name']}!")
                self.job_search()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials!")

        ctk.CTkButton(login_button_frame, text="Log in", command=attempt_login, fg_color="#EC7A01", hover_color="#bd6201").pack(side=tk.RIGHT)
        
        ctk.CTkLabel(self.root, text="Don't have an account?", font=("Helvetica", 12)).pack(pady=(10, 0))
        ctk.CTkButton(self.root, text="Register", command=self.jobseeker_register_step1).pack(pady=(5, 10))
        
    # first step registration page  
    def jobseeker_register_step1(self):
        clear_frame(self.root)
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        title_label = ctk.CTkLabel(
            header_frame,
            text="Job Seeker",
            font=("Arial", 30),
            fg_color="#444444",
            text_color="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)
        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")
        ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(footer_frame, text="Back", command=self.jobseeker_login_page).pack(side=tk.RIGHT, padx=5, pady=5)
        form_frame = ctk.CTkFrame(self.root, fg_color="#646463", width=400, height=285, corner_radius=10)
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False)
        ctk.CTkLabel(form_frame, text="Sign Up", font=("Arial", 30), anchor="w")\
            .pack(padx=30, pady=(30, 15), anchor="w")
        username_entry = ctk.CTkEntry(form_frame, width=350, height=50, placeholder_text="   Username")
        username_entry.pack(pady=(5, 10), padx=15)
        password_entry = ctk.CTkEntry(form_frame, width=350, height=50, show="*", placeholder_text="   Password")
        password_entry.pack(pady=10, padx=15)
        signup_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)
        
        # go next step registration
        def next_step():
            temp_username = username_entry.get().strip()
            temp_password = password_entry.get().strip()
            
            if not temp_username or not temp_password:
                messagebox.showerror("Error", "Username and Password cannot be empty.")
                return

            if len(temp_username) < 3:
                messagebox.showerror("Error", "Username must be at least 3 characters long.")
                return

            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection to database failed")
                return

            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (temp_username,))
            existing_user = cursor.fetchone()
            cursor.close()
            conn.close()

            if existing_user:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                return

            if len(temp_password) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters long.")
                return

            self.temp_username = temp_username
            self.temp_password = temp_password
            self.jobseeker_register_step2()

        ctk.CTkButton(signup_button_frame, text="Next", command=next_step).pack(side=tk.RIGHT)

    # secon step registration
    def jobseeker_register_step2(self):
        clear_frame(self.root)
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        title_label = ctk.CTkLabel(
            header_frame,
            text="Job Seeker",
            font=("Arial", 30),
            fg_color="#444444",
            text_color="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)
        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")
        ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(footer_frame, text="Back", command=self.jobseeker_register_step1).pack(side=tk.RIGHT, pady=5, padx=5)
        form_frame = ctk.CTkFrame(self.root, fg_color="#646463", width=400, height=450, corner_radius=10)
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False)
        ctk.CTkLabel(form_frame, text="Sign Up", font=("Arial", 30), anchor="w").pack(padx=30, pady=(30, 5), anchor="w")
        ctk.CTkLabel(form_frame, text="Please fill in the following details", font=("Arial", 12), anchor="w").pack(padx=30, pady=(0, 10), anchor="w")
        
        gender_var = tk.StringVar(value="   Gender")
        name_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Name")
        name_entry.pack(pady=5, padx=15)
        age_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Age")
        age_entry.pack(pady=5, padx=15)
        location_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Location")
        location_entry.pack(pady=5, padx=15)
        contact_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Contact Number")
        contact_entry.pack(pady=5, padx=15)
        gender_option = ctk.CTkOptionMenu(form_frame, values=["Male", "Female", "Others"], variable=gender_var, width=350, height=40, font=("Arial", 14), fg_color="#343638", button_color="#1a1b1c", button_hover_color="#515151", text_color="#9e9e8f",
                                            dropdown_font=("Arial", 14))
        gender_option.pack(pady=5, padx=15)
        signup_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)
        
        # complete registration process
        def complete_registration():
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            location = location_entry.get().strip()
            gender = gender_option.get().strip()
            contact = contact_entry.get().strip()

            if not (name and age and location and gender and contact):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                parsed_age = int(age)
                if parsed_age < 1 or parsed_age > 150:
                    messagebox.showerror("Error", "Input a valid age")
                    return
            except ValueError:
                messagebox.showerror("Error", "Input a valid age")
                return
            
            if gender == "Gender":
                messagebox.showerror("Error", "Please select your gender.")
                return

            if not contact.isdigit():
                messagebox.showerror("Error", "Contact number must only contain numbers.")
                return

            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection to database failed")
                return
            cursor = conn.cursor()
            
            try:
                query_users = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                cursor.execute(query_users, (self.temp_username, self.temp_password, 'jobseeker'))
                user_id = cursor.lastrowid
                query_jobseekers = ("INSERT INTO jobseekers (user_id, name, age, location, gender, contact) "
                                    "VALUES (%s, %s, %s, %s, %s, %s)")
                cursor.execute(query_jobseekers, (user_id, name, parsed_age, location, gender, contact))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                conn.close()
            
            self.jobseeker_login_page()

        ctk.CTkButton(signup_button_frame, text="Register", command=complete_registration, fg_color="#EC7A01", hover_color="#bd6201").pack(side=tk.RIGHT)
    
    
    """===================================================================================================================================================================================="""
    
    # search jobs page
    def job_search(self):
        self.root.configure(bg="#1f1f1f")
        clear_frame(self.root)

        def validate_int(new_value):
            if new_value == "":
                return True
            return new_value.isdigit()

        def validate_location(new_value):
            if new_value == "":
                return True
            for char in new_value:
                if not (char.isalpha() or char.isspace()):
                    return False
            return True

        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        title_label = ctk.CTkLabel(
            header_frame,
            text="Job Search",
            font=("Arial", 30),
            fg_color="#444444",
            text_color="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)
        filter_container = ctk.CTkFrame(header_frame, fg_color="#444444")
        filter_container.pack(side=tk.RIGHT, padx=10, pady=10)
        int_vcmd = (self.root.register(validate_int), '%P')
        loc_vcmd = (self.root.register(validate_location), '%P')
        ctk.CTkLabel(filter_container, text="Min Salary:", fg_color="#444444", text_color="white").grid(row=0, column=0, padx=5, pady=2)
        salary_entry = ctk.CTkEntry(filter_container, width=100, validate="key", validatecommand=int_vcmd)
        salary_entry.grid(row=0, column=1, padx=5, pady=2)
        ctk.CTkLabel(filter_container, text="Min Age Req:", fg_color="#444444", text_color="white").grid(row=0, column=2, padx=5, pady=2)
        age_entry = ctk.CTkEntry(filter_container, width=100, validate="key", validatecommand=int_vcmd)
        age_entry.grid(row=0, column=3, padx=5, pady=2)
        ctk.CTkLabel(filter_container, text="Location:", fg_color="#444444", text_color="white").grid(row=0, column=4, padx=5, pady=2)
        location_entry = ctk.CTkEntry(filter_container, width=100, validate="key", validatecommand=loc_vcmd)
        location_entry.grid(row=0, column=5, padx=5, pady=2)
        ctk.CTkButton(filter_container, text="Filter", command=lambda: search_jobs(), width=80).grid(row=0, column=6, padx=5, pady=2)

        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")
        ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10)
        
        # logout confirmation
        def confirm_back():
            if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout and go back to the Main Menu?"):
                self.switch_to_main_menu()

        button_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        button_frame.pack(side=tk.RIGHT, pady=5)
        ctk.CTkButton(button_frame, text="Track Applications", command=self.track_applications, fg_color="#00991b", hover_color="#006612").pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Log-Out", command=confirm_back, font=("Helvetica", 16, "bold"), fg_color="#e61800", hover_color="#991000").pack(side=tk.LEFT, padx=5)

        job_scroll_frame = ctk.CTkScrollableFrame(self.root, width=600, height=1000, corner_radius=0, fg_color="transparent")
        job_scroll_frame.pack(fill="x", pady=5)

        # searching jobs
        def search_jobs():
            salary_filter = salary_entry.get().strip()
            age_filter = age_entry.get().strip()
            location_filter = location_entry.get().strip()
            query = """
                SELECT j.*, e.company_name
                FROM jobs j
                LEFT JOIN employers e ON j.employer_id = e.id
                WHERE 1=1
            """
            params = []
            if salary_filter:
                query += " AND j.salary >= %s"
                params.append(salary_filter)
            if age_filter:
                query += " AND j.age_requirement <= %s"
                params.append(age_filter)
            if location_filter:
                query += " AND j.location LIKE %s"
                params.append("%" + location_filter + "%")
            print("Executing Query:", query, params)
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, tuple(params))
                jobs = cursor.fetchall()
                print("Jobs fetched:", jobs)
            except Exception as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
                return
            finally:
                cursor.close()
                conn.close()
            for widget in job_scroll_frame.winfo_children():
                widget.destroy()
            self.job_results = []
            for job in jobs:
                job_card = ctk.CTkFrame(
                    job_scroll_frame,
                    corner_radius=8,
                    border_width=1,
                    border_color="#D3D3D3"
                )
                job_card.pack(fill="x", padx=15, pady=5)
                job_label = ctk.CTkLabel(
                    job_card,
                    text=job['job_title'],
                    font=("Helvetica", 28, "bold"),
                    anchor="w"
                )
                job_label.pack(fill="x", padx=10, pady=10)
                job_card.bind("<Double-Button-1>", lambda event, job=job: self.view_job_details(job))
                job_label.bind("<Double-Button-1>", lambda event, job=job: self.view_job_details(job))
                self.job_results.append(job)
        search_jobs()

    """===================================================================================================================================================================================="""

    # view details of job
    def view_job_details(self, job):
        clear_frame(self.root)
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            header_frame,
            text="Job Details",
            font=("Arial", 30),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")
        ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(footer_frame, text="Back to Job Search", command=self.job_search).pack(side=tk.RIGHT, padx=5, pady=5)
        job_title_label = ctk.CTkLabel(
            self.root,
            text=job['job_title'],
            font=("Helvetica", 72, "bold"),
            anchor="w"
        )
        job_title_label.pack(fill="x", padx=23, pady=(30, 12))
        details_card = ctk.CTkFrame(
            self.root,
            corner_radius=8,
            border_width=2,
            border_color="#D3D3D3"
        )
        details_card.pack(pady=(8, 40), padx=15, fill="x")
        details_data = [
            ("Employer:", job.get('company_name', 'N/A')),
            ("Location:", job['location']),
            ("Salary:", job['salary']),
            ("Age Requirement:", job['age_requirement'])
        ]
        # loop details
        for label_text, value in details_data:
            row_frame = ctk.CTkFrame(details_card, fg_color="transparent")
            row_frame.pack(side=tk.LEFT, padx=30, pady=10)
            category_label = ctk.CTkLabel(
                row_frame,
                text=label_text,
                font=("Helvetica", 20, "bold"),
                anchor="w"
            )
            category_label.pack(side=tk.LEFT)
            value_label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                font=("Helvetica", 20, "italic"),
                anchor="w"
            )
            value_label.pack(side=tk.LEFT, padx=5)
        # user apply job
        def apply_job():
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
            cursor = conn.cursor()
            try:
                check_query = "SELECT * FROM applications WHERE job_id = %s AND jobseeker_id = %s"
                cursor.execute(check_query, (job['id'], self.current_user_id))
                existing_application = cursor.fetchone()
                if existing_application:
                    messagebox.showerror("Application already exists", "You have already applied for this job!")
                    return
                insert_query = (
                    "INSERT INTO applications (job_id, jobseeker_id, status, message) VALUES (%s, %s, %s, %s)"
                )
                cursor.execute(insert_query, (job['id'], self.current_user_id, "Pending", ""))
                conn.commit()
                messagebox.showinfo("Success", "Your application has been submitted.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                conn.close()
            self.job_search()
        ctk.CTkButton(
            self.root,
            text="Apply for this Job",
            command=apply_job,
            font=("Helvetica", 16, "bold"),
            fg_color="#009688",
            width=400,
            height=60
        ).pack(pady=5)

    """===================================================================================================================================================================================="""

    # delete a application 
    def delete_application(self, app_id):
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed")
            return
        cursor = conn.cursor()
        try:
            query = "DELETE FROM applications WHERE id = %s AND jobseeker_id = %s"
            cursor.execute(query, (app_id, self.current_user_id))
            conn.commit()
            messagebox.showinfo("Success", "Application deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()
        self.track_applications()

    # confirm delete process  
    def confirm_delete(self, app_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
            self.delete_application(app_id)

    # track applied jobs 
    def track_applications(self):
        clear_frame(self.root)
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            header_frame,
            text="Track Applications",
            font=("Arial", 30),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        footer_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill="x")
        ctk.CTkLabel(
            footer_frame,
            text="© CCCS105 Information Management 1 Group 10 - Final Project",
            font=("Helvetica", 10),
            fg_color="#444444",
            text_color="white"
        ).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(footer_frame, text="Back to Job Search", command=self.job_search).pack(side=tk.RIGHT, padx=5, pady=5)
        apps_scroll_frame = ctk.CTkScrollableFrame(
            self.root, 
            width=600, 
            height=1000, 
            corner_radius=8, 
            fg_color="transparent"
        )
        apps_scroll_frame.pack(fill="x", pady=5)
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed")
            return
        cursor = conn.cursor(dictionary=True)
        query = (
            "SELECT a.id, a.status, a.message, j.job_title FROM applications a "
            "JOIN jobs j ON a.job_id = j.id WHERE a.jobseeker_id = %s"
        )
        cursor.execute(query, (self.current_user_id,))
        apps = cursor.fetchall()
        cursor.close()
        conn.close()
        self.app_records = {}
        # list each app
        for app in apps:
            app_card = ctk.CTkFrame(
                apps_scroll_frame,
                corner_radius=8,
                border_width=1,
                border_color="#D3D3D3"
            )
            app_card.pack(fill="x", padx=10, pady=5)
            details_text = f"{app['job_title']} | {app['status']}"
            app_label = ctk.CTkLabel(
                app_card,
                text=details_text,
                font=("Helvetica", 18, "bold"),
                anchor="w"
            )
            app_label.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            button_frame = ctk.CTkFrame(app_card, fg_color="transparent", corner_radius=0)
            button_frame.pack(side="right", padx=10, pady=10)
            view_msg_button = ctk.CTkButton(
                button_frame,
                text="View Message",
                width=100,
                command=lambda msg=app['message']: messagebox.showinfo(
                    "Employer Message", 
                    msg.strip() if msg and msg.strip() else "No message yet"
                )
            )
            view_msg_button.pack(side="left", padx=(0, 5))
            delete_button = ctk.CTkButton(
                button_frame,
                text="Delete",
                fg_color="#e61800",
                hover_color="#991000",
                width=80,
                command=lambda app_id=app['id']: self.confirm_delete(app_id)
            )
            delete_button.pack(side="left")
            self.app_records[app['id']] = app
