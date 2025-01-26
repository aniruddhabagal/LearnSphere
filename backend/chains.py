# chains.py
from ollama_llm import OllamaLLM
from vectorstore import load_vectorstore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def get_chain(course_id: int):
    # Load the vectorstore
    vectorstore = load_vectorstore()
    if vectorstore is None:
        raise Exception("Vector store not found. Please run the ingestion script first.")

    # Filter documents based on course_id
    def filter_func(doc):
        return doc['metadata'].get('course_id') == course_id

    retriever = vectorstore.as_retriever(
        search_kwargs={'k': 3},
        search_type='similarity',
        search_function_kwargs={'filter': filter_func}
    )

    # Initialize LLM
    llm = OllamaLLM(model_name='deepseek-r1:1.5b')

    # Define prompt
    prompt_template = PromptTemplate(
        input_variables=['context', 'question'],
        template="""
Use the following context to answer the question at the end.
If you don't know the answer, say "I don't know".
Keep the answer concise (3-4 sentences).

Context:
{context}

Question:
{question}

Answer:"""
    )

    # Create the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        chain_type_kwargs={'prompt': prompt_template}
    )

    return qa_chain
