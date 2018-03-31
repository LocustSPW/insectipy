"""This is the insectipy module"""
from pymongo import MongoClient
import scheme


REPLICA_SET_SCHEMA = scheme.Structure({
    'name': scheme.Text(nonempty=True),
    'servers': scheme.Sequence(
        scheme.Text(nonempty=True),
        unique=True,
        nonempty=True)
})

TABLENAMES = [
    'locations',
    'scheduled_reports',
    'scheduled_volunteers',
    'schedules',
    'temp_volunteer_shifts',
    'volunteer_assignments',
    'volunteers'
]


class Locusts(object):
    """A class for interacting with the Locusts app"""

    def __init__(self, replica_set, dbname=None, client=MongoClient):
        """ Initialize the Locusts class, setting up a mongo db connection

        Args:
            :param replica_set: A dictionary of mongo connection data matching
                REPLICA_SET_SCHEMA
            :param dbname: A string representing the database name
            :param client: A class for connecting to a mongodb service
                Typically the pymongo.MongoClient class. Provided as a keyword
                argument for the sake of testing via dependency injection.

        """
        self.replica_set = REPLICA_SET_SCHEMA.serialize(replica_set)
        self.mongo_client = client(
            self.replica_set['servers'],
            replicaSet=self.replica_set['name']
        )
        if dbname:
            self.dbname = dbname
        else:
            self.dbname = self.replica_set['name']

        self.db = self.mongo_client[self.dbname]

        for attribute in TABLENAMES:
            setattr(self, attribute, getattr(self.db, attribute))
