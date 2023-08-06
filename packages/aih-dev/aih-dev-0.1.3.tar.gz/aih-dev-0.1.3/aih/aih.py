import jwt
import requests
from requests.auth import AuthBase
import json
from aih_package.utils.face_utils import *


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
        self.__url = "http://aih-api.vmod1.com"
        # self.__url = "http://localhost:5000"

    def detect_face(self, file_binary):
        try:
            face = get_face_b2b(file_binary)
            if not face:
                return {
                    "message": "Face not found"
                }
            # path = f'{self.__url}/rekognition/faces'
            path = f'{self.__url}/sagemaker/faces'
            res = requests.post(path, files={'file': file_binary},
                                auth=TokenAuth(self.__token))
            return res.json()
        except Exception as e:
            raise e

    # def update_face_info(self, fullname, face_id):
    #     try:
    #         path = f'{self.__url}/rekognition/faces/{face_id}'
    #         res = requests.patch(path, data={"fullname": fullname}, auth=TokenAuth(self.__token))
    #         return res.json()
    #     except Exception as e:
    #         raise e

    def train_image(self, fullname, images):
        try:
            path = f'{self.__url}/sagemaker/faces'
            crop_faces = map(lambda image: get_face_b2b(image), images)
            files = map(lambda image: ('file', image), crop_faces)
            res = requests.patch(path, data={"fullname": fullname}, files=files, auth=TokenAuth(self.__token))
            # print(res)
            return res.json()
        except Exception as e:
            raise e

    def train_only_face(self, fullname, images):
        try:
            path = f'{self.__url}/sagemaker/faces'
            crop_faces = map(lambda image: normalize_image(image), images)
            files = map(lambda image: ('file', image), crop_faces)
            res = requests.patch(path, data={"fullname": fullname}, files=files, auth=TokenAuth(self.__token))
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
