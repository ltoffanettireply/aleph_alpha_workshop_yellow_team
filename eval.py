from dotenv import load_dotenv
from pydantic import BaseModel
from collections.abc import Iterable
from typing import Iterable
from statistics import mean
from uuid import uuid4
import requests
import os
from pathlib import Path
import json
import argparse
import sqlglot
from sqlglot.optimizer import optimizer
from sqlglot.optimizer import optimize
import re
import sqlparse
from intelligence_layer.connectors import StudioClient

from intelligence_layer.core import NoOpTracer, Task, TaskSpan

from intelligence_layer.evaluation import (
    Example,
    StudioDatasetRepository,
    AggregationLogic,
    StudioBenchmarkRepository,
    SingleOutputEvaluationLogic,
)

from intelligence_layer.evaluation.dataset.domain import Example
from pharia_skill.testing import DevCsi

import sys
import os
def remove_aliases(sql):
    """
    Remove `AS alias_name` from SELECT clause
    """
    # Use regex to remove "AS alias", accounting for optional whitespace
    return re.sub(r'\s+AS\s+\w+', '', sql, flags=re.IGNORECASE)

def normalize_sql(sql):
    """
    Format and normalize SQL string for comparison
    """
    # First remove aliases
    sql = remove_aliases(sql)

    # Format the SQL consistently
    formatted = sqlparse.format(sql, keyword_case='lower', identifier_case='lower', strip_comments=True, reindent=False)

    # Remove excess whitespace
    return ' '.join(formatted.split())

# Replace this with your target directory
directory = test_data_path = os.path.join(Path(__file__).parent, "text_to_sql_yellow_team", "skill") 

# Convert to absolute path and add to sys.path if not already present
abs_directory = os.path.abspath(directory)
if abs_directory not in sys.path:
    sys.path.insert(0, abs_directory)

from qa import sql_agent
from qa import Input, Output


load_dotenv("text_to_sql_yellow_team/skill/.env")
PHARIA_STUDIO_PROJECT_NAME = "text-to-sql-yellow-team"

studio_client = StudioClient(
    project=PHARIA_STUDIO_PROJECT_NAME,
    studio_url=os.getenv("PHARIA_STUDIO_ADDRESS"),
    auth_token=os.getenv("PHARIA_AI_TOKEN"),
    create_project=True,
)


class QATask(Task[Input, Output]):
    def __init__(self) -> None:
        self.token = os.getenv("PHARIA_AI_TOKEN")
        self.kernel_url = os.getenv("PHARIA_KERNEL_ADDRESS")
        self.skill_namespace = "customer-playground"
        self.skill_name = "text_to_sql_yellow_team_qa"

        self.csi = DevCsi().with_studio(project=PHARIA_STUDIO_PROJECT_NAME)

    def do_run(self, input: Input, task_span: TaskSpan) -> Output:
        return sql_agent(self.csi, input)
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.kernel_url}/v1/skills/{self.skill_namespace}/{self.skill_name}/run"
            response = requests.post(
                url,
                json=input.model_dump() if isinstance(input, BaseModel) else input,
                headers=headers,
            )
            response = response.json()
            print(response)
            return Output(answer=response["answer"])
        except Exception as e:
            print(e)
            return Output(answer=None)
        
class EvaluationExpectedOutput(BaseModel):
        query: str

class QaEvaluation(BaseModel):
    passed: bool
class QaEvaluationLogic(
SingleOutputEvaluationLogic[Input, Output, EvaluationExpectedOutput, QaEvaluation]
):

    def __init__(self) -> None:
        #self.threshold = 0.5  ## Thrershold to define when an evaluation is passed
        return

    def do_evaluate_single_output(
        self, example: Example[Input, EvaluationExpectedOutput], output: Output
    ) -> QaEvaluation:
        output_text = output.answer
        try:
            query1 = output_text
            query2 = example.expected_output.query
            query1 = normalize_sql(query1)
            query2 = normalize_sql(query2)
            expression = optimize(sqlglot.parse_one(query1))
            query1 = optimizer.normalize(expression, dnf=False).sql()
            expression = optimize(sqlglot.parse_one(query2))
            query2 = optimizer.normalize(expression, dnf=False).sql()
            passed = query1 == query2
        except Exception as e:
            passed = output_text==example.expected_output.query

        return QaEvaluation(
            passed=passed,
        )
    
class QaAggregatedEvaluation(BaseModel):
    pass_rate: float
  #  average_match_score: float

class QaAggregationLogic(
    AggregationLogic[
        QaEvaluation,
        QaAggregatedEvaluation,
    ]
):
    def aggregate(self, evaluations: Iterable[QaEvaluation]) -> QaAggregatedEvaluation:
        evaluation_list = list(evaluations)
        if len(evaluation_list) == 0:
            return QaAggregatedEvaluation(
                pass_rate=0.0,
                #average_match_score=0.0,
            )

        passed_count = sum(1 for eval in evaluation_list if eval.passed)
        pass_rate = passed_count / len(evaluation_list)

      #  average_match_score = mean(eval.match_score for eval in evaluation_list)

        return QaAggregatedEvaluation(
            pass_rate=pass_rate,
           # average_match_score=average_match_score,
        )



test_data_path = os.path.join(Path(__file__).parent, "data", "test-data", "examples.json") 
with open(test_data_path) as f:
    test_set = json.load(f)


studio_dataset_repo = StudioDatasetRepository(studio_client=studio_client)

examples = [
    Example(
        input=Input(question=example["question"], db_id=example["db_id"]),
        expected_output=EvaluationExpectedOutput(query=example["query"]),
    )
    for example in test_set
]

studio_dataset = studio_dataset_repo.create_dataset(
    examples=examples, dataset_name="test-dataset-schema"
)

studio_dataset.id


    
aggregation_logic = QaAggregationLogic()
evaluation_logic = QaEvaluationLogic()

benchmark_repository = StudioBenchmarkRepository(studio_client=studio_client)

benchmark = benchmark_repository.create_benchmark(
    dataset_id=studio_dataset.id,
    eval_logic=evaluation_logic,
    aggregation_logic=aggregation_logic,
    name="query-benchmark-16",
    description="This benchmark evaluates the model query creation output and the expected output.",
)

benchmark.id

benchmark = benchmark_repository.get_benchmark(
    benchmark_id=benchmark.id,
    eval_logic=evaluation_logic,
    aggregation_logic=aggregation_logic,
)
task = QATask()
benchmark_execution_id = benchmark.execute(
    task=task,
    name=str(uuid4()),
)