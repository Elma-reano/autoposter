import os

from notificator import notify

from cache_code import cache_handler
from file_operator import get_txt_file_contents
from imgur_api import imgur_upload_video, imgur_delete
from graph_api import create_media_container, publish_media

global DEBUG
DEBUG = False

# Carga las keys y los paths de las fotos
IMGUR_CLIENT_ID = get_txt_file_contents("Keys/imgur_client_id.txt")
ACCESS_TOKEN = get_txt_file_contents("Keys/access_key.txt")
MEDIA_FOLDER_PREFIX = "media/"
VIDEO_PATH = f"{MEDIA_FOLDER_PREFIX}test_video.mov"

DEFAULT_CAPTION = "AutoMarimomosBot: Marimomos. Atte: AutoMarimomosBot #memes #momos #marimomos #shitpost #funny #humor #memesdaily"
SLEEP_BETWEEN_TRIES = 10


def main():

    video_url, video_delete_hash = upload_video_to_imgur(video_path= VIDEO_PATH,
                                    client_id= IMGUR_CLIENT_ID
                                    )
    
    container_id = create_video_container(video_url= video_url,
                                          access_token= ACCESS_TOKEN,
                                          caption= DEFAULT_CAPTION
                                          )
    
    publish_video(media_container_id= container_id,
                  access_token= ACCESS_TOKEN,
                  sleep_between_tries= SLEEP_BETWEEN_TRIES
                  )
    
    delete_video_from_imgur(delete_hash= video_delete_hash,
                            client_id= IMGUR_CLIENT_ID
                            )

    notify("Done")
    return

@cache_handler()
def upload_video_to_imgur(video_path: str,
                          client_id: str) -> tuple[str, str]:
    """
    Uploads a video to Imgur and returns the video URL and delete hash.
    """
    return imgur_upload_video(client_id= client_id,
                              video_path= video_path)

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

@cache_handler(expect_result=False)
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

@cache_handler(expect_result=False)
def delete_video_from_imgur(delete_hash: str,
                            client_id: str) -> None:
    """
    Deletes a video from Imgur using the delete hash.
    """
    return imgur_delete(client_id= client_id,
                        delete_hash= delete_hash)


if __name__ == "__main__":
    notify("Starting")
    main()