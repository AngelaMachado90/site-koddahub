import logging
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .db import connect, transaction
from .identity import Identity, get_current_identity
from . import repository
from .schemas import EventOut, MessageCreate, MessageOut, ProductOut, TicketCreate, TicketOut

logger = logging.getLogger("support-api")
settings = get_settings()
app = FastAPI(title="KoddaHub Support API", docs_url=None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.get("/health")
def health():
    try:
        with connect() as connection:
            connection.execute("SELECT 1").fetchone()
    except Exception:
        logger.warning("Database health check failed")
        raise HTTPException(status_code=503, detail="Service unavailable")
    return {"status": "ok", "database": "ok"}


@app.get("/api/products", response_model=list[ProductOut])
def list_products(identity: Identity = Depends(get_current_identity)):
    with connect() as connection:
        return repository.products(connection, identity)


@app.get("/api/tickets", response_model=list[TicketOut])
def list_tickets(limit: int = Query(50, ge=1, le=100), identity: Identity = Depends(get_current_identity)):
    with connect() as connection:
        return repository.tickets(connection, identity, limit)


@app.get("/api/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, identity: Identity = Depends(get_current_identity)):
    with connect() as connection:
        result = repository.ticket(connection, identity, ticket_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result


@app.post("/api/tickets", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def post_ticket(payload: TicketCreate, identity: Identity = Depends(get_current_identity)):
    with transaction() as connection:
        result = repository.create_ticket(connection, identity, payload)
    if not result:
        raise HTTPException(status_code=400, detail="Product or development identity is not available")
    return result


@app.get("/api/tickets/{ticket_id}/messages", response_model=list[MessageOut])
def list_messages(ticket_id: int, identity: Identity = Depends(get_current_identity)):
    with connect() as connection:
        result = repository.messages(connection, identity, ticket_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result


@app.post("/api/tickets/{ticket_id}/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def post_message(ticket_id: int, payload: MessageCreate, identity: Identity = Depends(get_current_identity)):
    with transaction() as connection:
        result = repository.create_message(connection, identity, ticket_id, payload.body)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result


@app.get("/api/tickets/{ticket_id}/events", response_model=list[EventOut])
def list_events(ticket_id: int, identity: Identity = Depends(get_current_identity)):
    with connect() as connection:
        result = repository.events(connection, identity, ticket_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result
