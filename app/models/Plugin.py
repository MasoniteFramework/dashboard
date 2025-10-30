"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masonite.authentication import Authenticates


class Plugin(Model):
    """User Model."""

    __fillable__ = ["name", "slug", "description", "repo", "price", "rating" "version", "author", "repository"]
