import mysql.connector

class MySQLConector:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.mydb.cursor()

    def selectLastInsertion(self):
        self.cursor.execute("SELECT jogador1, jogador2, velha FROM results ORDER BY jogo DESC LIMIT 1")
        result = self.cursor.fetchall()

        if result == []:
            result = (0,0,0)
        else:
            result = result[0]

        return result 
    
    def insertResult(self, result):
        lastResult = self.selectLastInsertion()

        sql = "INSERT INTO results (`jogador1`, `jogador2`, `velha`) VALUES (%s, %s, %s)"

        if(result == 1):
            val = (lastResult[0]+1, lastResult[1], lastResult[2]) # jogador 1 ganhou
        elif(result == 2):
            val = (lastResult[0], lastResult[1]+1, lastResult[2]) # jogador 2 ganhou
        else:
            val = (lastResult[0], lastResult[1], lastResult[2]+1) # velha
        
        self.cursor.execute(sql, val)
        self.mydb.commit()
