import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="나만의 와인 어시스턴트 💬", page_icon="💬")

# Top section with title and clear button aligned to the right
col1, col2 = st.columns([8, 2])
with col1:
    st.title("와인은 내게 물어봐💬")
with col2:
    # Button with custom HTML for line break
    clear_btn = st.markdown(
        """
        <style>
        .clear-button button {
            display: inline-block;
            white-space: pre-wrap;
            line-height: 1.2;
            padding: 8px 15px;
        }
        </style>
        <div class="clear-button">
            <button onclick="window.location.reload()">대화내용<br>초기화</button>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Initialize chat history if not in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to print chat history
def print_history():
    for msg in st.session_state["messages"]:
        st.chat_message(msg.role).write(msg.content)

# Function to add a message to the history
def add_history(role, content):
    st.session_state["messages"].append(ChatMessage(role=role, content=content))

# Function to create a prompt chain with a default prompt
def create_chain(prompt_text, model):
    prompt_template = prompt_text + "\n\n#Question:\n{question}\n\n#Answer:"
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | ChatOpenAI(model_name=model) | StrOutputParser()
    return chain

# Clear chat history if the button is clicked
if clear_btn:
    st.session_state["messages"].clear()

# Display chat history
print_history()
    


# Set up default prompt chain if not yet configured
if "chain" not in st.session_state:
    default_prompt = "당신은 시니컬한 AI 와인 전문가 입니다. 사용자의 질문에 간결하게 답변해 주세요."
    st.session_state["chain"] = create_chain(default_prompt, "ft:gpt-4o-mini-2024-07-18:personal::AT1DiWe2")

# Chat input at the bottom
if user_input := st.chat_input("메시지를 입력하세요"):
    add_history("user", user_input)

    
    st.chat_message("user").write(user_input)
    with st.chat_message("assistant"):
        chat_container = st.empty()

        # Stream the assistant's response
        stream_response = st.session_state["chain"].stream({"question": user_input})
        ai_answer = ""
        for chunk in stream_response:
            ai_answer += chunk
            chat_container.markdown(ai_answer)
        add_history("ai", ai_answer)
