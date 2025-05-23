import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

st.title("HBK's 챗GPT")

# 처음 한번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화기록을 저장하기위한 용도로 생성
    st.session_state["messages"] = []


# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메세지를 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))


# 체인생성
def create_chain():
    # prompt | llm | out_parser
    # 프롬프트
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트 입니다."),
            ("user", "#Question:\n{question}"),
        ]
    )
    # GPT
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # 출력파서
    output_parser = StrOutputParser()

    # 체인생성
    chain = prompt | llm | output_parser
    return chain


print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요")

# 만약에 사용자 입력이 들어오면...
if user_input:
    # 사용자의 입력
    st.chat_message("user").write(user_input)
    # chain을 생성
    chain = create_chain()
    ai_answer = chain.invoke({"question": user_input})

    # AI의 답변
    st.chat_message("assistant").write(ai_answer)

    # 대화기록을 저장
    add_message("user", user_input)
    add_message("assistant", ai_answer)
