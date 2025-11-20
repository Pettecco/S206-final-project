import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
import os

load_dotenv()

from src.ultimate_tictactoe import UltimateTicTacToe

if __name__ == "__main__":

    #Inicialização e funcionamento do jogo
    app = QApplication(sys.argv)
    window = UltimateTicTacToe()
    window.show()
    sys.exit(app.exec_())