from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, author, book, loan

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(author.router, prefix="/authors", tags=["authors"])
api_router.include_router(loan.router, prefix="/loan", tags=["loan"])
