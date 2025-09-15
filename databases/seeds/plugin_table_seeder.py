"""PluginTableSeeder Seeder."""

from masoniteorm.seeds import Seeder
from app.models.Plugin import Plugin


class PluginTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        Plugin.truncate()
        Plugin.create(
            {
                "name": "User Management",
                "slug": "user-management",
                "description": "Manage users accounts",
                "rating": 4.5,
                "price": 0.00,
                "version": "1.0.0",
                "author": "Joseph Mancuso",
                "repository": "https://github.com/your-repo/user-management",
            }
        )
