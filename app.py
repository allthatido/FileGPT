"""
main program to launch the streamlit app for local LLM inference over a document
"""
import streamlit as st
import llm
import db


if "model" not in st.session_state:
    st.session_state["model"] = ''

if "file" not in st.session_state:
    st.session_state["file"] = ''

st.set_page_config(layout="wide", page_title='FileGPT: Local cognitive search over a document',
                   page_icon='./media/favicon.png')

with open('css.py', encoding='utf_8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<h2>🗂️ FileGPT</h2>',
            unsafe_allow_html=True)
st.markdown("""---""")

model_list = [''] + llm.get_models()

with st.sidebar:
    st.markdown(
        "## How to use :\n"
        "1. Select a model 💻\n"
        "2. Upload a pdf file (no ocr support)📄\n"
        "3. Ask a question about the document ❓\n"
    )
    st.markdown("""---""")

    selection = st.selectbox(
        '1-Select Model', model_list)
    if selection != '':
        with st.spinner("Loading model.."):
            model = llm.LlmModel(selection)
            model.load_model()

    pdf_file = st.file_uploader("2  - File Upload", type=[
        'pdf'], accept_multiple_files=False)

    if pdf_file is not None:
        with st.spinner("Loading file.."):
            data = db.Data(pdf_file)
            data.load_docs()
            data.gen_vectorstore(chunk_size=500, chunk_overlap=100)

    st.markdown("---")
    st.markdown("# About")
    st.markdown(
        "🗂️ FileGPT allows you to ask questions about your "
        "documents and get answers without your data leaving your network. "
    )
    st.markdown(
        "It lets you evaluate various LLM models and choose the one that works best for you.\
        This is a work in progress. For feedback and suggestions: \
        [GitHub](https://github.com/ankurkaul17/file_gpt)."
    )
    st.markdown(
        "Made by [Ankur Kaul](https://www.linkedin.com/in/ankurkaul17)"
    )
    st.markdown("---")

    st.markdown(
        """
            # FAQ
            ## How to add new models?
            You can create a new folder inside the '/models' directory and place downloaded
            models there. Make sure to keep the folder name same as the model bin file name. 

            ## Is my data safe?
            Yes, your data is safe. FileGPT stores your documents as embedding in a local
            directory called 'db'. The data does not leave your network. Questions and responses
            are not stored.

            ## Why does it take so long to run?
            Since the whole operation runs locally, the speed of inferencing depends on the
            local hardware. CPU's are usually slow at running LLM models than GPU's.

            ## Are the answers 100% accurate?
            No, the answers are not 100% accurate. The quality of the answer depends on the LLM
            that you are using. These LLM's sometimes make mistakes and are prone to hallucinations.

            But for most use cases, it is quite accurate and can answer most questions. Always
            check with the sources to make sure that the answers are correct.
            """
    )

l_col, r_col = st.columns((1.5, 1))

with l_col:

    question = st.text_area("3 - Ask a Question", height=30)
    response = st.empty()

    if st.button('Get Response'):

        ans = model.get_answer(
            ques=question, retriever=data.retriever)
        response.text_area('Response', value=ans, height=250)

with r_col:
    if pdf_file is None:
        st.text_area(
            'Document Preview: Raw Text', height=650, placeholder="Upload file first !!!", disabled=True)
    else:
        preview = st.text_area(
            'Document Preview: Raw Text', height=650, value=data.documents)
