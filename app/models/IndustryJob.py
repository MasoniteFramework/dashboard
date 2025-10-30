"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masoniteorm.relationships import belongs_to, has_one


class IndustryJob(Model):
    """IndustryJob Model."""

    __fillable__ = [
        'character_id',
        'job_id',
        'status',
        'blueprint_id',
        'blueprint_type_id',
        'cost',
        'duration',
        'start_date',
        'licensed_runs',
        'runs',
        'activity_id',
        'end_date',
    ]

    @belongs_to("corporation_id", "id")
    def corporation(self):
        from .Corporation import Corporation
        return Corporation
    

    @belongs_to("blueprint_type_id", "item_id")
    def item(self):
        from .Item import Item
        return Item
