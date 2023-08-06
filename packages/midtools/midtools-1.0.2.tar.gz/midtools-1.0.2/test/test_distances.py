from unittest import TestCase

from six import assertRaisesRegex

from midtools.distances import DistanceCache


class TestDistanceCache(TestCase):
    """
    Test the DistanceCache class.
    """
    def testEmpty(self):
        """
        The distance group must give a distance as provided by the distance
        function on two new elements.
        """
        def dist(a, b):
            return 4

        dc = DistanceCache(dist)
        # self.assertEqual(4, dc.distance('hey', 'you'))

    def testRepeatedCall(self):
        """
        The distance group must only call the distance function once when asked
        for the distance between two elements it has already computed a
        distance for.
        """
        count = 0

        def dist(a, b):
            nonlocal count
            count += 1
            return 4

        dc = DistanceCache(dist)
        dc.add('hey')
        dc.add('you')
        self.assertEqual(4, dc.distance('hey', 'you'))
        self.assertEqual(1, count)
        self.assertEqual(4, dc.distance('hey', 'you'))
        self.assertEqual(1, count)

    def testDistanceOnRemovedPair(self):
        """
        The distance method must raise KeyError if called on a pair of objects
        that have been removed.
        """
        def dist(a, b):
            return 4

        dc = DistanceCache(dist)
        dc.add('hey')
        dc.add('you')

        self.assertEqual(4, dc.distance('hey', 'you'))

        dc.remove('hey')
        dc.remove('you')

        error = 'you'
        assertRaisesRegex(self, KeyError, error, dc.distance, 'hey', 'you')

    def testDistanceOnRemovedOneOfPair(self):
        """
        The distance method must raise KeyError if called on a pair of objects
        one of which has been removed.
        """
        def dist(a, b):
            return 4

        dc = DistanceCache(dist)
        dc.add('hey')
        dc.add('you')

        self.assertEqual(4, dc.distance('hey', 'you'))

        dc.remove('you')

        error = 'you'
        assertRaisesRegex(self, KeyError, error, dc.distance, 'hey', 'you')

    def testLowestDistance(self):
        """
        The lowestDistance method must return the lowest distance.
        """
        def dist(a, b):
            (a, b) = sorted([a, b])
            if (a, b) == (1, 2):
                return 5
            elif (a, b) == (1, 3):
                return 4
            elif (a, b) == (2, 3):
                return 6
            else:
                raise ValueError('Oops: (%s, %s)' % (a, b))

        dc = DistanceCache(dist)
        dc.add(1)
        dc.add(2)
        dc.add(3)

        self.assertEqual(4, dc.lowestDistance())

    def testPopReturnsLowestDistance(self):
        """
        The pop method must return the lowest distance pair.
        """
        def dist(a, b):
            (a, b) = sorted([a, b])
            if (a, b) == (1, 2):
                return 5
            elif (a, b) == (1, 3):
                return 4
            elif (a, b) == (2, 3):
                return 6
            else:
                raise ValueError('Oops: (%s, %s)' % (a, b))

        dc = DistanceCache(dist)
        dc.add(1)
        dc.add(2)
        dc.add(3)

        a, b = dc.pop()
        self.assertEqual((1, 3), (a, b))
