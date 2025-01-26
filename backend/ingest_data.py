# ingest_data.py
import asyncio
from database import get_db
from models import Material
from sqlalchemy.future import select
from langchain.schema import Document  # Updated import statement
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vectorstore import create_vectorstore
import os

async def ingest():
    # Load materials from database
    async for session in get_db():
        result = await session.execute(select(Material))
        materials = result.scalars().all()

    docs = []
    for material in materials:
        doc = Document(
            page_content=material.content,
            metadata={'course_id': material.course_id, 'title': material.title}
        )
        docs.append(doc)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    # Create vector store
    create_vectorstore(split_docs)
    print("Vector store created successfully.")

if __name__ == "__main__":
    asyncio.run(ingest())
