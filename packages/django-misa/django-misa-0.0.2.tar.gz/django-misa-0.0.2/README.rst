==========
misa
==========

|Build Status (Travis)| |Py versions|

ISA organisation for metabolomic studies with Django

Further documentation available on `ReadTheDocs <https://mogi.readthedocs.io/en/latest/>`__

Quick start
-----------

1. Add "misa" and django application dependencies to your INSTALLED_APPS setting like this (misa should come before gfiles and mbrowse)::


    INSTALLED_APPS = [
        ...
        'misa',
        'mbrowse',
        'gfiles',

        'django_tables2',
        'django_tables2_column_shifter',
        'django_filters',
        'bootstrap3',
        'django_sb_admin',
        'dal',
        'dal_select2',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^', include('gfiles.urls')),
    url('mbrowse/', include('mbrowse.urls')),
    url('misa/', include('misa.urls')),


3. Run `python manage.py migrate` to create the misa models.

4. Start the development server and visit http://127.0.0.1:8000/misa/ilist/

5. Register http://127.0.0.1:8000/register/ and login http://127.0.0.1:8000/login/

5. Create an investigation http://127.0.0.1:8000/icreate/, study http://127.0.0.1:8000/icreate/, assay http://127.0.0.1:8000/icreate/acreate

6. Upload data to an assay http://127.0.0.1:8000/upload_assay_data_files/[assay-id]/

7. Add a protocol e.g. Chromatography protocol http://127.0.0.1:8000/cp_create

8. Add ontology information http://127.0.0.1:8000/search_ontologyterm


.. |Build Status (Travis)| image:: https://travis-ci.com/computational-metabolomics/django-misa.svg?branch=master
   :target: https://travis-ci.com/computational-metabolomics/django-misa/

.. |Py versions| image:: https://img.shields.io/pypi/pyversions/django-misa.svg?style=flat&maxAge=3600
   :target: https://pypi.python.org/pypi/django-misa/
