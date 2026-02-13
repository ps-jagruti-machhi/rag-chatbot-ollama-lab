# import basics
import os
from dotenv import load_dotenv

# import streamlit
import streamlit as st

# import langchain
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# load environment variables
load_dotenv()  

###############################   INITIALIZE EMBEDDINGS MODEL  #################################################################################################

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

###############################   INITIALIZE CHROMA VECTOR STORE   #############################################################################################

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"), 
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})


###############################   INITIALIZE CHAT MODEL   #######################################################################################################

llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0
)


###############################   CREATE RAG CHAIN   ###########################################################################################################

def format_docs(docs):
    """Format retrieved documents for display."""
    serialized = ""
    for doc in docs:
        serialized += f"Source: {doc.metadata['source']}\nContent: {doc.page_content}\n\n"
    return serialized

# Create the RAG prompt template (for when context is available)
rag_template = """You are a helpful assistant. You will be provided with a query and retrieved context.
Your task is to provide a response based on the retrieved information.

The query is as follows:
{query}

The retrieved context is as follows:
{context}

Please provide a concise and informative response based on the retrieved information.

For every piece of information you provide, also provide the source.

Return text as follows:

<Answer to the question>
Source: source_url
"""

rag_prompt = ChatPromptTemplate.from_template(rag_template)

# Create the general knowledge prompt template (for when no context is available)
general_template = """You are a helpful assistant. Answer the user's question to the best of your ability.

The query is as follows:
{query}

Provide a clear and informative response. Since this is a general knowledge question (not from your knowledge base), you don't need to provide a source.
"""

general_prompt = ChatPromptTemplate.from_template(general_template)

# Create the RAG chain
rag_chain = (
    {"context": retriever | format_docs, "query": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Create the general knowledge chain
general_chain = (
    {"query": RunnablePassthrough()}
    | general_prompt
    | llm
    | StrOutputParser()
)


###############################   INITIATE STREAMLIT APP   ####################################################################################################

st.set_page_config(page_title="RAG Chatbot", page_icon="🦜")
st.title("🦜 RAG Chatbot")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


# create the bar where we can type messages
user_question = st.chat_input("How are you?")


# did the user submit a prompt?
if user_question:

    # add the message from the user (prompt) to the screen with streamlit
    with st.chat_message("user"):
        st.markdown(user_question)

        st.session_state.messages.append(HumanMessage(user_question))

    # invoking the chain
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # First, retrieve documents to check if relevant context exists
        retrieved_docs = retriever.invoke(user_question)
        
        # Check if we have relevant context
        # We consider context relevant if we have documents with meaningful content
        has_relevant_context = False
        context_text = ""
        
        if retrieved_docs:
            context_text = format_docs(retrieved_docs)
            # Check if context has meaningful content (not just empty or very short)
            if context_text and len(context_text.strip()) > 50:
                has_relevant_context = True
        
        # Use appropriate chain based on whether we have relevant context
        if has_relevant_context:
            ai_message = rag_chain.invoke(user_question)
        else:
            ai_message = general_chain.invoke(user_question)
        
        response_placeholder.markdown(ai_message)
        st.session_state.messages.append(AIMessage(ai_message))
