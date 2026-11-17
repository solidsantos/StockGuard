
"""Testes automatizados da API StockGuard 1.0."""


def test_create_item(client):
    response = client.post(
        "/items",
        json={
            "sku": "TESTE-001",
            "name": "Produto de teste",
            "stock": 10,
            "min_stock": 5,
            "unit": "UN",
            "location": "A1"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["sku"] == "TESTE-001"
    assert data["name"] == "Produto de teste"
    assert data["stock"] == 10
    assert data["min_stock"] == 5
    assert isinstance(data["id"], int)


def test_create_item_duplicate_sku(client):
    item = {
        "sku": "PROD-001",
        "name": "Produto original",
        "stock": 10,
        "min_stock": 5
    }

    first = client.post("/items", json=item)

    duplicate = client.post(
        "/items",
        json={
            "sku": "prod-001",
            "name": "Produto duplicado",
            "stock": 20,
            "min_stock": 5
        }
    )

    assert first.status_code == 201
    assert duplicate.status_code == 409


def test_create_item_negative_stock(client):
    response = client.post(
        "/items",
        json={
            "sku": "PROD-002",
            "name": "Produto inválido",
            "stock": -5,
            "min_stock": 2
        }
    )

    assert response.status_code == 422


def test_list_items(client):
    client.post(
        "/items",
        json={
            "sku": "PROD-003",
            "name": "Mouse",
            "stock": 10,
            "min_stock": 3
        }
    )

    client.post(
        "/items",
        json={
            "sku": "PROD-004",
            "name": "Teclado",
            "stock": 5,
            "min_stock": 2
        }
    )

    response = client.get("/items")

    assert response.status_code == 200

    items = response.json()

    assert len(items) == 2
    assert items[0]["sku"] == "PROD-003"
    assert items[1]["sku"] == "PROD-004"


def test_get_item_by_id(client):
    created = client.post(
        "/items",
        json={
            "sku": "PROD-005",
            "name": "Monitor",
            "stock": 8,
            "min_stock": 2
        }
    )

    assert created.status_code == 201

    item_id = created.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == "Monitor"


def test_get_item_not_found(client):
    response = client.get("/items/99999")

    assert response.status_code == 404


def test_list_items_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_patch_item(client):
    created = client.post(
        "/items",
        json={
            "sku": "PATCH-001",
            "name": "Mouse",
            "stock": 10,
            "min_stock": 3
        }
    )

    item_id = created.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={
            "name": "Mouse Gamer",
            "min_stock": 5,
            "location": "B2"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Mouse Gamer"
    assert data["min_stock"] == 5
    assert data["location"] == "B2"
    assert data["stock"] == 10


def test_patch_cannot_change_stock(client):
    created = client.post(
        "/items",
        json={
            "sku": "PATCH-002",
            "name": "Teclado",
            "stock": 10
        }
    )

    item_id = created.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={"stock": 100}
    )

    assert response.status_code == 422

    item = client.get(f"/items/{item_id}").json()

    assert item["stock"] == 10


def test_patch_item_not_found(client):
    response = client.patch(
        "/items/99999",
        json={"name": "Produto inexistente"}
    )

    assert response.status_code == 404


def test_patch_duplicate_sku(client):
    client.post(
        "/items",
        json={"sku": "SKU-A", "name": "Produto A"}
    )

    second = client.post(
        "/items",
        json={"sku": "SKU-B", "name": "Produto B"}
    )

    item_id = second.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={"sku": "sku-a"}
    )

    assert response.status_code == 409


def test_movement_in(client):
    created = client.post(
        "/items",
        json={
            "sku": "MOV-IN",
            "name": "Monitor",
            "stock": 10
        }
    )

    item_id = created.json()["id"]

    response = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "IN",
            "quantity": 5,
            "reason": "Recebimento"
        }
    )

    assert response.status_code == 201

    movement = response.json()

    assert movement["stock_before"] == 10
    assert movement["stock_after"] == 15

    item = client.get(f"/items/{item_id}").json()

    assert item["stock"] == 15


def test_movement_out(client):
    created = client.post(
        "/items",
        json={
            "sku": "MOV-OUT",
            "name": "Mouse",
            "stock": 10
        }
    )

    item_id = created.json()["id"]

    response = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "OUT",
            "quantity": 4,
            "reason": "Venda"
        }
    )

    assert response.status_code == 201
    assert response.json()["stock_before"] == 10
    assert response.json()["stock_after"] == 6

    item = client.get(f"/items/{item_id}").json()

    assert item["stock"] == 6


def test_movement_adjust(client):
    created = client.post(
        "/items",
        json={
            "sku": "MOV-ADJUST",
            "name": "Teclado",
            "stock": 10
        }
    )

    item_id = created.json()["id"]

    response = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "ADJUST",
            "quantity": 3,
            "reason": "Inventário"
        }
    )

    assert response.status_code == 201
    assert response.json()["stock_before"] == 10
    assert response.json()["stock_after"] == 3

    item = client.get(f"/items/{item_id}").json()

    assert item["stock"] == 3


