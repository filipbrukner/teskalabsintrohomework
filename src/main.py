import json
from datetime import datetime, timezone
from tinydb import TinyDB, Query
import os
import asyncio


# Filters data from input dictionary
def transform_dictionary(dictionary):
    output = {'name': dictionary['name'],
              'created_at': datetime.fromisoformat(
                  dictionary['created_at']).astimezone(timezone.utc).__str__(),
              'status': dictionary['status']}
    if dictionary['state'] is not None:
        output['cpu_usage'] = dictionary['state']['cpu']['usage']
        output['memory_usage'] = dictionary['state']['memory']['usage']
        addresses = []
        for network in dictionary['state']['network']:
            for address in dictionary['state']['network'][network][
                'addresses']:
                addresses.append(address['address'])
        output['addresses'] = addresses
    else:
        output['cpu_usage'] = None
        output['memory_usage'] = None
        output['addresses'] = []
    return output


def safe_insert(database, document):
    database.upsert(document, Query().name == document['name'])


async def transform_insert(database, document):
    transformed = transform_dictionary(document)
    safe_insert(database, transformed)


async def main(path, documents):
    db = TinyDB(os.path.abspath(path))
    await asyncio.gather(*(transform_insert(db, document) for document in documents))


if __name__ == '__main__':
    # Data fetch
    with open(os.path.abspath('resources/sample-data.json')) as json_file:
        data = json.load(json_file)

    # Data transformation
    documents = [transform_dictionary(dictionary) for dictionary in data]

    asyncio.run(main('resources/db.json', data))

    # # Data storing
    # db = TinyDB(os.path.abspath('resources/db.json'))
    # for document in documents:
    #     db.upsert(document, Query().name == document['name'])
