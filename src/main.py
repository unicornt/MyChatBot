from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from tool import get_completion, qa_prompt, memory_prompt
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

if __name__ == '__main__':
    persist_directory = 'mem/'
    chroma_client = chromadb.PersistentClient(path=persist_directory)
    
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/distiluse-base-multilingual-cased-v1")

    user_name = input('请输入你的名字：')
    try:
        collection = chroma_client.get_collection(name=user_name)
    except Exception as e:
        print("Creating new user")
        collection = chroma_client.create_collection(name=user_name, embedding_function=sentence_transformer_ef)

    # collection.add(
    #     documents=["This is a document about engineer", "This is a document about steak"],
    #     metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    #     ids=["id1", "id2"]
    # )

    # results = collection.query(
    #     query_texts=["Which food is the best?"],
    #     n_results=5
    # )
    # print(results)
    memory = ConversationBufferWindowMemory(k=10)
    while True:
        user_input = input('输入：')
        if user_input == 'q':
            break
        # 查询数据库
        results = collection.query(
            query_texts=[user_input],
            n_results=5
        )

        # 生成回复
        completion = get_completion(qa_prompt.format(memory=results, input=user_input))
        print(completion)

        # 生成记忆点并更新到数据库中
        extra_mem = get_completion(memory_prompt.format(input=user_input, history=memory.load_memory_variables({})['history']))
        collection.add(
            documents=[extra_mem],
            metadatas=[{"source": "user"}],
            ids=[datetime.now().strftime("%Y%m%d%H%M%S")]
        )

        # 缓存对话历史
        memory.save_context({"input": user_input}, {"output": completion})