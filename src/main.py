import json
from datetime import datetime, timezone
from tinydb import TinyDB
import os


# Filters data from input dictionary
def transform_dictionary(dictionary):
    output = {'name': dictionary['name'],
              'created_at': datetime.fromisoformat(
                  dictionary['created_at']).astimezone(timezone.utc).__str__()}
    if dictionary['state'] is not None:
        output['cpu_usage'] = dictionary['state']['cpu']['usage']
        output['memory_usage'] = dictionary['state']['memory']['usage']
        addresses = []
        for network in dictionary['state']['network']:
            for address in dictionary['state']['network'][network]['addresses']:
                addresses.append(address['address'])
        output['addresses'] = addresses
    else:
        output['cpu_usage'] = None
        output['memory_usage'] = None
        output['addresses'] = []
    return output


if __name__ == '__main__':
    # Data fetch
    with open(os.path.abspath('resources/sample-data.json')) as json_file:
        data = json.load(json_file)

    # Data transformation
    documents = [transform_dictionary(dictionary) for dictionary in data]

    # Data storing
    db = TinyDB(os.path.abspath('resources/db.json'))
    for document in documents:
        db.insert(document)
