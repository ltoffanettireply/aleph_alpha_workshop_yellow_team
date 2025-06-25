import sys
import os

#Helper function
from pharia_skill.testing import DevCsi
from sql_skill import sql_agent, Input
#from rag_tutorial.skill.qa import IndexPath, Input, custom_rag # Update this with the app name

def test_skill():
    csi = DevCsi().with_studio("rag-tutorial")
    input = Input(
        question="How many suppliers do we have?",
    )
    result = sql_agent(csi, input)
    print("#"*10+"ANSWER"+"#"*10)
    print(result)

if __name__ == "__main__":
    test_skill()