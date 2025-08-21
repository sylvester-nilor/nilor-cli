import pytest
from unittest.mock import patch, Mock
from src.chat import send_chat_message
import requests


def test_send_chat_message_success():
    """Test successful message sending"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Hello from the agent!"}
    
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    
    with patch('src.chat.get_auth_token', return_value="fake_token"), \
         patch('requests.post', return_value=mock_response):
        
        result = send_chat_message("Hello", "test-thread-123", book_agent_url)
        
        assert result == "Hello from the agent!"


def test_send_chat_message_no_auth():
    """Test when auth token is not available"""
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    
    with patch('src.chat.get_auth_token', return_value=None):
        result = send_chat_message("Hello", "test-thread-123", book_agent_url)
        
        assert result is None


def test_send_chat_message_api_error():
    """Test when API returns an error"""
    mock_response = Mock()
    mock_response.status_code = 500
    
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    
    with patch('src.chat.get_auth_token', return_value="fake_token"), \
         patch('requests.post', return_value=mock_response):
        
        result = send_chat_message("Hello", "test-thread-123", book_agent_url)
        
        assert result is None


def test_send_chat_message_network_error():
    """Test when network request fails"""
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    
    with patch('src.chat.get_auth_token', return_value="fake_token"), \
         patch('requests.post', side_effect=requests.exceptions.RequestException("Network error")):
        
        result = send_chat_message("Hello", "test-thread-123", book_agent_url)
        
        assert result is None
