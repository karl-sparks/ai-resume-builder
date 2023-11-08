from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from models import ChatMessage

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")

chat_messages = [
    ChatMessage(user="SparksAI", message="Hello!"),
    ChatMessage(user="user", message="Please call me Karl."),
    ChatMessage(user="SparksAI", message="Will do. How can I help you?"),
]


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html", {"request": request, "chat_messages": chat_messages}
    )


@app.post("/ask-ai", response_class=HTMLResponse)
def ask_ai(request: Request, message: str = Form(...)) -> HTMLResponse:
    chat_messages.append(ChatMessage(user="user", message=message))

    return templates.TemplateResponse(
        "chat-messages.html", {"request": request, "chat_messages": chat_messages}
    )
