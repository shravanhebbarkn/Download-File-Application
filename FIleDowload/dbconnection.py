import pymongo


def get_database():
    """Returns a MongoDB connection for the given database..
    """
    connection = pymongo.MongoClient('localhost',
                                     27017)
    db = connection['downloadstatus']
    col=db['status']
    return col