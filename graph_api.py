#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 12:51:34 2025

@author: marianoluna
"""

import requests
import asyncio
import aiohttp
from verboser import verboser

GRAPH_API_VERSION = "22.0"
with open("Keys/ig_acc_num.txt", "r") as file:
    IG_ACC_NUMBER = file.read().strip()

LONG_TERM_ACCESS_TOKEN_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"
PAGE_ACCESS_TOKEN_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/accounts"
CREATE_MEDIA_CONTAINER_URL = f"https://graph.facebook.com/v{GRAPH_API_VERSION}/{IG_ACC_NUMBER}/media"
PUBLISH_MEDIA_URL = f"https://graph.facebook.com/v{GRAPH_API_VERSION}/{IG_ACC_NUMBER}/media_publish"

@verboser("Get new long term access token")
def get_new_long_term_access_token(*,
                                   client_id: str,
                                   client_secret: str,
                                   current_access_token: str) -> str:
    
    url = LONG_TERM_ACCESS_TOKEN_URL
    
    parameters = {
        'grant_type': 'fb_exchange_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'fb_exchange_token': current_access_token
        }
    
    response = requests.get(url, params= parameters)
    response_dict = response.json()
    print(response_dict)
    
    return response_dict['access_token']

@verboser("Get ig page access token")
def get_ig_page_access_token(*,
                             user_access_token: str) -> str:
    
    url = PAGE_ACCESS_TOKEN_URL
    parameters = {
            'access_token': user_access_token
        }
    
    response = requests.get(url, params= parameters)
    response_dict = dict(response.json())
    
    print(response_dict)
    
    return response_dict['data']['access_token']
    

@verboser("Create media container")
def create_media_container(*,
                           access_token: str,
                           media_url: str,
                           caption: str = None,
                           is_video: bool= False,
                           multiple: bool = False) -> str:
    
    url = CREATE_MEDIA_CONTAINER_URL
    parameters = {
            'access_token': access_token
        }
    if is_video:
        parameters['video_url'] = media_url
        parameters['media_type'] = "REELS"
    else:
        parameters['image_url'] = media_url 
    if not multiple and caption:
        parameters['caption'] = caption  
    if multiple:
        parameters['is_carousel_item'] = "true"
             
    response = requests.post(url, params= parameters)
    response_dict = dict(response.json())
    
    print(response_dict)
    
    return response_dict['id']

@verboser("Create media container async", trace_variables= ['response'])
async def create_media_container_async(*,
                                    access_token: str,
                                    media_url: str,
                                    caption: str = None,
                                    is_video: bool= False,
                                    multiple: bool = False) -> str:
    url = CREATE_MEDIA_CONTAINER_URL
    parameters = {'access_token': access_token}
    if is_video:
        parameters['video_url'] = media_url
        parameters['media_type'] = "REELS"
    else:
        parameters['image_url'] = media_url   
    if not multiple and caption:
        parameters['caption'] = caption
    if multiple:
        parameters['is_carousel_item'] = "true"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params= parameters) as response:
            response_dict = await response.json()
            response_dict = dict(response_dict)
            # print(response_dict)
            return response_dict['id']

@verboser("Create carousel")
def create_media_carousel(*,
                          access_token: str,
                          children: list,
                          caption: str = None) -> str:
    
    url = CREATE_MEDIA_CONTAINER_URL
    parameters = {
            'access_token': access_token,
            'media_type': 'CAROUSEL',
            'children': children,
            'caption': caption
        }
    
    response = requests.post(url, json= parameters)
    print(response.url)
    response_dict = dict(response.json())
    
    print(response_dict)
    
    return response_dict['id']
    
    
@verboser("Publish media")
def publish_media(*,
                  access_token: str,
                  media_id: str) -> None:
    
    url = PUBLISH_MEDIA_URL
    parameters = {
            'access_token': access_token,
            'creation_id': media_id
        }
    
    response = requests.post(url, params= parameters)
    response_dict = dict(response.json())
    
    print(response_dict)
    
    return response_dict['id']

    