import logging

from archivekit import open_collection

log = logging.getLogger(__name__)


class DataManager(object):
    """ The data manager coordinates read and write access to the
    ETL data storage. """

    def __init__(self):
        self.app = None
        self._coll = None

    @property
    def configured(self):
        return self.app is not None

    def init_app(self, app):
        self.app = app

    def package(self, dataset):
        """ Get a package for a given dataset name. """
        assert self.configured, 'Data manager not configured!'
        return self.collection.get(dataset)

    @property
    def collection(self):
        if not self.configured:
            return
        if self._coll is None:
            env = self.app.config
            storage_type = env.get('STORAGE_TYPE', 's3')
            if storage_type == 's3':
                args = {
                    'aws_key_id': env.get('AWS_KEY_ID'),
                    'aws_secret': env.get('AWS_SECRET'),
                    'bucket_name': env.get('AWS_DATA_BUCKET')
                }
            elif storage_type == 'file':
                args = {
                    'path': env.get('STORAGE_PATH', 'data')
                }
            self._coll = open_collection('datasets', storage_type, **args)
        return self._coll
