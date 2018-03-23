'''This is the insectipy module'''


class Locusts(object):
    '''A class for interacting with the Locusts app'''

    def __init__(self, replica_set):
        self.replica_set = replica_set
