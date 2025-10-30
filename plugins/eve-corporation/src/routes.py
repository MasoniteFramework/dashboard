from masonite.routes import Route
from .controllers.CorporationController import CorporationController


ROUTES = {
    "Corporation": [
        # Add routes related to Corporation here
        Route.get("/dashboard/corporation-home", CorporationController.index).name("Corporation Home").middleware("web"),
    ],
}