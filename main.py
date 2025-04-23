from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from julep import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
JULEP_API_KEY = os.getenv("JULEP_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")  # Set this after running create_agent.py

# Initialize FastAPI app
app = FastAPI(title="Julep AI Research Assistant API")

# Initialize Julep client
julep_client = Client(api_key=JULEP_API_KEY)

# Define request model


class ResearchRequest(BaseModel):
    topic: str
    format: str


# Define supported formats
SUPPORTED_FORMATS = ["summary", "bullet points", "short report"]


@app.post("/research")
async def research(request: ResearchRequest):
    try:
        # Validate format
        if request.format.lower() not in SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid format. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
            )

        # Create a session for the agent
        session = julep_client.sessions.create(
            agent_id=AGENT_ID,
            instructions=[
                f"Research the topic: {request.topic}",
                f"Present the findings in the following format: {request.format}"
            ]
        )

        # Get the agent's response
        response = julep_client.sessions.chat(
            session_id=session.id,
            agent_id=AGENT_ID,
            messages=[
                {"role": "user", "content": f"Provide research on {request.topic} in {request.format} format."}
            ]
        )

        # Extract the assistant's response
        if response and response.choices:
            result = response.choices[0].message.content
            return {"result": result}
        else:
            raise HTTPException(
                status_code=500, detail="No response from Julep agent")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Julep AI Research Assistant API"}
