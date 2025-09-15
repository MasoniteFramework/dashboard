"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
from app.models.Plugin import Plugin
from masonite.request import Request


class PluginController(Controller):
    """WelcomeController Controller Class."""

    def index(self, view: View):
        return view.render("plugins.search")
    
    def show(self, view: View, request: Request):
        name = request.param("name")
        plugin = Plugin.where("slug", name).first()
        return view.render("plugins.detail", {"plugin": plugin})
