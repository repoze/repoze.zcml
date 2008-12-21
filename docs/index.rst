Documentation for repoze.zcml
=============================

:mod:`repoze.zcml` is a package which provides core ZCML directives
for the Zope Component Architecture (particularly, ``utility``,
``subscriber``, and ``adapter``).

Note that ``zope.configuration`` already *has* implementations of
handlers that allow similar directives to work.  You should only use
the ``repoze.zcml`` versions of these directives if your application
doesn't need the more advanced features of the "stock" directive types
of the same names present in ``zope.configuration``.  The "stock"
implementations use the concepts of "permissions", and "trusted"
adapters and utilities.  In most applications, these features are
unnecessary, and exposing them to users may be harmful.  Using
``repoze.zcml`` in this case makes it possible to use ZCML with fewer
Zope Python packages as dependencies, and removes the possibility that
your users will attempt to use these advanced features without any
understanding of what they do.

.. note:: The effect of ``repoze.zcml`` directives is exactly
   equivalent to the effect that the "stock" directives would have,
   save for the omission of more advanced features.

:mod:`repoze.zcml` contains "meta" ZCML that can be included within
your application's ZCML that makes certain directives work (listed
below).  After this meta ZCML is loaded, you can use the directives.

For an overall description of the concepts backing the directives
defined within :mod:`repoze.zcml`, see `A Comprehensive Guide to Zope
Component Architecture <http://www.muthukadan.net/docs/zca.html>`_.

Usage
-----

To make use of :mod:`repoze.zcml`, you should install the
:mod:`repoze.zcml` package, then subsequently include its "meta.zcml"
from within some ZCML that is used by your application::

  <include package="repoze.zcml" file="meta.zcml"/>

Thereafter, you will be able to use the directive types it defines
within your ZCML.

The directives defined in :mod:`repoze.zcml` are defined within the
namespace ``http://namespaces.repoze.org/bfg``.  Therefore to use any
of the :mod:`repoze.zcml` -defined directives without a
namespace-qualified name, you should write your ZCML like so:

.. code-block:: xml

  <configure xmnls="http://namespaces.repoze.org/bfg">

    <adapter
       factory="some.package.Foo"
       provides="some.package.IFoo"
       for="some.package.IBar some.package.IBaz"
       name="myadapter"
       />

  </configure>

On the other hand, if you want to use these directives with a
qualified name within another application that already has a default
``xmlns``, you can do so by adding a different XML namespace to the
``configure`` tag:

.. code-block:: xml

  <configure xmnls="http://namespaces.zope.org/zope">
       xmlns:bfg="http://namespaces.repoze.org/bfg">

    <bfg:adapter
       factory="some.package.Foo"
       provides="some.package.IFoo"
       for="some.package.IBar some.package.IBaz"
       name="myadapter"
       />

   </configure>

Directives
----------

`adapter`
~~~~~~~~~

The ``adapter`` directive registers an adapter within the component
architecture registry.

Example:

.. code-block:: xml

   <adapter
     factory="some.package.Foo"
     provides="some.package.IFoo"
     for="some.package.IBar some.package.IBaz"
     name="myadapter"
     />

factory
^^^^^^^

The factory which creates an adapter (dotted name).

provides
^^^^^^^^

This implies the interface that the adapter provides (dotted name).

for
^^^

This implies the interface(s) which the adapter is "for".  (One or
more dotted names).

name
^^^^

The name by which the adapter should be looked up.

`utility`
~~~~~~~~~

The ``utility`` directive registers a utility within the component
architecture registry.

Example:

.. code-block:: xml

   <utility
     factory="some.package.Foo"
     provides="some.package.IFoo"
     name="myutility"
     />

factory
^^^^^^^

Describes the factory which should create the utility to be
registered.  This attribute is mutually exlusive with the
``component`` attribute.

component
^^^^^^^^^

Describes the component registered as the adapter.  This attribute is
mutually exlusive with the ``factory`` attribute.

provides
^^^^^^^^

Describes the provides interface for an adapter.

for
^^^

Describes the for interface(s) for an adapter.

name
^^^^

Describes the name of the adapter.

`subscriber`
~~~~~~~~~~~~

The ``subscriber`` directive registers an event subscriber within the
component architecture registry.

Example:

.. code-block:: xml

   <subscriber
     handler="some.package.myhandler"
     provides="some.package.IFoo"
     for="some.package.IBar"
     />

handler
^^^^^^^

The handler for the subscriber.  This is a subscriber which does not
require a factory.  This attribute is mutually exclusive with the
``factory`` directive.

factory
^^^^^^^

The factory which creates an subscriber (dotted name).  This attribute
is mutually exclusive with the ``handler`` directive.

provides
^^^^^^^^

This implies the interface that the subscriber adapter provides
(dotted name).

for
^^^

This implies the interface(s) which the subscriber adapter is "for".
(One or more dotted names).

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
