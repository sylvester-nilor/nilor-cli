import requests
from typing import Optional
from auth import get_auth_token


def send_chat_message(message: str, thread_id: str, book_agent_url: str) -> Optional[str]:
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
    print("=== Testing chat.py with real API ===")

    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    thread_id = "test-chat-main-123"
    test_message = "Hello! This is a test message from the CLI."

    print(f"📝 Thread ID: {thread_id}")
    print(f"💬 Message: {test_message}")
    print(f"🌐 URL: {book_agent_url}")
    print("-" * 50)


    response = send_chat_message(test_message, thread_id, book_agent_url)

    if response:
        print(f"✅ Success! Response: {response}")
    else:
        print("❌ Failed to get response")
