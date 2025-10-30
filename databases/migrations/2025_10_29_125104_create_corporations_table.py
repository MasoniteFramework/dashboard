"""CreateCorporationsTable Migration."""

from masoniteorm.migrations import Migration


class CreateCorporationsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("corporations") as table:
            table.increments("id")
            table.string("name")
            table.integer("member_count").default(0)
            table.integer("corporation_id").unique()
            table.string("ticker")
            table.text("description").nullable()
            table.integer("alliance_id").nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("corporations")
