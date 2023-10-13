#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
from socket import gethostname

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, abort, jsonify, request

loop = asyncio.get_event_loop()
app = Flask(__name__)



from . import process_data, cache_service
from .service import fetch_current_weather

cache = cache_service.Cache(120)
cache.thread_memory_task_cleaner(120)


@app.route('/weather', methods=['GET'])
def handle_weather():
    error_list = []
    q = request.args
    if 'city' not in q:
        error_list.append('city')
    if 'country' not in q:
        error_list.append('country')
    if error_list:
        missing_params = " and ".join(error_list)
        error = jsonify({"error": f"parameters {missing_params} are missing"})
        error.status = 400
        return error

    city = q['city'].lower()
    country = q['country'].lower()

    key = f"{city},{country}"
    weather_data = cache.get(key)
    if not weather_data:
        api_weather_data = loop.run_until_complete(fetch_current_weather(city, country))
        if 'error' in api_weather_data:
            error = jsonify(api_weather_data)
            error.status = 400
            return error
        weather_data = process_data.process_json(api_weather_data)
        cache.set(key, weather_data)
    
    return jsonify(weather_data)


def run():
    host = env.get('HOST', None)
    port = env.get('PORT', 8080)
    app.run(host=host, port=port)

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        run()
