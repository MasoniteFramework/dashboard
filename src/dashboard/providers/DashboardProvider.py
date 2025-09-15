from masonite.providers import Provider



class DashboardProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.bind('dashboard.routes', {})
        self.application.make("view").share({
            "app": self.application
        })
        

    def boot(self):
        pass
        
