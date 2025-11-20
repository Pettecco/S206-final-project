import threading
import time
import os
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QGridLayout, QWidget, 
    QVBoxLayout, QHBoxLayout, QFrame
)
from src.tabuleiro import Tabuleiro
from database.mysql_conector import MySQLConector

class UltimateTicTacToe(QMainWindow):

    #inicialização da parte gráfica
    def __init__(self, AutoStart = False):
        super().__init__()
        self.setWindowTitle("Jogo da velha com threads")
        self.setGeometry(100, 100, 900, 600)
        self.initUI()
        self.mySQLConector = MySQLConector(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
        if AutoStart:
            time.sleep(5)
            self.start_button.click()

    #Iniciando a interface
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout() #layout horizontal para o jogo principal e minijogos

        self.grid = QGridLayout()
        self.buttons = [[QPushButton("") for _ in range(3)] for _ in range(3)] #botões para representar as posições

        #Matriz do jogo principal
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setFixedSize(150, 150)
                self.buttons[i][j].setStyleSheet("font-size: 24px;")
                self.grid.addWidget(self.buttons[i][j], i, j)

        #Botão de Iniciar
        self.start_button = QPushButton("Começar Jogo")
        self.start_button.clicked.connect(self.start_games) #inicializa o jogo

        #Botão de Reiniciar
        self.reset_button = QPushButton("Reiniciar")
        self.reset_button.clicked.connect(self.restart_game) #reinicia o jogo
        self.reset_button.setEnabled(False) #só ativa após o jogo começar

        #Layout principal (à esquerda)
        left_layout = QVBoxLayout()
        left_layout.addLayout(self.grid) #jogo principal
        left_layout.addWidget(self.start_button) #botão de início
        left_layout.addWidget(self.reset_button) #botão de reinicialização

        #Matriz de minijogos
        self.mini_games_layout = QGridLayout()
        self.mini_games = [[self.create_mini_board(i * 3 + j) for j in range(3)] for i in range(3)]

        #Montagem da matriz composta pelos 9 minijogos
        for i in range(3):
            for j in range(3):
                self.mini_games_layout.addWidget(self.mini_games[i][j], i, j)

        # Layout do lado direito com os mini-jogos
        right_layout = QVBoxLayout()
        right_layout.addLayout(self.mini_games_layout)

        #Layout principal que organiza o lado esquerdo e direito
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        central_widget.setLayout(main_layout)

    #Especificações gráficas dos minijogos
    def create_mini_board(self, board_index):
        frame = QFrame()
        frame.setStyleSheet("border: 2px solid black;")
        layout = QGridLayout()
        buttons = [[QPushButton("") for _ in range(3)] for _ in range(3)]

        #Matriz de cada minijogo
        for i in range(3):
            for j in range(3):
                buttons[i][j].setFixedSize(40, 40)
                buttons[i][j].setStyleSheet("font-size: 14px;")
                layout.addWidget(buttons[i][j], i, j)
        frame.setLayout(layout)
        return frame

    #Atualizando a interface
    def update_ui(self, board_index, player, tamanho, x, y): #tamanho 0=pequeno, 1=grande
        row, col = divmod(board_index, 3)

        #Inserindo a jogada no tabuleiro maior
        if tamanho == 1 and player != 0:
            self.buttons[row][col].setText("X" if player == 1 else "O") #conversão de 1 e 2 para X e O

        #Atualizando os mini-jogos na lateral
        if tamanho == 0:
            mini_game_row, mini_game_col = row, col
            widget = self.mini_games[mini_game_row][mini_game_col] #obtém o QFrame do mini-tabuleiro

            layout = widget.layout() #obtém o layout de grade dentro do mini-tabuleiro

            btn = layout.itemAtPosition(x, y).widget()
            if btn.text() == "": #encontra um botão vazio e preenche com a jogada
                btn.setText("X" if player == 1 else "O")
                return #sai da função após marcar a jogada
        else:
            return

    #Para começar o jogo
    def start_games(self):
        self.start_button.setEnabled(False) #desativa o botão de início
        self.reset_button.setEnabled(False) #ativa o botão de reinício

        #Criar sempre novos tabuleiros ao iniciar
        self.tabuleiros = [Tabuleiro(i, self.update_ui, self.mySQLConector) for i in range(9)]

        def ciclo_de_jogo():
            tabuleiro_atual = 0
            while not Tabuleiro.game_over_maior: #enquanto não acabar o jogo no tabuleiro maior...
                t = self.tabuleiros[tabuleiro_atual]
                if not t.game_over: #se o jogo não acabou no tabuleiro menor...
                    t.start()  # chamar start para iniciar as threads
                    t.resultado()  #esperar pela jogada das duas threads antes de prosseguir

                tabuleiro_atual = (tabuleiro_atual + 1) % 9
                time.sleep(0.5)

            #habilitar o botão de reiniciar
            self.reset_button.setEnabled(True)
        threading.Thread(target=ciclo_de_jogo, daemon=True).start()


    #Def para resetar o jogo
    def restart_game(self):
        #Reset das variáveis estáticas da classe Tabuleiro
        Tabuleiro.resultados.fill(0)
        Tabuleiro.finalizados.fill(0)
        Tabuleiro.game_over_maior = False

        #Apagar os mini-tabuleiros antigos e recriar novos
        for i in range(3):
            for j in range(3):
                #Limpa os botões principais
                self.buttons[i][j].setText("")

                #Limpa os mini-tabuleiros
                mini_game_widget = self.mini_games[i][j]  #obtém o QFrame
                layout = mini_game_widget.layout()  #obtém o QGridLayout do QFrame
                for x in range(3):
                    for y in range(3):
                        btn = layout.itemAtPosition(x, y).widget()
                        if btn:
                            btn.setText("")  #limpa o texto dos botões pequenos

        #Criar novos tabuleiros (descartar os antigos)
        self.tabuleiros = []

        #Habilitar e desabilitar botões
        self.start_button.setEnabled(True)  #permite iniciar um novo jogo
        self.reset_button.setEnabled(False)  #desativa o botão de reinício até novo jogo começar
