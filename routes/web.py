from masonite.routes import Route
from masonite.authentication import Auth

ROUTES = [
    Route.get("/", "WelcomeController@show"),
    Route.get('/dashboard', 'DashboardController@show'),
    Route.get('/auth/eve/callback', 'CallbackController@fetch').middleware('web'),
]

ROUTES += Auth.routes()
