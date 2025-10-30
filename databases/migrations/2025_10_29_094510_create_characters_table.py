"""CreateCharactersTable Migration."""

from masoniteorm.migrations import Migration


class CreateCharactersTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("characters") as table:
            table.increments("id")
            table.big_integer("character_id").unique()
            table.string("name")
            table.big_integer("user_id").unsigned().nullable()
            table.big_integer("corporation_id")
            table.integer("bloodline_id").nullable()
            table.text("description").nullable()
            table.datetime("birthday").nullable()
            table.integer("race_id").nullable()
            table.integer("ancestry_id").nullable()
            table.string("access_token").nullable()
            table.string("refresh_token").nullable()
            table.timestamps()
            table.soft_deletes()

            table.foreign("user_id").references("id").on("users")


    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("characters")
