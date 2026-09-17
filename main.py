from freelanceManager import FreelanceManager
from reports import reports
import re
date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
client_regex = re.compile(r'^C-\d{3}$')
freelancer_regex = re.compile(r'^F-\d{3}$')
project_regex = re.compile(r'^P-\d{3}$')
invoice_regex = re.compile(r"^INV-\d{4}-\d{4}$")

def client_menu(manager,user,report):
    while True:
        print(f"\n=== Client Menu: Welcome {user.get_name()} ===")
        print("1. View My Profile")
        print("2. Create a New Project")
        print("3. Assign a Project to a Freelancer")
        print("4. Pay an Invoice")
        print("5. View System Reports")
        print("6. Logout")
        try:
            choice = int(input("Enter your choice from 1 to 6: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if choice == 1:
            user.display_profile()
        elif choice == 2:
            print("\n--- Create a New Project ---")
            title = input("Enter Project Title: ")
            while True:
                deadline = input("Enter Deadline (YYYY-MM-DD): ")
                if not date_regex.search(deadline):
                    print("Please enter a valid date in YYYY-MM-DD format.")
                    continue
                break
            while True:
                client_id = input("Enter Client ID (e.g. C-001): ")
                if not client_regex.search(client_id):
                    print("Please enter a valid client ID in the form C- followed by 3 numbers!")
                    continue
                break
            users = manager.get_users()
            client = users.get(client_id)
            if client and client.get_role().lower() == 'client':
                manager.create_project(title, deadline, client)
            else:
                print("Client not found or invalid ID!")
        elif choice == 3:
            print("\n--- Assign Project to Freelancer ---")
            while True:
                p_id = input("Enter Project ID: ")
                if not project_regex.search(p_id):
                    print("Please enter a valid project ID in the form P- followed by 3 numbers!")
                    continue
                break
            while True:
                f_id = input("Enter Freelancer ID: ")
                if not freelancer_regex.search(f_id):
                    print("Please enter a valid Freelancer ID in the form F-followed by 3 numbers!")
                    continue
                break
            manager.assign_project(p_id, f_id)
        elif choice == 4:
            print("\n--- Pay an Invoice ---")
            while True:
                code = input("Enter Invoice Code (e.g., INV-2026-0001): ")
                if not invoice_regex.search(code):
                    print("Invalid format! Must be INV-YYYY-NNNN")
                    continue
                break
            try:
                manager.process_invoice_payment(code)
            except Exception as e:
                print(e)
        elif choice == 5:
            print("\n--- View System Reports ---")
            report.earnings_report()
            report.late_projects_report()
            report.active_projects_report()
        elif choice == 6:
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def freelancer_menu(manager,user,report):
    while True:
        print(f"\n=== Freelancer Menu: Welcome {user.get_name()} ===")
        print("1. View My Profile")
        print("2. Update Project Milestone")
        print("3. Create an Invoice")
        print("4. View System Reports")
        print("5. Logout")
        try:
            choice = int(input("Enter your choice from 1 to 5: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if choice == 1:
            user.display_profile()
        elif choice == 2:
            print("\n--- Update Project Milestone ---")
            while True:
                p_id = input("Enter Project ID: ")
                if not project_regex.search(p_id):
                    print("Please enter a valid project ID in the form P- followed by 3 numbers!")
                    continue
                break
            while True:
                new_milestone = input("Enter new Milestone: ")
                if not new_milestone.strip():
                    print("Milestone cannot be empty!")
                    continue
                break
            manager.update_milestone(p_id, new_milestone)
        elif choice == 3:
            print("\n--- Create an Invoice ---")
            while True:
                code = input("Enter Invoice Code (e.g., INV-2026-0001): ")
                if not invoice_regex.search(code):
                    print("Invalid format! Must be INV-YYYY-NNNN")
                    continue
                break
            while True:
                try:
                    amount = float(input("Enter Invoice Amount ($): "))
                    break
                except ValueError:
                    print("Please enter a valid amount.")
            try:
                manager.create_invoice(code, amount)
            except Exception as e:
                print(e)
        elif choice == 4:
            print("\n--- View System Reports ---")
            report.active_projects_report()
        elif choice == 5:
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    manager = FreelanceManager()
    report=reports(manager)
    while True:
        print("\n==== SIC Freelance Project Hub ====")
        print("1. Login")
        print("2. Register (New User)")
        print("3. Exit System")
        try:
            choice = int(input("Enter your choice from 1 to 3: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if choice == 1:
            user=manager.login()
            if user:
                if user.get_role().lower() == "client":
                    client_menu(manager,user,report)
                elif user.get_role().lower() == "freelancer":
                    freelancer_menu(manager,user,report)
        elif choice == 2:
            manager.add_client_freelancer()
        elif choice == 3:
            manager.save_data()
            print("Exiting System, Bye!")
            break
        else:
            print("Please enter a valid choice from 1 to 3.")
            continue
if __name__ == "__main__":
    main()

