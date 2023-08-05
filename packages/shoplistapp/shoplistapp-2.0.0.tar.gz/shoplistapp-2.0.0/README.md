Shoppinglist
Shoppinglist is a simple Django app designed to keep a record of shoppinglist items for easy remembrance.

Quick start
Add "shoppinglist" to your INSTALLED_APPS setting like this:

INSTALLED_APPS = [
    ...
    'shoppinglist',
]
Include the application's URLconf in your project urls.py like this:

path('', include('shoppinglist.urls')),
Run python manage.py migrate to create the shoppinglist models.

Visit https://www.remindershoplist.duckdns.org/  to view your list.
