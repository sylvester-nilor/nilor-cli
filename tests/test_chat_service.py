import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.chat_service import ChatService, ChatResponse, SessionInfo


def test_chat_service_initialization():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    assert service.book_agent_url == book_agent_url
    assert service.thread_id is None
    assert service.start_time is None
    assert service.message_count == 0


def test_chat_service_start_session():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    session_info = service.start_session()
    
    assert isinstance(session_info, SessionInfo)
    assert session_info.thread_id is not None
    assert isinstance(session_info.start_time, datetime)
    assert session_info.message_count == 0
    assert service.thread_id == session_info.thread_id


def test_chat_service_send_message():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    # Start session first
    service.start_session()
    
    with patch('src.chat_service.send_chat_message', return_value="Test response"):
        response = service.send_message("Hello")
        
        assert isinstance(response, ChatResponse)
        assert response.message == "Test response"
        assert response.thread_id == service.thread_id
        assert isinstance(response.timestamp, datetime)
        assert service.message_count == 1


def test_chat_service_send_message_no_session():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    response = service.send_message("Hello")
    
    assert response is None


def test_chat_service_end_session():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    # Start session and send a message
    service.start_session()
    with patch('src.chat_service.send_chat_message', return_value="Test response"):
        service.send_message("Hello")
    
    # End session
    session_summary = service.end_session()
    
    assert isinstance(session_summary, SessionInfo)
    assert session_summary.message_count == 1
    assert service.thread_id is None
    assert service.start_time is None
    assert service.message_count == 0


def test_chat_service_get_session_info():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    service = ChatService(book_agent_url)
    
    # No session started
    assert service.get_session_info() is None
    
    # Start session
    session_info = service.start_session()
    current_info = service.get_session_info()
    
    assert current_info is not None
    assert current_info.thread_id == session_info.thread_id
    assert current_info.start_time == session_info.start_time
    assert current_info.message_count == 0
