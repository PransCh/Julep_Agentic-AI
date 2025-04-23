from julep import Client
import os
from dotenv import load_dotenv
import uuid


load_dotenv()
JULEP_API_KEY = os.getenv("JULEP_API_KEY")


client = Client(api_key=JULEP_API_KEY)


agent_id = str(uuid.uuid4())


agent = client.agents.create(
    name="ResearchAssistant",
    about="A helpful research assistant that provides concise and accurate information on user-specified topics.",
    instructions=[

        "You are a helpful research assistant. Your goal is to find concise information on topics provided by the user.",

        "When given a topic and an output format (e.g., 'summary', 'bullet points', 'short report'), you must gather relevant information and structure it according to the requested format.",
        "Maintain a neutral, objective tone. Strictly adhere to the requested output format. Keep summaries to 3-4 sentences, bullet points concise (max 5 points), and short reports under 150 words. If you cannot find reliable information, state that clearly."
    ],
    model="gpt-4o",
    default_settings={
        "temperature": 0.7,
        "top_p": 1,
        "min_p": 0.01,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "length_penalty": 1.0
    },
    metadata={"agent_id": agent_id}
)

print(f"Agent created with ID: {agent.id}")