'''Unit tests for the Locusts Class'''
import unittest

import insectipy


class LocustsTest(unittest.TestCase):
    '''Tests for the insectipy.Locusts Class'''
    def setUp(self):
        '''Set some pre-test state for each test in this class'''

    def tearDown(self):
        '''clean up the state after each test'''

    def test_init(self):
        '''Test that we can instantiate a Locusts class'''
        self.assertTrue(insectipy.Locusts())
