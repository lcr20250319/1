import streamlit as st
from 视频脚本生成器_后端 import generate_script,get_chat_response
from langchain.memory import ConversationBufferMemory

st.title("🎬 视频脚本生成器")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_message=True)
    st.session_state["messages"] = [{"role": "ai", "content": "你好,我是视频脚本生成助手"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])



with st.sidebar:
    subject = st.text_input("请输入视频的主题")
    keyword = st.text_input("请输入视频的关键词(不同关键词用,隔开即可)")
    video_length = st.number_input("请输入视频的大致时长(单位:分钟)",min_value=1.0,step=0.1)
    creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
    submit = st.button("生成脚本")
if submit and not subject:
    st.write("请输入视频的主题")
    st.stop()
if submit and not video_length:
    "请输入视频的大致时长(单位:分钟)"
    st.stop()
prompt = st.chat_input()

if submit:
    with st.spinner("AI正在思考回答中,请等待..."):
        title, script = generate_script(subject, video_length, creativity,keyword)

        st.session_state["messages"].append({"role":"ai","content":title})
        st.session_state["messages"].append({"role": "ai", "content":script})
        with st.chat_message("ai"):#新方法
            st.subheader("标题")
            st.write(title)
            st.subheader("视频脚本")
            st.write(script)
            input_str = f"生成视频脚本请求: subject={subject}, video_length={video_length}, creativity={creativity}, keyword={keyword}"
            output_str = f"{title}\n{script}"
            st.session_state['memory'].save_context({"input": input_str}, {"output": output_str})

if prompt:
    if 'memory' in st.session_state:
        st.session_state["messages"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)
        with st.spinner("AI正在思考回答中,请稍等..."):
            response = get_chat_response(prompt,st.session_state["memory"])
            st.session_state["messages"].append({"role": "ai", "content": response})
            st.chat_message("ai").write(response)