from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
import os

def generate_script(subject,video_length,creativity,keyword):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human","请为'{subject}'这个主题的视频想一个吸引人的标题")])

    script_template = ChatPromptTemplate.from_messages([
        ("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求,关键词:{keyword},生成的脚本要包含关键词且加粗表达,同一关键词出现1-2次即可,不用开头,中间,结尾都出现。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             """)
    ])

    model = ChatOpenAI(model="9dc913a037774fc0b248376905c85da5",
                       api_key="1e4ce7db819c4891a6365f59308b46f8",
                       temperature=creativity,
                       base_url = "https://wishub-x1.ctyun.cn/v1")

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    script = script_chain.invoke({"title": title, "duration": video_length,"keyword":keyword}).content

    return title,script

def get_chat_response(prompt,memory):
    model = ChatOpenAI(model="9dc913a037774fc0b248376905c85da5",
                       api_key="1e4ce7db819c4891a6365f59308b46f8",
                       base_url = "https://wishub-x1.ctyun.cn/v1")
    chain = ConversationChain(llm= model,
                              memory = memory
                              )
    response = chain.invoke({"input":prompt})
    return response["response"]