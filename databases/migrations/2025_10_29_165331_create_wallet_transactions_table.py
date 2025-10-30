"""CreateWalletTransactionsTable Migration."""

from masoniteorm.migrations import Migration


class CreateWalletTransactionsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("wallet_transactions") as table:
            table.increments("id")
            table.big_integer("journal_id").unique()
            table.string("transaction_type")
            table.unsigned_integer("character_id")
            table.decimal("amount", 18, 4)
            table.decimal("balance", 18, 4)
            table.text("reason").nullable()
            table.text("ref_type").nullable()
            table.integer("quantity").nullable()
            table.big_integer("transaction_id")
            table.string("transaction_date")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("wallet_transactions")
