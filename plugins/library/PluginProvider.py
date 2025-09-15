from masonite.providers import Provider
from masonite.routes import Route
from .src.controllers.PluginController import PluginController


class PluginProvider(Provider):
    
    prefix = "Users"
    templates = "plugins/library/templates"
    
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make('dashboard.routes').update({
            "Plugins": Route.group("Plugins", self.routes())
        })

        self.application.make('view').add_location(self.templates)
        self.application.make("router").add(
            [Route.group(self.routes())]
        )

    def boot(self):
        pass
    
    def routes(self):
        return [
            Route.get("/plugins/search", PluginController.index).name("Search Plugins"),
            Route.get("/plugins/@name", PluginController.show)
        ]