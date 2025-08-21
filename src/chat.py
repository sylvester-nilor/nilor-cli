import requests
from typing import Optional
from auth import get_auth_token


def send_chat_message(message: str, thread_id: str, book_agent_url: str) -> Optional[str]:
    """Send a single message to the book-agent service and return the response"""
    auth_token = get_auth_token()
    if not auth_token:
        return None

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": message,
        "thread_id": thread_id
    }

    try:
        response = requests.post(
            f"{book_agent_url}/chat",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return None

    except requests.exceptions.RequestException:
        return None
