"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masoniteorm.relationships import belongs_to


class Character(Model, SoftDeletesMixin):
    """User Model."""

    __fillable__ = [
        'character_id',
        'user_id',
        'name',
        'corporation_id',
        'bloodline_id',
        'race_id',
        'ancestry_id',	
        'birthday',
        'description',
        'access_token',
        'refresh_token',
        'member_count'
    ]

    @belongs_to("corporation_id", "id")
    def corporation(self):
        from .Corporation import Corporation
        return Corporation
