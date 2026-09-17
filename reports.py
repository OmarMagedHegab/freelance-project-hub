from datetime import datetime
from functools import reduce

class reports:
    def __init__(self,manager):
        self.manager = manager


    def earnings_report(self):
        paid_invoices = filter(lambda invoices : invoices.get_status().lower()=="paid",self.manager.get_invoices())
        total_earnings = reduce(lambda total,invoices : total + invoices.get_amount(), paid_invoices,0
                                )
        print()
        print(">>>>>>>>>>>>>Earnings Report<<<<<<<<<<<<<<<")
        print("Total Earnings: ",total_earnings)
        return total_earnings

    def late_projects_report(self):
        today = str(datetime.now().date())

        late_projects = list(filter(lambda projects : projects.get_deadline() < today and projects.get_status().lower() != "completed",self.manager.get_projects()))
        print()
        print(">>>>>>>>>>>>>Late Projects Report<<<<<<<<<<<<<<<")
        if len(late_projects) == 0:
            print("No Late Projects Available")

        else:
            for project in late_projects:
                print("Project: ",project.get_title())
                print("Deadline: ",project.get_deadline())
                print("Status: ",project.get_status())
        return late_projects

    def active_projects_report(self):
        today = datetime.now().date()
        active_projects = list(filter(lambda projects : projects.get_status().lower() in ["open","in progress"],self.manager.get_projects()))
        print()
        print(">>>>>>>>>Active Projects Report<<<<<<<<<<<<<")
        if len(active_projects) == 0:
            print("No Active Projects Available")
        else:
            for project in active_projects:
                print("Project: ",project.get_title())
                print("Deadline: ",project.get_deadline())

                freelancer = project.get_freelancer()
                client = project.get_client()
                if freelancer:
                    print("Freelancer: ", freelancer.get_name())
                else:
                    print("Freelancer: Not Assigned")

                if client:
                    print("Client: ", client.get_name())
                else:
                    print("Client: Not Assigned")

                print()
        return active_projects