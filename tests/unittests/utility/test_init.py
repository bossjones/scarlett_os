"""Test Home Assistant utility methods."""
# pylint: disable=too-many-public-methods
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

from scarlett_os import utility
import scarlett_os.utility.dt as dt_utility

# FIXME: Convert to pytest
# FIXME: 5/10/2017
class TestUtil(unittest.TestCase):
    """Test utility methods."""

    def test_sanitize_filename(self):
        """Test sanitize_filename."""
        self.assertEqual("test", utility.sanitize_filename("test"))
        self.assertEqual("test", utility.sanitize_filename("/test"))
        self.assertEqual("test", utility.sanitize_filename("..test"))
        self.assertEqual("test", utility.sanitize_filename("\\test"))
        self.assertEqual("test", utility.sanitize_filename("\\../test"))

    def test_sanitize_path(self):
        """Test sanitize_path."""
        self.assertEqual("test/path", utility.sanitize_path("test/path"))
        self.assertEqual("test/path", utility.sanitize_path("~test/path"))
        self.assertEqual("//test/path",
                         utility.sanitize_path("~/../test/path"))

    def test_slugify(self):
        """Test slugify."""
        self.assertEqual("test", utility.slugify("T-!@#$!#@$!$est"))
        self.assertEqual("test_more", utility.slugify("Test More"))
        self.assertEqual("test_more", utility.slugify("Test_(More)"))

    def test_repr_helper(self):
        """Test repr_helper."""
        self.assertEqual("A", utility.repr_helper("A"))
        self.assertEqual("5", utility.repr_helper(5))
        self.assertEqual("True", utility.repr_helper(True))
        self.assertEqual("test=1",
                         utility.repr_helper({"test": 1}))
        self.assertEqual("1986-07-09T12:00:00+00:00",
                         utility.repr_helper(datetime(1986, 7, 9, 12, 0, 0)))

    def test_convert(self):
        """Test convert."""
        self.assertEqual(5, utility.convert("5", int))
        self.assertEqual(5.0, utility.convert("5", float))
        self.assertEqual(True, utility.convert("True", bool))
        self.assertEqual(1, utility.convert("NOT A NUMBER", int, 1))
        self.assertEqual(1, utility.convert(None, int, 1))
        self.assertEqual(1, utility.convert(object, int, 1))

    def test_ensure_unique_string(self):
        """Test ensure_unique_string."""
        self.assertEqual(
            "Beer_3",
            utility.ensure_unique_string("Beer", ["Beer", "Beer_2"]))
        self.assertEqual(
            "Beer",
            utility.ensure_unique_string("Beer", ["Wine", "Soda"]))

    def test_ordered_enum(self):
        """Test the ordered enum class."""
        class TestEnum(utility.OrderedEnum):
            """Test enum that can be ordered."""

            FIRST = 1
            SECOND = 2
            THIRD = 3

        self.assertTrue(TestEnum.SECOND >= TestEnum.FIRST)
        self.assertTrue(TestEnum.SECOND >= TestEnum.SECOND)
        self.assertFalse(TestEnum.SECOND >= TestEnum.THIRD)

        self.assertTrue(TestEnum.SECOND > TestEnum.FIRST)
        self.assertFalse(TestEnum.SECOND > TestEnum.SECOND)
        self.assertFalse(TestEnum.SECOND > TestEnum.THIRD)

        self.assertFalse(TestEnum.SECOND <= TestEnum.FIRST)
        self.assertTrue(TestEnum.SECOND <= TestEnum.SECOND)
        self.assertTrue(TestEnum.SECOND <= TestEnum.THIRD)

        self.assertFalse(TestEnum.SECOND < TestEnum.FIRST)
        self.assertFalse(TestEnum.SECOND < TestEnum.SECOND)
        self.assertTrue(TestEnum.SECOND < TestEnum.THIRD)

        # Python will raise a TypeError if the <, <=, >, >= methods
        # raise a NotImplemented error.
        self.assertRaises(TypeError,
                          lambda x, y: x < y, TestEnum.FIRST, 1)

        self.assertRaises(TypeError,
                          lambda x, y: x <= y, TestEnum.FIRST, 1)

        self.assertRaises(TypeError,
                          lambda x, y: x > y, TestEnum.FIRST, 1)

        self.assertRaises(TypeError,
                          lambda x, y: x >= y, TestEnum.FIRST, 1)

    def test_ordered_set(self):
        """Test ordering of set."""
        set1 = utility.OrderedSet([1, 2, 3, 4])
        set2 = utility.OrderedSet([3, 4, 5])

        self.assertEqual(4, len(set1))
        self.assertEqual(3, len(set2))

        self.assertIn(1, set1)
        self.assertIn(2, set1)
        self.assertIn(3, set1)
        self.assertIn(4, set1)
        self.assertNotIn(5, set1)

        self.assertNotIn(1, set2)
        self.assertNotIn(2, set2)
        self.assertIn(3, set2)
        self.assertIn(4, set2)
        self.assertIn(5, set2)

        set1.add(5)
        self.assertIn(5, set1)

        set1.discard(5)
        self.assertNotIn(5, set1)

        # Try again while key is not in
        set1.discard(5)
        self.assertNotIn(5, set1)

        self.assertEqual([1, 2, 3, 4], list(set1))
        self.assertEqual([4, 3, 2, 1], list(reversed(set1)))

        self.assertEqual(1, set1.pop(False))
        self.assertEqual([2, 3, 4], list(set1))

        self.assertEqual(4, set1.pop())
        self.assertEqual([2, 3], list(set1))

        self.assertEqual('OrderedSet()', str(utility.OrderedSet()))
        self.assertEqual('OrderedSet([2, 3])', str(set1))

        self.assertEqual(set1, utility.OrderedSet([2, 3]))
        self.assertNotEqual(set1, utility.OrderedSet([3, 2]))
        self.assertEqual(set1, set([2, 3]))
        self.assertEqual(set1, {3, 2})
        self.assertEqual(set1, [2, 3])
        self.assertEqual(set1, [3, 2])
        self.assertNotEqual(set1, {2})

        set3 = utility.OrderedSet(set1)
        set3.update(set2)

        self.assertEqual([3, 4, 5, 2], set3)
        self.assertEqual([3, 4, 5, 2], set1 | set2)
        self.assertEqual([3], set1 & set2)
        self.assertEqual([2], set1 - set2)

        set1.update([1, 2], [5, 6])
        self.assertEqual([2, 3, 1, 5, 6], set1)

    def test_throttle(self):
        """Test the add cooldown decorator."""
        calls1 = []
        calls2 = []

        @utility.Throttle(timedelta(seconds=4))
        def test_throttle1():
            calls1.append(1)

        @utility.Throttle(timedelta(seconds=4), timedelta(seconds=2))
        def test_throttle2():
            calls2.append(1)

        now = dt_utility.utcnow()
        plus3 = now + timedelta(seconds=3)
        plus5 = plus3 + timedelta(seconds=2)

        # Call first time and ensure methods got called
        test_throttle1()
        test_throttle2()

        self.assertEqual(1, len(calls1))
        self.assertEqual(1, len(calls2))

        # Call second time. Methods should not get called
        test_throttle1()
        test_throttle2()

        self.assertEqual(1, len(calls1))
        self.assertEqual(1, len(calls2))

        # Call again, overriding throttle, only first one should fire
        test_throttle1(no_throttle=True)
        test_throttle2(no_throttle=True)

        self.assertEqual(2, len(calls1))
        self.assertEqual(1, len(calls2))

        with patch('scarlett_os.utility.utcnow', return_value=plus3):
            test_throttle1()
            test_throttle2()

        self.assertEqual(2, len(calls1))
        self.assertEqual(1, len(calls2))

        with patch('scarlett_os.utility.utcnow', return_value=plus5):
            test_throttle1()
            test_throttle2()

        self.assertEqual(3, len(calls1))
        self.assertEqual(2, len(calls2))

    def test_throttle_per_instance(self):
        """Test that the throttle method is done per instance of a class."""
        class Tester(object):
            """A tester class for the throttle."""

            @utility.Throttle(timedelta(seconds=1))
            def hello(self):
                """Test the throttle."""
                return True

        self.assertTrue(Tester().hello())
        self.assertTrue(Tester().hello())

    def test_throttle_on_method(self):
        """Test that throttle works when wrapping a method."""
        class Tester(object):
            """A tester class for the throttle."""

            def hello(self):
                """Test the throttle."""
                return True

        tester = Tester()
        throttled = utility.Throttle(timedelta(seconds=1))(tester.hello)

        self.assertTrue(throttled())
        self.assertIsNone(throttled())

    def test_throttle_on_two_method(self):
        """Test that throttle works when wrapping two methods."""
        class Tester(object):
            """A test class for the throttle."""

            @utility.Throttle(timedelta(seconds=1))
            def hello(self):
                """Test the throttle."""
                return True

            @utility.Throttle(timedelta(seconds=1))
            def goodbye(self):
                """Test the throttle."""
                return True

        tester = Tester()

        self.assertTrue(tester.hello())
        self.assertTrue(tester.goodbye())
