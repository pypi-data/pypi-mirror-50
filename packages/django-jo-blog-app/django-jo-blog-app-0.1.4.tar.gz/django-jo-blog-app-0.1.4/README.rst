=====
blog 
=====

blog is an app that enables users to publish posts across the the platform.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "blog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'blog',
        'contact',
    ]

2. Include the blog URLconf in your project urls.py like this::

    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls', namespace='contact')),

3. Run `python manage.py migrate` to create the post models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a Post (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to participate in the blog.