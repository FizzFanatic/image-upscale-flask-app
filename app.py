from flask import Flask, render_template, session
from modules.upscaleimage import upscale_image
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY_APP")

@app.route('/')
def home():
    return render_template('upscaleimage.html')

@app.route('/upscale_image', methods=['POST'])
def upscale_image_route():
    return upscale_image()

@app.route('/result')
def result():
    image_url = session.get('image_url')
    credits_used = session.get('credits_used')
    credits_remaining = session.get('credits_remaining')
    asset_id = session.get('asset_id')

    if not image_url:
        return "Изображение не найдено", 400

    return render_template(
        'result.html',
        image_url=image_url,
        credits_used=credits_used,
        credits_remaining=credits_remaining,
        asset_id=asset_id
    )
