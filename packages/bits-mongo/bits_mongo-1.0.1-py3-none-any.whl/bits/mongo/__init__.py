"""Mongo class file."""

import pymongo

from bits.progressbar import Progress
from bson.json_util import dumps


class Mongo(object):
    """Mongo class."""

    def __init__(self, uri, db, auth=None, verbose=False):
        """Initialize a Mongo instance."""
        self.uri = uri
        self.db_name = db

        self.auth = auth
        self.verbose = verbose

        # check if the auth class sets verbose
        if auth:
            self.verbose = auth.verbose

        # create a mongo client
        self.mongoclient = pymongo.MongoClient(uri)

        # select a database
        self.db = self.mongoclient[db]

        # provide the pymongo package
        self.pymongo = pymongo

    def delete_document(self, collection, key, value):
        """Delete a document from a collection by key = value."""
        data = {key: value}
        return self.db[collection].delete_one(data)

    def get_collection(self, collection):
        """Return all items from a collection."""
        collectiondb = self.db[collection]
        return list(collectiondb.find())

    def get_collection_dict(
        self,
        collection,
        delete=False,
        key='_id',
        valid_keys=None
    ):
        """Return all items from a collection in dictionary form."""
        data = {}
        for d in self.get_collection(collection):
            # skip documents without the key attribute
            if key not in d:
                continue
            k = d.get(key)
            # delete invalid documents
            if valid_keys and k not in valid_keys:
                if delete:
                    self.delete_document(collection, key, k)
                continue

            data[k] = d

        return data

    def get_collection_stats(self):
        """Return statistics about the collections."""
        stats = {}
        for collection in self.db.list_collection_names():
            stats[collection] = self.db[collection].estimated_document_count()
        return stats

    def get_collections(self):
        """Return a list of collections by name."""
        return self.db.list_collection_names()

    def update_collection(self, collection, data, delete=False, sub=False):
        """Update a collection in Mongo."""
        collectiondb = self.db[collection]
        progress = Progress().start(data, self.verbose)
        count = 0
        # perform updates
        for key in data:
            progress.update()
            d = data[key]
            # deal with sub documents
            if sub:
                d = {'_id': key, sub: d}
            # update a document
            try:
                collectiondb.replace_one({'_id': key}, d, upsert=True)
                count += 1
            except Exception as e:
                print('ERROR document in "%s": %s' % (collection, key))
                print(e)
                if self.verbose:
                    print(dumps(d, indent=2, sort_keys=True))
        progress.finish()
        # delete extra documents
        if delete:
            for document in collectiondb.find({}, ['_id']):
                key = document['_id']
                if key not in data:
                    self.delete_document(collection, '_id', key)
        return count

    def update_document(self, collection, key, data):
        """Update a single document in Mongo."""
        collectiondb = self.db[collection]
        try:
            return collectiondb.replace_one({'_id': key}, data, upsert=True)
        except Exception as e:
            print('ERROR updating document %s' % (key))
            print(e)
            print(dumps(data, indent=2, sort_keys=True))

    #
    # Backward Compatibility Methods
    #
    def getCollection(self, collection, remove={}, keyname='_id'):
        """Retrieve a collection from BITSdb."""
        delete = False
        if remove:
            delete = True
        return self.get_collection_dict(
            collection,
            delete=delete,
            key=keyname,
            valid_keys=remove,
        )

    def updateCollection(self, collection, data, sub=False):
        """Update a collection in BITSdb."""
        # slack notification
        if self.auth:
            s = self.auth.slack()
            message = 'Updating *%s* collection: `%s` (%s records).' % (
                self.db_name,
                collection,
                len(data)
            )
            s.post_message(s.notifications, message)
        # update the collection
        return self.update_collection(collection, data, sub=sub)

    def updateDocument(self, collection, key, data):
        """Update a document in BITSdb."""
        return self.update_document(collection, key, data)
