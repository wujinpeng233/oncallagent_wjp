from rag.answer_service import create_chat_model,generate_answer
from rag.context_builder import build_context
from rag.embedding_service import create_embedding_service
from rag.vector_store import create_vector_store,search_documents

def answer_question(question:str)-> dict:
    if not question.strip():
        raise ValueError("问题不能为空")

    embeddings = create_embedding_service()
    vector_store = create_vector_store(embeddings)

    documents = search_documents(vector_store,question,k=3)
    context,citations = build_context(documents)

    chat_model = create_chat_model()
    answer = generate_answer(chat_model,question,context)

    return {
        "answer": answer,
        "citations": citations,
    }
