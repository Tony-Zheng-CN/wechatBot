import json
import base64
import random

import requests
import time
import os
import logging

logger_sd = logging.getLogger('sd')
logger_sd_formatter = logging.Formatter("[%(levelname)s][%(name)s]%(message)s")


def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def save_encoded_image(b64_image: str, output_path: str):
    # 确保缓存目录存在
    cache_dir = os.path.dirname(output_path)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))


def sd_api_t2i(prompt, sd_api_url='http://localhost:7860'):
    txt2img_url = f'{sd_api_url}/sdapi/v1/txt2img'
    logger_sd.info(f"SD draw.Post to {txt2img_url}.Prompt: {prompt}")
    data = {'prompt': prompt,
            'negative_prompt': '',
            'sampler_index': 'DPM++ SDE',
            'seed': int(time.time()),
            'steps': random.randint(20, 30),
            'width': random.randint(512, 1024),
            'height': random.randint(512, 1024),
            'cfg_scale': 8}

    try:
        response = submit_post(txt2img_url, data)
        # 检查HTTP响应状态
        if response.status_code != 200:
            logger_sd.error(f"SD API request failed with status code: {response.status_code}")
            return None

        response_json = response.json()

        # 检查响应是否包含图像数据
        if 'images' not in response_json or not response_json['images']:
            logger_sd.error("SD API response does not contain valid image data")
            return None

        save_image_path = os.path.join(os.getcwd(), 'cache', f"sd_{int(time.time())}.png")
        save_encoded_image(response_json['images'][0], save_image_path)
        logger_sd.info(f"SD draw.Save to {save_image_path}")
        return save_image_path

    except requests.exceptions.RequestException as e:
        logger_sd.error(f"SD API request error: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logger_sd.error(f"SD API response JSON decode error: {str(e)}")
        return None
    except Exception as e:
        logger_sd.error(f"SD API unexpected error: {str(e)}")
        return None


if __name__ == '__main__':
    sd_api_t2i(prompt='a dog wearing a hat', sd_api_url='http://192.168.31.229:8000')
