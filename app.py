import streamlit as st


def main():
    st.set_page_config(page_title="chat with multiple pdf", page_icon=":books")
    st.header("chat with multiple pdf :books:")
    st.text_input("Ask question about your documents:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your documents", accept_multiple_files=True)
        if st.button("Process"):
            # get the pdx 

            # get the text chunks 

            # create vector store 



if __name__ == "__main__":
    main()

