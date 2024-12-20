

from fastapi import APIRouter



router = APIRouter(
    prefix="/test/v1",
    tags=['tests'],
    responses={404: {"description" : "Nother here bwaii"}}
)


@router.get("/")
async def readTest():
    return {"Message" : "Lets gooooo "}