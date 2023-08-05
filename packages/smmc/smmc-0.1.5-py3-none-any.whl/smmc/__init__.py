import json
import base64
import os.path


class SMMC(object):
    def __init__(self, message_limiter=["---BEGIN-SCANNERMANAGER-MESSAGE---", "---END-SCANNERMANAGER-MESSAGE---"]):
        """
        Scanner Manager Message Coder is a library offering functions to set Atlas Scan Status and send Scan Output via StdOut.
        When writing scripts for Atlas Docker Containers make sure you never write something to StdOut because it's the standard
        way to send messages to Atlas.

        --Arguments--
        Optional:
        message_limiter (List[str]): Limiter strings used to mark begin and end of ATLAS message
        """
        self._message_limiter = message_limiter
        self._nr_of_files = 0

    def send_status(self, status, details={}):
        """send a status update

        --Arguments--
        Required:
        status [str]:   new status, currently following are valid (preparing, running, failed)

        Optional:
        details [dict]: details for the further description of the status
        """
        message = {
            "message_type": "status", "payload": {"status": status,
                                                  "details": details}
        }
        self.__send_message(message)

    def __send_output(self, filename, encoding, payload, description=None):
        """send an output file in given encoding"""
        message = {"message_type": "output", "encoding": encoding, "filename": filename,
                   "payload": payload}

        if description:
            message["description"] = description

        self._nr_of_files += 1
        self.__send_message(message)

    def send_output_string(self, filename, payload, description=None):
        """send a string as output file

        --Arguments--
        Required:
        filename [str]: name of the output file
        payload [str]:  string that should be content of the file

        Optional:
        description [str]: description for the file if its not clear how to interpret the content
        """
        if not isinstance(payload, str):
            raise Exception("payload is no valid object of type string")
        self.__send_output(filename=filename, encoding="plaintext",
                           payload=payload, description=description)

    def send_output_json(self, filename, payload, description=None):
        """send a json as output

         --Arguments--
        Required:
        filename [str]: name of the output file
        payload [json]:  json (dict) that should be content of the file

        Optional:
        description [str]: description for the file if its not clear how to interpret the content
        """
        self.__send_output(filename=filename, encoding="json",
                           payload=payload, description=description)

    def send_output_file(self, path_to_file, filename=None, description=None):
        """send a file as output

        --Arguments--
        Required:
        path_to_file [str]:  path to the file to be send

        Optional:
        filename [str]: name of the output file
        description [str]: description for the file if its not clear how to interpret the content
        """
        if not os.path.isfile(path_to_file):
            raise Exception("File is not existent")
        with open(path_to_file, "rb") as f:
            file_bytes = f.read()
        payload = base64.b64encode(file_bytes).decode()
        original_filename = os.path.basename(path_to_file)
        if not filename:
            filename = original_filename
        self.__send_output(filename=filename, payload=payload,
                           description=description, encoding="base64")

    def __send_message(self, message):
        """send message encoded as json and having start and end limiter """
        message_json = json.dumps(message)
        print(self._message_limiter[0])
        print(message_json)
        print(self._message_limiter[1])

    def get_nr_of_output_files(self):
        """return the number of send output files"""
        return self._nr_of_files
