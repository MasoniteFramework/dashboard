from masonite.providers import Provider
from masonite.routes import Route
import importlib.util
import sys


class EveHomePluginProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        """Register plugin routes and templates"""
        # Register plugin controller directory
        from masonite.routes import Route as RouteClass
        RouteClass.add_controller_locations("plugins/eve-home/src/controllers")
        
        # Import routes from plugin using importlib
        spec = importlib.util.spec_from_file_location(
            "eve_home_routes",
            "plugins/eve-home/src/routes.py"
        )
        routes_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(routes_module)
        ROUTES = routes_module.ROUTES
        
        # Register routes with the router
        for group_name, routes in ROUTES.items():
            self.application.make("router").add(
                Route.group(routes, middleware=["web"])
            )
        
        # Add routes to dashboard navigation
        dashboard_routes = self.application.make('dashboard.routes')
        dashboard_routes.update(ROUTES)
        
        # Register plugin template directory
        view = self.application.make("view")
        view.add_location("plugins/eve-home/src/templates")

    def boot(self):
        """Bootstrap any plugin services"""
        pass

