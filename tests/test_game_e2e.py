import importlib
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def test_game_end_to_end(qtbot, monkeypatch, db_connection):
    # Configuração do banco de dados
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_USER", "tttuser")
    monkeypatch.setenv("DB_PASSWORD", "tttpass")
    monkeypatch.setenv("DB_NAME", "tictactoe")

    # Importar módulo UI após configurar env
    ut_mod = importlib.import_module("src.ultimate_tictactoe")
    UltimateTicTacToe = ut_mod.UltimateTicTacToe

    # MODO COM INTERFACE VISÍVEL
    window = UltimateTicTacToe()
    window.show()
    window.raise_()
    window.activateWindow()
    qtbot.addWidget(window)

    # MODO HEADLESS (SEM JANELA)
    # window = UltimateTicTacToe()
    # qtbot.addWidget(window)
    # qtbot.wait(200)  # processa eventos iniciais no modo offscreen

    app = QApplication.instance()
    app.processEvents()

    # Antes do jogo começar
    assert window.start_button.isEnabled()        # Start deve estar habilitado
    assert not window.reset_button.isEnabled()    # Reset desabilitado

    # Iniciar jogo
    qtbot.mouseClick(window.start_button, Qt.LeftButton)

    # Espera o jogo terminar
    qtbot.waitUntil(lambda: window.reset_button.isEnabled(), timeout=120_000)

    # Depois do jogo
    assert not window.start_button.isEnabled()    # Start desabilitado
    assert window.reset_button.isEnabled()        # Reset habilitado

    # Verifica resultados no banco
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM results;")
    count = cursor.fetchone()[0]
    cursor.close()
    assert count >= 1  # pelo menos um resultado inserido

    # Clica no botão Reset
    qtbot.mouseClick(window.reset_button, Qt.LeftButton)
    qtbot.wait(500)

    # Verifica se os botões voltaram ao estado inicial
    assert window.start_button.isEnabled()        # Start habilitado novamente
    assert not window.reset_button.isEnabled()    # Reset desabilitado
