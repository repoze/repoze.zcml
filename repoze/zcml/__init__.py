# the five imports below are not really unused, despite what PyFlakes
# thinks of the situation

import zope.interface
import zope.schema
import zope.configuration
import zope.component
import zope.configuration.fields

from zope.component.interface import provideInterface

def handler(methodName, *args, **kwargs):
    method = getattr(zope.component.getSiteManager(), methodName)
    method(*args, **kwargs)

def adapter(_context, factory, provides=None, for_=None, name=''):

    if for_ is None:
        if len(factory) == 1:
            for_ = zope.component.adaptedBy(factory[0])

        if for_ is None:
            raise TypeError("No for attribute was provided and can't "
                            "determine what the factory adapts.")

    for_ = tuple(for_)

    if provides is None:
        if len(factory) == 1:
            p = list(zope.interface.implementedBy(factory[0]))
            if len(p) == 1:
                provides = p[0]

        if provides is None:
            raise TypeError("Missing 'provides' attribute")

    # Generate a single factory from multiple factories:
    factories = factory
    if len(factories) == 1:
        factory = factories[0]
    elif len(factories) < 1:
        raise ValueError("No factory specified")
    elif len(factories) > 1 and len(for_) != 1:
        raise ValueError("Can't use multiple factories and multiple for")
    else:
        factory = _rolledUpFactory(factories)

    _context.action(
        discriminator = ('adapter', for_, provides, name),
        callable = handler,
        args = ('registerAdapter',
                factory, for_, provides, name, _context.info),
        )

class IAdapterDirective(zope.interface.Interface):
    """
    Register an adapter
    """

    factory = zope.configuration.fields.Tokens(
        title=u"Adapter factory/factories",
        description=(u"A list of factories (usually just one) that create"
                     " the adapter instance."),
        required=True,
        value_type=zope.configuration.fields.GlobalObject()
        )

    provides = zope.configuration.fields.GlobalInterface(
        title=u"Interface the component provides",
        description=(u"This attribute specifies the interface the adapter"
                     " instance must provide."),
        required=False,
        )

    for_ = zope.configuration.fields.Tokens(
        title=u"Specifications to be adapted",
        description=u"This should be a list of interfaces or classes",
        required=False,
        value_type=zope.configuration.fields.GlobalObject(
          missing_value=object(),
          ),
        )

    name = zope.schema.TextLine(
        title=u"Name",
        description=(u"Adapters can have names.\n\n"
                     "This attribute allows you to specify the name for"
                     " this adapter."),
        required=False,
        )

_handler = handler
def subscriber(_context, for_=None, factory=None, handler=None, provides=None):
    if factory is None:
        if handler is None:
            raise TypeError("No factory or handler provided")
        if provides is not None:
            raise TypeError("Cannot use handler with provides")
        factory = handler
    else:
        if handler is not None:
            raise TypeError("Cannot use handler with factory")
        if provides is None:
            raise TypeError(
                "You must specify a provided interface when registering "
                "a factory")

    if for_ is None:
        for_ = zope.component.adaptedBy(factory)
        if for_ is None:
            raise TypeError("No for attribute was provided and can't "
                            "determine what the factory (or handler) adapts.")

    for_ = tuple(for_)

    if handler is not None:
        _context.action(
            discriminator = None,
            callable = _handler,
            args = ('registerHandler',
                    handler, for_, u'', _context.info),
            )
    else:
        _context.action(
            discriminator = None,
            callable = _handler,
            args = ('registerSubscriptionAdapter',
                    factory, for_, provides, u'', _context.info),
            )


class ISubscriberDirective(zope.interface.Interface):
    """
    Register a subscriber
    """

    factory = zope.configuration.fields.GlobalObject(
        title=u"Subscriber factory",
        description=u"A factory used to create the subscriber instance.",
        required=False,
        )

    handler = zope.configuration.fields.GlobalObject(
        title=u"Handler",
        description=u"A callable object that handles events.",
        required=False,
        )

    provides = zope.configuration.fields.GlobalInterface(
        title=u"Interface the component provides",
        description=(u"This attribute specifies the interface the adapter"
                     " instance must provide."),
        required=False,
        )

    for_ = zope.configuration.fields.Tokens(
        title=u"Interfaces or classes that this subscriber depends on",
        description=u"This should be a list of interfaces or classes",
        required=False,
        value_type=zope.configuration.fields.GlobalObject(
          missing_value = object(),
          ),
        )

def utility(_context, provides=None, component=None, factory=None, name=''):
    if factory and component:
        raise TypeError("Can't specify factory and component.")

    if provides is None:
        if factory:
            provides = list(zope.interface.implementedBy(factory))
        else:
            provides = list(zope.interface.providedBy(component))
        if len(provides) == 1:
            provides = provides[0]
        else:
            raise TypeError("Missing 'provides' attribute")

    if factory:
        kw = dict(factory=factory)
    else:
        # older zope.component registries don't accept factory as a kwarg,
        # so if we don't need it, we don't pass it
        kw = {}

    _context.action(
        discriminator = ('utility', provides, name),
        callable = handler,
        args = ('registerUtility', component, provides, name),
        kw = kw,
        )

class IUtilityDirective(zope.interface.Interface):
    """Register a utility."""

    component = zope.configuration.fields.GlobalObject(
        title=u"Component to use",
        description=(u"Python name of the implementation object.  This"
                     " must identify an object in a module using the"
                     " full dotted name.  If specified, the"
                     " ``factory`` field must be left blank."),
        required=False,
        )

    factory = zope.configuration.fields.GlobalObject(
        title=u"Factory",
        description=(u"Python name of a factory which can create the"
                     " implementation object.  This must identify an"
                     " object in a module using the full dotted name."
                     " If specified, the ``component`` field must"
                     " be left blank."),
        required=False,
        )

    provides = zope.configuration.fields.GlobalInterface(
        title=u"Provided interface",
        description=u"Interface provided by the utility.",
        required=False,
        )

    name = zope.schema.TextLine(
        title=u"Name",
        description=(u"Name of the registration.  This is used by"
                     " application code when locating a utility."),
        required=False,
        )

def _rolledUpFactory(factories):
    def factory(ob):
        for f in factories:
            ob = f(ob)
        return ob
    # Store the original factory for documentation
    factory.factory = factories[0]
    return factory
