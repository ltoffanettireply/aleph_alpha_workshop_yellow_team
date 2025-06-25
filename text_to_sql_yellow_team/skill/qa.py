from pathlib import Path
from pharia_skill import ChatParams, Csi, Message, skill
from pydantic import BaseModel
import os
from schema import schema


class Input(BaseModel):
    question: str

class Output(BaseModel):
    answer: str | None = None

NAMESPACE = "Studio"
COLLECTION = "papers"
INDEX = "asym-64"

@skill
def sql_agent(csi: Csi, input: Input) -> Output:

    # current_file = Path(__file__).resolve()
    # parent_dir = current_file.parent
    # schema_path = os.path.join(parent_dir, "schema.py")
    # with open(schema_path, "r") as file:
    #     structure = file.read()
    content = f"""Using the provided database structure give a sql query that corresponds to the question.

    DB structure: {schema}
    
    Question: {input.question}
    """
    print("#"*10+"PROMPT"+"#"*10)
    print(content)
    message = Message.user(content)
    params = ChatParams(max_tokens=512)
    response = csi.chat("llama-3.1-8b-instruct", [message], params)
    return Output(answer=response.message.content)
