import asyncio
import requests
import config

class LookupEngine:
    @classmethod
    async def query_target(cls, search_term: str) -> str:
        """
        Executes a GET request to the new Divyansh API endpoint.
        Maps the search_term to the 'number' parameter required by the API.
        """
        # New API Configuration
        payload = {
            "key": config.LOOKUP_API_KEY,
            "number": search_term
        }
        
        # Offload the synchronous request to a thread worker
        loop = asyncio.get_running_loop()
        try:
            response = await loop.run_in_executor(
                None, lambda: requests.get(config.LOOKUP_BASE_URL, params=payload, timeout=10)
            )
            
            # Raise an error for bad responses
            response.raise_for_status()
            
            # The API returns data directly; returning as string for bot output
            data = response.json()
            return str(data)
            
        except Exception as error:
            return f"Error connecting to lookup registry: {str(error)}"
