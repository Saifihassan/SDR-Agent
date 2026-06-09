# from agents import function_tool
# from ai_agents import professional_agent, humorous_agent, concise_agent
# import resend 
# import os

# tool1 = professional_agent.as_tool(tool_name="Professional Agent", description="Writes a professional cold email.")
# tool2 = humorous_agent.as_tool(tool_name="Humorous Agent", description="Writes a witty and humorous cold email.")
# tool3 = concise_agent.as_tool(tool_name="Concise Agent", description="Writes a short and direct cold email.")


# @function_tool
# def send_email(to: str, subject: str, body: str):
#     """
#     Sends an email using the Resend API.
    
#     Parameters:
#     - to: The recipient's email address.
#     - subject: The subject of the email.
#     - body: The body content of the email.
    
#     Returns:
#     - A confirmation message indicating the email was sent.
#     """
#     client = resend.Client(api_key=os.getenv("RESEND_APIKEY"))
    
#     email = resend.Email(
#         from_email="onboarding@resend.dev",
#         to=[to], 
#         subject=subject,
#         html=body  
#     )

#     print("sending email...")


# Agent_tools= [tool1, tool2, tool3, send_email]