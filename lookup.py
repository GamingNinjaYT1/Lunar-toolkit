import asyncio
import requests
import config

class LookupEngine:
    @classmethod
    async def query_target(cls, search_term: str) -> str:
        """Asynchronously triggers the native ID_TO_NUM lookup algorithm without blocking the loop."""
        payload = {
            "key": config.LOOKUP_API_KEY,
            "type": "tg",
            "term": search_term
        }
        
        # Diverts the synchronous requests call to an external thread worker pool
        loop = asyncio.get_running_loop()
        try:
            response = await loop.run_in_executor(
                None, lambda: requests.get(config.LOOKUP_BASE_URL, params=payload, timeout=10)
            )
            data = response.json()
            # Safely handle either a direct dictionary string or a targeted result key
            if isinstance(data, dict) and "result" in data:
                return str(data["result"])
            return str(data)
        except Exception as error:
            return f"Error executing communication pipeline query: {str(error)}"
