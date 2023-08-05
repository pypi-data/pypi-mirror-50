import sys
import logging
import json

from jsonresume import Resume
from jsonresume.exceptions import InvalidResumeError


class JsonObject(object):
    """
    All work for this function go to
    https://dev.to/mandrewcito/nested-json-to-python-object--5ajp
    """
    def __init__(self, json):
        jsonDict = dict(json)

        for key, val in jsonDict.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if type(value) is list:
            return [self.compute_attr_value(x) for x in value]
        elif type(value) is dict:
            return JsonObject(value)
        else:
            return value


def load(json_filepath):
    try:
        logging.info("JSON parsing...")
        with open(json_filepath, 'r') as f:
            resume_json = json.load(f)
    except IOError:
        msg = "Json file could not be loaded. Perhaps file path: \n\
      [{}] is incorrect".format(json_filepath)
        logging.exception(msg)
        sys.exit(1)
    except ValueError:
        logging.exception(
            "Json file could not be loaded. The syntax is not valid.")
        sys.exit(1)
    else:
        resume = Resume(resume_json)
        try:
            resume.validate()
        except InvalidResumeError:
            msg = "The json resume don't respect standard. Check: \n\
      https://jsonresume.org/schema/."
            logging.exception(msg)
            sys.exit(1)
        else:
            logging.info("JSON parsing done.")
            return JsonObject(resume_json)
