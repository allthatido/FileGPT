"""
llm class for instatntiating llm models and tokenizers based on the selection
"""
import os
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


def get_models(path='models'):
    """
    get the list of all vailable model directories
    """
    directories = [name for name in os.listdir(
        path) if os.path.isdir(os.path.join(path, name))]
    return directories


class LlmModel:
    """
    LLM class to instantiate a llm model
    """

    def __init__(self, selection):
        self.tokenizer = None
        self.model = None
        self.llm = None
        self.selection = selection
        self.model_dir = 'models'
        self.llm_path = f'{self.model_dir}/{selection}'

    def load_model(self):
        """
        function to generate model and tokenizer from selection
        """

        if self.selection in ('flan-t5-base'):
            self.tokenizer = AutoTokenizer.from_pretrained(self.llm_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.llm_path, device_map="auto")
            pipe = pipeline(
                'text2text-generation',
                model=self.model,
                tokenizer=self.tokenizer
            )
            self.llm = HuggingFacePipeline(pipeline=pipe)

        else:
            callback_manager = CallbackManager(
                [StreamingStdOutCallbackHandler()])
            self.llm = LlamaCpp(
                model_path=f"{self.llm_path}/{self.selection}.bin", n_gpu_layers=25, n_ctx=1024, n_threads=8, callback_manager=callback_manager, verbose=True)

    def get_answer(self, ques, retriever):
        """
        Generate a llm response based on a query
        """
        prompt_template = """Use the context to answer the question. If you don't know the answer,\
        just say that you don't know, don't try to make up an answer. Think step by step.
         
        Context:
        {context}

        Question: {question}
        Answer :"""

        prompt = PromptTemplate(template=prompt_template, input_variables=[
                                "context", "question"])
        chain_type_kwargs = {"prompt": prompt}

        qa_chain = RetrievalQA.from_chain_type(llm=self.llm,
                                               chain_type="stuff",
                                               retriever=retriever,
                                               chain_type_kwargs=chain_type_kwargs,
                                               return_source_documents=True)
        reply = qa_chain(ques)
        answer = reply['result']

        return answer
