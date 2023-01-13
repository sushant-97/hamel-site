# AUTOGENERATED! DO NOT EDIT! File to edit: index.ipynb.

# %% auto 0
__all__ = ['app', 'items', 'load_model', 'pred', 'startup_event', 'health', 'Sentence', 'predict']

# %% index.ipynb 3
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List
import tensorflow as tf
import numpy as np

def load_model(model_path='/home/hamel/hamel/notes/serving/tfserving/model/1'):
    "Load the SavedModel Object."
    sm = tf.saved_model.load(model_path)
    return sm.signatures["serving_default"] # this is the default signature when you save a model

# %% index.ipynb 4
def pred(model: tf.saved_model, data:np.ndarray, pred_layer_nm='dense_3'):
    """
    Make a prediction from a SavedModel Object.  `pred_layer_nm` is the last layer that emits logits.
    
    https://www.tensorflow.org/guide/saved_model
    """
    data = tf.convert_to_tensor(data, dtype='int32')
    preds = model(data)
    return preds[pred_layer_nm].numpy().tolist()

# %% index.ipynb 10
app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    "Load the model on startup https://fastapi.tiangolo.com/advanced/events/"
    items['model'] = load_model()


@app.get("/")
def health(status_code=status.HTTP_200_OK):
    "A health-check endpoint"
    return 'Ok'

# %% index.ipynb 12
class Sentence(BaseModel):
    tokens: List[List[int]]

@app.post("/predict")
def predict(data:Sentence, status_code=status.HTTP_200_OK):
    preds = pred(items['model'], data.tokens)
    return preds
