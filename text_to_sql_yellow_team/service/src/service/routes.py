from fastapi import APIRouter, Depends, HTTPException

import os
from pathlib import Path

from service.dependencies import get_token, with_kernel
from service.kernel import Kernel, KernelException, Skill
from service.models import HealthResponse, QaInput, QaOutput, QueryResults
from service.db_service import SQLiteDatabase

router: APIRouter = APIRouter()


@router.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/qa", response_model=QaOutput)
async def qa(
    request_data: QaInput,
    token: str = Depends(get_token),
    kernel: Kernel = Depends(with_kernel),
) -> QaOutput:
    skill = Skill(namespace="customer-playground", name="text_to_sql_yellow_team_qa")
    try:
        # Run the skill to generate the SQL query
        skill_response = await kernel.run(skill, token, request_data.dict())
        
        # Extract the SQL query from the skill response
        if isinstance(skill_response, dict) and "answer" in skill_response:
            sql_query = skill_response["answer"]
            result = QaOutput(answer=sql_query)
            
            if sql_query:
                try:
                    # Set up the path to the Northwind database
                    root_dir = Path(__file__).parent.parent.parent.parent.parent
                    db_path = os.path.join(
                        root_dir, "data", "northwind-SQLite3", "dist", "northwind.db"
                    )
                    
                    # Execute the query against the local database
                    with SQLiteDatabase(db_path) as db:
                        headers, rows = db.query(sql_query)
                        
                        # Convert tuples to lists and remove the last element from each row for better serialization
                        list_rows = [list(row[:]) for row in rows]
                        
                        # Add the query results to the response
                        result.query_results = QueryResults(headers=headers, rows=list_rows)
                        
                except Exception as db_error:
                    # Add error information to the response if the query execution fails
                    result.query_error = str(db_error)
            
            return result
        else:
            # If the response doesn't have the expected format, return empty response
            return QaOutput()
    except KernelException as exp:
        error_message = ",".join(exp.args)
        if error_message.startswith(
            "Sorry, We could not find the skill you requested in its namespace"
        ):
            error_message += "\n\nPlease check https://docs.aleph-alpha.com/products/pharia-ai/pharia-studio/tutorial/pharia-applications-quick-start/#phariaai-application-skill for instructions on deploying the skill"
        print(error_message)
        raise HTTPException(exp.status_code, error_message) from exp
