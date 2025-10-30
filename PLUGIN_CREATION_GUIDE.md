# Plugin Creation Guide

## Overview
This guide explains how to create new plugins for the EVE Online dashboard, based on the patterns established in the `eve-home` and `eve-blueprints` plugins.

## Plugin Structure

Each plugin should follow this directory structure:

```
plugins/
└── your-plugin-name/
    ├── YourPluginProvider.py     # Plugin provider (required)
    ├── README.md                  # Plugin documentation
    └── src/
        ├── __init__.py
        ├── routes.py              # Routes configuration
        ├── controllers/
        │   ├── __init__.py
        │   └── YourController.py
        └── templates/
            └── your-plugin/
                └── views.html
```

## Step-by-Step Guide

### Step 1: Create Plugin Directory

```bash
mkdir -p plugins/your-plugin-name/src/controllers
mkdir -p plugins/your-plugin-name/src/templates/your-plugin
touch plugins/your-plugin-name/src/__init__.py
touch plugins/your-plugin-name/src/controllers/__init__.py
```

### Step 2: Create Controller

Create `src/controllers/YourController.py`:

```python
from masonite.controllers import Controller
from masonite.views import View

class YourController(Controller):
    def index(self, view: View):
        """Your main view method"""
        return view.render("your-plugin.index", {
            "data": "your data here"
        })
```

### Step 3: Create Routes

Create `src/routes.py`:

```python
from masonite.routes import Route
import importlib.util

# Import controller using importlib (handles hyphens in directory names)
spec = importlib.util.spec_from_file_location(
    "YourController",
    "plugins/your-plugin-name/src/controllers/YourController.py"
)
controller_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller_module)
YourController = controller_module.YourController

ROUTES = {
    "Your Plugin Name": [
        Route.get("/dashboard/your-plugin", YourController.index).name("your.plugin.index"),
    ]
}
```

**Note**: The dictionary key ("Your Plugin Name") will appear in the dashboard navigation menu.

### Step 4: Create Plugin Provider

Create `YourPluginProvider.py` in the plugin root:

```python
from masonite.providers import Provider
from masonite.routes import Route
import importlib.util
import sys


class YourPluginProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        """Register plugin routes and templates"""
        # Register plugin controller directory
        from masonite.routes import Route as RouteClass
        RouteClass.add_controller_locations("plugins/your-plugin-name/src/controllers")
        
        # Import routes from plugin using importlib
        spec = importlib.util.spec_from_file_location(
            "your_plugin_routes",
            "plugins/your-plugin-name/src/routes.py"
        )
        routes_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(routes_module)
        ROUTES = routes_module.ROUTES
        
        # Register routes with the router
        for group_name, routes in ROUTES.items():
            self.application.make("router").add(
                Route.group(routes, middleware=["web"])
            )
        
        # Add routes to dashboard navigation
        dashboard_routes = self.application.make('dashboard.routes')
        dashboard_routes.update(ROUTES)
        
        # Register plugin template directory
        view = self.application.make("view")
        view.add_location("plugins/your-plugin-name/src/templates")

    def boot(self):
        """Bootstrap any plugin services"""
        pass
```

### Step 5: Create Templates

Create `src/templates/your-plugin/index.html`:

```html
{% extends 'dashboard/base.html' %}

{% block title %}Your Plugin{% endblock %}

{% block page_title %}Your Plugin{% endblock %}

{% block breadcrumbs %}
<nav class="flex mb-6" aria-label="Breadcrumb">
    <ol class="inline-flex items-center space-x-1 md:space-x-3">
        <li class="inline-flex items-center">
            <a href="/dashboard" class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-light-blue-600">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
                </svg>
                Dashboard
            </a>
        </li>
        <li>
            <div class="flex items-center">
                <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                <span class="ml-1 text-sm font-medium text-gray-500 md:ml-2">Your Plugin</span>
            </div>
        </li>
    </ol>
</nav>
{% endblock %}

{% block content %}
<div class="bg-white rounded-lg shadow-md p-6">
    <h1 class="text-2xl font-bold text-gray-900 mb-4">Your Plugin Content</h1>
    <p class="text-gray-600">{{ data }}</p>
</div>
{% endblock %}
```

### Step 6: Register Plugin

Update `config/providers.py`:

```python
# Import using importlib (at the top of the file after other imports)
import importlib.util
import sys

# Load YourPluginProvider
spec = importlib.util.spec_from_file_location(
    "YourPluginProvider",
    "plugins/your-plugin-name/YourPluginProvider.py"
)
your_plugin_module = importlib.util.module_from_spec(spec)
sys.modules["YourPluginProvider"] = your_plugin_module
spec.loader.exec_module(your_plugin_module)
YourPluginProvider = your_plugin_module.YourPluginProvider

# Add to PROVIDERS list
PROVIDERS = [
    # ... existing providers
    YourPluginProvider,  # Add your plugin here
]
```

### Step 7: Test Your Plugin

1. Start the development server:
   ```bash
   python craft serve
   ```

2. Navigate to your plugin:
   ```
   http://localhost:8000/dashboard/your-plugin
   ```

3. Check the dashboard navigation menu for your plugin section

## Important Notes

### Why ImportLib?
Python doesn't allow hyphens in module names. Since our plugin directories use hyphens (e.g., `eve-home`), we must use `importlib` to dynamically load modules.

### Route Naming
- Use descriptive route names with dots: `"your.plugin.index"`
- This makes it easy to generate URLs: `{{ route('your.plugin.index') }}`

### Dashboard Navigation
The dictionary key in your ROUTES configuration determines the menu section name:
```python
ROUTES = {
    "Your Menu Section": [  # This appears in the sidebar
        Route.get(...).name("link.name"),
    ]
}
```

### Template Inheritance
Always extend `dashboard/base.html` to maintain consistent styling and navigation.

### Middleware
Routes are automatically registered with the `web` middleware group, which includes:
- Session handling
- CSRF protection
- User authentication loading

## Example Plugins

### Simple Plugin (eve-home)
- Single route
- One controller method
- Character information display
- ESI API integration

### Complex Plugin (eve-blueprints)
- Multiple routes (index + detail)
- Helper methods
- Data organization and statistics
- Search and filter UI
- Category grouping

## Best Practices

1. **Keep controllers focused**: One controller per major feature
2. **Use helper methods**: Extract complex logic into private methods
3. **Mock data first**: Use mock data during development, integrate APIs later
4. **Responsive design**: Always use TailwindCSS responsive classes
5. **Error handling**: Wrap API calls in try-except blocks
6. **Documentation**: Include a README.md with each plugin

## Troubleshooting

### Controller Not Found Warnings
You may see warnings like "Controller not found" during startup. These are non-critical - the controllers load correctly via importlib.

### Template Not Found
Ensure you've registered the template directory in your provider's `register()` method:
```python
view.add_location("plugins/your-plugin-name/src/templates")
```

### Routes Not Appearing
Check that:
1. Routes are registered with the router
2. Routes are added to `dashboard.routes`
3. The ROUTES dictionary key is descriptive (appears in menu)

## Additional Resources

- **Masonite Documentation**: https://docs.masoniteproject.com/
- **TailwindCSS**: https://tailwindcss.com/docs
- **EVE ESI Documentation**: https://esi.evetech.net/ui/

## Plugin Ideas

Here are some ideas for additional plugins:
- Industry Jobs Tracker
- Market Browser
- Asset Library
- Planetary Interaction Manager
- Contract Manager
- Wallet Journal
- Skill Queue Planner
- Fleet Composition Tool
- Corporation Management
- Alliance Dashboard

