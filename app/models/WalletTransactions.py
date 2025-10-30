"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masoniteorm.relationships import belongs_to


class WalletTransaction(Model):
    """User Model."""

    __fillable__ = [
        "journal_id",
        "amount", 
        "balance",
        "reason",
        "ref_type",
        "character_id",
        "quantity",
        "location_id",
        "transaction_id",
        "transaction_date",
        "character_id",
        "transaction_type",
    ]

    __casts__ = {
        "amount": "float",
        "balance": "float",
    }

    @belongs_to("corporation_id", "id")
    def corporation(self):
        from .Corporation import Corporation
        return Corporation
