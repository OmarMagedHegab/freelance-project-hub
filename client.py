from user import User
class Client(User):
    def __init__(self,id,name,phone,email,password,role,orders=None):
        super().__init__(id,name,phone,email,password,role)
        self.__orders = orders if orders is not None else []

    def get_orders(self):
        return self.__orders
    def set_orders(self, orders):
        self.__orders = orders

    def display_profile(self):
        print("Client Profile")
        super().display_profile()
        print("Orders: ", self.__orders)
        print()

