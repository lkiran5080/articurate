
import os
import secrets
from flask import url_for, current_app

from PIL import Image


def save_picture(form_picture):

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    # resizing image using Pillow
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)  # actually saving image data

    return picture_fn
