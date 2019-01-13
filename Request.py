import random

import requests


class Request:

    @staticmethod
    def make_request(url):
        # Use a variety of random user agents to avoid blocking of IP.
        user_agent_list = [
            # Linux - Chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            # Mac - Chrome
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        ]
        user_agent = random.choice(user_agent_list)
        headers = {
            'User-Agent': user_agent
        }
        # Get the HTML.
        # If it takes more than 10 seconds to get the response, then stop waiting
        # If it takes more than 15 seconds to read the response, then stop waiting
        return requests.get(url, headers=headers, timeout=(10, 15))
