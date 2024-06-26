from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi.responses import RedirectResponse
from dotenv import dotenv_values
import httpx

from models import User, Board, CardList, Card
from api import user, login, google, github, cardlist, card, board, delete, openapi

# Tags for organizing Swagger UI

tags_metadata = [
    {"name": "User"},
    {"name": "Board"},
    {"name": "Card"},
    {"name": "CardList"},
    {"name": "GitHub Login"},
    {"name": "Standard Login"}
]

router = APIRouter()

config = dotenv_values(".env")
github_client_id = config["GITHUB_CLIENT_ID"]
github_client_secret = config["GITHUB_CLIENT_SECRET"]

# User manipulation 

@router.post("/user/create", response_model=User, tags=["User"])
async def user_create(request: Request, user_item: User):
    return await user.user_create(request, user_item)

@router.get("/user/get", response_model=User, tags=["User"])
async def user_get(request: Request, id: str):
    return await user.user_get(request, id)

@router.delete("/user/delete", tags=["User"])
async def user_delete(request: Request, id: str):
    await user.user_delete(request, id)

@router.post("/user/update", response_model=User, tags=["User"])
async def user_update(request: Request, user_item: User):
    return await user.user_update(request, user_item)

@router.post("/user/update/field", tags=["User"])
async def update_user_field(request: Request, user_id: str, field_name: str, new_value):
    return await user.update_user_field(request, user_id, field_name, new_value)

@router.get("/user/get/all", response_model=List[str], tags=["User"])
async def user_get_all(request: Request):
    return await user.user_get_all(request)

# Board manipulation

@router.post("/board/create", response_model=Board, tags=["Board"])
async def board_create(request: Request, board_item: Board):
    return await board.board_create(request, board_item)

@router.get("/board/get", tags=["Board"])
async def board_get(request: Request, id: str):
    return await board.board_get(request, id)

@router.delete("/board/delete", tags=["Board"])
async def board_delete(request: Request, id: str):
    await delete.board_delete(request, id)

@router.post("/board/update", response_model=Board, tags=["Board"])
async def board_update(request: Request, board_item: Board):
    return await board.board_update(request, board_item)

@router.post("/board/update/field", tags=["Board"])
async def update_board_field(request: Request, board_id: str, field_name: str, new_value):
    return await board.update_board_field(request, board_id, field_name, new_value)

@router.get("/board/get/users", response_model=List[Board], tags=["Board"])
async def board_get_users(request: Request, user_id: str):
    return await board.board_get_users(request, user_id)

@router.post("/board/invite", tags=["Board"])
async def invite(request: Request, user_id: str, board_id: str):
    return await board.invite(request, user_id, board_id)

# Card manipulation

@router.post("/card/create", response_model=Card, tags=["Card"])
async def card_create(request: Request, card_item: Card):
    return await card.card_create(request, card_item)

@router.get("/card/get", tags=["Card"])
async def card_get(request: Request, id: str):
    return await card.card_get(request, id)

@router.delete("/card/delete", tags=["Card"])
async def card_delete(request: Request, id: str):
    await delete.card_delete(request, id)

@router.post("/card/update", response_model=Card, tags=["Card"])
async def card_update(request: Request, card_item: Card):
    return await card.card_update(request, card_item)

@router.post("/card/update/field", tags=["Card"])
async def update_card_field(request: Request, card_id: str, field_name: str, new_value):
    return await card.update_card_field(request, card_id, field_name, new_value)

@router.get("/card/get/cardlists", response_model=List[Card], tags=["Card"])
async def card_get_cardlists(request: Request, cardlist_id: str):
    return await card.card_get_cardlists(request, cardlist_id)

@router.post("/card/move", tags=["Card"])
async def card_move(request: Request, card_id: str, old_list_id: str, new_list_id: str = None, target_position: int = None):
    return await card.card_move(request, card_id, old_list_id, new_list_id, target_position)

# CardList manipulation

@router.post("/cardlist/create", response_model=CardList, tags=["CardList"])
async def cardlist_create(request: Request, cardlist_item: CardList):
    return await cardlist.cardlist_create(request, cardlist_item)

@router.get("/cardlist/get", tags=["CardList"])
async def cardlist_get(request: Request, id: str):
    return await cardlist.cardlist_get(request, id)

@router.delete("/cardlist/delete", tags=["CardList"])
async def cardlist_delete(request: Request, id: str):
    await delete.cardlist_delete(request, id)

@router.post("/cardlist/update", response_model=CardList, tags=["CardList"])
async def cardlist_update(request: Request, cardlist_item: CardList):
    return await cardlist.cardlist_update(request, cardlist_item)

@router.post("/cardlist/update/field", tags=["CardList"])
async def update_cardlist_field(request: Request, cardlist_id: str, field_name: str, new_value):
    return await cardlist.update_cardlist_field(request, cardlist_id, field_name, new_value)

@router.get("/cardlist/get/boards", response_model=List[CardList], tags=["CardList"])
async def cardlist_get_boards(request: Request, board_id: str):
    return await cardlist.cardlist_get_boards(request, board_id)

# GitHub Login

@router.get("/github/login", tags=["GitHub Login"])
def login_with_github(request: Request):
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@router.get("/login/callback", tags=["GitHub Login"])
async def login_callback(request: Request, code: str):
    return await github.login_callback(request, code)

@router.get("/github/get/user", tags=["GitHub Login"])
async def get_github_user_data(request: Request, access_token: str):
    return await github.github_authorize_url(request, access_token)

# Standard Login 

@router.post("/login", tags=["Standard Login"])
async def cred_get(request: Request, email: str, password: str):
    return await login.cred_get(request, email, password)

# Google Login held within google.py

# OpenAI

@router.post("/openapi/dejargon", tags=["OpenAI APIs"])
async def translate_jargon(request: Request, description: str):
    return await openapi.translate_jargon(request, description)

@router.post("/openapi/title", tags=["OpenAI APIs"])
async def suggest_title(request: Request, description: str):
    return await openapi.suggest_title(request, description)

@router.post("/openapi/tags", tags=["OpenAI APIs"])
async def generate_tags(request: Request, description: str):
    return await openapi.generate_tags(request, description)