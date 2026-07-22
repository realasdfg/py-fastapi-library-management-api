from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError

import crud
from database import SessionDep
from schemas import AuthorCreateSchema, AuthorSchema

app = FastAPI()


@app.get("/authors/")
def get_all_authors(session: SessionDep) -> list[AuthorSchema]:
    authors = crud.get_all_authors(session)
    return [AuthorSchema.model_validate(author) for author in authors]


@app.post("/authors/")
def add_author(author_data: AuthorCreateSchema, session: SessionDep) -> AuthorSchema:
    try:
        author = crud.create_author(session=session, data=author_data)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return AuthorSchema.model_validate(author)


@app.get("/authors/{author_id}")
def get_author(author_id: int, session: SessionDep) -> AuthorSchema:
    author = crud.get_author_by_id(session=session, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorSchema.model_validate(author)
