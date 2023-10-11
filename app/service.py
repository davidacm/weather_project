#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os

from aiohttp import web
import aiohttp

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

from . import process_data, cache_service

cache = cache_service.Cache(120)


appId = env['APPID']


# URL to get the current weather.
API_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&q=%s&appid=%s"


async def fetch_current_weather(city, country):
    try:
        async with aiohttp.ClientSession() as session:
            api_url = API_URL % (f"{city},{country}", appId)
            async with session.get(api_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    return {'error': error_message, 'status': response.status}
    except Exception as e:
        return {'error': str(e), 'status': 400}


content_type = 'application/json'
async def handle_weather(request: web.Request) -> web.json_response:
    q = request.query
    error_list = []
    if 'city' not in q:
        error_list.append('city')
    if 'country' not in q:
        error_list.append('country')
    if error_list:
        missing_params = " and ".join(error_list)
        return web.json_response({"error": f"parameters {missing_params} are missing"}, status=400)

    city = q['city'].lower()
    country = q['country'].lower()

    key = f"{city},{country}"
    weather_data = cache.get(key)
    if not weather_data:
        api_weather_data = await fetch_current_weather(city, country)
        if 'error' in api_weather_data:
            return web.json_response(api_weather_data, status=api_weather_data['status'])
        weather_data = process_data.process_json(api_weather_data)
        cache.set(key, weather_data)
    
    return web.json_response(weather_data)

app = web.Application()
app.router.add_get('/weather', handle_weather)


async def background_tasks(app):
    app['memory_cleaner'] = asyncio.create_task(cache.memory_task_cleaner(120))
    yield
    app['memory_cleaner'].cancel()
    await app['memory_cleaner']
app.cleanup_ctx.append(background_tasks)


def run():
    web.run_app(app, host=env['HOST'], port=env['PORT'])


if __name__ == '__main__':
    run()

