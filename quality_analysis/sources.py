class Sources:
    def __init__(self,web,name,email):
        self.web = web
        self.name = name
        self.email = email
    
    def sourcesKG(self):  #to print information about sources
        return f" Sources: web:{self.web}, name:{self.name}, email:{self.email}"