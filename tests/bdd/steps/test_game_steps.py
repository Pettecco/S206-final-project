import importlib
import pytest
from pytest_bdd import given, when, then, scenarios
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# Carrega o arquivo .feature
scenarios("../features/game.feature")

pytestmark = pytest.mark.bdd

@pytest.fixture
def app_window(monkeypatch, qtbot):
    """Cria a janela da aplicação já configurada."""
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_USER", "tttuser")
    monkeypatch.setenv("DB_PASSWORD", "tttpass")
    monkeypatch.setenv("DB_NAME", "tictactoe")

    ut_mod = importlib.import_module("src.ultimate_tictactoe")
    UltimateTicTacToe = ut_mod.UltimateTicTacToe

    window = UltimateTicTacToe()
    qtbot.addWidget(window)
    window.show()

    QApplication.instance().processEvents()
    return window

@given("a aplicação está carregada com acesso ao banco")
def given_app_loaded(app_window, db_connection):
    return app_window

@when("eu inicio o jogo")
def when_start_game(app_window, qtbot):
    qtbot.mouseClick(app_window.start_button, Qt.LeftButton)

@then("o jogo deve começar")
def then_game_started(app_window):
    assert not app_window.start_button.isEnabled()
    assert app_window.reset_button.isEnabled() is False

@then("o jogo deve terminar automaticamente")
def then_game_finished(app_window, qtbot):
    qtbot.waitUntil(lambda: app_window.reset_button.isEnabled(), timeout=120_000)

@then("o resultado deve estar salvo no banco")
def then_db_saved(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM results;")
    count = cursor.fetchone()[0]
    cursor.close()
    assert count >= 1

@when("eu resetar o jogo")
def when_reset(app_window, qtbot):
    qtbot.mouseClick(app_window.reset_button, Qt.LeftButton)
    qtbot.wait(300)

@then("os botões devem voltar ao estado inicial")
def then_buttons_reset(app_window):
    assert app_window.start_button.isEnabled()
    assert not app_window.reset_button.isEnabled()
