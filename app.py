import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import conversational_retrieval
# from langchain.chat_models import ChatOpenAI
from htmlTemplate import css, bot_template, user_template


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for pages in pdf_reader.pages:
            text += pages.extract_text()
    return text


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    embedding = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(text_chunks, embedding=embedding)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = 
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = conversational_retrieval.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory

    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history.append(response['chat_history'])

    for i, message in enumerate(st.scatter_chart.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="chat with multiple pdf", page_icon=":books")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("chat with multiple pdf :books:")
    user_question = st.text_input("Ask question about your documents:")

    if user_question:
        handle_userinput(user_question)

    st.write(user_template.replace("{{MSG}}", "Hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello human"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your documents", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get the pdx 
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks 
                text_chunks = get_text_chunks(raw_text)

                # create vector store 
                vectorstore = get_vectorstore(text_chunks)

                # create conversation
                st.session_state.conversation = get_conversation_chain(vectorstore)
    st.session_state.conversation



if __name__ == "__main__":
    main()

