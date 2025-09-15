"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
from app.models.User import User
from masonite.request import Request
from masonite.response import Response
from masonite.facades import Hash


class UsersController(Controller):
    """WelcomeController Controller Class."""

    def index(self, view: View):
        total = User.count()
        users = User.all()
        return view.render("users.all", {"total": total, "users": users})

    def edit(self, view: View, request: Request):
        user = User.find(request.param("id"))
        editable_columns = User.get_columns()
        hidden_fields = User.__hidden__
        return view.render("users.edit", {"user": user, "editable_fields": editable_columns, "hidden_fields": hidden_fields})

    def update(self, request: Request, response: Response):
        user = User.find(request.param("id"))
        fields = request.all()
        for field in fields:
            if field == "password":
                fields[field] = Hash.make(fields[field])
                
            
        
        user.update(fields)
        return response.redirect("/dashboard/users/all")