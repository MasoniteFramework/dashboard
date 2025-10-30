"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masoniteorm.relationships import belongs_to


class Division(Model):
    """User Model."""

    __fillable__ = [
        'corporation_id',
        'name',
        'division_id',
        'amount'
    ]

    @belongs_to("corporation_id", "id")
    def corporation(self):
        from .Corporation import Corporation
        return Corporation
