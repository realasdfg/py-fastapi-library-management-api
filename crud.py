from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

import models
from models import Author
from schemas import AuthorCreateSchema


def get_all_authors(session: Session) -> Sequence[models.Author]:
    stmt = select(models.Author)
    return session.execute(stmt).scalars().all()


def get_author_by_id(session: Session, author_id: int) -> type[Author] | None:
    return session.get(models.Author, author_id)


def create_author(session: Session, data: AuthorCreateSchema) -> models.Author:
    author = models.Author(**data.model_dump())
    session.add(author)
    session.commit()
    session.refresh(author)
    return author
