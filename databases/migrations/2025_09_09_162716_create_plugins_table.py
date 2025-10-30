"""CreatePluginsTable Migration."""

from masoniteorm.migrations import Migration


class CreatePluginsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("plugins") as table:
            table.increments("id")
            table.string("name").unique()
            table.string("slug").unique()
            table.string("repo").unique()
            table.string("description").nullable()
            table.decimal("price", 8, 2).default(0.00)
            table.decimal("rating", 2, 1).default(0.0)
            table.string("version").nullable()
            table.string("author").nullable()
            table.string("repository").nullable()

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("plugins")
