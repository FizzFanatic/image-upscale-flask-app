from flask import session, redirect, url_for, request
import requests
import os

API_KEY = os.getenv("LMWR_API_TOKEN")

def upscale_image():
    if 'image' not in request.files:
        return "Файл не загружен", 400

    image_file = request.files['image']

    url = "https://api.limewire.com/api/image/upscaling"
    headers = {
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    files = {
        'image': image_file
    }
    data = {
        'upscale_factor': '2'
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    response_data = response.json()

    if response.status_code == 200 and response_data.get('status') == 'COMPLETED':
        asset_url = response_data['data'][0]['asset_url']
        credits_used = response_data.get('credits_used')
        credits_remaining = response_data.get('credits_remaining')
        asset_id = response_data['data'][0]['asset_id']

        session['image_url'] = asset_url
        session['credits_used'] = credits_used
        session['credits_remaining'] = credits_remaining
        session['asset_id'] = asset_id

        return redirect(url_for('result'))
    else:
        return f"Ошибка при улучшении изображения: {response_data}", 400