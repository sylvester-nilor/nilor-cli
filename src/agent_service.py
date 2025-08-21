import os
from typing import List, Optional, TypedDict, Annotated

import google.auth
from google.auth.transport.requests import AuthorizedSession, Request
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_vertexai import ChatVertexAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from auth import get_auth_token


def get_system_prompt() -> str:
    return """You are a thoughtful, well-read conversational assistant with access to a rich knowledge base. Your goal is to engage in natural, helpful conversations while proactively enriching discussions with relevant knowledge when it could add value.

## Your Approach:
- **Engage naturally**: Have genuine conversations on any topic the user brings up
- **Proactive knowledge**: When you sense that insights from your knowledge base could help, use the search_knowledge tool to find relevant concepts, themes, or ideas
- **Weave knowledge naturally**: Integrate search results conversationally into your responses, not as lectures or formal citations
- **Stay helpful**: Focus on being genuinely useful to the user's situation or interests
- **Conversational flow**: Keep the conversation flowing naturally - the user doesn't know what's in your knowledge base

## When to Use search_knowledge:
- When the user shares a problem, challenge, or situation that might benefit from broader insights
- When discussing topics that could be enriched with relevant concepts or frameworks  
- When the user seems stuck, curious, or could benefit from a fresh perspective
- When you sense an opportunity to share relevant knowledge that could help
- When the conversation could benefit from deeper context or new perspectives

## How to Use Search Results:
- Don't formally cite sources - just weave insights naturally into conversation
- Connect concepts to the user's specific situation or interests
- Share ideas that might offer new perspectives or approaches
- Keep responses conversational and engaging, not academic
- Use search results to enhance your understanding, not replace your conversational skills

## Examples:
- User: "I'm feeling stuck on this project" → Use search_knowledge("creative blocks problem solving motivation")
- User: "My team is having communication issues" → Use search_knowledge("team collaboration communication leadership")
- User: "I'm thinking about starting something new" → Use search_knowledge("innovation new ventures risk taking")

## Important:
- You decide when to search based on conversational context
- Don't search for every message - only when it would genuinely add value
- If search results don't seem relevant, respond conversationally without forcing them in
- Always maintain natural conversation flow
- Be genuinely helpful and thoughtful, not just informative

Remember: You're having a conversation with someone who values thoughtful insights, not querying a database."""


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]


class AgentService:
    def __init__(self, project_id: str, book_agent_url: str, auth_token: Optional[str] = None):
        self.project_id = project_id
        self.book_agent_url = book_agent_url
        self.auth_token = auth_token
        self.memory_saver = MemorySaver()
        self._auth_session = None

        self.llm = ChatVertexAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            max_tokens=1000
        )

        from tool_search import create_search_tool
        tools = [create_search_tool(self.book_agent_url, self.auth_token)]

        system_message = SystemMessage(content=get_system_prompt())

        self.agent = create_react_agent(
            model=self.llm,
            tools=tools,
            checkpointer=self.memory_saver,
            prompt=system_message
        )

    def _get_auth_session(self) -> AuthorizedSession:
        if self._auth_session is None:
            credentials, _ = google.auth.default()
            if not credentials.valid:
                credentials.refresh(Request())
            self._auth_session = AuthorizedSession(credentials)
        return self._auth_session

    def chat(self, message: str, thread_id: str) -> str:
        try:
            config = {"configurable": {"thread_id": thread_id}}

            result = self.agent.invoke(
                {"messages": [HumanMessage(content=message)]},
                config=config
            )

            messages = result["messages"]
            if messages and isinstance(messages[-1], AIMessage):
                return messages[-1].content

            return "I'm sorry, I couldn't generate a response at this time."

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return f"I encountered an error while processing your request: {str(e)}"


if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT", "robot-rnd-nilor-gcp")
    book_agent_url = os.getenv("BOOK_AGENT_URL", "https://book-agent-v1-959508709789.us-central1.run.app")
    auth_token = get_auth_token()

    service = AgentService(
        project_id=project_id,
        book_agent_url=book_agent_url,
        auth_token=auth_token
    )

    thread_id = "test-proactive-agent-123"

    print("=== Testing Proactive Knowledge Agent ===")

    print("\n--- Test 1: Force RAG Usage ---")
    response1 = service.chat("Please search your knowledge base for information about digital sovereignty and tell me what you find", thread_id)
    print(f"User: Please search your knowledge base for information about digital sovereignty and tell me what you find")
    print(f"Agent: {response1}")

    print("\n--- Test 2: Creative Block with RAG ---")
    response2 = service.chat("I'm feeling stuck on a creative project. Can you search your knowledge base for insights about creative blocks and motivation?", thread_id)
    print(f"User: I'm feeling stuck on a creative project. Can you search your knowledge base for insights about creative blocks and motivation?")
    print(f"Agent: {response2}")

    print("\n--- Test 3: Decision Making with RAG ---")
    response3 = service.chat("My team is struggling with decision-making. Please search your knowledge base for insights about organizational decision-making and leadership", thread_id)
    print(f"User: My team is struggling with decision-making. Please search your knowledge base for insights about organizational decision-making and leadership")
    print(f"Agent: {response3}")
