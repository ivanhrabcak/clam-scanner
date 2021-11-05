import aiohttp
import asyncio
import time

start_time = time.time()

async def main():
    async with aiohttp.ClientSession() as session:
        for _ in range(500):
            url = 'http://127.0.0.1:8080/scan'
            f = open("eicarcom2.zip", "rb")
            async with session.post(url, data={"file": f}) as resp:
                response = await resp.text()
                print(response)

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))