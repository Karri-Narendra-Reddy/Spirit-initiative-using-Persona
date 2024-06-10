import os
from openai import AzureOpenAI

# //persona type: role
# //role: //generic/software profession
def createpersona(persona_type,role, product_name):
    persona_type = persona_type.upper()
    if(persona_type == "ROLE"):
        prompt = (
            "Write me 1 different" f"{persona_type} "
            "based personas with the role of " f"{role} " " interested in buying" f"{product_name} "
            ".Include a short biography about their age, goals, needs and wants, pain points, motivations and what influences them most in 150 words. "
            "Give me a table of all the personas which have the probability of buying the "f"{product_name}? Also list their buying capability and their preferences to the "f"{product_name} ?"
        )
    elif(persona_type == "GOAL"):
        prompt = (
            "Write me 1 different" f"{persona_type} "
            "based personas with the Goal of " f"{role} " " interested in buying" f"{product_name} "
            ".Include a short biography about their age, goals, needs and wants, pain points, motivations and what influences them most in 150 words. "
            "Give me a table of all the personas which have the probability of buying the "f"{product_name}? Also list their buying capability and their preferences to the "f"{product_name} ?"
        )
    else:
        prompt = (
            "IGNORE EVERYTHING BEFORE THIS PROMPT."
            "Write me 1 different" f"{persona_type} "
            "based personas with the Scenario of " f"{role} " " interested in buying" f"{product_name} "
            ".Include a short biography about their age, goals, needs and wants, pain points, motivations and what influences them most in 150 words. "
            "Give me a table of all the personas which have the probability of buying the "f"{product_name}? Also list their buying capability and their preferences to the "f"{product_name} ?"
        )

    os.environ["AZURE_OPENAI_API_VERSION"] = "2023-12-01-preview"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://analyst-augmentation-non-us.openai.azure.com/"
    os.environ["AZURE_OPENAI_API_KEY"] = "73141bf1b4eb4f6bba5216cb6a8e0a33"
    os.environ["OPENAI_API_TYPE"] = "azure_ad"
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4-32k"
    client = AzureOpenAI(
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )
    completion = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
    )
    return completion.choices[0].message.content

def answersfrompersonas(questions,options,persona,type):
    prompt = (
        "this is my question:" f"{questions} \n"
        "these are my options: " f"{options} \n" 
        "this is my persona:" f"{persona} "
        "this is my type of question: " f"{type}\n" 
        ".now you are my above persona your goal is to answer the options for above question based on the question type \n"
        "Return me the only selected options in array format."
        " Don't give context and reasons i just want only the options array format"
    )

    os.environ["AZURE_OPENAI_API_VERSION"] = "2023-12-01-preview"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://analyst-augmentation-non-us.openai.azure.com/"
    os.environ["AZURE_OPENAI_API_KEY"] = "73141bf1b4eb4f6bba5216cb6a8e0a33"
    os.environ["OPENAI_API_TYPE"] = "azure_ad"
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4-32k"
    client = AzureOpenAI(
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )
    completion = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
    )
    return completion.choices[0].message.content

def answersfrompersona(questions,persona,type):
    prompt = (
        "this is my question:" f"{questions} \n" 
        "this is my persona:" f"{persona} "
        "this is my type of question: " f"{type}\n" 
        ".now you are my above persona your goal is to answer the question \n"
        "Return me only string in array format"
        " Don't give context and reasons"
    )

    os.environ["AZURE_OPENAI_API_VERSION"] = "2023-12-01-preview"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://analyst-augmentation-non-us.openai.azure.com/"
    os.environ["AZURE_OPENAI_API_KEY"] = "73141bf1b4eb4f6bba5216cb6a8e0a33"
    os.environ["OPENAI_API_TYPE"] = "azure_ad"
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4-32k"
    client = AzureOpenAI(
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )
    completion = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
    )
    return completion.choices[0].message.content

