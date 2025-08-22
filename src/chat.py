import requests
from typing import Optional
from auth import get_auth_token


def send_chat_message(message: str, thread_id: str, book_agent_url: str, auth_token: Optional[str] = None) -> Optional[str]:
    if auth_token is None:
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


if __name__ == "__main__":
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    thread_id = "test-chat-memory-123"

    # Test memory persistence
    response1 = send_chat_message("Remember this: my favorite color is purple", thread_id, book_agent_url)
    response2 = send_chat_message("What is my favorite color?", thread_id, book_agent_url)
    
    if "purple" in response2.lower():
        print("✅ Memory test PASSED")
    else:
        print("❌ Memory test FAILED")
        exit(1)
