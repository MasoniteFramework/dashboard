from masoniteorm.models import Model

class Item(Model):
    """User Model."""

    __fillable__ = [
        "item_id",
        "name",
        "description",
        "volume",
        "packaged_volume",
        "graphic_id",
    ]