.. gcudm_tutorial

.. image:: _static/images/logo.svg
   :width: 150px
   :alt: gcudm
   :align: right

--------
Tutorial
--------

Installation
------------

You can install the library using `pip`.

.. code-block:: bash

   pip install gcudm

If you need a specific version of the data model, specify it when you install.

.. code-block:: bash

   pip install gcudm==0.0.1

Build Your Database
-------------------

`gcudm` is built on `GeoAlchemy 2 <http://geoalchemy-2.readthedocs.io/en/latest/>`_
(and `SqlAlchey <https://www.sqlalchemy.org/>`_).  We try not to come between
you and the underlying platforms, so if you're familiar with these frameworks
everything should work as you expect.

One convenience that is provided is the :py:func:`gcudm.model.load` function
which you can call to make sure that all the modules that define
`object-relational mappings <http://geoalchemy-2.readthedocs.io/en/latest/orm_tutorial.html#>`_
are loaded.  You should do this before you create your database tables from
the model to make sure that all the classes that implement the
`declarative base <http://geoalchemy-2.readthedocs.io/en/latest/orm_tutorial.html#declare-a-mapping>`_
are loaded.

.. code-block:: python

   from gcudm.base import Base
   import gcudm.model
   from sqlalchemy import create_engine

   # Load the entire model.
   gcudm.model.load()

   # The rest is standard SQLAlchemy...
   # ...just create an engine.
   engine = create_engine(
       'postgresql://<user>:<password>@<host>/<your-database>',
       echo=True)

   # Now create the tables in your database.
   Base.metadata.create_all(engine)