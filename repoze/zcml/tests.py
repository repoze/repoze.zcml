import unittest
from zope.testing.cleanup import cleanUp

class TestAdapter(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def _callFUT(self, *arg, **kw):
        from repoze.zcml import adapter
        return adapter(*arg, **kw)

    def test_for_is_None_no_adaptedBy(self):
        context = DummyContext()
        factory = DummyFactory()
        self.assertRaises(TypeError, self._callFUT, context, [factory],
                          provides=None, for_=None)

    def test_for_is_None_adaptedBy_still_None(self):
        context = DummyContext()
        factory = DummyFactory()
        factory.__component_adapts__ = None
        self.assertRaises(TypeError, self._callFUT, context, [factory],
                      provides=None, for_=None)

    def test_for_is_None_adaptedBy_set(self):
        from repoze.zcml import handler
        context = DummyContext()
        factory = DummyFactory()
        factory.__component_adapts__ = (ITest,)
        self._callFUT(context, [factory], provides=IFactory, for_=None)
        self.assertEqual(len(context._actions), 1)
        regadapt = context._actions[0]
        self.assertEqual(regadapt['discriminator'],
                         ('adapter', (ITest,), IFactory, ''))
        self.assertEqual(regadapt['callable'],
                         handler)
        self.assertEqual(regadapt['args'],
                         ('registerAdapter', factory, (ITest,), IFactory,
                          '', None))

    def test_provides_missing(self):
        context = DummyContext()
        factory = DummyFactory()
        self.assertRaises(TypeError, self._callFUT, context, [factory],
                          provides=None, for_=(ITest,))

    def test_provides_obtained_via_implementedBy(self):
        from repoze.zcml import handler
        context = DummyContext()
        self._callFUT(context, [DummyFactory], for_=(ITest,))
        regadapt = context._actions[0]
        self.assertEqual(regadapt['discriminator'],
                         ('adapter', (ITest,), IFactory, ''))
        self.assertEqual(regadapt['callable'],
                         handler)
        self.assertEqual(regadapt['args'],
                         ('registerAdapter', DummyFactory, (ITest,), IFactory,
                          '', None))

    def test_multiple_factories_multiple_for(self):
        context = DummyContext()
        factory = DummyFactory()
        self.assertRaises(ValueError, self._callFUT, context,
                          [factory, factory],
                          provides=IFactory,
                          for_=(ITest, ITest))

    def test_no_factories_multiple_for(self):
        context = DummyContext()
        factory = DummyFactory()
        self.assertRaises(ValueError, self._callFUT, context,
                          factory=[],
                          provides=IFactory,
                          for_=(ITest, ITest))
        
    def test_rolled_up_factories(self):
        from repoze.zcml import handler
        context = DummyContext()
        factory = DummyFactory()
        self._callFUT(context,
                      [factory, factory],
                      provides=IFactory,
                      for_=(ITest,))
        regadapt = context._actions[0]
        self.assertEqual(regadapt['discriminator'],
                         ('adapter', (ITest,), IFactory, ''))
        self.assertEqual(regadapt['callable'],
                         handler)
        self.assertEqual(len(regadapt['args']), 6)
        

class TestSubscriber(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def _callFUT(self, *arg, **kw):
        from repoze.zcml import subscriber
        return subscriber(*arg, **kw)

    def test_no_factory_no_handler(self):
        context = DummyContext()
        self.assertRaises(TypeError,
                          self._callFUT, context, for_=None, factory=None,
                          handler=None,
                          provides=None)

    def test_handler_with_provides(self):
        context = DummyContext()
        self.assertRaises(TypeError,
                          self._callFUT, context, for_=None, factory=None,
                          handler=1, provides=1)

    def test_handler_and_factory(self):
        context = DummyContext()
        self.assertRaises(TypeError,
                          self._callFUT, context, for_=None, factory=1,
                          handler=1, provides=None)

    def test_no_provides_with_factory(self):
        context = DummyContext()
        self.assertRaises(TypeError,
                          self._callFUT, context, for_=None, factory=1,
                          handler=None, provides=None)

    def test_adapted_by_as_for_is_None(self):
        context = DummyContext()
        factory = DummyFactory()
        factory.__component_adapts__ = None
        self.assertRaises(TypeError, self._callFUT, context, for_=None,
                          factory=factory, handler=None, provides=IFactory)
        
    def test_register_with_factory(self):
        from repoze.zcml import handler
        context = DummyContext()
        factory = DummyFactory()
        self._callFUT(context, for_=(ITest,),
                      factory=factory, handler=None, provides=IFactory)
        self.assertEqual(len(context._actions), 1)
        subadapt = context._actions[0]
        self.assertEqual(subadapt['discriminator'], None)
        self.assertEqual(subadapt['callable'], handler)
        self.assertEqual(subadapt['args'],
                         ('registerSubscriptionAdapter', factory,
                          (ITest,), IFactory, u'', None) )

    def test_register_with_handler(self):
        from repoze.zcml import handler
        context = DummyContext()
        factory = DummyFactory()
        self._callFUT(context, for_=(ITest,),
                      factory=None, handler=factory)
        self.assertEqual(len(context._actions), 1)
        subadapt = context._actions[0]
        self.assertEqual(subadapt['discriminator'], None)
        self.assertEqual(subadapt['callable'], handler)
        self.assertEqual(subadapt['args'],
                         ('registerHandler', factory,
                          (ITest,), u'', None) )

class TestUtility(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def _callFUT(self, *arg, **kw):
        from repoze.zcml import utility
        return utility(*arg, **kw)

    def test_factory_and_component(self):
        context = DummyContext()
        self.assertRaises(TypeError, self._callFUT,
                          context, factory=1, component=1)

    def test_missing_provides(self):
        context = DummyContext()
        self.assertRaises(TypeError, self._callFUT, context, provides=None)
        
    def test_provides_from_factory_implements(self):
        from repoze.zcml import handler
        context = DummyContext()
        self._callFUT(context, factory=DummyFactory)
        self.assertEqual(len(context._actions), 1)
        utility = context._actions[0]
        self.assertEqual(utility['discriminator'], ('utility', IFactory, ''))
        self.assertEqual(utility['callable'], handler)
        self.assertEqual(utility['args'],
                         ('registerUtility', None, IFactory, ''))
        self.assertEqual(utility['kw'],
                         {'factory': DummyFactory})

    def test_provides_from_component_provides(self):
        from repoze.zcml import handler
        context = DummyContext()
        component = DummyFactory()
        self._callFUT(context, component=component)
        self.assertEqual(len(context._actions), 1)
        utility = context._actions[0]
        self.assertEqual(utility['discriminator'], ('utility', IFactory, ''))
        self.assertEqual(utility['callable'], handler)
        self.assertEqual(utility['args'],
                         ('registerUtility', component, IFactory, ''))
        self.assertEqual(utility['kw'], {})

class TestLoadZCML(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def test_it(self):
        from zope.configuration import xmlconfig
        import repoze.zcml
        xmlconfig.file('meta.zcml', package=repoze.zcml)

    

from zope.interface import Interface
from zope.interface import implements

class ITest(Interface):
    pass

class IFactory(Interface):
    pass

class DummyFactory(object):
    implements(IFactory)
    def __call__(self):
        return 1
        
class DummyContext(object):
    info = None
    
    def __init__(self):
        self._actions = []

    def action(self, discriminator, callable, args, kw=None):
        self._actions.append(
            {'discriminator':discriminator,
             'callable':callable,
             'args':args,
             'kw':kw
             }
            )
