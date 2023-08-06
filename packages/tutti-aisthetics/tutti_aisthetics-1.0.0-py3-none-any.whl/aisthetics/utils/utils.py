import os
import json
import keras
import numpy as np
from typing import List


def load_json(file_path):
    with open(file_path, 'r') as fd:
        return json.load(fd)


def save_json(data, target_file):
    with open(target_file, 'w') as fd:
        json.dump(data, fd, indent=2, sort_keys=True)


def random_crop(img, crop_dims: List[int]):
    """ Crop an image randomly into a given dimensions """
    h, w = img.shape[0], img.shape[1]
    ch, cw = crop_dims[0], crop_dims[1]
    assert h >= ch, 'image height is less than crop height'
    assert w >= cw, 'image width is less than crop width'
    x = np.random.randint(0, w - cw + 1)
    y = np.random.randint(0, h - ch + 1)
    return img[y:(y+ch), x:(x+cw), :]


def random_horizontal_flip(img):
    """ Apply a horizontal flip to an image with a 50% probability """
    assert len(img.shape) == 3, 'input tensor must have 3 dimensions (height, width, channels)'
    assert img.shape[2] == 3, 'image not in channels last format'
    if np.random.random() < 0.5:
        img = img.swapaxes(1, 0)
        img = img[::-1, ...]
        img = img.swapaxes(0, 1)
    return img


def load_image(img_file, target_size):
    """ Load an image from a file and return it as an array """
    return np.asarray(keras.preprocessing.image.load_img(img_file, target_size=target_size))


def normalize_labels(labels):
    """ Normalize a list by dividing each element by the total sum """
    labels_np = np.array(labels)
    return labels_np / labels_np.sum()


def calc_mean_score(score_dist):
    """ Compute the mean from a histogram with values from 1 to 10 """
    score_dist = normalize_labels(score_dist)
    return (score_dist*np.arange(1, 11)).sum()


def calc_sd_score(score_dist):
    """ Compute the standard deviation from a histogram with values from 1 to 10 """
    mean = calc_mean_score(score_dist)
    score_dist = normalize_labels(score_dist)
    return np.sqrt((np.square(np.arange(1, 11) - mean) * score_dist).sum())


def ensure_dir_exists(dir):
    """ Checks if a directory exists """
    if not os.path.exists(dir):
        os.makedirs(dir)
