from masonite.routes import Route
from .controllers.HomeController import HomeController

ROUTES = {
    "Eve Home": [
        Route.get("/dashboard/eve-home", HomeController.index).name("Eve Home").middleware("web"),
    ],
    "Industry": [
        # Add routes related to Industry Jobs here
        Route.get("/dashboard/eve-home/industry-jobs", HomeController.industry_jobs).name("Industry Jobs").middleware("web"),
    ],
    "Finance": [
        # Add routes related to Wallet here
        Route.get("/dashboard/eve-home/wallet", HomeController.wallet).name("Wallet").middleware("web"),
    ],
}