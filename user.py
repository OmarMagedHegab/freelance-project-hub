class User:
    def __init__(self,id,name,phone,email,password,role):
        self.__id = id
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__password = password
        self.__role = role

    # Getters
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_phone(self):
        return self.__phone
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_role(self):
        return self.__role

    def display_profile(self):
        print("User Profile")
        print("Name: ",self.__name)
        print("ID: ", self.__id)
        print("Phone: ",self.__phone)
        print("Email: ",self.__email)
        print("Role: ",self.__role)
        print()



