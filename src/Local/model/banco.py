import os
import sqlite3

class Banco:
    def startDatabase(self):
        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        database_path = os.path.join(os.path.dirname(current_path), 'data', 'quiz.db')
        
        conn = sqlite3.connect(database_path)

        # Create a cursor to execcute commands from sql
        cursor = conn.cursor()
        
        #Create a table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        
        print('Banco de dados inicializado')
    
    def executeCommandPost(self, command, params=None):
        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        database_path = os.path.join(os.path.dirname(current_path), 'data', 'quiz.db')
        
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        try:
            if params:
                cursor.execute(command, params)
            else:
                cursor.execute(command)
            connection.commit()
        except sqlite3.Error as e:
            print(f"Erro ao executar o comando: {e}")
            return False
        finally:
            connection.close()
            return True
    
    def executeCommandGet(self, command):
        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        database_path = os.path.join(os.path.dirname(current_path), 'data', 'quiz.db')
        
        print(database_path)
        
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        response = None
        
        try:
            cursor.execute(command)
            response = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao executar o comando: {e}")
            return None
        finally:
            connection.close()
            return response

class Consultas (Banco):
    def createQuestion(self, question, answer):
        return self.executeCommandPost('INSERT INTO quiz (question, answer) VALUES (?, ?)', (question, answer))
    
    def editQuestion(self, id, question, answer):
        return self.executeCommandPost('UPDATE quiz SET question = ?, answer = ? WHERE id = ?', (question, answer, id, ))
    
    def deleteQuestion(self, id):
        return self.executeCommandPost('DELETE FROM quiz WHERE id = ?', (id, ))
    
    def getQuestions(self):
        return self.executeCommandGet('SELECT * FROM quiz')