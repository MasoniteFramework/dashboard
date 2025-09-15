from masonite.providers import Provider
from masonite.routes import Route
from .src.controllers.UsersController import UsersController


class UsersPluginProvider(Provider):
    
    prefix = "Users"
    templates = [
        "plugins/users/templates",
    ]
    
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make('dashboard.routes').update({
            self.prefix: Route.group("Users", self.routes())
        })
        for template in self.templates:
            self.application.make('view').add_location(template)
        self.application.make("router").add(
            [Route.group(self.routes())]
        )

    def boot(self):
        pass
    
    def routes(self):
        return [
            Route.get("/dashboard/users/all", UsersController.index).name("Manage Users"),
            Route.get("/dashboard/users/@id/edit", UsersController.edit),
            Route.post("/dashboard/users/@id/update", UsersController.update)
        ]
