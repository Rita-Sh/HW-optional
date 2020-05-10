import aiofiles
import aiohttp
import asyncio
import os
import requests
import io
from PIL import Image
async def download_coroutine(session, url):
        async with session.get(url) as response:
            filename = os.path.basename(url)
            async with aiofiles.open(filename, 'wb') as fd:
                while True:
                    chunk = await response.content.read()
                    if not chunk:
                        break
                    img = Image.open(io.BytesIO(chunk))
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    img.save(filename)
                    await fd.write(chunk)
            return await response.release()


async def main(loop, url):
    async with aiohttp.ClientSession(loop=loop) as session:
        await download_coroutine(session, url)


if __name__ == '__main__':
    urls = []
    res = requests.get('http://142.93.138.114/images').content.decode('utf-8').split()
    for i in res:
        urls.append('http://142.93.138.114/images' + i)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(main(loop, url) for url in urls)
        )
    )
