class Project:
    def __init__(self,id,title,deadline,client,freelancer=None,status="Open",milestone="Not Started"):
        self.__id=id
        self.__title=title
        self.__deadline=deadline
        self.__client=client
        self.__freelancer=freelancer
        self.__status=status
        self.__milestone=milestone

    def get_id(self):
        return self.__id
    def get_title(self):
        return self.__title
    def get_deadline(self):
        return self.__deadline
    def get_client(self):
        return self.__client
    def get_freelancer(self):
        return self.__freelancer
    def get_status(self):
        return self.__status
    def get_milestone(self):
        return self.__milestone
    def set_freelancer(self,freelancer):
        self.__freelancer = freelancer
    def set_status(self, status):
        self.__status = status
    def set_milestone(self, milestone):
        self.__milestone = milestone
