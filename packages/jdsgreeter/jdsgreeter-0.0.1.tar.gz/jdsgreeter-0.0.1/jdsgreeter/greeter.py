import datetime


class Greeter:
    def __init__(self, standard='hello', include_time=False):
        self.greeting = standard
        self.include_time = include_time
    

    def greet(self, name):
        rsp = ''
        if self.include_time:
            rsp += '{:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now())
        
        rsp += self.greeting + ' ' + name
        return rsp