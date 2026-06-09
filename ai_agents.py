from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from prompts import MANAGER_AGENT, PROFESSIONAL_SDR, HUMOUROUS_SDR, CONCISE_SDR
from agents import Agent, OpenAIChatCompletionsModel, function_tool, trace
import resend

print("Initializing AI Agents System")

load_dotenv(override=True)

print("Loading environment variables")

groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("Groq API client initialized")

model= OpenAIChatCompletionsModel(openai_client=groq_client, model="qwen/qwen3-32b")

print("Model configured (qwen/qwen3-32b)")

print("Creating Agent Instances")

print("Creating Professional_Agent")
professional_agent = Agent(
    name="Professional_Agent",
    instructions=PROFESSIONAL_SDR,
    model=model)

print("Creating Humorous_Agent")
humorous_agent = Agent(
    name="Humorous_Agent",
    instructions=HUMOUROUS_SDR,
    model=model)

print("Creating Concise_Agent")
concise_agent = Agent(
    name="Concise_Agent",
    instructions=CONCISE_SDR,
    model=model)

print("Registering Agent Tools")

print("Registering Professional_Agent as tool")
tool1 = professional_agent.as_tool(tool_name="Professional_Agent", tool_description="Writes a professional cold email.")

print("Registering Humorous_Agent as tool")
tool2 = humorous_agent.as_tool(tool_name="Humorous_Agent", tool_description="Writes a witty and humorous cold email.")

print("Registering Concise_Agent as tool")
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
    print("Sending email")
    print(f"Subject: {subject}")
    
    with trace("send_email"):
        try:
            resend.api_key = os.getenv("RESEND_APIKEY")
            
            result = resend.Emails.send({
                "from": os.environ.get("EMAIL_FROM", "Acme <onboarding@resend.dev>"),
                "to": ["saifihassan656@gmail.com"],
                "subject": subject,
                "html": body,
                "text": "Welcome! This email was sent using Resend's Python SDK",
            })
            print("Email sent successfully to: saifihassan656@gmail.com")
            return "Email sent successfully"
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise

print("Creating Manager Agent")
manager_agent = Agent(
    name="Manager Agent",   
    instructions=MANAGER_AGENT,
    tools=[tool1, tool2, tool3, send_email],
    model=model
)

print("Manager Agent created and ready")



