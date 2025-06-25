from pharia_skill import ChatParams, Csi, Message, skill
from pydantic import BaseModel


class Input(BaseModel):
    question: str

class Output(BaseModel):
    answer: str | None = None


@skill
def sql_agent(csi: Csi, input: Input) -> Output:

    with open("schema.txt", "r") as file:
        structure = file.read()
    content = f"""Using the provided database structure give a sql query that corresponds to the question.

DB structure: {structure}

Question: {input.question}

Answer only with the SQL query do not include any other text
"""
    print("#"*10+"PROMPT"+"#"*10)
    print(content)
    message = Message.user(content)
    params = ChatParams(max_tokens=512)
    response = csi.chat("llama-3.1-8b-instruct", [message], params)
    return Output(answer=response.message.content)