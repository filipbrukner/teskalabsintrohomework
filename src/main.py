import json
from datetime import datetime, timezone
from tinydb import TinyDB, Query
import os
import asyncio


# Filters data from input dictionary
def transform_dictionary(dictionary):
    output = {'name': dictionary['name'],
              'created_at': str(datetime.fromisoformat(
                  dictionary['created_at']).astimezone(timezone.utc)),
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


# Safe insert into database
def safe_insert(database, document):
    database.upsert(document, Query().name == document['name'])


# Transform and insert a single document into database
async def transform_insert(database, document):
    transformed = transform_dictionary(document)
    safe_insert(database, transformed)


# Asyncio main function
async def main(path, documents):
    db = TinyDB(os.path.abspath(path))
    await asyncio.gather(*(transform_insert(db, document) for document in documents))


if __name__ == '__main__':
    # Data fetch
    with open(os.path.abspath('resources/sample-data.json')) as json_file:
        data = json.load(json_file)

    # Data transformation and storing
    asyncio.run(main('resources/db.json', data))
