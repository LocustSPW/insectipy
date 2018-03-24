'''Unit tests for the Locusts Class'''
import unittest

import insectipy


class LocustsTest(unittest.TestCase):
    '''Tests for the insectipy.Locusts Class'''
    def setUp(self):
        '''Set some pre-test state for each test in this class'''
        self.replica_set = {
            'name': 'testing',
            'servers': [
                'test1:27017',
                'test2:27018',
                'test3:27019'
            ]
        }

    def tearDown(self):
        '''clean up the state after each test'''

    def test_init(self):
        '''Test that we can instantiate a Locusts class'''
        self.assertTrue(insectipy.Locusts(self.replica_set))

    def test_init_replica_set_requires_a_dictionary(self):
        '''Test that init will raise an exception if replica_set is not a
           dictionary'''
        with self.assertRaises(Exception):
            insectipy.Locusts('blah')
