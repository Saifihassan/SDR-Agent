from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from prompts import MANAGER_AGENT, PROFESSIONAL_SDR, HUMOUROUS_SDR, CONCISE_SDR
from agents import Agent, OpenAIChatCompletionsModel, function_tool, trace
import resend

load_dotenv(override=True)

groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model= OpenAIChatCompletionsModel(openai_client=groq_client, model="qwen/qwen3-32b")


professional_agent = Agent(
    name="Professional_Agent",
    instructions=PROFESSIONAL_SDR,
    model=model)
humorous_agent = Agent(
    name="Humorous_Agent",
    instructions=HUMOUROUS_SDR,
    model=model)
concise_agent = Agent(
    name="Concise_Agent",
    instructions=CONCISE_SDR,
    model=model)

tool1 = professional_agent.as_tool(tool_name="Professional_Agent", tool_description="Writes a professional cold email.")
tool2 = humorous_agent.as_tool(tool_name="Humorous_Agent", tool_description="Writes a witty and humorous cold email.")
tool3 = concise_agent.as_tool(tool_name="Concise_Agent", tool_description="Writes a short and direct cold email.")

@function_tool
def send_email(subject: str, body: str):
    """
    Sends an email using the Resend API.
    
    Parameters:
    - to: The recipient's email address.
    - subject: The subject of the email.
    - body: The body content of the email.
    
    Returns:
    - A confirmation message indicating the email was sent.
    """
    with trace("send_email"):
        resend.api_key = os.getenv("RESEND_APIKEY")
        
        result = resend.Emails.send({
            "from": os.environ.get("EMAIL_FROM", "Acme <onboarding@resend.dev>"),
            "to": ["saifihassan656@gmail.com"],  # Use test address for development
            "subject": subject,
            "html": body,
            # Optional: plain text version
            "text": "Welcome! This email was sent using Resend's Python SDK",
        })
        print ("Email sent with subject:", subject)
        


manager_agent = Agent(
name="Manager Agent",   
instructions=MANAGER_AGENT,
tools=[tool1, tool2, tool3, send_email],
model=model)



