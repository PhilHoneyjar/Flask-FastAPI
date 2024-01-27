import os
import argparse
import threading
import multiprocessing
import asyncio
import time
from flask import Flask, render_template, request, jsonify
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

app = Flask(__name__)


def download_image(url, save_path):
    with urlopen(url) as response:
        with open(save_path, 'wb') as out_file:
            out_file.write(response.read())


def process_url(url):
    image_name = os.path.basename(url)
    save_path = os.path.join("downloads", image_name)

    start_time = time.time()
    download_image(url, save_path)
    end_time = time.time()

    print(f"Downloaded {image_name} in {end_time - start_time:.2f} seconds")


def download_images_multithreaded(urls):
    with ThreadPoolExecutor() as executor:
        executor.map(process_url, urls)


def download_images_multiprocess(urls):
    with ProcessPoolExecutor() as executor:
        executor.map(process_url, urls)


async def download_images_async(urls):
    tasks = [process_url(url) for url in urls]
    await asyncio.gather(*tasks)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    urls = request.form.get('urls').split('\n')
    concurrency_method = request.form.get('concurrency')

    start_time = time.time()

    if concurrency_method == 'multithreaded':
        download_images_multithreaded(urls)
    elif concurrency_method == 'multiprocess':
        download_images_multiprocess(urls)
    elif concurrency_method == 'asyncio':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(download_images_async(urls))
    else:
        return jsonify({'error': 'Please specify a valid concurrency method'})

    end_time = time.time()
    total_time = end_time - start_time

    return jsonify({'success': True, 'total_time': total_time})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image Downloader')
    parser.add_argument('--multithreaded', action='store_true', help='Use multithreading')
    parser.add_argument('--multiprocess', action='store_true', help='Use multiprocessing')
    parser.add_argument('--asyncio', action='store_true', help='Use asyncio')

    args = parser.parse_args()

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    app.run(debug=True)
