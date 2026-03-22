import os
import time

from notificator import notify

from cache_code import cache_handler
from file_operator import get_txt_file_contents
from cloudinary_api import (
    upload_video as cloudinary_upload_video,
    delete_video as cloudinary_delete_video
)
from graph_api import create_media_container, publish_media

global DEBUG
DEBUG = False

# Carga las keys y los paths de las fotos
IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")
MEDIA_FOLDER_PREFIX = "media/"
VIDEO_PATH = f"{MEDIA_FOLDER_PREFIX}test_video.mov"

DEFAULT_CAPTION = "AutoMarimomosBot: Marimomos. Atte: AutoMarimomosBot #memes #momos #marimomos #shitpost #funny #humor #memesdaily"
SLEEP_BEFORE_PUBLISHING = 20
SLEEP_BETWEEN_TRIES = 2


def main_video():

    video_url, video_public_id = upload_video_to_cloudinary(video_path= VIDEO_PATH,
                                    folder= "marimomos"
                                    )

    # video_url, video_delete_hash = upload_video_to_imgur(video_path= VIDEO_PATH,
    #                                 client_id= IMGUR_CLIENT_ID
    #                                 )
    
    container_id = create_video_container(video_url= video_url,
                                          access_token= ACCESS_TOKEN,
                                          caption= DEFAULT_CAPTION
                                          )
    
    # Sleep before publishing to ensure that the media container is ready
    print(f"Sleeping for {SLEEP_BEFORE_PUBLISHING} seconds before publishing...")
    time.sleep(SLEEP_BEFORE_PUBLISHING)
    
    publish_video_result = publish_video(media_container_id= container_id,
                                        access_token= ACCESS_TOKEN,
                                        sleep_between_tries= SLEEP_BETWEEN_TRIES
                                        )

    print(f"Publish video result: {publish_video_result} ----------------------")
    
    if publish_video_result:
        delete_result = delete_video_from_cloudinary(public_id= video_public_id)
        notify("Done")
        return
    
    notify("Failed to publish video. Check logs for details.")
    # TODO: Añadir una capa de validacion de cada paso
    return

# @cache_handler()
# def upload_video_to_imgur(video_path: str,
#                           client_id: str) -> tuple[str, str]:
#     """
#     Uploads a video to Imgur and returns the video URL and delete hash.
#     """
#     return imgur_upload_video(client_id= client_id,
#                               video_path= video_path)

# A life built on the suffering of others is just a gold-plated cage 
# - Un analisis de One Piece en TikTok que vi mientras me hacia wey de seguir codeando esto

@cache_handler()
def upload_video_to_cloudinary(video_path: str,
                             folder: str) -> tuple[str, str]:
    """
    Uploads a video to Cloudinary and returns the video URL and public ID.
    """
    return cloudinary_upload_video(video_path= video_path,
                                  folder= folder)

@cache_handler()
def create_video_container(video_url: str,
                           access_token: str,
                           caption: str | None = None) -> str:
    """
    Creates a media container for a video on Instagram and returns the container ID.
    """
    return create_media_container(access_token= access_token,
                                  media_url= video_url,
                                  caption= caption,
                                  is_video= True,
                                  multiple= False)

@cache_handler()
def publish_video(media_container_id: str,
                  access_token: str,
                  sleep_between_tries: int | float = 3
                  ) -> str | None:
    """
    Publishes a video on Instagram and returns the media ID.
    """
    return publish_media(access_token= access_token,
                         media_id= media_container_id,
                         sleep_between_tries= sleep_between_tries)

# @cache_handler(expect_result=False)
# def delete_video_from_imgur(delete_hash: str,
#                             client_id: str) -> None:
#     """
#     Deletes a video from Imgur using the delete hash.
#     """
#     return imgur_delete(client_id= client_id,
#                         delete_hash= delete_hash)

@cache_handler()
def delete_video_from_cloudinary(public_id: str) -> bool:
    """
    Deletes a video from Cloudinary using the public ID.
    """
    return cloudinary_delete_video(public_id= public_id)


if __name__ == "__main__":
    notify("Starting")
    main_video()