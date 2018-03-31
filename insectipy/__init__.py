"""This is the insectipy module"""
from datetime import datetime, timedelta

from pymongo import MongoClient
import scheme


REPLICA_SET_SCHEMA = scheme.Structure({
    'name': scheme.Text(nonempty=True),
    'servers': scheme.Sequence(
        scheme.Text(nonempty=True),
        unique=True,
        nonempty=True)
})


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

    def aggregate_shift_assignments(self):
        """Provide a grouped projection of volunteers who have joined
           the schedule from the last 3 months going forward

            Returns:
                a pymongo CommandCursor of volunteer data
        """
        # clean up db before starting
        self.db.temp_volunteer_shifts.drop()

        # Look through only the last 12 weeks of scheduling activity
        today = datetime.utcnow()
        window = today - timedelta(weeks=12)

        # Prepare temporary collection of all volunteers that worked a shift
        # in the past 12 weeks. The data is unwound by the shifts and
        # rearranged to include just the information contained in the
        # $project setting.
        for vol_type in ['volunteer_ids', 'key_man']:
            for shift in range(6):
                key = '.'.join(['$shifts', str(shift), vol_type])

                pipeline_operations = [
                    {"$match": {"date": {"$gte": window}}}
                ]

                if vol_type == 'volunteer_ids':
                    pipeline_operations.append({"$unwind": key})

                pipeline_operations.append({
                    "$project": {
                        "_id": 0,
                        "schedule_id": "$_id",
                        "volunteer_id": key,
                        "location_id": 1,
                        "appointment": 1
                    }
                })

                for result in self.db.schedules.aggregate(
                        pipeline_operations):
                    if 'volunteer_id' in result:
                        volunteer_data = self.db.volunteers.find_one(
                            {'_id': result['volunteer_id']})
                        if volunteer_data:
                            new = dict(result)
                            new['full_name'] = ' '.join([
                                volunteer_data['first_name'],
                                volunteer_data['last_name']])
                            new['appointment'] = volunteer_data['appointment']
                            self.db.temp_volunteer_shifts.insert(new)
        op_group = [{
            "$group": {
                "_id": {
                    "volunteer_id": "$volunteer_id",
                    "full_name": "$full_name",
                    "appointment": "$appointment"
                },
                "location_ids": {"$addToSet": "$location_id"}
            }
        }]
        return self.db.temp_volunteer_shifts.aggregate(op_group)
