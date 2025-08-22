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
    print("🧪 Testing Memory Persistence in CLI")
    print("=" * 50)

    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    thread_id = "test-chat-memory-123"

    print(f"📝 Thread ID: {thread_id}")
    print(f"🌐 URL: {book_agent_url}")
    print("-" * 50)

    # Test conversation with memory
    print("📝 Message 1: Remembering favorite color...")
    response1 = send_chat_message("Remember this: my favorite color is purple", thread_id, book_agent_url)
    
    if response1:
        print(f"Response 1: {response1}")
    else:
        print("❌ Failed to get response 1")
        exit(1)

    print("\n📝 Message 2: Asking about favorite color...")
    response2 = send_chat_message("What is my favorite color?", thread_id, book_agent_url)
    
    if response2:
        print(f"Response 2: {response2}")
    else:
        print("❌ Failed to get response 2")
        exit(1)

    # Check if memory worked
    if "purple" in response2.lower():
        print("\n✅ Memory test PASSED - Agent remembered the color!")
    else:
        print("\n❌ Memory test FAILED - Agent forgot the color!")
        exit(1)

    print("\n🎉 All memory tests passed!")
