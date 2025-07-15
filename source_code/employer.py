import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection
from utils import clear_frame

# EmployerUI class, it handles interactive UI for employer
class EmployerUI:
    def __init__(self, root, switch_to_main_menu):
        self.root = root
        self.switch_to_main_menu = switch_to_main_menu
        self.current_username = None
        self.current_employer_id = None 
        self.temp_username = None
        self.temp_password = None
        self.app_records = {}  # store applications records

    def set_current_username(self, username):
        self.current_username = username  # set current username

    def set_current_employer_id(self, employer_id):
        self.current_employer_id = employer_id  # set employer id

    """===================================================================================================================================================================================="""

    def employer_login_page(self):
        clear_frame(self.root)  # clear previous frame
        
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Employer Login",
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

        password_entry = ctk.CTkEntry(form_frame, width=350, height=50, show="*", placeholder_text="   Password")
        password_entry.pack(pady=10, padx=15)
        
        login_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)

        # try to login function
        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT u.*, e.id AS employer_id, e.company_name 
                FROM users u 
                LEFT JOIN employers e ON u.id = e.user_id
                WHERE u.username = %s AND u.password = %s AND u.role = %s
            """
            cursor.execute(query, (username, password, "employer"))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                self.set_current_username(username)
                self.set_current_employer_id(user['employer_id'])
                company_name = user.get("company_name", username)
                messagebox.showinfo("Login Success", f"Welcome, {company_name}!")
                self.employer_menu()  # go to employer menu
            else:
                messagebox.showerror("Login Failed", "Invalid credentials!")

        ctk.CTkButton(login_button_frame, text="Log in", command=attempt_login, fg_color="#EC7A01", hover_color="#bd6201").pack(side=tk.RIGHT)

        ctk.CTkLabel(self.root, text="Don't have an account?", font=("Helvetica", 12)).pack(pady=(10, 0))
        ctk.CTkButton(self.root, text="Register", command=self.employer_register_step1).pack(pady=(5, 10))
        
    """===================================================================================================================================================================================="""

    def employer_register_step1(self):
        clear_frame(self.root)  # clear frame for register step 1

        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        title_label = ctk.CTkLabel(
            header_frame,
            text="Employer Registration",
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
        ctk.CTkButton(
            footer_frame,
            text="Back",
            command=self.employer_login_page
        ).pack(side=tk.RIGHT, padx=5, pady=5)

        form_frame = ctk.CTkFrame(
            self.root,
            fg_color="#646463",
            width=400,
            height=285,
            corner_radius=10
        )
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False)

        ctk.CTkLabel(
            form_frame,
            text="Sign Up",
            font=("Arial", 30),
            anchor="w"
        ).pack(padx=30, pady=(30, 15), anchor="w")

        username_entry = ctk.CTkEntry(
            form_frame,
            width=350,
            height=50,
            placeholder_text="   Username"
        )
        username_entry.pack(pady=(5, 10), padx=15)

        password_entry = ctk.CTkEntry(
            form_frame,
            width=350,
            height=50,
            show="*",
            placeholder_text="   Password"
        )
        password_entry.pack(pady=10, padx=15)

        signup_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)

        # save info and go next step
        def next_step():
            temp_username = username_entry.get().strip()
            temp_password = password_entry.get().strip()

            if not temp_username or not temp_password:
                messagebox.showerror("Error", "Username and Password required!")
                return

            self.temp_username = temp_username
            self.temp_password = temp_password
            self.employer_register_step2()

        ctk.CTkButton(signup_button_frame, text="Next", command=next_step).pack(side=tk.RIGHT)

    """===================================================================================================================================================================================="""

    def employer_register_step2(self):
        clear_frame(self.root)  # clear frame for register step 2
    
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

        ctk.CTkButton(footer_frame, text="Back", command=self.employer_register_step1).pack(side=tk.RIGHT, pady=5, padx=5)

        form_frame = ctk.CTkFrame(self.root, fg_color="#646463", width=400, height=300, corner_radius=10)
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text="Sign Up", font=("Arial", 30), anchor="w").pack(padx=30, pady=(30, 5), anchor="w")
        ctk.CTkLabel(form_frame, text="Please fill in the following details", font=("Arial", 12), anchor="w").pack(padx=30, pady=(0, 10), anchor="w")
        
        company_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Company Name")
        company_entry.pack(pady=5, padx=15)
        location_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Location")
        location_entry.pack(pady=5, padx=15)
        
        signup_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)
        
        # complete registration and save data
        def complete_registration():
            company_name = company_entry.get().strip()
            location = location_entry.get().strip()
            
            if not (company_name and location):
                messagebox.showerror("Error", "All fields are required.")
                return
            
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
            
            cursor = conn.cursor()
            try:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (self.temp_username,))
                if cursor.fetchone():
                    messagebox.showerror("Registration Failed", "Username already exists.")
                    return
                
                query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                cursor.execute(query, (self.temp_username, self.temp_password, "employer"))
                user_id = cursor.lastrowid
                
                query = "INSERT INTO employers (user_id, company_name, location) VALUES (%s, %s, %s)"
                cursor.execute(query, (user_id, company_name, location))
                
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                conn.close()
            
            self.employer_login_page()  # go back to login

        ctk.CTkButton(signup_button_frame, text="Register", command=complete_registration, fg_color="#EC7A01", hover_color="#bd6201").pack(side=tk.RIGHT)
    
    """===================================================================================================================================================================================="""

    def employer_menu(self):
        clear_frame(self.root)  # clear frame for employer menu

        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Employer Job Portal",
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

        def confirm_back():
            if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout and go back to the Main Menu?"):
                self.switch_to_main_menu()

        button_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        button_frame.pack(side=tk.RIGHT, pady=5)

        ctk.CTkButton(button_frame, text="Log-Out", command=confirm_back, font=("Helvetica", 16, "bold"), fg_color="#e61800", hover_color="#991000").pack(side=tk.LEFT, padx=5)

        uniform_width = 300
        uniform_height = 60

        post_job_button = ctk.CTkButton(
            self.root,
            text="Post a Job",
            command=self.post_job,
            fg_color="#2173b3",
            hover_color="#1a5a8e",
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            width=uniform_width,
            height=uniform_height
        )
        post_job_button.pack(pady=5, padx=20)

        view_posted_button = ctk.CTkButton(
            self.root,
            text="View Posted Jobs",
            command=self.posted_jobs,
            fg_color="#c65d14",
            hover_color="#9c460f",
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            width=uniform_width,
            height=uniform_height
        )
        view_posted_button.pack(pady=5, padx=20)

        review_applications_button = ctk.CTkButton(
            self.root,
            text="Review Applications",
            command=self.review_applications,
            fg_color="#1e8449",
            hover_color="#166437",
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            width=uniform_width,
            height=uniform_height
        )
        review_applications_button.pack(pady=5, padx=20)

    """===================================================================================================================================================================================="""

    def post_job(self):
        clear_frame(self.root)  # clear frame for posting a job
        
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Employer Job Posting",
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

        ctk.CTkButton(footer_frame, text="Back to Employer Menu", command=self.employer_menu).pack(side=tk.RIGHT, pady=5, padx=5)

        form_frame = ctk.CTkFrame(self.root, fg_color="#646463", width=400, height=390, corner_radius=10)
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text="Post a Job", font=("Arial", 30), anchor="w").pack(padx=30, pady=(30, 5), anchor="w")
        ctk.CTkLabel(form_frame, text="Please fill in the following details", font=("Arial", 12), anchor="w").pack(padx=30, pady=(0, 10), anchor="w")
        
        title_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Job Title")
        title_entry.pack(pady=5, padx=15)
        salary_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Salary")
        salary_entry.pack(pady=5, padx=15)
        location_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Location")
        location_entry.pack(pady=5, padx=15)
        age_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Age")
        age_entry.pack(pady=5, padx=15)
        
        signup_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)
        
        # submit job posting function
        def submit_job():
            title = title_entry.get().strip()
            location = location_entry.get().strip()
            salary_input = salary_entry.get().strip()
            age_req_input = age_entry.get().strip()
            
            if not (title and location and salary_input and age_req_input):
                messagebox.showerror("Validation Error", "All fields are required.")
                return

            try:
                salary = float(salary_input)
                age_req = int(age_req_input)
            except Exception as ex:
                messagebox.showerror("Validation Error", "Salary must be a number and Age Requirement must be an integer.")
                return

            if not hasattr(self, 'current_employer_id') or not self.current_employer_id:
                messagebox.showerror("Error", "Employer ID not set. Please log in again.")
                return

            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
                
            cursor = conn.cursor()
            try:
                query = ("INSERT INTO jobs (job_title, employer_id, location, salary, age_requirement) "
                        "VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(query, (title, self.current_employer_id, location, salary, age_req))
                conn.commit()
                messagebox.showinfo("Success", f"Job '{title}' posted successfully!")
                self.employer_menu()  # back to menu after posting
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                conn.close()

        ctk.CTkButton(signup_button_frame, text="Submit Job", command=submit_job, fg_color="#EC7A01", hover_color="#bd6201").pack(side=tk.RIGHT)

    """===================================================================================================================================================================================="""
    
    def posted_jobs(self):
        clear_frame(self.root)  # clear frame for posted job list
        
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Posted Jobs",
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
        ctk.CTkButton(footer_frame, text="Back to Employer Menu", command=self.employer_menu).pack(side=tk.RIGHT, pady=5, padx=5)

        jobs_scroll_frame = ctk.CTkScrollableFrame(self.root, width=600, height=1000, corner_radius=0, fg_color="transparent")
        jobs_scroll_frame.pack(fill="x", pady=5)

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed")
            return
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT id, job_title, location, salary FROM jobs WHERE employer_id = %s"
        cursor.execute(query, (self.current_employer_id,))
        jobs = cursor.fetchall()
        print("Jobs fetched from database:", jobs)
        cursor.close()
        conn.close()

        if not jobs:
            ctk.CTkLabel(jobs_scroll_frame, text="No jobs posted yet.", font=("Helvetica", 14)).pack(pady=10)
        else:
            for job in jobs:
                job_card = ctk.CTkFrame(
                    jobs_scroll_frame,
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
                job_label.pack(side=tk.LEFT, padx=20, pady=10)
               
                buttons_frame = ctk.CTkFrame(job_card, fg_color="transparent")
                buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)
                ctk.CTkButton(
                    buttons_frame,
                    text="Edit",
                    command=lambda job=job: self.edit_job(job)
                ).pack(side=tk.TOP, padx=5, pady=2)
                ctk.CTkButton(
                    buttons_frame,
                    text="Delete",
                    command=lambda job=job: self.delete_job(job)
                ).pack(side=tk.TOP, padx=5, pady=2)

        ctk.CTkButton(self.root, text="Back to Employer Menu", command=self.employer_menu).pack(pady=5)

    def edit_job(self, job):
        clear_frame(self.root)  # clear frame for editing job
        
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
        ctk.CTkButton(footer_frame, text="Back", command=self.employer_register_step1).pack(side=tk.RIGHT, pady=5, padx=5)

        form_frame = ctk.CTkFrame(self.root, fg_color="#646463", width=400, height=370, corner_radius=10)
        form_frame.pack(pady=20, padx=20, expand=True)
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text="Edit Job", font=("Arial", 30), anchor="w").pack(padx=30, pady=(30, 5), anchor="w")
        ctk.CTkLabel(form_frame, text="Please fill in the necessary details", font=("Arial", 12), anchor="w").pack(padx=30, pady=(0, 10), anchor="w")
        
        title_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Job Title")
        title_entry.insert(0, job['job_title'])
        title_entry.pack(pady=5, padx=15)
        location_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Location")
        location_entry.insert(0, job['location'])
        location_entry.pack(pady=5, padx=15)
        salary_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="   Salary")
        salary_entry.insert(0, job['salary'])
        salary_entry.pack(pady=5, padx=15)
        
        signup_button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_button_frame.pack(side=tk.BOTTOM, fill="x", padx=20, pady=20)
        
        # submit edit information
        def submit_edit():
            new_title = title_entry.get().strip()
            new_location = location_entry.get().strip()
            new_salary = salary_entry.get().strip()
            
            if not new_title:
                messagebox.showerror("Validation Error", "Job title cannot be empty.")
                return
            
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed.")
                return
            
            cursor = conn.cursor()
            query_update = ("UPDATE jobs SET job_title = %s, location = %s, salary = %s "
                            "WHERE id = %s AND employer_id = %s")
            try:
                cursor.execute(query_update, (new_title, new_location, new_salary, job['id'], self.current_employer_id))
                conn.commit()
                if cursor.rowcount == 0:
                    messagebox.showerror("Update Error", "No matching job found, or you are not authorized to update this job.")
                    return
            except Exception as e:
                messagebox.showerror("Update Error", str(e))
                return
            finally:
                cursor.close()
                conn.close()
            
            messagebox.showinfo("Success", "Job updated successfully!")
            self.posted_jobs()  # go back to posted jobs
        
        ctk.CTkButton(signup_button_frame, text="Submit Changes", command=submit_edit, fg_color="#EC7A01", hover_color="#bd6201").pack(side=tk.RIGHT)

    def delete_job(self, job):
        # confirm delete job
        answer = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete job '{job['job_title']}'?")
        if not answer:
            return
        
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed.")
            return
        
        cursor = conn.cursor()
        query_delete = "DELETE FROM jobs WHERE id = %s AND employer_id = %s"
        try:
            cursor.execute(query_delete, (job['id'], self.current_employer_id))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showerror("Deletion Error", "Job not found or unauthorized deletion attempt.")
                return
        except Exception as e:
            messagebox.showerror("Deletion Error", str(e))
            return
        finally:
            cursor.close()
            conn.close()
        
        messagebox.showinfo("Success", "Job deleted successfully!")
        self.posted_jobs()  # update the list

    """===================================================================================================================================================================================="""

    def review_applications(self):
        clear_frame(self.root)  # clear frame for reviewing applications
        
        header_frame = ctk.CTkFrame(self.root, fg_color="#444444", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            header_frame,
            text="Review Applications",
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
        ctk.CTkButton(
            footer_frame,
            text="Back to Employer Menu",
            command=self.employer_menu
        ).pack(side=tk.RIGHT, padx=5, pady=5)
        
        apps_scroll_frame = ctk.CTkScrollableFrame(
            self.root,
            width=600,
            height=1000,
            corner_radius=8,
            fg_color="transparent"
        )
        apps_scroll_frame.pack(pady=5, fill='x')
        
        print("Current Employer ID:", self.current_employer_id)
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed")
            return
        cursor = conn.cursor(dictionary=True)
        
        query = (
            "SELECT a.id, j.job_title, a.jobseeker_id, IFNULL(js.name, 'Unknown') AS applicant_name "
            "FROM applications a "
            "JOIN jobs j ON a.job_id = j.id "
            "LEFT JOIN jobseekers js ON a.jobseeker_id = js.user_id "
            "WHERE j.employer_id = %s AND a.status NOT IN ('Accepted', 'Rejected')"
        )
        cursor.execute(query, (self.current_employer_id,))
        apps = cursor.fetchall()
        print("Fetched applications:", apps)
        cursor.close()
        conn.close()
        
        if not apps:
            messagebox.showinfo("Info", "No pending applications found.")
            return
        
        self.app_records = {}  # reset application records
        
        for app in apps:
            app_card = ctk.CTkFrame(
                apps_scroll_frame,
                corner_radius=8,
                border_width=1,
                border_color="#D3D3D3"
            )
            app_card.pack(fill="x", padx=10, pady=5)
            
            details_text = f"{app['job_title']} | Applicant: {app['applicant_name']}"
            app_label = ctk.CTkLabel(
                app_card,
                text=details_text,
                font=("Helvetica", 14, "bold"),
                anchor="w"
            )
            app_label.pack(side=tk.LEFT, padx=15, pady=10)
            
            ctk.CTkButton(
                app_card,
                text="View",
                command=lambda app=app: self.process_application(app)
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
            self.app_records[app['id']] = app  # save record

    """===================================================================================================================================================================================="""

    def process_application(self, app):
        clear_frame(self.root)  # clear frame for processing application
        
        header_frame = ctk.CTkFrame(self.root, fg_color="transparent", height=80)
        header_frame.pack(fill="x", pady=(10, 20))
        
        header_label = ctk.CTkLabel(
            header_frame,
            text=f"Processing Application: {app['job_title']}",
            font=("Arial", 24, "bold"),
            text_color="white",
            fg_color="transparent"
        )
        header_label.pack(pady=20)
        
        content_frame = ctk.CTkFrame(self.root, fg_color="transparent", corner_radius=15)
        content_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        applicant_frame = ctk.CTkFrame(content_frame, fg_color="#004776", corner_radius=10, width=300)
        applicant_frame.pack(padx=20, pady=10)
        
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed")
            return
        cursor = conn.cursor(dictionary=True)
        query = "SELECT name, age, location, gender, contact FROM jobseekers WHERE user_id = %s"
        cursor.execute(query, (app['jobseeker_id'],))
        applicant_details = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if applicant_details:
            details = [
                ("Name:", applicant_details.get("name", "N/A")),
                ("Age:", applicant_details.get("age", "N/A")),
                ("Location:", applicant_details.get("location", "N/A")),
                ("Gender:", applicant_details.get("gender", "N/A")),
                ("Contact:", applicant_details.get("contact", "N/A"))
            ]
            for idx, (label_text, value) in enumerate(details):
                cat_label = ctk.CTkLabel(
                    applicant_frame,
                    text=label_text,
                    font=("Helvetica", 16, "bold"),
                    anchor="w",
                    fg_color="transparent"
                )
                cat_label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
                val_label = ctk.CTkLabel(
                    applicant_frame,
                    text=str(value),
                    font=("Helvetica", 16),
                    anchor="w",
                    fg_color="transparent"
                )
                val_label.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
        else:
            not_found_label = ctk.CTkLabel(
                applicant_frame,
                text="Applicant details not found.",
                font=("Helvetica", 16),
                fg_color="transparent"
            )
            not_found_label.pack(padx=10, pady=10)
        
        decision_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=10)
        decision_frame.pack(padx=20, pady=10, fill="x")

        decision_label = ctk.CTkLabel(
            decision_frame,
            text="Decision:",
            font=("Helvetica", 16),
            fg_color="transparent"
        )
        decision_label.pack(side=tk.TOP, anchor="w", padx=20, pady=(10, 0))

        decision_var = ctk.StringVar(value="Hire")
        decision_option = ctk.CTkOptionMenu(
            decision_frame,
            variable=decision_var,
            values=["Hire", "Reject"],
            height=50
        )
        decision_option.pack(fill="x", padx=10, pady=(0, 10))

        message_label = ctk.CTkLabel(
            decision_frame,
            text="Message to Applicant:",
            font=("Helvetica", 16),
            fg_color="transparent"
        )
        message_label.pack(side=tk.TOP, anchor="w", padx=20, pady=(10, 0))

        message_entry = ctk.CTkEntry(
            decision_frame,
            font=("Helvetica", 14),
            height=50
        )
        message_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=10)
        button_frame.pack(padx=20, pady=20)
        
        # update application status based on decision
        def submit_decision():
            decision = decision_var.get()
            msg = message_entry.get().strip()
            if not msg:
                messagebox.showerror("Validation Error", "Please enter a message.")
                return
            
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Connection failed")
                return
            cursor = conn.cursor()
            new_status = "Accepted" if decision == "Hire" else "Rejected"
            update_query = "UPDATE applications SET status = %s, message = %s WHERE id = %s"
            try:
                cursor.execute(update_query, (new_status, msg, app['id']))
                conn.commit()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                conn.close()
            messagebox.showinfo("Updated", f"Application marked as {new_status}")
            self.review_applications()  # back to review apps
        
        submit_button = ctk.CTkButton(
            button_frame,
            text="Submit Decision",
            command=submit_decision,
            fg_color="#27ae60",
            hover_color="#1e8449",
            font=("Helvetica", 16, "bold"),
            width=150,
            height=50
        )
        back_button = ctk.CTkButton(
            button_frame,
            text="Back to Applications",
            command=self.review_applications,
            fg_color="#c0392b",
            hover_color="#922b21",
            font=("Helvetica", 16, "bold"),
            width=150,
            height=50
        )
        
        submit_button.grid(row=0, column=0, padx=20, pady=10)
        back_button.grid(row=0, column=1, padx=20, pady=10)
