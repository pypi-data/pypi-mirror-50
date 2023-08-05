import os
import glob
import json
from absl import logging
from typing import Tuple, List, Dict

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    from aisthetics.utils.utils import calc_mean_score, calc_sd_score, save_json
    from aisthetics.handlers.model_builder import Nima
    from aisthetics.handlers.data_generator import TestDataGenerator

logging._warn_preinit_stderr = 0
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def image_file_to_json(img_path: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Convert a path to an image into a tuple (dir, [file])

    :param img_path: path to file
    :return: tuple (dir, list(dict)) where the list has only one element, being the name of the file without
    extension
    """
    img_dir = os.path.dirname(img_path)
    img_id = os.path.basename(img_path).split('.')[0]

    return img_dir, [{'image_id': img_id}]


def image_dir_to_json(img_dir, img_type='jpg') -> List[Dict[str, str]]:
    """
    Given a path to a directory, return a list of files of the specified extension

    :param img_dir: path to directory containing images
    :param img_type: extension of images to collect
    :return: tuple (dir, list(dict)), where the list contain all the images of the specified img_type
    """
    img_paths = glob.glob(os.path.join(img_dir, '*.'+img_type))

    samples = []
    for img_path in img_paths:
        img_id = os.path.basename(img_path).split('.')[0]
        samples.append({'image_id': img_id})

    return samples


def predict(model, data_generator) -> List:
    """
    Return a list of predictions from a model for a set of input data

    :param model: model that is used for predictions
    :type model: keras.models.Model
    :param data_generator: sequence of data to predict
    :type data_generator: keras.utils.Sequence
    :return: list of predictions
    """
    return model.predict_generator(data_generator, workers=8, use_multiprocessing=True, verbose=1)


def prediction_summary(base_model_name: str, weights_file: str, image_source: str, predictions_file: str = None,
                       img_format='jpg') -> None:
    """
    Wrapper function that receives all the necessary parameters for scoring given images and outputs the result on
    stdout and in a file

    :param base_model_name: name of the CNN to use (MobileNet, ResNet...)
    :param weights_file: file containing the weights of the trained model
    :param image_source: local file of the image to predict
    :param predictions_file: file to store the results
    :param img_format: format of the image to score
    :return: nothing
    """

    import tensorflow as tf
    logging.set_verbosity(logging.ERROR)

    # load samples
    if os.path.isfile(image_source):
        image_dir, samples = image_file_to_json(image_source)
    else:
        image_dir = image_source
        samples = image_dir_to_json(image_dir, img_type=img_format)

    # build model and load weights
    nima = Nima(base_model_name, weights=None)
    nima.build()
    nima.nima_model.load_weights(weights_file)

    # initialize data generator
    data_generator = TestDataGenerator(samples, image_dir, 64, 10, nima.preprocessing_function(),
                                       img_format=img_format)

    # get predictions
    predictions = predict(nima.nima_model, data_generator)

    # calc mean scores and add to samples
    for i, sample in enumerate(samples):
        sample['predictions'] = predictions[i].tolist()
        sample['mean_score_prediction'] = calc_mean_score(predictions[i])
        sample['sd_score_prediction'] = calc_sd_score(predictions[i])

    print(json.dumps(samples, indent=2))

    if predictions_file is not None:
        save_json(samples, predictions_file)
