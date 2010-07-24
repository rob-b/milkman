import unittest
import types
import string
from django.db import models
from milkman.dairy import milkman
from milkman.dairy import MilkTruck
from milkman.generators import email_generator, random_choice_iterator, random_string, random_float, random_ipaddress_maker, random_float_maker,random_comma_seperated_integer_maker, random_time_string_maker
from testapp.models import *

MODELS = [Root, Child]
class ModelTest(unittest.TestCase):
    def tearDown(self):
        for m in MODELS:
            m._default_manager.all().delete()
    
    def test_create(self):
        r = milkman.deliver(Root)
        self.assertEqual(Root, r.__class__)
        self.assertTrue(bool(r.id))
        assert r.name is not None

    def test_create_explicit(self):
        r = milkman.deliver(Root, name='foo')
        self.assertEqual('foo', r.name)

    def test_create_child(self):
        child = milkman.deliver(Child)
        assert child.root
    
    def test_optional_relation(self):
        sibling = milkman.deliver(Sibling)
        self.assertEqual(None, sibling.root)
    
    def test_recurs_on_grandchildren(self):
        gc = milkman.deliver(GrandChild)
        self.assertNotEqual(None, gc.parent.root)

    def test_m2m(self):
        aunt = milkman.deliver(Aunt)
        self.assertEquals(1, len(aunt.uncles.all()))
        self.assertEquals(1, len(Uncle.objects.all()))
        self.assertEquals(Uncle.objects.all()[0], aunt.uncles.all()[0])
    
    def test_m2m_explicit(self):
        uncle = milkman.deliver(Uncle)
        aunt = milkman.deliver(Aunt, uncles=[uncle])
        self.assertEquals(uncle, aunt.uncles.all()[0])
    
class RandomFieldTest(unittest.TestCase):
    def test_required_field(self):
        root = milkman.deliver(Root)
        assert root.name
        assert isinstance(root.boolean, bool)
        assert isinstance(root.csi, str)
        assert isinstance(root.df, str)
        assert isinstance(root.dt, str)
        assert isinstance(root.decimal, str)
        assert isinstance(root.email, str)
        assert isinstance(root.my_float, float)
        assert isinstance(root.integer, int)
        assert isinstance(root.big_integer, int)
        assert isinstance(root.small_integer, int)
        assert isinstance(root.ip, str)
        assert isinstance(root.s, str)
        assert isinstance(root.mytime, str)
        assert isinstance(root.positive_integer, int)
        assert isinstance(root.small_positive_integer, int)
        assert (isinstance(root.null_boolean, bool) or isinstance(root.null_boolean, types.NoneType))
  
        
class FieldTest(unittest.TestCase):
    def test_needs_generated_value(self):
        f = Root._meta.get_field('name')
        assert MilkTruck(None).needs_generated_value(f)
        assert not f.has_default()
        self.assertEqual('', f.get_default())

class FieldValueGeneratorTest(unittest.TestCase):
    def test_email_generator(self):
        f = models.EmailField()
        g = email_generator('test', 'fake.com')(f)()
        self.assertEquals('test1@fake.com', g.next())
        self.assertEquals('test2@fake.com', g.next())

    def test_random_str(self):
        self.assertEqual(8, len(random_string()))
        self.assertEqual('a' * 8, random_string(chars=['a']))
        self.assertEqual('a' * 10, random_string(10, ['a']))
        
    def test_random_choice_iterator(self):
        self.assertEqual([''],[x for x in random_choice_iterator()])
        self.assertEqual([1],[x for x in random_choice_iterator([1])])
        self.assertEqual(['', ''], [s for s in random_choice_iterator(size=2)])
        self.assertEqual([1, 1], [s for s in random_choice_iterator([1], 2)])
        
    def test_random_float(self):
        assert random_float() > 1
        assert random_float() < 101
        assert isinstance(random_float(), float)
        
    def test_random_ipaddress(self):
        f = models.IPAddressField()
        ip = random_ipaddress_maker(f)().next()
        ip = ip.split('.')
        self.assertEquals(len(ip), 4)
        
    def test_random_comma_seperated_integer_maker(self):
        f = models.CommaSeparatedIntegerField()
        v = random_comma_seperated_integer_maker(f)().next()
        self.assertEquals(len(v.split(',')), 4)
        
    def test_timefield_maker(self):
        f = models.TimeField()
        v = random_time_string_maker(f)().next()
        times = v.split(':')
        self.assertEquals(len(times), 3)