''' A User Model Service Provider '''
from masonite.provider import ServiceProvider
import os
from config.dashboard import MODELS

package_directory = os.path.dirname(os.path.realpath(__file__))

class DashboardProvider(ServiceProvider):

    wsgi = False 

    def register(self):
        self.app.bind('DashboardModels', MODELS)

        self.app.make('Storage').STATICFILES.update({
            os.path.join(package_directory, 'static/'): '_dashboard/'
        })

        # Register Links:
        self.app.bind('DashboardNavLinks', {
            'Dashboard': '/dashboard',
            'Export': 'http://google.com'
        })

        Export.register(self.app)

    def boot(self, Storage, ViewClass):
        ViewClass.composer(['/dashboard*'], {'nav_links': self.app.collect('*NavLinks')})

class Export:

    def register(app):
        app.bind('AnotherProviderNavLinks', {
            'Export': 'http://google.com',
            'CSV': 'http://google.com'
        })