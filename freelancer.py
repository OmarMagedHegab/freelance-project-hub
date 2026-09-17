from user import User
class Freelancer(User):
    def __init__(self,id,name,phone,email,password,role,skills=None,hourly_rate=0.0,projects=None):
        super().__init__(id,name,phone,email,password,role)
        self.__skills = skills if skills is not None else []
        self.__hourly_rate = hourly_rate
        self.__projects = projects if projects is not None else []

    def set_projects(self,projects):
        self.__projects = projects
    def set_hourly_rate(self,hourly_rate):
        self.__hourly_rate = hourly_rate
    def get_projects(self):
        return self.__projects
    def get_hourly_rate(self):
        return self.__hourly_rate
    def get_skills(self):
        return self.__skills


    def display_profile(self):
        print("Freelancer Profile")
        super().display_profile()
        print("Skills: ",self.__skills)
        print("Hourly Rate: ",self.__hourly_rate)
        print("Projects: ",self.__projects)
        print()
