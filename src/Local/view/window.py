import sys 
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from model.banco import Consultas

class Window(Consultas):
    def showInfo(self, msg):
        messagebox.showinfo("Aviso", msg)
    
    def variables(self):
        self.window = Tk() # start window
        
        # Get quetions from database
        self.questions = self.getQuestions()
        
        print(self.questions)
        
        self.hits = 0
        self.errors = 0
        
    def startWindow(self):
        # start the datebase
        self.startDatabase()
        
        self.variables()
        
        # configure the window
        self.window.title('Quiz')
        
        largura = 450
        altura = 500
        largura_tela = self.window.winfo_screenwidth()
        altura_tela = self.window.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        self.window.resizable(False, False)
        
        if self.questions != None and self.questions != []:
            self.fillMainFrame(self.questions[0][0], self.questions[0][1], self.questions[0][2], 0)
        else:
            self.fillMainFrame(None, None, None, None)
            
        self.window.mainloop()
        

    ### New Question Frame
    def newQuestionButtonCreate(self):
        response = self.createQuestion(self.question.get(), self.answer.get())
        
        if response == True:
            self.showInfo("Question created successfully")
        else:
            self.showInfo("Question creation failed")
            
        self.clearNewQuestion()
    
    def backButton (self):
        # Get quetions from database
        self.questions = self.getQuestions()
        
        self.fillMainFrame(self.questions[0][0], self.questions[0][1], self.questions[0][2], 0)
        
    def fillFrameNewQuestion (self):
        self.mainFrame.destroy()
        
        # Start Frame
        self.tabNewQuestion = ttk.Frame(self.window)
        self.tabNewQuestion.place(relheight=1, relwidth=1)
        
        # Question
        Label(self.tabNewQuestion, text='Question:').place(relx=0.05, rely=0.1)
        self.question = Entry(self.tabNewQuestion)
        self.question.place(relx=0.20, rely=0.1, width=330)
        
        # Answer
        Label(self.tabNewQuestion, text='Answer:').place(relx=0.05, rely=0.3)
        self.answer = Entry(self.tabNewQuestion)
        self.answer.place(relx=0.20, rely=0.3, width=330)
        
        # Button create new question
        Button(self.tabNewQuestion, text='create', command= self.newQuestionButtonCreate).place(relx=0.85, rely=0.6)
        
        # Button back main frame
        
        Button(self.tabNewQuestion, text='back', command=self.backButton).place(relx=0.05, rely=0.6)
        
    def clearNewQuestion(self):
        self.question.delete(0, END)
        self.answer.delete(0, END)
    
    def editButton(self, id, question, answer):
        print(self.editQuestion(id, question, answer))
        
        # Get quetions from database
        self.questions = self.getQuestions()
        print(self.questions)
        
        self.fillMainFrame(self.questions[0][0], self.questions[0][1], self.questions[0][2], 0)
    
    ### Edit Frame
    def fillEditFrame(self, question, answer, id):
        if question != None:
            self.mainFrame.destroy()
        
        # Start Frame
        self.editFrame = ttk.Frame(self.window)
        self.editFrame.place(relheight=1, relwidth=1)
        
        # Question
        Label(self.editFrame, text='Question:').place(relx=0.05, rely=0.1)
        self.question = Entry(self.editFrame)
        self.question.insert(0, question)
        self.question.place(relx=0.20, rely=0.1, width=330)
        
        # Answer
        Label(self.editFrame, text='Answer:').place(relx=0.05, rely=0.3)
        self.answer = Entry(self.editFrame)
        self.answer.insert(0, answer)
        self.answer.place(relx=0.20, rely=0.3, width=330)
        
        # Button create new question
        Button(self.editFrame, text='edit', command=lambda: self.editButton(id, question, answer)).place(relx=0.48, rely=0.5)
    
    ### Main Frame
    def deleteButton (self, id):
        self.deleteQuestion(id)
        
        # Get quetions from database
        self.questions = self.getQuestions()
        
        if self.questions != None and self.questions != []:
            self.fillMainFrame(self.questions[0][0], self.questions[0][1], self.questions[0][2], 0)
        else:
            self.fillMainFrame(None, None, None, None)

    def restartButton (self):
        self.finishFrame.destroy()
        
        self.fillMainFrame(self.questions[0][0], self.questions[0][1], self.questions[0][2], 0)
        
    def endQuiz (self):
        self.mainFrame.destroy()
        
        self.finishFrame = Frame(self.window)
        self.finishFrame.place(relwidth=1, relheight=1)
        
        font_size = 100
        y_ini = 50
        
        mistakes = Label(self.finishFrame, text=str(self.hits), font=('Arial', font_size))
        mistakes.place(x=70, y=y_ini)
        
        mistakes_text = Label(self.finishFrame, text='mistakes', font=('Arial', 20))
        mistakes_text.place(x=60, y=y_ini+font_size+25)
        
        sucesses = Label(self.finishFrame, text=str(self.errors), font=('Arial', font_size))
        sucesses.place(x=300, y=y_ini)
        
        sucesses_text = Label(self.finishFrame, text='sucesses', font=('Arial', 20))
        sucesses_text.place(x=290, y=y_ini+font_size+25)
        
        restart = Button(self.finishFrame, text='restart', font=('Arial', 20), command=self.restartButton)
        restart.place(x=180, y=270) 
              
    def fillMainFrame (self, id, question, answer, indice):
        self.mainFrame = ttk.Frame(self.window)
        self.mainFrame.place(relheight=1, relwidth=1)
        
        if self.questions != None and self.questions != []:
            # Destroy all widgets of the frame
            for widget in self.mainFrame.winfo_children():
                widget.destroy()
                
            canvas = Canvas(self.mainFrame, width=430, height=150, bg="white")
            canvas.place(x=10, y=50)
            
            canvas.create_rectangle(0, 0, 430, 150, fill='gray', outline='white')
            
            Label(self.mainFrame, fg='white', text=str(indice+1) + '/' + str(len(self.questions)), background='gray').place(x=210, y=15)
            
            # Show question
            Label(self.mainFrame, fg='white', text=question, background='gray').place(x=15, y=55)
            
            # Button show answer
            Button(self.mainFrame, text='show answer', command=lambda: self.showAnswerButton(answer)).place(x=350, y=210)
            
            # Button Next
            if indice + 1 < len(self.questions):
                Button(self.mainFrame, text='next', command=lambda: self.fillMainFrame(self.questions[indice+1][0], self.questions[indice+1][1], self.questions[indice+1][2], indice+1)).place(x=393, y=410)
            else:
                Button(self.mainFrame, text='finish', command=self.endQuiz).place(x=393, y=410)
            # Standard buttons  
            new_question = Button(self.mainFrame, text='new question', command=self.fillFrameNewQuestion) 
            new_question.place(x=10, y=15, width=80)
            
            delete = Button(self.mainFrame, text='delete', command=lambda: self.deleteButton(id))
            delete.place(x=290, y=15, width=70)
            
            edit = Button(self.mainFrame, text='edit', command=lambda: self.fillEditFrame(question, answer, id))
            edit.place(x=370, y=15, width=70)
        else:
            new_question = Button(self.mainFrame, text='new question', command=self.fillFrameNewQuestion) 
            new_question.place(x=200, y=200, width=80)
            
    def showAnswerButton (self, answer):
        canvas = Canvas(self.mainFrame, width=430, height=150, bg="gray")
        canvas.place(x=10, y=245)
        
        Label(self.mainFrame, fg='white', text=answer, background='gray').place(x=15, y=250)
        
        # scoreboard system
        right = Button(self.window, text='right', fg='white', bg='green', command=lambda: self.placar('right'))
        right.place(x=10, y=410, width=50)
        
        wrong = Button(self.window, fg='white', bg='red', text='wrong', command=lambda: self.placar('wrong'))
        wrong.place(x=70, y=410, width=50)
        
    def placar (self, answer):
        if answer == 'right':
            self.hits += 1
        else:
            self.errors += 1