from typing import List, Optional, Annotated
from fastapi import Query, Depends

async def common_parameters_list(
        query:  Optional[List[str]] = Query(None),
        limit: int = Query(9, gt=0, description="Number of records to return"),
        skip: int = Query(0, ge=0, description="Number of records to skip")
):
    return {
        "query": query,
        "limit": limit,
        "skip": skip,
    }

async def common_parameters_str(
        query:  Optional[str] = Query(None, description="Query parameters separated by coma"),
        limit: int = Query(9, gt=0, description="Number of records to return"),
        skip: int = Query(0, ge=0, description="Number of records to skip")
):
    return {
        "query": query,
        "limit": limit,
        "skip": skip,
    }

CommonsDepList = Annotated[dict, Depends(common_parameters_list)]
CommonsDepStr = Annotated[dict, Depends(common_parameters_str)]
