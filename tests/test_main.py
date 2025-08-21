import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.main import main
from src.chat_service import ChatResponse, SessionInfo


def test_main_initialization():
    from src.main import main
    assert callable(main)


@patch('builtins.input')
@patch('src.main.ChatService')
def test_main_exit_command(mock_chat_service_class, mock_input):
    """Test that main exits properly on quit command"""
    # Mock the service
    mock_service = Mock()
    mock_chat_service_class.return_value = mock_service
    
    # Mock session info
    session_info = SessionInfo(
        thread_id="test-thread-123",
        start_time=datetime.now(),
        message_count=0
    )
    mock_service.start_session.return_value = session_info
    
    # Mock session summary
    session_summary = SessionInfo(
        thread_id="test-thread-123",
        start_time=datetime.now(),
        message_count=1
    )
    mock_service.end_session.return_value = session_summary
    
    # Mock user input to quit immediately
    mock_input.return_value = "quit"
    
    # This should not raise any exceptions
    main()


@patch('builtins.input')
@patch('src.main.ChatService')
def test_main_send_message(mock_chat_service_class, mock_input):
    """Test that main can send a message and display response"""
    # Mock the service
    mock_service = Mock()
    mock_chat_service_class.return_value = mock_service
    
    # Mock session info
    session_info = SessionInfo(
        thread_id="test-thread-123",
        start_time=datetime.now(),
        message_count=0
    )
    mock_service.start_session.return_value = session_info
    
    # Mock response
    response = ChatResponse(
        message="Hello from the agent!",
        thread_id="test-thread-123",
        timestamp=datetime.now()
    )
    mock_service.send_message.return_value = response
    
    # Mock session summary
    session_summary = SessionInfo(
        thread_id="test-thread-123",
        start_time=datetime.now(),
        message_count=1
    )
    mock_service.end_session.return_value = session_summary
    
    # Mock user input: send message, then quit
    mock_input.side_effect = ["Hello", "quit"]
    
    # This should not raise any exceptions
    main()
    
    # Verify service was called correctly
    mock_service.start_session.assert_called_once()
    mock_service.send_message.assert_called_once_with("Hello")
    mock_service.end_session.assert_called_once()
