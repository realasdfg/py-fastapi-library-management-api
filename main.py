from fastapi import FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError

import crud
from database import SessionDep
from schemas import AuthorCreateSchema, AuthorSchema, PaginatedAuthorsSchema

app = FastAPI()


@app.get("/authors/")
def get_all_authors(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> PaginatedAuthorsSchema:
    authors = crud.get_all_authors(session, skip=skip, limit=limit)
    total = crud.count_authors(session=session)
    return PaginatedAuthorsSchema(
        items=[AuthorSchema.model_validate(author) for author in authors],
        total=total,
        skip=skip,
        limit=limit,
    )


@app.get("/authors/{author_id}")
def get_author(author_id: int, session: SessionDep) -> AuthorSchema:
    author = crud.get_author_by_id(session=session, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorSchema.model_validate(author)


@app.post("/authors/")
def add_author(author_data: AuthorCreateSchema, session: SessionDep) -> AuthorSchema:
    try:
        author = crud.create_author(session=session, data=author_data)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return AuthorSchema.model_validate(author)
