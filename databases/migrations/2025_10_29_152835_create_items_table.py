"""CreateItemsTable Migration."""

from masoniteorm.migrations import Migration


class CreateItemsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("items") as table:
            table.big_increments("id")
            table.big_integer("item_id").unique()
            table.string("name")
            table.text("description")
            table.decimal("volume", 18, 4)
            table.decimal("packaged_volume", 18, 4)
            table.integer("graphic_id")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("items")
