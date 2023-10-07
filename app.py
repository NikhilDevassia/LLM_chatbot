import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

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


def main():
    st.set_page_config(page_title="chat with multiple pdf", page_icon=":books")
    st.header("chat with multiple pdf :books:")
    st.text_input("Ask question about your documents:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your documents", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get the pdx 
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks 
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)



            # create vector store 



if __name__ == "__main__":
    main()

