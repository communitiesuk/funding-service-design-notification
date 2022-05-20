from app.config import FLASK_ROOT
import os
import json
from dataclasses import dataclass


def get_data():
    """ This is a dummy data for data mapping.
    TO BE DELETED ONCE INTEGRATED WITH AUTHENTICATOR SERVICE. 
    """
    file_path = os.path.join(FLASK_ROOT,"app","notification","application_submission",
    "dummy_data.json")

    json_data = open(file_path)
    data = json.load(json_data)
    json_data.close()
    print(data)

get_data()



@dataclass
class ProcessApplicationData:
    pass
