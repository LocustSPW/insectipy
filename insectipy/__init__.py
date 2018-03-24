'''This is the insectipy module'''
import scheme


REPLICA_SET_SCHEMA = scheme.Structure({
    'name': scheme.Text(nonempty=True),
    'servers': scheme.Sequence(
        scheme.Text(nonempty=True),
        unique=True,
        nonempty=True)
})


class Locusts(object):
    '''A class for interacting with the Locusts app'''

    def __init__(self, replica_set):
        self.replica_set = REPLICA_SET_SCHEMA.serialize(replica_set)
