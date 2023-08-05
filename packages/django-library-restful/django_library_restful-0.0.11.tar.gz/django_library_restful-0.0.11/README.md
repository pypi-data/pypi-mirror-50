# Django Library RESTful API

### project description
A django app RESTful api to manage multiple libraries concurrently.
1. Can add many library
2. Book shelves can be added to any library with a specific number
3. Lending books from libraries to one user can be managed

### About
This is a RESTful api to manage multiple libraries that borrow book to user. the [admin.py](https://github.com/MHolger77/django-libraries/blob/master/admin.py)
create good django adminstration for library that you can:
1. Search name , author or user that borrow book
2. Filter author of books
3. Search book and library between list of shelves
4. Filter shelves of specific library
5. Search Library in specific city
6. Look for which library has a specific book
7. Filter borrows list with borrow date and give back date


### Installation

Install using ``pip``::

    pip install djangorestframework
    pip install django-library-restful
    
1. Add "polls" to your INSTALLED_APPS setting like this::


    INSTALLED_APPS = [
    ...
    'django_library_restful',
    ]
        
2. Include the library URLconf in your project urls.py like this::

```python
from django.urls import path, include
from django_library_restfull.router import bookstore_api_router

urlpatterns = [
    path('api/library/', include(bookstore_api_router.urls))
]    
```

4. Run `python manage.py makemigrations django_library_restfull` to create the sql.

3. Run `python manage.py migrate` to create the polls models.

4. Use library api


### License
Uses the MIT license.

* Django Library RESTful api : https://github.com/MHolger77/django-libraries
* MIT: http://opensource.org/licenses/MIT
