import sys
from chat_service import ChatService


def main():
    book_agent_url = "https://book-agent-v1-959508709789.us-central1.run.app"
    
    print("🤖 NILOR CLI - Interactive Book Agent")
    print("💬 Type 'quit' or 'exit' to end session, Ctrl+C to interrupt")
    print("-" * 50)

    service = ChatService(book_agent_url)
    
    session_info = service.start_session()
    print(f"📝 Session started with thread_id: {session_info.thread_id}")
    print()
    
    while True:
        try:
            try:
                user_input = input("nilor> ").strip()
            except EOFError:
                print("\n👋 End of input. Ending session...")
                session_summary = service.end_session()
                if session_summary:
                    print(f"📊 Session summary: {session_summary.message_count} messages exchanged")
                print("Goodbye!")
                break
            
            if user_input.lower() in ["quit", "exit"]:
                print("👋 Ending session...")
                session_summary = service.end_session()
                if session_summary:
                    print(f"📊 Session summary: {session_summary.message_count} messages exchanged")
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = service.send_message(user_input)
            
            if response:
                print(f"\n{response.message}\n")
            else:
                print("❌ Failed to get response from agent")
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Ending session...")
            session_summary = service.end_session()
            if session_summary:
                print(f"📊 Session summary: {session_summary.message_count} messages exchanged")
            print("Goodbye!")
            break
        except EOFError:
            print("\n👋 End of input. Ending session...")
            session_summary = service.end_session()
            if session_summary:
                print(f"📊 Session summary: {session_summary.message_count} messages exchanged")
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
