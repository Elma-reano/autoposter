#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 08:59:42 2025

@author: marianoluna
"""

import requests
from verboser import verboser
import base64

IMGUR_UPLOAD_URL = lambda: "https://api.imgur.com/3/upload"
IMGUR_DELETE_URL = lambda delete_hash: f"https://api.imgur.com/3/image/{delete_hash}"

@verboser("imgur_upload")
def imgur_upload(*, 
                 client_id: str,
                 image_path: str) -> tuple:
    
    url = IMGUR_UPLOAD_URL()
    headers = {
            "Authorization": f"Client-ID {client_id}"
        }
    files = {
            "image": open(image_path, 'rb')
        }
    
    response = requests.post(url, headers= headers, files= files)
    response_dict = dict(response.json())
    
    image_url = response_dict['data']['link']
    image_delete_hash = response_dict['data']['deletehash']
    
    return (image_url, image_delete_hash)


@verboser("imgur_upload_video")
def imgur_upload_video(*,
                       client_id: str,
                       video_path: str) -> tuple:
    
    url = IMGUR_UPLOAD_URL()
    headers = {
            "Authorization": f"Client-ID {client_id}"
        }
    
    with open(video_path, 'rb') as file:
        video = file.read()
    
    data = {
        "video": base64.b64encode(video).decode("ascii")
        }
    
    response = requests.post(url, headers= headers, data= data)
    response_dict = dict(response.json())
    
    video_url = response_dict['data']['link']
    video_delete_hash = response_dict['data']['deletehash']
    
    return (video_url, video_delete_hash)


@verboser("imgur_delete")
def imgur_delete(*,
                 client_id: str,
                 delete_hash: str) -> None:
    
    url = IMGUR_DELETE_URL(delete_hash)
    headers = {
            "Authorization": f"Client-ID {client_id}"
        }
    
    response = requests.delete(url, headers= headers)
    
    print(response.json())
    
    return



