import json
from project import Project
from invoice import*
from client import Client
from freelancer import Freelancer
import re

regex_email = re.compile(r'[\w]+@[\w]+\.[\w]+$')
regex_phone = re.compile(r'^[0]+[1]+[\d]+$')
regex_role = re.compile(r'^[CcFf]+[\w]+$')
regex_password = re.compile(r'[\w]+$')

class FreelanceManager:
    def __init__(self):
        try:
            with open('users.json', 'r') as f:
                raw_users= json.load(f) # data will be as text not objects of user
                self.__users = {}
                for user_id,user_data in raw_users.items():
                    if user_data['role'].lower() == 'client':
                        current_client = Client(user_data['id'], user_data['name'], user_data['phone'], user_data['email'], user_data['password'], user_data['role'],user_data.get('orders',[]))
                        self.__users[user_id] = current_client
                    else:
                        current_freelancer=Freelancer(user_data['id'], user_data['name'],user_data['phone'],user_data['email'], user_data['password'],user_data['role'],user_data.get('skills', []),user_data.get('hourly_rate', 0),user_data.get('projects', []))
                        self.__users[user_id] = current_freelancer
        except (FileNotFoundError,json.JSONDecodeError):
            self.__users = {}
        try:
            with open('projects.json', 'r') as f:
                raw_projects= json.load(f)
                self.__projects = []
                for project in raw_projects:
                    client_id=project['client_id']
                    freelancer_id=project.get('freelancer_id') # to not crash if project not assigned to freelancer
                    project_client=self.__users[client_id]
                    project_freelancer = self.__users.get(freelancer_id) if freelancer_id else None # if project not assigned to a freelancer yet
                    current_project=Project(project['id'],project['title'],project['deadline'],project_client,project_freelancer,project['status'],project['milestone'])
                    self.__projects.append(current_project)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__projects = []
        try:
            with open('invoices.json', 'r') as f:
                raw_invoices = json.load(f)
                self.__invoices = []
                for invoice in raw_invoices:
                    current_invoice=Invoice(invoice['code'],invoice['amount'],invoice['commission'],invoice['status'])
                    self.__invoices.append(current_invoice)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__invoices = []

    def save_data(self):
        users_dict={}
        for user_id,user in self.__users.items():
            current_user={
                'id':user.get_id(),
                'name':user.get_name(),
                'phone': user.get_phone(),
                'password':user.get_password(),
                'email':user.get_email(),
                'role':user.get_role()
            }  # making the dictionary keys manully to not look like _Client__id if i used __dict__
            if user.get_role().lower()=='client':
                current_user['orders']=user.get_orders()
            else:
                current_user['skills']=user.get_skills()
                current_user['hourly_rate'] = user.get_hourly_rate()
                current_user['projects'] = user.get_projects()
            users_dict[user_id]=current_user
        with open('users.json', 'w') as f:
            json.dump(users_dict,f,indent=4)
        projects_list=[]
        for project in self.__projects:
            client=project.get_client()
            freelancer=project.get_freelancer() # we get them first to exract the id to be saved in the file
            current_project={
                'id':project.get_id(),
                'title':project.get_title(),
                'deadline':project.get_deadline(),
                'client_id':client.get_id(),
                'freelancer_id':freelancer.get_id() if freelancer else None,
                'status': project.get_status(),
                'milestone': project.get_milestone()
            }
            projects_list.append(current_project)
        with open('projects.json', 'w') as f:
            json.dump(projects_list,f,indent=4)
        invoices_list=[]
        for invoice in self.__invoices:
            current_invoice={
                'code':invoice.get_code(),
                'amount':invoice.get_amount(),
                'commission':invoice.get_commission(),
                'status':invoice.get_status()
            }
            invoices_list.append(current_invoice)
        with open('invoices.json', 'w') as f:
            json.dump(invoices_list,f,indent=4)

    def generate_project_id(self):
        existing_ids=list(map(lambda p: int(p.get_id().split("-")[1]),self.__projects))
        next_id=max(existing_ids)+1 if existing_ids else 1 # make start= 1 if list is empty
        return f"P-{next_id:03d}"

    def create_project(self,project_title,project_deadline,client):
        new_id=self.generate_project_id()
        new_project=Project(new_id,project_title,project_deadline,client,None)
        self.__projects.append(new_project)
        print(f"Project '{project_title}' created successfully with ID '{new_id}'!")

    def assign_project(self,project_id,freelancer_id):
        freelancer=self.__users.get(freelancer_id)
        if not freelancer or freelancer.get_role().lower() !='freelancer': # check
            print("Invalid freelancer ID!")
            return
        temp_list=list(filter(lambda p:p.get_id()==project_id,self.__projects))
        target_project=temp_list[0] if temp_list else None
        if not target_project:
            print("Project not found!")
            return
        if target_project.get_status().lower() !='open':
            print(f"Cannot assign. Project is '{target_project.get_status()}'!")
            return
        target_project.set_status('In Progress')
        target_project.set_freelancer(freelancer)
        print("Project assigned successfully!")

    def update_milestone(self,project_id,new_milestone):
        temp_list = list(filter(lambda p: p.get_id() == project_id, self.__projects))
        target_project = temp_list[0] if temp_list else None
        if not target_project:
            print("Project not found!")
            return
        target_project.set_milestone(new_milestone)
        print(f"Milestone for '{target_project.get_title()}' updated to: {new_milestone} successfully!")

    def create_invoice(self,code,amount):
        temp_list=list(filter(lambda i: i.get_code() == code,self.__invoices))
        existing_invoice=temp_list[0] if temp_list else None
        if existing_invoice:
            raise DuplicateInvoiceError("ERROR: Invoice already exists.")
        if amount<=0:
            raise InvalidInvoiceAmountError("ERROR: Invoice amount must be greater than 0.")
        new_invoice=Invoice(code,amount)
        self.__invoices.append(new_invoice)
        print(f"Invoice for '{code}' created successfully!")

    def process_invoice_payment(self,code):
        temp_list = list(filter(lambda i: i.get_code() == code,self.__invoices))
        target_invoice = temp_list[0] if temp_list else None
        if not target_invoice:
            print("Invoice not found!")
            return
        if target_invoice.get_status().lower() in ['paid','cancelled']:
            raise InvalidPaymentStateError("ERROR: Invoice is already paid/has been cancelled.")
        commission=commission_calculator(target_invoice.get_amount())
        target_invoice.set_commission(commission)
        target_invoice.set_status("paid")
        print(f"Payment processed for {code}. Commission recorded: ${commission}")

    def generate_user_id(self,role):
        prefix = 'C' if role.lower().startswith('client') else 'F'
        existing_ids=[]
        for user_id in self.__users.keys():
            if user_id.startswith(prefix):
                existing_ids.append(int(user_id.split("-")[1]))
        next_id = max(existing_ids) + 1 if existing_ids else 1
        return f"{prefix}-{next_id:03d}"

    def login(self):
        print("Logging in...")
        while True:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            for user in self.__users.values():
                if user.get_email() == email and user.get_password() == password:
                    print("Login successful")
                    return user

            print("Invalid email or password")

    def add_client_freelancer(self):
        name = input("Enter your name: ")
        while len(name) < 3:
            print("Invalid name")
            name = input("Enter your name: ")

        email = input("Enter your email: ")
        email_check = re.search(regex_email, email)
        while email_check is None:
            print("Invalid email")
            email = input("Enter your email: ")
            email_check = re.search(regex_email, email)

        phone = input("Enter your phone number: ")
        phone_check = re.search(regex_phone, phone)
        while phone_check is None or len(phone) != 11:
            print("Invalid phone number")
            phone = input("Enter your phone number: ")
            phone_check = re.search(regex_phone, phone)

        role = input("Enter your role: ")
        role_check = re.search(regex_role, role)
        while role_check is None:
            print("Invalid role")
            role = input("Enter your role: ")
            role_check = re.search(regex_role, role)

        password = input("Enter your password: ")
        password_check = re.search(regex_password, password)
        while password_check is None or len(password) < 8:
            print("Invalid password")
            password = input("Enter your password: ")
            password_check = re.search(regex_password, password)
        new_id=self.generate_user_id(role)
        if role.lower().startswith("client"):
            new_user = Client(new_id,name, phone, email, password, role)
        elif role.lower().startswith("freelancer"):
            skills = input("Enter your skills (separated by space): ").split(" ")
            while True:
                try:
                    hourly_rate = float(input("Enter your hourly rate ($): "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
            new_user = Freelancer(new_id, name, phone, email, password, role.capitalize(), skills, hourly_rate)
        else:
            print("Invalid role")
            return
        self.__users[new_id] = new_user
        print(f"User '{name}' added successfully with ID: {new_id}")

    def get_users(self):
        return self.__users
    def get_projects(self):
        return self.__projects
    def get_invoices(self):
        return self.__invoices

