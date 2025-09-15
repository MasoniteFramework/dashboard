# Modular Dashboard Template Guide

This guide explains how to use the modular TailwindCSS dashboard template system for extending your dashboard with plugins and custom menu items.

## Template Structure

### Base Template: `templates/dashboard/base.html`

The base template provides:
- **Left Sidebar Navigation**: Fixed sidebar with accordion-style menu items
- **Responsive Design**: Mobile-friendly with collapsible sidebar
- **White & Light Blue Theme**: Clean, professional color scheme
- **Modular Menu System**: Easy to extend with new menu categories
- **Alpine.js Integration**: Interactive components with minimal JavaScript

### Sample Page: `templates/dashboard/home.html`

A complete example showing how to extend the base template with:
- Breadcrumb navigation
- Statistics cards
- Activity timeline
- Quick action buttons

## Key Features

### 1. Accordion Menu System

Each menu category uses Alpine.js for accordion functionality:

```html
<div x-data="{ open: false }" class="space-y-1">
    <button @click="open = !open" class="group w-full flex items-center justify-between px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-light-blue-50 hover:text-light-blue-700">
        <div class="flex items-center">
            <svg class="mr-3 h-5 w-5 text-gray-400 group-hover:text-light-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <!-- Icon SVG -->
            </svg>
            Category Name
        </div>
        <svg class="h-4 w-4 transition-transform duration-200" :class="{ 'rotate-180': open }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
    </button>
    <div x-show="open" x-transition class="ml-6 space-y-1">
        <a href="/dashboard/category/item1" class="block px-3 py-2 text-sm text-gray-600 rounded-md hover:bg-light-blue-50 hover:text-light-blue-700">Item 1</a>
        <a href="/dashboard/category/item2" class="block px-3 py-2 text-sm text-gray-600 rounded-md hover:bg-light-blue-50 hover:text-light-blue-700">Item 2</a>
    </div>
</div>
```

### 2. Plugin Integration Hook

The template includes a special block for plugin menu items:

```html
<!-- Plugin Hook for Additional Menu Items -->
{% block sidebar_menu_items %}{% endblock %}
```

### 3. Color Theme

The template uses a custom light blue color palette:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'light-blue': {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: '#7dd3fc',
                    400: '#38bdf8',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                }
            }
        }
    }
}
```

## How to Extend the Dashboard

### 1. Adding New Menu Categories

To add a new menu category, extend the base template and override the `sidebar_menu_items` block:

```html
{% extends 'dashboard/base.html' %}

{% block sidebar_menu_items %}
<!-- Your Plugin Menu Section -->
<div x-data="{ open: false }" class="space-y-1">
    <button @click="open = !open" class="group w-full flex items-center justify-between px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-light-blue-50 hover:text-light-blue-700">
        <div class="flex items-center">
            <svg class="mr-3 h-5 w-5 text-gray-400 group-hover:text-light-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <!-- Your icon SVG -->
            </svg>
            Your Plugin
        </div>
        <svg class="h-4 w-4 transition-transform duration-200" :class="{ 'rotate-180': open }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
    </button>
    <div x-show="open" x-transition class="ml-6 space-y-1">
        <a href="/dashboard/your-plugin/page1" class="block px-3 py-2 text-sm text-gray-600 rounded-md hover:bg-light-blue-50 hover:text-light-blue-700">Page 1</a>
        <a href="/dashboard/your-plugin/page2" class="block px-3 py-2 text-sm text-gray-600 rounded-md hover:bg-light-blue-50 hover:text-light-blue-700">Page 2</a>
    </div>
</div>
{% endblock %}
```

### 2. Creating New Pages

Create new pages by extending the base template:

```html
{% extends 'dashboard/base.html' %}

{% block title %}Your Page Title{% endblock %}

{% block page_title %}Your Page Title{% endblock %}

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
                <span class="ml-1 text-sm font-medium text-gray-500 md:ml-2">Your Page</span>
            </div>
        </li>
    </ol>
</nav>
{% endblock %}

{% block content %}
<!-- Your page content here -->
<div class="bg-white shadow rounded-lg p-6">
    <h1 class="text-2xl font-bold text-gray-900 mb-4">Your Content</h1>
    <p class="text-gray-600">Your page content goes here.</p>
</div>
{% endblock %}
```

### 3. Available Template Blocks

The base template provides these blocks for customization:

- `title`: Page title (appears in browser tab)
- `page_title`: Main page heading in the header
- `breadcrumbs`: Breadcrumb navigation
- `content`: Main page content
- `sidebar_menu_items`: Additional menu items for plugins
- `head`: Additional CSS or meta tags
- `js`: Additional JavaScript

### 4. Responsive Features

- **Mobile Sidebar**: Automatically collapses on mobile devices
- **Hamburger Menu**: Toggle button for mobile navigation
- **Overlay**: Dark overlay when mobile sidebar is open
- **Responsive Grid**: Content adapts to different screen sizes

### 5. Interactive Elements

- **Dark Mode Toggle**: Built-in dark mode support (toggle in header)
- **Search Bar**: Functional search input in header
- **Notifications**: Notification bell with indicator
- **Smooth Transitions**: Alpine.js powered animations

## Best Practices

1. **Consistent Icons**: Use Heroicons for consistent iconography
2. **Color Scheme**: Stick to the light blue theme for consistency
3. **Responsive Design**: Always test on mobile devices
4. **Accessibility**: Use proper ARIA labels and semantic HTML
5. **Performance**: Keep Alpine.js components lightweight

## Dependencies

The template requires:
- **TailwindCSS**: For styling
- **Alpine.js**: For interactivity
- **Heroicons**: For icons (optional, can use other icon libraries)

All dependencies are loaded via CDN for easy setup, but you can install them locally for production use.