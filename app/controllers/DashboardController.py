"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller


class DashboardController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        return view.render("dashboard.home")
