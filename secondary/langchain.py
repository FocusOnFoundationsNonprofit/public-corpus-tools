import os
from pinecone import Pinecone as PineconePinecone

from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain

from secondary.streamlit_bots.streamlit_prompts import CONDENSE_QUESTION_PROMPT

from primary.rag_prompts_routes import *
from config import PINECONE_API_KEY, OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # reconsider where we are getting the openai api keys

#DEFAULT_LLM_MODEL = 'gpt-4-turbo'
DEFAULT_LLM_MODEL = 'gpt-4o'
pc = PineconePinecone(api_key=PINECONE_API_KEY)  # 'pc' is the standard convention so we'll keep it despite it being unclear

# first version of qrag and similar to call_vrag_chat_langchain but using langchain load_qa_chain
# from before qrag_routing work
# not sure if it was tested and worked at all because we moved to routing
def call_qrag_chat_langchain(question, prompt_template, index_name, llm_model=DEFAULT_LLM_MODEL):
    """
    Initiates a chat session using question retrieval augmented generation (QRAG) with a specified question, prompt template, and index name.

    :param question: string of the question to initiate the chat with.
    :param prompt_template: string of the template used to format the chat prompt.
    :param index_name: string of the name of the pinecone index to use for retrieval.
    :return: dictionary containing the chat response and metadata.
    """
    # Actual QRAG chatbot function,  give question and return response and metadata from bot
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore = PineconeVectorStore(index, embeddings, text_key="ANSWER")
    # Setting up chat model and retrieval QA chain. Use max marginal relevance search to increase diversity of results.
    llm = ChatOpenAI(model_name = llm_model, temperature=0)
    retriever = vectorstore.as_retriever(search_type="mmr")

    QA_PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(chain_type="stuff", prompt=QA_PROMPT, llm=llm, verbose=True)
    chat_history = ''
    qa_chain = ConversationalRetrievalChain(
        retriever=retriever,
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
        return_source_documents=True,
    )
    result = qa_chain({"question": question, "chat_history": chat_history})
    # result = qa_chain
    return result

# from before refactor into qrag_routing_and_llm_OLD (renamed from qrag_sim_routed)
def call_sim_routed_qrag_chat_langchain(question, prompt_dict, index_name, llm_model=DEFAULT_LLM_MODEL):
    """
    Initiates a chat session using question retrieval augmented generation (QRAG) with a specified question and index name, dynamically selecting the prompt template based on similarity scores.

    :param question: string of the question to initiate the chat with.
    :param index_name: string of the name of the pinecone index to use for retrieval.
    :return: dictionary containing the chat response and metadata.
    """
    # Actual QRAG chatbot function, give question and return response and metadata from bot
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore = PineconeVectorStore(index, embeddings, text_key="ANSWER")
    # Setting up chat model and retrieval QA chain. Use max marginal relevance search to increase diversity of results.
    llm = ChatOpenAI(model_name=llm_model, temperature=0)
    retriever = vectorstore.as_retriever(search_type="mmr")
    

    # Retrieve documents and similarity scores
    retrieved_docs, scores = retriever.retrieve(question, return_scores=True)
    # Select prompt template based on the highest similarity score

    if scores and max(scores) > 0.8: 
        prompt_template = prompt_dict['prompt_template_route3']
        # streamlit_bots.prompts.prompt_template_route1
    elif scores and max(scores) > 0.5: #
        prompt_template = prompt_dict['prompt_template_route2']
        # streamlit_bots.prompts.prompt_template_route2
    else:
        prompt_template = prompt_dict['prompt_template_route1']
        # streamlit_bots.prompts.prompt_template_route3

    QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(chain_type="stuff", prompt=QA_PROMPT, llm=llm, verbose=True)
    chat_history = ''
    qa_chain = ConversationalRetrievalChain(
        retriever=retriever,
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
        return_source_documents=True,
    )
    chat_result = qa_chain({"question": question, "chat_history": chat_history})
    return chat_result


