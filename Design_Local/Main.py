import sqlite3

class Banco:
    def startDatabase(self):
        # Connect to database
        conn = sqlite3.connect('quiz.db')

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
        connection = sqlite3.connect('quiz.db')  # Substitua pelo caminho correto
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
            return 
    
    def executeCommandGet(self, command):
        connection = sqlite3.connect('quiz.db')  # Substitua pelo caminho correto
        cursor = connection.cursor()
        
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
    
    def getQuestionsQuiz(self):
        return self.executeCommandGet('SELECT question FROM quiz')
    
    def getAnswerQuiz(self):
        return self.executeCommandGet('SELECT answer FROM quiz')
    
    def getIdQuiz(self):
        return self.executeCommandGet('SELECT id FROM quiz')
            
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Quiz(Consultas):
    def showInfo(self, msg):
        messagebox.showinfo("Aviso", msg)
    
    def variables(self):
        self.window = Tk() # start window
        self.notebook = ttk.Notebook(self.window) # start notebook
        
        #start tabs
        self.tabNewQuestion = ttk.Frame(self.notebook)
        self.tabQuiz = ttk.Frame(self.notebook)
        
        # Get quetions from database
        self.questions = self.getQuestionsQuiz()
        
        # Get answers from database
        self.answers = self.getAnswerQuiz()
        
        # Get ids from database
        self.ids = self.getIdQuiz()
        
    def startWindow(self):
        # start the datebase
        self.startDatabase()
        
        self.variables()
        
        # configure the window
        self.window.title('Quiz')
        
        largura = 450
        altura = 400
        largura_tela = self.window.winfo_screenwidth()
        altura_tela = self.window.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        self.window.resizable(False, False)
        
        # create a tabs menu
        self.tabsMenu()
        
        self.window.mainloop()
    
    def tabsMenu (self):
        # Create a notebook (tabs menu)
        self.notebook.pack(expand=True, fill='both')
        
        # add tabs to notebook
        self.notebook.add(self.tabNewQuestion, text="New Question")
        self.notebook.add(self.tabQuiz, text='Quiz')
        
        self.fillTabNewQuestion()
        self.fillTabQuiz()

    ### TAB New Question
    def newQuestionButtonCreate(self):
        response = self.createQuestion(self.question.get(), self.answer.get())
        
        if response:
            self.showInfo("Question created successfully")
        else:
            self.showInfo("Question creation failed")
            
        self.clearNewQuestion()
        
    def clearNewQuestion(self):
        self.question.delete(0, END)
        self.answer.delete(0, END)
        
    def fillTabNewQuestion (self):
        # Question
        Label(self.tabNewQuestion, text='Question:').place(relx=0.05, rely=0.1)
        self.question = Entry(self.tabNewQuestion)
        self.question.place(relx=0.20, rely=0.1, width=330)
        
        # Answer
        Label(self.tabNewQuestion, text='Answer:').place(relx=0.05, rely=0.3)
        self.answer = Entry(self.tabNewQuestion)
        self.answer.place(relx=0.20, rely=0.3, width=330)
        
        # Button create new question
        Button(self.tabNewQuestion, text='create', command=lambda: self.newQuestionButtonCreate()).place(relx=0.48, rely=0.5)
    ### TAB Quiz 
    def showAnswerButton (self, answer):
        Canvas(self.tabNewQuestion, width=400, height=50, bg="black").place(relx=0.05, rely=0.5)
        
        Label(self.tabQuiz, text=answer).place(relx=0.05, rely=0.65)
        
    def showQuestion (self, question, answer, indice):
        # Destrói todos os widgets dentro do frame
        for widget in self.tabQuiz.winfo_children():
            widget.destroy()
        
        # Show question
        Label(self.tabQuiz, text=question).place(relx=0.20, rely=0.05)
        
        # Button show answer
        Button(self.tabQuiz, text='show answer', command=lambda: self.showAnswerButton(answer)).place(relx=0.75, rely=0.4)
        
        # Button Next
        if indice < len(self.questions):
            Button(self.tabQuiz, text='next', command=lambda: self.showQuestion(self.questions[indice+1], self.answers[indice+1], indice+1)).place(relx=0.85, rely=0.9)
        elif indice == len(self.questions):
            Button(self.tabQuiz, text='finish', command=lambda: self.endQuiz()).place(relx=0.85, rely=0.9)            
                
    def fillTabQuiz (self):
        if len(self.questions) > 0:
            try:
                Button(self.tabQuiz, text='start', command=lambda: self.showQuestion(self.questions[0], self.answers[0], 1)).place(relx=0.24, rely=0.34, relwidth=0.5, relheight=0.3)
            except:
                self.showInfo("Please, Before start the game create at least one question")
            
                
class Main(Quiz):
    def __init__(self):
        self.startWindow()
        
Main()