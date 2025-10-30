"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
from masonite.request import Request


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View, request: Request):
        print('cookiey', request.cookie('SESSID'))
        return view.render("welcome")
