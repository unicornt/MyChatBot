from openai import OpenAI
import os

qa_prompt = """你是一个积极开朗、善解人意的人，今天你的一位朋友来找你聊天，你需要根据你和他聊天的相关记忆，积极乐观地回复他
相关记忆：
{memory}
朋友说的话：
{input}
你的回答："""

memory_prompt = """你是一个细心的人，今天你的一位朋友来找你聊天，你需要参考你和他的聊天记录，基于他当前说的话生成未来聊天可能会提到的记忆点。记忆点请用简单的一句话表述。
聊天记录：
{history}
朋友说的话：
{input}
记忆点："""

api_key = None
with open('APIKey.env','r',encoding='utf-8') as f:
    api_key = f.read()
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

def get_completion(prompt, model="gpt-3.5-turbo"):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="moonshot-v1-8k",
        temperature=0.5
    )
    return chat_completion.choices[0].message.content