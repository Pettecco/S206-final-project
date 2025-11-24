import pytest
import numpy as np
from unittest.mock import MagicMock
from src.tabuleiro import Tabuleiro

def mock_ui_callback(nome, player, tipo, x, y):
    "Função vazia apenas para o Tabuleiro não dar erro ao tentar atualizar a tela"
    pass

class MockMySQLConector:
    "Simula o comportamento do banco de dados"
    def __init__(self):
        self.ultimo_resultado_salvo = None

    def insertResult(self, result):
        self.ultimo_resultado_salvo = result
    
    def selectLastInsertion(self):
        return "Registro Teste #1"

@pytest.fixture(autouse=True)
def reset_board():
    "Reseta o tabuleiro no início de cada teste"
    Tabuleiro.resultados = np.zeros((3, 3), dtype=int)
    Tabuleiro.game_over_maior = False
    Tabuleiro.finalizados = np.zeros((3, 3), dtype=int)

def test_integration_victory_player_1():
    "Verifica se o player 1 ganhou o jogo"
    fake_db = MockMySQLConector()
    tabuleiro = Tabuleiro(0, mock_ui_callback, fake_db)
    
    #situação onde o jogador 1 ganha
    mock_board_maior = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    Tabuleiro.check_maior(tabuleiro, mock_board_maior)

    #verifica se o jogo acabou e se o resultado enviado para o banco foi 1
    assert Tabuleiro.game_over_maior is True
    assert fake_db.ultimo_resultado_salvo == 1

def test_integration_victory_player_2():
    "Verifica se o player 1 ganhou o jogo"
    fake_db = MockMySQLConector()
    tabuleiro = Tabuleiro(0, mock_ui_callback, fake_db)

    #situação onde o jogador 1 ganha
    mock_board_maior = np.array([
        [2, 0, 0],
        [2, 0, 0],
        [2, 0, 0]
    ])

    #verifica se o jogo acabou e se o resultado enviado para o banco foi 2
    Tabuleiro.check_maior(tabuleiro, mock_board_maior)
    assert fake_db.ultimo_resultado_salvo == 2

def test_integration_without_winner():
    "Jogo em andamento"
    fake_db = MockMySQLConector()
    tabuleiro = Tabuleiro(0, mock_ui_callback, fake_db)

    #ninguém ganhou
    mock_board_maior = np.array([
        [1, 2, 0],
        [0, 1, 0],
        [0, 0, 2]
    ])

    Tabuleiro.check_maior(tabuleiro, mock_board_maior)

    #jogo não acabou, nada deve ser salvo no banco
    assert Tabuleiro.game_over_maior is False
    assert fake_db.ultimo_resultado_salvo is None