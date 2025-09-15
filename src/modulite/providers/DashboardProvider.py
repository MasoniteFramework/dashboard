from masonite.providers import Provider
from masonite.routes import Route
from modulite.controllers.PluginController import PluginController
from masonite.utils.structures import load


class DashboardProvider(Provider):
    
    templates = "modulite/plugins/library/templates"
    
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.bind('dashboard.routes', {})
        self.application.make("view").share({
            "app": self.application
        })
        
        self.application.make('view').add_location(self.templates)
        self.application.make("router").add(
            [Route.group(self.routes())]
        )
        
        self.application.make('dashboard.routes').update({
            "Plugins": Route.group("Plugins", self.routes())
        })
        self.application.make('dashboard.routes').update({
            "User Management": Route.group("Plugins", load("plugins/users/routes", "ROUTES"))
        })
        
        self.application.make("router").add(load("plugins/users/routes", "ROUTES"))
        self.application.make('view').add_location("plugins/users/templates")
        
        
        
        
        

    def boot(self):
        pass
    
    
    def routes(self):
        return [
        Route.get("/plugins/search", PluginController.index).name("Search Plugins"),
            Route.get("/plugins/@name", PluginController.show)
        ]
        
