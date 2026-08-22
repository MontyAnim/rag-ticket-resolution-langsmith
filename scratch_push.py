import os
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and precise technical support resolution assistant. Use the `retrieve_knowledge` tool to look up technical documentation and troubleshooting manuals. Use the `query_ticket_status` tool to check previous ticket history and details in the database. Always be polite, concise, and provide accurate answers based on the retrieved context."),
    ("placeholder", "{messages}")
])

c = Client()
try:
    url = c.push_prompt('support-agent-prompt', object=prompt)
    print(f"Success! Handle URL: {url}")
except Exception as e:
    print(f"Error: {e}")
