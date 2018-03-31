"""Unit tests for the Locusts Class"""
import unittest
from unittest.mock import MagicMock

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
        self.mongo_client = MagicMock(MongoClient)
        self.mongo_client.__getitem__.side_effect = MagicMock()
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
        self.assertTrue(isinstance(self.locusts.mongo_client, MagicMock))

    def test_db_name_argument(self):
        """Test that the db name can be set by passing an argument"""
        locusts = insectipy.Locusts(
            self.replica_set, dbname='blobby', client=self.mongo_client)
        self.assertEqual(locusts.dbname, 'blobby')

    def test_db_name_defaults_to_replica_set_name(self):
        """Test that dbname falls back to replica_set name"""
        self.assertEqual(self.locusts.dbname, self.replica_set['name'])

    def test_aggregate_shift_assignments(self):
        """Test that aggregate_shift_assignments returns an object with a
           next method"""
        data = self.locusts.aggregate_shift_assignments()
        next_method = getattr(data, 'next')
        self.assertTrue(callable(next_method))

    def test_aggregate_shift_assignments_data_insert(self):
        """Test that aggregate_shift_assignments inserts data correctly"""
        self.locusts.db.schedules.aggregate.return_value = [{
            'volunteer_id': 1234
        }]
        self.locusts.db.volunteers.find_one.return_value = {
            'first_name': 'Joe',
            'last_name': 'Blobby',
            'appointment': 'Guy'
        }
        self.locusts.aggregate_shift_assignments()
        self.locusts.db.temp_volunteer_shifts.insert.assert_called_with(
            {
                'volunteer_id': 1234,
                'full_name': 'Joe Blobby',
                'appointment': 'Guy'
            }
        )

    def test_aggregate_shift_assignments_when_no_volunteer_id(self):
        """Test that aggregate_shift_assignments does not insert data if
           no volunteer_ids have been returned from db.schedules"""
        self.locusts.db.schedules.aggregate.return_value = [{}]
        self.locusts.aggregate_shift_assignments()
        self.locusts.db.temp_volunteer_shifts.insert.assert_not_called()

    def test_aggregate_shift_assignments_when_no_volunteer_data(self):
        """Test that aggregate_shift_assignments does not insert data if
           no volunteer_data has been returned from db.volunteers"""
        self.locusts.db.schedules.aggregate.return_value = [{
            'volunteer_id': 1234
        }]
        self.locusts.db.volunteers.find_one.return_value = None
        self.locusts.aggregate_shift_assignments()
        self.locusts.db.temp_volunteer_shifts.insert.assert_not_called()
