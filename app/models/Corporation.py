"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masonite.authentication import Authenticates


class Corporation(Model):
    """User Model."""

    __primary_key__ = "id"

    __fillable__ = [
        'name',
        'corporation_id',
        'ticker',
        'description',
        'alliance_id',
        'date_founded',
        'member_count',
        'ceo_id'
    ]