def test_movement_insufficient_stock_is_atomic(client):
    created = client.post(
        "/items",
        json={
            "sku": "MOV-ATOMIC",
            "name": "Produto de teste",
            "stock": 5
        }
    )

    item_id = created.json()["id"]

    response = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "OUT",
            "quantity": 20,
            "reason": "Saída inválida"
        }
    )

    assert response.status_code == 409

    # O estoque deve permanecer inalterado.
    item = client.get(f"/items/{item_id}").json()
    assert item["stock"] == 5

    # A movimentação rejeitada não pode aparecer no histórico.
    history = client.get(
        f"/items/{item_id}/movements"
    )

    assert history.status_code == 200
    assert history.json() == []


def test_movement_zero_quantity_rejected(client):
    created = client.post(
        "/items",
        json={
            "sku": "MOV-ZERO",
            "name": "Produto de teste",
            "stock": 10
        }
    )

    item_id = created.json()["id"]

    response = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "IN",
            "quantity": 0,
            "reason": "Entrada inválida"
        }
    )

    assert response.status_code == 422


def test_automation_opens_alert(client):
    created = client.post(
        "/items",
        json={
            "sku": "ALERT-001",
            "name": "Produto crítico",
            "stock": 2,
            "min_stock": 5
        }
    )
    assert created.status_code == 201

    item_id = created.json()["id"]

    response = client.post("/automation/check")

    assert response.status_code == 200
    assert response.json()["opened"] == 1
    assert response.json()["resolved"] == 0

    alerts = client.get("/alerts?alert_status=OPEN")

    assert alerts.status_code == 200
    assert len(alerts.json()) == 1
    assert alerts.json()[0]["item_id"] == item_id
    assert alerts.json()[0]["status"] == "OPEN"


def test_automation_is_idempotent(client):
    created = client.post(
        "/items",
        json={
            "sku": "ALERT-002",
            "name": "Produto baixo",
            "stock": 1,
            "min_stock": 5
        }
    )
    assert created.status_code == 201

    first = client.post("/automation/check")
    second = client.post("/automation/check")

    assert first.status_code == 200
    assert first.json()["opened"] == 1

    assert second.status_code == 200
    assert second.json()["opened"] == 0
    assert second.json()["resolved"] == 0

    alerts = client.get("/alerts?alert_status=OPEN")

    assert len(alerts.json()) == 1


def test_automation_resolves_alert(client):
    created = client.post(
        "/items",
        json={
            "sku": "ALERT-003",
            "name": "Produto normalizado",
            "stock": 2,
            "min_stock": 5
        }
    )
    assert created.status_code == 201

    item_id = created.json()["id"]

    first_scan = client.post("/automation/check")
    assert first_scan.json()["opened"] == 1

    movement = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "ADJUST",
            "quantity": 20,
            "reason": "Reposição"
        }
    )
    assert movement.status_code == 201

    second_scan = client.post("/automation/check")

    assert second_scan.status_code == 200
    assert second_scan.json()["opened"] == 0
    assert second_scan.json()["resolved"] == 1

    alerts = client.get("/alerts?alert_status=RESOLVED")

    assert alerts.status_code == 200
    assert len(alerts.json()) == 1
    assert alerts.json()[0]["status"] == "RESOLVED"
    assert alerts.json()[0]["resolved_at"] is not None


def test_movements_do_not_resolve_alerts_automatically(client):
    created = client.post(
        "/items",
        json={
            "sku": "ALERT-004",
            "name": "Produto monitorado",
            "stock": 1,
            "min_stock": 5
        }
    )
    assert created.status_code == 201

    item_id = created.json()["id"]

    client.post("/automation/check")

    movement = client.post(
        f"/items/{item_id}/movements",
        json={
            "type": "IN",
            "quantity": 10,
            "reason": "Reposição de estoque"
        }
    )
    assert movement.status_code == 201

    # O alerta permanece aberto até a próxima varredura.
    before_scan = client.get("/alerts?alert_status=OPEN")

    assert before_scan.status_code == 200
    assert len(before_scan.json()) == 1

    client.post("/automation/check")

    after_scan = client.get("/alerts?alert_status=OPEN")

    assert after_scan.status_code == 200
    assert after_scan.json() == []


