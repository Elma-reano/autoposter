import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

import asyncio

from file_operator import get_txt_file_contents

CLOUD_NAME = "daoucjdlp"
API_KEY = get_txt_file_contents("Keys/cloudinary_api_key.txt")
API_SECRET = get_txt_file_contents("Keys/cloudinary_secret.txt")

# Configuration
cloudinary.config(
    cloud_name = CLOUD_NAME,
    api_key = API_KEY,
    api_secret = API_SECRET
)

def upload_image(image_path: str, folder: str = "marimomos") -> tuple[str, str]:
    result = cloudinary.uploader.upload(image_path, folder= folder)
    return (result['secure_url'], result['public_id'])

def delete_image(public_id: str) -> bool:
    result = cloudinary.uploader.destroy(public_id)
    if result['result'] == 'not found':
        raise ValueError(f"Image with public_id '{public_id}' not found.")
    if result['result'] != 'ok':
        raise Exception(f"Failed to delete image with public_id '{public_id}'. Result: {result}")
    return True

# upload_result = cloudinary.uploader.upload("media/test1.png", folder= "marimomos")
# print(upload_result)

# destroy_result = cloudinary.uploader.destroy("marimomos/dsafoi235gikm", folder= "marimomos")
# print(destroy_result)

def upload_video(video_path: str, folder: str = "marimomos") -> tuple[str, str]:
    result = cloudinary.uploader.upload(video_path, resource_type= "video", folder= folder)
    return (result['secure_url'], result['public_id'])

def delete_video(public_id: str) -> bool:
    result = cloudinary.uploader.destroy(public_id, resource_type= "video")
    if result['result'] == 'not found':
        raise ValueError(f"Video with public_id '{public_id}' not found.")
    if result['result'] != 'ok':
        raise Exception(f"Failed to delete video with public_id '{public_id}'. Result: {result}")
    return True

# upload_video_result = cloudinary.uploader.upload("media/test_video.mov", resource_type= "video", folder= "marimomos")
# print(upload_video_result)

# delete_video_result = cloudinary.uploader.destroy("marimomos/r8vfcsotxeskyuclmmja", resource_type= "video")
# print(delete_video_result)

# Vibecoded
async def upload_image_async(sem: asyncio.Semaphore, img, folder: str):
    loop = asyncio.get_event_loop()
    async with sem:
        return await loop.run_in_executor(None, upload_image, img, folder)

async def delete_image_async(sem: asyncio.Semaphore, public_id: str):
    loop = asyncio.get_event_loop()
    async with sem:
        return await loop.run_in_executor(None, delete_image, public_id)

if __name__ == "__main__":

    image_url, img_public_id = upload_image("media/test1.png", folder= "testDaCode")

    print(f"{image_url=}\n{img_public_id=}")
    input("Press enter to continue...")

    delete_image_result = delete_image(public_id=img_public_id)
    print("Success" if delete_image_result else "Error")
    input("Press enter to continue...")

    video_url, video_public_id = upload_video("media/test_video.mov", folder= "testDaCode")
    print(f"{video_url=}\n{video_public_id=}")
    input("Press enter to continue...")

    delete_video_result = delete_video(public_id=video_public_id)
    print("Success" if delete_video_result else "Error")