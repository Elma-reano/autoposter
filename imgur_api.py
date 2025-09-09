#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 08:59:42 2025

@author: marianoluna
"""

import aiohttp
import asyncio
import requests
from verboser import verboser
import base64

def IMGUR_UPLOAD_URL():
    return "https://api.imgur.com/3/upload"
def IMGUR_DELETE_URL(delete_hash: str):
    return f"https://api.imgur.com/3/image/{delete_hash}"

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

@verboser("imgur_upload_async")
async def imgur_upload_async(*, 
                             client_id: str,
                             image_path: str) -> tuple:
    url = IMGUR_UPLOAD_URL()
    headers = {"Authorization": f"Client-ID {client_id}"}
    files = {"image": open(image_path, 'rb')}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers= headers, data= files) as response:
            response_dict = await response.json()
            # print(response_dict)
            response_dict = dict(response_dict)

    # print(response_dict)
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

# TODO
# @verboser("imgur_upload_video_async")
# async def imgur_upload_video_async(*,
#                                    client_id: str,
#                                    video_path: str) -> tuple:
#      lista.append(await imgur_upload_video(client_id= client_id, video_path= video_path))
#      return


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

@verboser("imgur_delete_async")
async def imgur_delete_async(*,
                             client_id: str,
                             delete_hash: str) -> None:
    url = IMGUR_DELETE_URL(delete_hash)
    headers = {"Authorization": f"Client-ID {client_id}"}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers= headers) as response:
            print(await response.json())
    return

