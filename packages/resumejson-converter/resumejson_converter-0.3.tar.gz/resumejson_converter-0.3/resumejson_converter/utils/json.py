import logging
import json

from jsonresume import Resume
from jsonresume.exceptions import InvalidResumeError


class JsonObject(object):
    """
    Simple JSON object.

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
    """
    Return a JsonObject from resumejson_converter.utils.json.
    """
    try:
        logging.info("JSON parsing...")
        if type(json_filepath) is str:
            with open(json_filepath, 'r') as f:
                resume_json = json.load(f)
        elif type(json_filepath) is dict:
            resume_json = json_filepath
        else:
            msg = "{} is not a valid type, type accepted are <class 'str'>\n\
                    or <class 'dict'>.".format(type(json_filepath))
            logging.error(msg)
            raise TypeError
    except IOError:
        msg = "Json file could not be loaded. Perhaps file path: \n\
      [{}] is incorrect".format(json_filepath)
        logging.error(msg)
        raise
    except ValueError:
        logging.error(
            "Json file could not be loaded. The syntax is not valid.")
        raise
    else:
        resume = Resume(resume_json)
        try:
            resume.validate()
        except InvalidResumeError:
            msg = "The json resume don't respect standard. Check: \n\
      https://jsonresume.org/schema/."
            logging.error(msg)
            raise
        else:
            logging.info("JSON parsing done.")
            return JsonObject(resume_json)
