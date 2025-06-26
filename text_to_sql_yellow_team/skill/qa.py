from pathlib import Path
from pharia_skill import ChatParams, Csi, Message, skill
from pydantic import BaseModel
import os
from schema import schema
from eval_schemas import car_1, concert_singer, employee_hire_evaluation, flight_2, pets_1


class Input(BaseModel):
    question: str
    db_id: str | None = None

class Output(BaseModel):
    answer: str | None = None

NAMESPACE = "Studio"
COLLECTION = "papers"
INDEX = "asym-64"

@skill
def sql_agent(csi: Csi, input: Input) -> Output:

    if input.db_id == None:
        db_schema = schema
    else:
        db_schema = globals()[input.db_id]
    content = f"""Using the provided database structure give a sql query that corresponds to the question.

    DB structure: {db_schema}
    
    Question: {input.question}
    
    give only the sql query nothing else
    The answer should look like this "SELECT..."
    """
    message = Message.user(content)
    params = ChatParams(max_tokens=512)
    response = csi.chat("llama-3.3-70b-instruct", [message], params)
    response_text = response.message.content
    response_text = response_text.replace("sql","").replace("\n","").replace('```', '')
    return Output(answer=response_text)
