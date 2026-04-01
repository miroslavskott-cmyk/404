 import aiohttp

class FootballData:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"

    async def get_today_matches(self):
        headers = {'x-apisports-key': self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/fixtures?date=2026-04-01", headers=headers) as resp:
                return await resp.json()
