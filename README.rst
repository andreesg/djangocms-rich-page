=========
Rich Page
=========

Adds rich content to django CMS 3 pages.

Quick start
-----------

1. Add "rich_page" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rich_page',
    )

2. Include "rich_page/sidebar_right.html" template like this::
    
    CMS_TEMPLATES = (
        ...
        ('rich_page/sidebar_right.html', 'Rich Page'),
    )

3. Execute migration or syncdb to create the rich_page models::

    $ python manage.py syncdb

    $ python manage.py migrate

=====
Usage
=====

You will find a new Toolbar Menu "Pages" with the following items::

    Add Page
    Add Sub Page
    Remove Page

And the following new items::

    Add Article / Edit Article
    Remove Article

Add Article - Allows to add rich content, "Lead in", "body" and "key visual" to the current page.

Don't forget to choose "Rich Page" as the template for the current page ;) 
