from pathlib import Path
from pharia_skill import ChatParams, Csi, IndexPath, Message, skill
from pydantic import BaseModel
from db_service import SQLiteDatabase
import os
# TODO: If you have used custom names for these values in the Data Setup step, please use these here
#NAMESPACE = "Studio" #Document Index Namespace, won't change
#COLLECTION = "pharia-tutorial-rag"
#INDEX = "rag-tutorial-index"


class Input(BaseModel):
    question: str

class Output(BaseModel):
    answer: str | None = None

NAMESPACE = "Studio"
COLLECTION = "papers"
INDEX = "asym-64"


@skill
def sql_agent(csi: Csi, input: Input) -> Output:

    parent_dir = Path(__file__).parent.parent
    path_to_db = os.path.join(
        parent_dir, "data", "northwind-SQLite3", "dist", "northwind.db"
    )
    print(path_to_db)
    db = SQLiteDatabase(path_to_db)
    structure = db.structure()
    content = f"""Using the provided database structure give a sql query that corresponds to the question.

DB structure: {structure}

Question: {input.question}
"""
    print("#"*10+"PROMPT"+"#"*10)
    print(content)
    message = Message.user(content)
    params = ChatParams(max_tokens=512)
    response = csi.chat("llama-3.1-8b-instruct", [message], params)
    return Output(answer=response.message.content)
