import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from chat import send_chat_message


@dataclass
class ChatResponse:
    message: str
    thread_id: str
    timestamp: datetime


@dataclass
class SessionInfo:
    thread_id: str
    start_time: datetime
    message_count: int


class ChatService:
    def __init__(self, book_agent_url: str):
        self.book_agent_url = book_agent_url
        self.thread_id: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.message_count = 0
    
    def start_session(self) -> SessionInfo:
        """Start a new conversation session"""
        self.thread_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.message_count = 0
        return SessionInfo(
            thread_id=self.thread_id,
            start_time=self.start_time,
            message_count=self.message_count
        )
    
    def send_message(self, message: str) -> Optional[ChatResponse]:
        """Send a message in the current session and return canonical response"""
        if not self.thread_id:
            return None
        
        response_text = send_chat_message(message, self.thread_id, self.book_agent_url)
        if response_text:
            self.message_count += 1
            return ChatResponse(
                message=response_text,
                thread_id=self.thread_id,
                timestamp=datetime.now()
            )
        return None
    
    def end_session(self) -> Optional[SessionInfo]:
        """End the current session and return summary"""
        if not self.thread_id:
            return None
        
        session_info = SessionInfo(
            thread_id=self.thread_id,
            start_time=self.start_time,
            message_count=self.message_count
        )
        
        # Reset session state
        self.thread_id = None
        self.start_time = None
        self.message_count = 0
        
        return session_info
    
    def get_session_info(self) -> Optional[SessionInfo]:
        """Get current session information"""
        if not self.thread_id:
            return None
        
        return SessionInfo(
            thread_id=self.thread_id,
            start_time=self.start_time,
            message_count=self.message_count
        )


if __name__ == "__main__":
    print("=== Testing chat_service.py with real API ===")
    
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    print(f"🌐 URL: {book_agent_url}")
    print("-" * 50)
    
    # Test starting a session
    print("🚀 Starting new session...")
    session_info = service.start_session()
    print(f"📝 Session started: {session_info.thread_id}")
    print(f"⏰ Start time: {session_info.start_time}")
    
    # Test sending messages
    test_message = "Hello from the chat service!"
    print(f"\n💬 Sending: {test_message}")
    
    response = service.send_message(test_message)
    
    if response:
        print(f"✅ Response: {response.message}")
        print(f"📝 Thread: {response.thread_id}")
        print(f"⏰ Time: {response.timestamp}")
    else:
        print("❌ Failed to get response")
    
    # Test sending another message
    test_message2 = "How are you doing today?"
    print(f"\n💬 Sending: {test_message2}")
    
    response2 = service.send_message(test_message2)
    
    if response2:
        print(f"✅ Response: {response2.message}")
    else:
        print("❌ Failed to get response")
    
    # Test ending session
    print("\n🛑 Ending session...")
    session_summary = service.end_session()
    if session_summary:
        print(f"📊 Session summary:")
        print(f"   Thread ID: {session_summary.thread_id}")
        print(f"   Start time: {session_summary.start_time}")
        print(f"   Messages: {session_summary.message_count}")
    else:
        print("❌ Failed to end session")
