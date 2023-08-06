import cv2
import os
import numpy as np


def normalize_image(data):
    img = read_binary(data)
    face = resize_image(img, 160)
    result = to_binary(face)
    return result


def get_face_b2b(data):
    img = read_binary(data)
    face = get_face(img)
    if face is None:
        return None
    face = resize_image(face, 160)
    result = to_binary(face)
    return result


def read_binary(data):
    nparr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return img


def get_face(img):
    faces = get_faces(img)
    face = get_max_size_image(faces)
    return face


def get_faces(img):
    result = []
    # img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('{}/utils/haarcascade_frontalface_default.xml'.format(os.getcwd()))

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        if not x:
            continue
        crop_img = img[y:y + h, x:x + w]
        result.append(crop_img)
    return result


def get_max_size_image(images):
    if not len(images):
        return None
    return max(images, key=lambda image: image.size)


def resize_image(image, size):
    dim = (size, size)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image


def cv2_bgr_to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def save_image(image, path):
    cv2.imwrite(path, image)


def to_binary(img):
    img_str = cv2.imencode('.png', img)[1].tostring()
    return img_str



