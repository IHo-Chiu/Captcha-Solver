
import os
import sys
import time

from typing import Union
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from minio import Minio

import argparse
import torch
from PIL import Image
import string

from strhub.data.module import SceneTextDataModule
from strhub.models.utils import load_from_checkpoint, parse_model_args


device = 'cuda'
kwargs = {}
charset_test = string.digits + string.ascii_uppercase
kwargs.update({'charset_test': charset_test})
print(f'Additional keyword arguments: {kwargs}')

checkpoint = 'outputs/parseq/combined/checkpoints/epoch=196-step=104472-val_accuracy=100.0000-val_NED=100.0000.ckpt'
model = load_from_checkpoint(checkpoint, **kwargs).eval().to(device)
img_transform = SceneTextDataModule.get_transform(model.hparams.img_size)

# minio setup
class MINIO_CONFIG:
    MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', '??.???.??.??')
    MINIO_PORT = os.environ.get('MINIO_PORT', '?????')
    MINIO_URI = '%s:%s' % (MINIO_ENDPOINT, MINIO_PORT)
    MINIO_ACCESSKEY = os.environ.get('MINIO_ACCESSKEY', '???????????????????????')
    MINIO_SECRETKEY = os.environ.get('MINIO_SECRETKEY', '??????????????????????????????')

config = MINIO_CONFIG()
app = FastAPI()


client = Minio(
    config.MINIO_URI,
    access_key=config.MINIO_ACCESSKEY,
    secret_key=config.MINIO_SECRETKEY,
    secure=False,
)

class CaptchaRequest(BaseModel):
    bucket_minio: str = None
    file_minio: str = None
    

@torch.inference_mode()
@app.post("/captcha/")
async def captcha(req: CaptchaRequest):

    LOG_DIR = f'api_cache'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    minio_path = f'{LOG_DIR}/{req.file_minio}'
    client.fget_object(
        req.bucket_minio, req.file_minio, minio_path
    )
    
    image = Image.open(minio_path).convert('RGB')
    image = img_transform(image).unsqueeze(0).to(device)

    p = model(image).softmax(-1)
    pred, p = model.tokenizer.decode(p)

    print(f'{minio_path}: {pred[0]}')

    return {
        "predict": {
            'file': req.file_minio,
            'results': pred[0],
            'success': True
        }
    }

    
if __name__ == '__main__':
    uvicorn.run('run_fastapi:app', host='0.0.0.0', port=10082, reload=True)