def test_alerts_filters(client):
    first = client.post(
        "/items",
        json={
            "sku": "ALERT-005",
            "name": "Produto A",
            "stock": 1,
            "min_stock": 5
        }
    )
    second = client.post(
        "/items",
        json={
            "sku": "ALERT-006",
            "name": "Produto B",
            "stock": 2,
            "min_stock": 5
        }
    )

    assert first.status_code == 201
    assert second.status_code == 201

    first_id = first.json()["id"]
    second_id = second.json()["id"]

    client.post("/automation/check")

    client.post(
        f"/items/{first_id}/movements",
        json={
            "type": "ADJUST",
            "quantity": 20,
            "reason": "Normalização"
        }
    )

    client.post("/automation/check")

    all_alerts = client.get("/alerts")
    open_alerts = client.get("/alerts?alert_status=OPEN")
    resolved_alerts = client.get("/alerts?alert_status=RESOLVED")

    assert all_alerts.status_code == 200
    assert open_alerts.status_code == 200
    assert resolved_alerts.status_code == 200

    assert len(all_alerts.json()) == 2
    assert len(open_alerts.json()) == 1
    assert len(resolved_alerts.json()) == 1

    assert open_alerts.json()[0]["item_id"] == second_id
    assert resolved_alerts.json()[0]["item_id"] == first_id


def test_alerts_invalid_filter(client):
    response = client.get(
        "/alerts",
        params={"alert_status": "INVALID"}
    )

    assert response.status_code == 422



# ============================================================
# ETAPA 12.5 — TESTES DO HELP COM IA SIMULADA
# ============================================================

import httpx


def test_help_success(client, monkeypatch):
    monkeypatch.setenv("AI_MODE", "openai_compatible")
    monkeypatch.setenv("AI_BASE_URL", "https://fake-ai.test/v1")
    monkeypatch.setenv("AI_API_KEY", "fake-test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")

    original_post = httpx.Client.post

    def fake_post(self, url, **kwargs):
        if str(url).startswith("https://fake-ai.test/"):
            assert str(url) == (
                "https://fake-ai.test/v1/chat/completions"
            )
            assert kwargs["json"]["model"] == "test-model"

            request = httpx.Request("POST", url)

            return httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "message": {
                                "content": (
                                    "O alerta é aberto conforme as políticas."
                                )
                            }
                        }
                    ]
                },
                request=request
            )

        return original_post(self, url, **kwargs)

    monkeypatch.setattr(httpx.Client, "post", fake_post)

    response = client.post(
        "/help",
        json={
            "question": "Quando devo abrir um alerta de estoque?",
            "max_sources": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "O alerta é aberto conforme as políticas."
    )
    assert data["provider"] == "openai_compatible"
    assert data["model"] == "test-model"
    assert len(data["sources"]) > 0


def test_help_without_documentation(client, monkeypatch):
    monkeypatch.setenv("AI_MODE", "openai_compatible")
    monkeypatch.setenv("AI_BASE_URL", "https://fake-ai.test/v1")
    monkeypatch.setenv("AI_API_KEY", "fake-test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")

    original_post = httpx.Client.post

    def unexpected_post(self, url, **kwargs):
        if str(url).startswith("https://fake-ai.test/"):
            raise AssertionError(
                "Não deveria chamar a IA sem documentação"
            )

        return original_post(self, url, **kwargs)

    monkeypatch.setattr(
        httpx.Client,
        "post",
        unexpected_post
    )

    response = client.post(
        "/help",
        json={
            "question": "xilofone nebulosa quasar",
            "max_sources": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sources"] == []
    assert data["provider"] == "local"
    assert data["model"] == "none"
    assert data["answer"] == (
        "Não encontrei base documental suficiente para responder."
    )


def test_help_provider_unavailable(client, monkeypatch):
    monkeypatch.setenv("AI_MODE", "openai_compatible")
    monkeypatch.setenv("AI_BASE_URL", "https://fake-ai.test/v1")
    monkeypatch.setenv("AI_API_KEY", "fake-test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")

    original_post = httpx.Client.post

    def fake_post(self, url, **kwargs):
        if str(url).startswith("https://fake-ai.test/"):
            raise httpx.ConnectError(
                "Falha simulada de conexão"
            )

        return original_post(self, url, **kwargs)

    monkeypatch.setattr(httpx.Client, "post", fake_post)

    response = client.post(
        "/help",
        json={
            "question": "Como funciona o alerta de estoque?",
            "max_sources": 3
        }
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Provedor de IA indisponível"
    )


def test_help_invalid_provider_response(client, monkeypatch):
    monkeypatch.setenv("AI_MODE", "openai_compatible")
    monkeypatch.setenv("AI_BASE_URL", "https://fake-ai.test/v1")
    monkeypatch.setenv("AI_API_KEY", "fake-test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")

    original_post = httpx.Client.post

    def fake_post(self, url, **kwargs):
        if str(url).startswith("https://fake-ai.test/"):
            request = httpx.Request("POST", url)

            return httpx.Response(
                200,
                json={
                    "unexpected": "invalid payload"
                },
                request=request
            )

        return original_post(self, url, **kwargs)

    monkeypatch.setattr(httpx.Client, "post", fake_post)

    response = client.post(
        "/help",
        json={
            "question": "Quando devo abrir um alerta de estoque?",
            "max_sources": 3
        }
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Resposta inválida do provedor de IA"
    )
