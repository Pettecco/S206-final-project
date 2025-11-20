import numpy as np
import threading
import time

from database.mysql_conector import MySQLConector

class Tabuleiro:
    #Criando tabuleiros auxiliares
    resultados = np.zeros((3, 3), dtype=int) #posições zeradas
    game_over_maior = False # variável de controle da finalização do tabuleiro maior
    finalizados = np.zeros((3, 3), dtype=int) #matriz de jogos finalizados
    semaforo = threading.Semaphore(value=1) #apenas uma thread pode acessar a zona crítica por vez

    def __init__(self, nome, ui_callback, mySQLConector):
        #Criando o tabuleiro
        self.board = np.zeros((3, 3), dtype=int)
        self.game_over = False #flag de finalização do jogo
        self.nome = nome #número referente à posição do tabuleiro maior
        self.result = 0 #inicializando com nenhum vencedor
        self.ui_callback = ui_callback #referente ao funcionamento da interface
        # Conectar com o bd
        self.mySQLConector = mySQLConector

    #Fazendo a jogada
    def play(self, player):
        #Analisando se pode fazer a jogada
        Tabuleiro.semaforo.acquire() # início de área crítica
        try:
            if self.game_over or Tabuleiro.game_over_maior: #se o jogo acabou (no tabuleiro menor ou maior)
                return
            while True:
                x, y = np.random.randint(0, 3, 2) #gerar aleatoriamente as posições do tabuleiro menor
                print(f'Tabuleiro {self.nome} - Jogador {player} - Jogada nas coordenadas ({x},{y})', flush=True)
                #Jogando
                if self.board[x, y] == 0: #se ainda não houve uma jogada nessa posição
                    self.board[x, y] = player #a posição assume o rótulo do jogador
                    self.ui_callback(self.nome, player, 0, x, y) #atualização da interface gráfica para o usuário
                    print(f'Tabuleiro {self.nome} - Jogada realizada\n{self.board}', flush=True)
                    self.check_winner() #checagem do tabuleiro por vencedores
                    time.sleep(0.5) #pequena pausa
                    break
        finally:
            Tabuleiro.semaforo.release() #liberação da área crítica
    

    #Verificando se alguém ganhou nos mini jogos da velha
    def check_winner(self):
        #Analisando as linhas e as colunas
        for i in range(3):
            if np.all(self.board[i] == 1) or np.all(self.board[:, i] == 1): #linha/coluna inteira composta por uns
                self.result = 1
            if np.all(self.board[i] == 2) or np.all(self.board[:, i] == 2): #linha/coluna inteira composta por dois
                self.result = 2

        #Analisando as diagonais
        if np.all(np.diagonal(self.board) == 1) or np.all(np.diagonal(np.fliplr(self.board)) == 1): #diagonal de uns
            self.result = 1
        if np.all(np.diagonal(self.board) == 2) or np.all(np.diagonal(np.fliplr(self.board)) == 2): #diagonal de dois
            self.result = 2
            
        #Mostrando o resultado, se alguém ganhou
        if self.result in [1, 2]:
            self.game_over = True #finaliza aquele minijogo
            self.ui_callback(self.nome, self.result, 1, 0, 0) #atualiza a ui do tabuleiro maior com a informação do jogador vencedor
            print(f'Tabuleiro {self.nome} - Jogador {self.result} ganhou!', flush=True)
            Tabuleiro.resultados[divmod(self.nome, 3)] = self.result
            Tabuleiro.finalizados[divmod(self.nome, 3)] = 1 #matriz de jogos finalizados
            Tabuleiro.check_maior(self, Tabuleiro.resultados) #solicita a conferência do tabuleiro maior

        #Mostrando se for velha
        elif np.all(self.board != 0):
            self.game_over = True #finaliza aquele minijogo
            self.ui_callback(self.nome, self.result, 1, 0, 0) #atualiza o tabuleiro maior mantendo a posição vazia
            print(f'Tabuleiro {self.nome} - Deu velha!', flush=True)
            Tabuleiro.finalizados[divmod(self.nome, 3)] = 1
            Tabuleiro.check_maior(self, Tabuleiro.resultados) #solicita a conferência do tabuleiro maior

    #Comecando o jogo
    def start(self):
        #Criando as threads
        self.j1 = threading.Thread(target=self.play, args=(1,)) #thread 1 como jogador 1
        self.j2 = threading.Thread(target=self.play, args=(2,)) #thread 2 como jogador 2

        #Iniciando as threads
        self.j1.start()
        self.j2.start()

    #Obtenção do resultado
    def resultado(self):
        self.j1.join()
        self.j2.join()
        return self.result
    
    #Analisando se alguém ganhou no tabuleiro maior
    @staticmethod
    def check_maior(self, board_maior):
        result = 0 #inicia sem vencedores
        for i in range(3):
            #Checagem das linhas e colunas
            if np.all(board_maior[i] == 1) or np.all(board_maior[:, i] == 1): #linha/coluna inteira composta por uns
                result = 1
            if np.all(board_maior[i] == 2) or np.all(board_maior[:, i] == 2): #linha/coluna inteira composta por dois
                result = 2

        #Checagem das diagonais
        if np.all(np.diagonal(board_maior) == 1) or np.all(np.diagonal(np.fliplr(board_maior)) == 1): #diagonal inteira composta por uns
            result = 1
        if np.all(np.diagonal(board_maior) == 2) or np.all(np.diagonal(np.fliplr(board_maior)) == 2): #diagonal inteira composta por dois
            result = 2

        #Caso haja um vencedor (result == 1 ou result == 2)
        if result in [1, 2]:
           Tabuleiro.game_over_maior = True #jogo finalizado
           self.mySQLConector.insertResult(result)
           print(f"Placar - {self.mySQLConector.selectLastInsertion()}", flush=True)
           print(f'Jogo principal - Jogador {result} ganhou!', flush=True)

        #Caso não tenha vencedores
        elif np.all(Tabuleiro.finalizados != 0): #verificar se todos os minijogos foram finalizados
            Tabuleiro.game_over_maior = True #se finalizaram, indica que o resultado é velha e o jogo também finalizou
            self.mySQLConector.insertResult(result)
            print(f"Placar - {self.mySQLConector.selectLastInsertion()}", flush=True)
            print(f'Jogo principal - Deu velha!', flush=True)
