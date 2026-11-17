"""StockGuard 1.0 — 9 endpoints para implementar (sem solução pronta)."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from .db import initialize
from .schemas import ItemCreate, ItemPatch, ItemOut, MovementCreate, MovementOut, AlertOut, ScanResult, HelpRequest, HelpResponse
import sqlite3
from .db import db_session
from .help_service import generate_help

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield

app = FastAPI(title="StockGuard 1.0 — Avaliação", version="1.0.0", lifespan=lifespan)

@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate):
    try:
        with db_session() as db:
            cursor = db.execute(
                """
                INSERT INTO items
                    (sku, name, stock, min_stock, unit, location)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.sku,
                    payload.name,
                    payload.stock,
                    payload.min_stock,
                    payload.unit,
                    payload.location,
                ),
            )

            item = db.execute(
                "SELECT * FROM items WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()

            return dict(item)

    except sqlite3.IntegrityError as error:
        if "UNIQUE constraint failed: items.sku" in str(error):
            raise HTTPException(
                status_code=409,
                detail="Já existe um produto com este SKU",
            ) from error

        raise

@app.get("/items", response_model=list[ItemOut])
def list_items():
    with db_session() as db:
        items = db.execute(
            "SELECT * FROM items ORDER BY id"
        ).fetchall()

        return [dict(item) for item in items]

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    with db_session() as db:
        item = db.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        return dict(item)


# TODO 4: PATCH /items/{item_id}: editar metadados, NÃO editar saldo diretamente
@app.patch("/items/{item_id}", response_model=ItemOut)
def patch_item(item_id: int, payload: ItemPatch):
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=422,
            detail="Nenhum campo informado para atualização"
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="Os campos não podem receber null"
        )

    allowed_fields = {
        "sku", "name", "min_stock", "unit", "location"
    }

    if not set(changes).issubset(allowed_fields):
        raise HTTPException(
            status_code=422,
            detail="Campo não permitido"
        )

    for field in ("sku", "name", "unit", "location"):
        if field in changes:
            changes[field] = changes[field].strip()

            if not changes[field]:
                raise HTTPException(
                    status_code=422,
                    detail=f"O campo {field} não pode estar vazio"
                )

    with db_session() as db:
        item = db.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        assignments = ", ".join(
            f"{field} = ?" for field in changes
        )

        values = list(changes.values()) + [item_id]

        try:
            db.execute(
                f"UPDATE items SET {assignments} WHERE id = ?",
                values,
            )
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: items.sku" in str(error):
                raise HTTPException(
                    status_code=409,
                    detail="Já existe um produto com este SKU"
                ) from error
            raise

        updated_item = db.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()

        return dict(updated_item)



@app.post(
    "/items/{item_id}/movements",
    response_model=MovementOut,
    status_code=201
)
def add_movement(item_id: int, payload: MovementCreate):
    with db_session() as db:
        # Inicia uma transação de escrita.
        db.execute("BEGIN IMMEDIATE")

        # Consulta o produto.
        item = db.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        stock_before = item["stock"]

        # Calcula o novo saldo.
        if payload.type == "IN":
            stock_after = stock_before + payload.quantity

        elif payload.type == "OUT":
            if payload.quantity > stock_before:
                raise HTTPException(
                    status_code=409,
                    detail="Estoque insuficiente"
                )

            stock_after = stock_before - payload.quantity

        else:  # ADJUST
            stock_after = payload.quantity

        # Atualiza o saldo do produto.
        db.execute(
            "UPDATE items SET stock = ? WHERE id = ?",
            (stock_after, item_id),
        )

        # Registra a movimentação.
        cursor = db.execute(
            """
            INSERT INTO movements (
                item_id,
                type,
                quantity,
                stock_before,
                stock_after,
                reason
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                payload.type,
                payload.quantity,
                stock_before,
                stock_after,
                payload.reason,
            ),
        )

        # Recupera a movimentação registrada.
        movement = db.execute(
            "SELECT * FROM movements WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

        return dict(movement)



@app.get(
    "/items/{item_id}/movements",
    response_model=list[MovementOut]
)
def get_movements(item_id: int):
    with db_session() as db:
        # Verifica se o produto existe.
        item = db.execute(
            "SELECT id FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        # Consulta o histórico do produto.
        movements = db.execute(
            """
            SELECT *
            FROM movements
            WHERE item_id = ?
            ORDER BY id ASC
            """,
            (item_id,),
        ).fetchall()

        return [dict(movement) for movement in movements]



@app.post("/automation/check", response_model=ScanResult)
def automation_check():
    opened = 0
    resolved = 0

    with db_session() as db:
        db.execute("BEGIN IMMEDIATE")

        # Consulta todos os produtos.
        items = db.execute(
            "SELECT id, stock, min_stock FROM items"
        ).fetchall()

        for item in items:
            item_id = item["id"]
            stock = item["stock"]
            min_stock = item["min_stock"]

            # Procura um alerta aberto para o produto.
            alert = db.execute(
                """
                SELECT id
                FROM alerts
                WHERE item_id = ? AND status = 'OPEN'
                """,
                (item_id,),
            ).fetchone()

            if stock <= min_stock:
                # Abre alerta somente se ainda não existir.
                if alert is None:
                    db.execute(
                        """
                        INSERT INTO alerts (item_id, status)
                        VALUES (?, 'OPEN')
                        """,
                        (item_id,),
                    )
                    opened += 1

            else:
                # Resolve alerta quando o estoque normaliza.
                if alert is not None:
                    db.execute(
                        """
                        UPDATE alerts
                        SET status = 'RESOLVED',
                            resolved_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (alert["id"],),
                    )
                    resolved += 1

    return ScanResult(opened=opened, resolved=resolved)



@app.get("/alerts", response_model=list[AlertOut])
def list_alerts(
    alert_status: str | None = Query(
        default=None,
        pattern="^(OPEN|RESOLVED)$"
    )
):
    with db_session() as db:

        if alert_status is None:
            alerts = db.execute(
                """
                SELECT *
                FROM alerts
                ORDER BY id ASC
                """
            ).fetchall()

        else:
            alerts = db.execute(
                """
                SELECT *
                FROM alerts
                WHERE status = ?
                ORDER BY id ASC
                """,
                (alert_status,),
            ).fetchall()

        return [dict(alert) for alert in alerts]



@app.post("/help", response_model=HelpResponse)
def help_endpoint(payload: HelpRequest):
    return generate_help(
        question=payload.question,
        max_sources=payload.max_sources
    )

