
"""Configuração compartilhada dos testes do StockGuard."""

import pytest
from fastapi.testclient import TestClient

from app.db import initialize
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Cria um caminho temporário exclusivo para o teste.
    test_db = tmp_path / "stockguard_test.sqlite3"

    # Faz a aplicação usar o banco de testes.
    monkeypatch.setenv("STOCKGUARD_DB", str(test_db))

    # Cria as tabelas nesse banco.
    initialize()

    # Cria um cliente HTTP de testes.
    with TestClient(app) as test_client:
        yield test_client
