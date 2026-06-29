import asyncio
import requests

class LookupEngine:
    @classmethod
    async def query_target(cls, search_term: str) -> str:
        """Sends a direct request to the specified API URL."""
        try:
            # The exact URL with the number parameter
            url = f"https://divyansh.store/num-info?key=jioxqt&number={search_term}"
            
            # Offload the synchronous request to a thread worker to keep the bot responsive
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, lambda: requests.get(url, timeout=10)
            )
            
            # Return the raw text from the website
            return response.text
            
        except Exception as error:
            return f"Error connecting to lookup registry: {str(error)}"
