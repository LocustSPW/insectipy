"""Unit tests for the Locusts Class"""
import unittest
from unittest.mock import Mock

from pymongo import MongoClient

import insectipy


class LocustsTest(unittest.TestCase):
    """Tests for the insectipy.Locusts Class"""
    def setUp(self):
        """Set some pre-test state for each test in this class"""
        self.replica_set = {
            'name': 'testing',
            'servers': [
                'test1:27017',
                'test2:27018',
                'test3:27019'
            ]
        }
        self.mongo_client = Mock(MongoClient)
        self.locusts = insectipy.Locusts(
                self.replica_set, client=self.mongo_client)

    def tearDown(self):
        """clean up the state after each test"""

    def test_init(self):
        """Test that we can instantiate a Locusts class"""
        self.assertTrue(self.locusts)

    def test_replica_set_matches_a_schema(self):
        """Test that init raises an exception if passed data does not match
           the replica_set schema"""
        with self.assertRaises(Exception):
            insectipy.Locusts('blah')
        with self.assertRaises(Exception):
            insectipy.Locusts({})

    def test_mongo_client(self):
        """Test that new instances of Locusts has a mongo client"""
        self.assertTrue(isinstance(self.locusts.mongo_client, Mock))
