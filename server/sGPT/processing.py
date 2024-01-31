import os
from pickle import load
from uu import Error
from numpy import argmax
from functools import lru_cache

from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import preprocess_input
from keras.models import Model, model_from_json

# pre-define the max sequence length (from training)
MAX_LENGTH = 34

# paths are relative to the directory where main file is located
MODEL_URL = os.path.abspath("./sGPT/model/model_9.h5")
MODEL_JSON_URL = os.path.abspath("./sGPT/model/model.json")
TOKENIZER_URL = os.path.abspath("./sGPT/model/tokenizer.pkl")


@lru_cache
def setup_caption_generator():
    model, tokenizer = None, None

    # load the tokenizer
    with open(TOKENIZER_URL, "rb") as tokenizer_file:
        tokenizer = load(tokenizer_file)

    # opening and store file in a variable
    with open(MODEL_JSON_URL, "r", encoding="utf-8") as json_file:
        loaded_model_json = json_file.read()

    # use Keras model_from_json to make a loaded model
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    if loaded_model is not None:
        loaded_model.load_weights(MODEL_URL)
        model = loaded_model

    return (model, tokenizer)


# extract features from each photo in the directory
def extract_features(filename: str):
    # load the model
    model = VGG16()
    # opening and store file in a variable
    # re-structure the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    # load the photo
    image = load_img(filename, target_size=(224, 224))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    # get features
    feature = model.predict(image, verbose="0")
    return feature


# map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


# generate a description for an image
def generate_desc(model, tokenizer, photo, max_length: int):
    # seed the generation process
    in_text = "startseq"
    # iterate over the whole length of the sequence
    for _ in range(max_length):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo, sequence], verbose=0)
        # convert probability to integer
        yhat = argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += " " + word
        # stop if we predict the end of the sequence
        if word == "endseq":
            break

    return in_text


def generate_caption(image_path: str) -> str:
    if image_path == "" or not os.path.exists(image_path):
        raise ValueError("path must be of a valid file in file system")

    model, tokenizer = setup_caption_generator()

    if not model or not tokenizer:
        raise Error("could not initialize machine learning model")

    # load and prepare the photograph
    photo = extract_features(image_path)

    # generate description
    description = generate_desc(model, tokenizer, photo, MAX_LENGTH)

    return description