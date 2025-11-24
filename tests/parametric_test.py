import pytest
import numpy as np
from unittest.mock import Mock
from src.tabuleiro import Tabuleiro

# FIXTURES

@pytest.fixture
def mock_ui():
    return Mock()

@pytest.fixture
def mock_mysql():
    mock = Mock()
    mock.insertResult = Mock()
    mock.selectLastInsertion = Mock(return_value="OK")
    return mock

@pytest.fixture(autouse=True)
def reset_static():
    Tabuleiro.resultados = np.zeros((3, 3), dtype=int)
    Tabuleiro.finalizados = np.zeros((3, 3), dtype=int)
    Tabuleiro.game_over_maior = False
    yield

@pytest.fixture
def tabuleiro(mock_ui, mock_mysql):
    return Tabuleiro(0, mock_ui, mock_mysql)

# TESTES PARAMETRIZADOS DE VITÓRIA

@pytest.mark.parametrize(
    "board, esperado",
    [
        pytest.param(
            np.array([
                [1, 1, 1],
                [0, 2, 0],
                [2, 0, 0]
            ]), 1,
            id="linha_vencedora"
        ),

        pytest.param(
            np.array([
                [2, 1, 0],
                [2, 1, 0],
                [2, 0, 1]
            ]), 2,
            id="coluna_vencedora"
        ),

        pytest.param(
            np.array([
                [1, 2, 0],
                [0, 1, 2],
                [0, 0, 1]
            ]), 1,
            id="diagonal_vencedora"
        ),
    ]
)
def test_vitorias(tabuleiro, mock_ui, board, esperado):
    tabuleiro.board = board
    tabuleiro.check_winner()

    assert tabuleiro.result == esperado
    assert tabuleiro.game_over is True
    mock_ui.assert_called()

# TESTE PARAMETRIZADO DA VELHA

@pytest.mark.parametrize(
    "board, esperado",
    [
        pytest.param(
            np.array([
                [1, 2, 1],
                [2, 1, 2],
                [2, 1, 2]
            ]), 0,
            id="velha"
        )
    ]
)
def test_velha(tabuleiro, board, esperado):
    tabuleiro.board = board
    tabuleiro.check_winner()

    assert tabuleiro.result == esperado
    assert tabuleiro.game_over is True

# TESTE DE JOGADA VÁLIDA

def test_jogada_valida(tabuleiro):
    tabuleiro.board[1, 1] = 0
    tabuleiro.board[0, 0] = 0

    x, y = 1, 1
    tabuleiro.board[x, y] = 1

    assert tabuleiro.board[1, 1] == 1

# TESTES PARAMETRIZADOS DO check_maior

@pytest.mark.parametrize(
    "finalizados, board, esperado_db",
    [
        pytest.param(
            np.zeros((3, 3), dtype=int),
            np.array([
                [1, 1, 1],
                [0, 2, 0],
                [0, 0, 2]
            ]),
            1,
            id="maior_vitoria"
        ),

        pytest.param(
            np.ones((3, 3), dtype=int),
            np.zeros((3, 3), dtype=int),
            0,
            id="maior_velha"
        ),
    ]
)
def test_check_maior(mock_mysql, mock_ui, finalizados, board, esperado_db):
    t = Tabuleiro(0, mock_ui, mock_mysql)

    Tabuleiro.finalizados = finalizados
    Tabuleiro.check_maior(t, board)

    assert Tabuleiro.game_over_maior is True
    mock_mysql.insertResult.assert_called_once_with(esperado_db)
