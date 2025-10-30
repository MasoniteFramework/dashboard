"""CreateIndustryJobsTable Migration."""

from masoniteorm.migrations import Migration


class CreateIndustryJobsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("industry_jobs") as table:
            table.increments("id")
            table.integer("character_id").unsigned()
            table.integer("activity_id")
            table.big_integer("job_id").unique()
            table.string("status")
            table.big_integer("blueprint_id")
            table.integer("blueprint_type_id")
            table.integer("licensed_runs").nullable()
            table.integer("runs").nullable()
            table.decimal("cost", 18, 4)
            table.integer("duration")
            table.string("start_date")
            table.string("end_date")
            table.timestamps()


            table.foreign("character_id").references("id").on("characters")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("industry_jobs")
