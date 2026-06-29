import aiohttp
import config

class InstagramEngine:
    @classmethod
    async def extract_profile(cls, session_id: str, target_user: str) -> dict:
        """Pulls exact metadata properties using non-blocking asynchronous HTTP sessions."""
        headers = {
            'x-ig-app-id': config.INSTA_APP_ID,
            'User-Agent': config.USER_AGENT
        }
        cookies = {"sessionid": session_id}
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target_user}"

        try:
            async with aiohttp.ClientSession(cookies=cookies) as session:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status != 200:
                        return {"success": False, "msg": f"API responded with HTTP status code: {response.status}"}
                    
                    raw_data = await response.json()
                    if 'data' not in raw_data or not raw_data['data'].get('user'):
                        return {"success": False, "msg": "Target profile data structure missing or invalid session identifier."}
                        
                    user_data = raw_data['data']['user']
                    return {
                        "success": True,
                        "full_name": user_data.get('full_name', 'N/A'),
                        "biography": user_data.get('biography', 'N/A'),
                        "external_url": user_data.get('external_url', 'N/A'),
                        "profile_pic": user_data.get('profile_pic_url', 'N/A')
                    }
        except Exception as e:
            return {"success": False, "msg": f"Pipeline internal failure: {str(e)}"}

