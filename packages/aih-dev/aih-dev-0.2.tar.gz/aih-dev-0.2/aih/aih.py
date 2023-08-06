import jwt
import requests
from requests.auth import AuthBase
# from ..utils.face_utils import *


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['Authorization'] = self.token
        return r


class AIH:
    def __init__(self, app_id, secret_key):
        self.__secret = 'Iz9uaoZtSV2TBO_M5m4f4Q'
        self.app_id = app_id
        self.__token = jwt.encode({'AppId': self.app_id, 'SecretKey': secret_key}, self.__secret)
        self.__url = "http://aih-apidev.vmod1.com"
        # self.__url = "http://localhost:5000"

    def detect_face(self, file_binary):
        try:
            path = f'{self.__url}/sagemaker/faces'
            res = requests.post(path, files={'file': file_binary},
                                auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    def detect_cropped_face(self, file_binary):
        try:
            path = f'{self.__url}/sagemaker/faces?only_face=true'
            res = requests.post(path, files={'file': file_binary},
                                auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    def train_face(self, fullname, images):
        try:
            path = f'{self.__url}/sagemaker/faces'
            files = map(lambda image: ('file', image), images)
            res = requests.patch(path, data={"fullname": fullname}, files=files, auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    def train_cropped_face(self, fullname, images):
        try:
            path = f'{self.__url}/sagemaker/faces?only_face=true'
            files = map(lambda image: ('file', image), images)
            res = requests.patch(path, data={"fullname": fullname}, files=files, auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    def list_models(self):
        try:
            path = f'{self.__url}/sagemaker/models'
            res = requests.get(path, auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    def get_model(self, model_id):
        try:
            path = f'{self.__url}/sagemaker/models/{model_id}'
            res = requests.get(path, auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    def speak(self, text):
        try:
            path = f'{self.__url}/polly/speak'
            res = requests.post(path, data={"text": text}, auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e
