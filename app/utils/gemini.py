from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def can_you_find_a_dataset(description):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Can you find a name of any dataset(s) in the following description from a paper abstract, give me a comma separated list of names of possible dataset names, if you dont think there is one, give me no response - not a single word:\n\n {description}",
    )
    return [x.lstrip().rstrip() for x in response.text.split(",")]


def can_you_find_a_tool(title, text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Can you find any github or external links to any software related to this data in the following text? Give me the link follwed by a description, if you find multiple, separate them by the delimter '---' :\n\n {text} \n\n the title of the paper was: {title}",
    )
    return [x.lstrip().rstrip() for x in response.text.split(",")]
