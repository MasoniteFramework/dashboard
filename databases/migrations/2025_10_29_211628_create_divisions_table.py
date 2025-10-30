"""CreateDivisionsTable Migration."""

from masoniteorm.migrations import Migration


class CreateDivisionsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("divisions") as table:
            table.increments("id")
            table.integer("corporation_id").unsigned()
            table.string("name")
            table.integer("division_id")
            table.integer("amount").default(0)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("divisions")
