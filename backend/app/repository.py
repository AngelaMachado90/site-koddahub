from datetime import datetime, timezone
from psycopg.errors import UniqueViolation
from .identity import Identity


TICKET_SELECT = """
SELECT t.id, t.reference_code, t.product_id, p.name AS product_name,
       t.title, t.status, t.priority, t.created_at, t.updated_at, t.closed_at
FROM tickets t JOIN products p ON p.id = t.product_id
"""


def products(connection, identity: Identity):
    return connection.execute("""
        SELECT p.id, p.name, p.slug
        FROM organization_products op JOIN products p ON p.id = op.product_id
        WHERE op.organization_id = %s AND op.status = 'active' AND p.status = 'active'
        ORDER BY p.name, p.id
    """, (identity.organization_id,)).fetchall()


def tickets(connection, identity: Identity, limit: int):
    return connection.execute(TICKET_SELECT + """
        WHERE t.organization_id = %s
        ORDER BY t.updated_at DESC, t.id DESC LIMIT %s
    """, (identity.organization_id, limit)).fetchall()


def ticket(connection, identity: Identity, ticket_id: int):
    return connection.execute(TICKET_SELECT + """
        WHERE t.organization_id = %s AND t.id = %s
    """, (identity.organization_id, ticket_id)).fetchone()


def _validate_context(connection, identity: Identity, product_id: int):
    return connection.execute("""
        SELECT 1
        FROM organizations o
        JOIN organization_members om ON om.organization_id = o.id
        JOIN users u ON u.id = om.user_id
        JOIN organization_products op ON op.organization_id = o.id
        JOIN products p ON p.id = op.product_id
        WHERE o.id = %s AND om.user_id = %s AND op.product_id = %s
          AND o.status = 'active' AND om.status = 'active' AND u.status = 'active'
          AND op.status = 'active' AND p.status = 'active'
    """, (identity.organization_id, identity.user_id, product_id)).fetchone()


def create_ticket(connection, identity: Identity, payload):
    if not _validate_context(connection, identity, payload.product_id):
        return None
    year = datetime.now(timezone.utc).year
    connection.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (f"ticket-reference-{year}",))
    sequence = connection.execute("""
        SELECT COALESCE(MAX((regexp_match(reference_code, %s))[1]::bigint), 0) + 1 AS value
        FROM tickets WHERE reference_code LIKE %s
    """, (rf"^KDH-{year}-([0-9]+)$", f"KDH-{year}-%")).fetchone()["value"]
    reference_code = f"KDH-{year}-{sequence:06d}"
    row = connection.execute("""
        INSERT INTO tickets (reference_code, organization_id, product_id, created_by_user_id, title, priority)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    """, (reference_code, identity.organization_id, payload.product_id, identity.user_id, payload.title, payload.priority)).fetchone()
    connection.execute("INSERT INTO ticket_messages (ticket_id, author_user_id, body) VALUES (%s, %s, %s)", (row["id"], identity.user_id, payload.message))
    connection.execute("INSERT INTO ticket_events (ticket_id, actor_user_id, event_type, metadata) VALUES (%s, %s, 'created', '{}'::jsonb)", (row["id"], identity.user_id))
    return ticket(connection, identity, row["id"])


def messages(connection, identity: Identity, ticket_id: int):
    if not ticket(connection, identity, ticket_id):
        return None
    return connection.execute("""
        SELECT m.id, m.ticket_id, m.author_user_id, u.name AS author_name, m.body, m.created_at
        FROM ticket_messages m JOIN users u ON u.id = m.author_user_id
        WHERE m.ticket_id = %s ORDER BY m.created_at, m.id
    """, (ticket_id,)).fetchall()


def create_message(connection, identity: Identity, ticket_id: int, body: str):
    if not ticket(connection, identity, ticket_id):
        return None
    row = connection.execute("""
        INSERT INTO ticket_messages (ticket_id, author_user_id, body)
        VALUES (%s, %s, %s) RETURNING id
    """, (ticket_id, identity.user_id, body)).fetchone()
    connection.execute("UPDATE tickets SET updated_at = CURRENT_TIMESTAMP WHERE id = %s", (ticket_id,))
    return connection.execute("""
        SELECT m.id, m.ticket_id, m.author_user_id, u.name AS author_name, m.body, m.created_at
        FROM ticket_messages m JOIN users u ON u.id = m.author_user_id WHERE m.id = %s
    """, (row["id"],)).fetchone()


def events(connection, identity: Identity, ticket_id: int):
    if not ticket(connection, identity, ticket_id):
        return None
    return connection.execute("""
        SELECT e.id, e.ticket_id, e.actor_user_id, u.name AS actor_name,
               e.event_type, e.metadata, e.created_at
        FROM ticket_events e LEFT JOIN users u ON u.id = e.actor_user_id
        WHERE e.ticket_id = %s ORDER BY e.created_at, e.id
    """, (ticket_id,)).fetchall()
