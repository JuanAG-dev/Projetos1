import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
from datetime import datetime

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('crm_sebrae.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    cpf TEXT UNIQUE,
                    cidade TEXT,
                    celular TEXT,
                    email TEXT NOT NULL,
                    cnpj TEXT,
                    segmento TEXT,
                    cnae TEXT,
                    usuario_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS projetos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    data TEXT,
                    local TEXT,
                    responsaveis TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT,
                    descricao TEXT,
                    data TEXT,
                    participantes TEXT)''')
    conn.commit()
    conn.close()

# Interface gráfica
class CRMSebraeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRM SEBRAE")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0078D7')
        init_db()
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:", bg='#0078D7', fg='white').pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", bg='#0078D7', fg='white').pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login, bg='#004A8F', fg='white').pack(pady=10)
        tk.Button(self.root, text="Register", command=self.create_register_screen, bg='#004A8F', fg='white').pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect('crm_sebrae.db')
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
        if c.fetchone():
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
        conn.close()

    def create_register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:", bg='#0078D7', fg='white').pack(pady=10)
        self.reg_username_entry = tk.Entry(self.root)
        self.reg_username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", bg='#0078D7', fg='white').pack(pady=10)
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register, bg='#004A8F', fg='white').pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_login_screen, bg='#004A8F', fg='white').pack(pady=10)

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        conn = sqlite3.connect('crm_sebrae.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
            self.create_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    def create_main_screen(self):
        self.clear_screen()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Aba de Clientes
        self.clientes_frame = tk.Frame(self.notebook, bg='#0078D7')
        self.notebook.add(self.clientes_frame, text="Clientes")
        self.create_clientes_screen()

        # Aba de Projetos
        self.projetos_frame = tk.Frame(self.notebook, bg='#0078D7')
        self.notebook.add(self.projetos_frame, text="Projetos")
        self.create_projetos_screen()

        # Aba de Agenda
        self.agenda_frame = tk.Frame(self.notebook, bg='#0078D7')
        self.notebook.add(self.agenda_frame, text="Agenda")
        self.create_agenda_screen()

    def create_clientes_screen(self):
        tk.Label(self.clientes_frame, text="Nome:", bg='#0078D7', fg='white').grid(row=0, column=0, padx=10, pady=10)
        self.nome_entry = tk.Entry(self.clientes_frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.clientes_frame, text="Sobrenome:", bg='#0078D7', fg='white').grid(row=1, column=0, padx=10, pady=10)
        self.sobrenome_entry = tk.Entry(self.clientes_frame)
        self.sobrenome_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.clientes_frame, text="CPF:", bg='#0078D7', fg='white').grid(row=2, column=0, padx=10, pady=10)
        self.cpf_entry = tk.Entry(self.clientes_frame)
        self.cpf_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.clientes_frame, text="Cidade:", bg='#0078D7', fg='white').grid(row=3, column=0, padx=10, pady=10)
        self.cidade_entry = tk.Entry(self.clientes_frame)
        self.cidade_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.clientes_frame, text="Celular:", bg='#0078D7', fg='white').grid(row=4, column=0, padx=10, pady=10)
        self.celular_entry = tk.Entry(self.clientes_frame)
        self.celular_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.clientes_frame, text="E-mail:", bg='#0078D7', fg='white').grid(row=5, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.clientes_frame)
        self.email_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(self.clientes_frame, text="Cadastrar Cliente", command=self.cadastrar_cliente, bg='#004A8F', fg='white').grid(row=6, column=0, columnspan=2, pady=10)

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        sobrenome = self.sobrenome_entry.get()
        cpf = self.cpf_entry.get()
        cidade = self.cidade_entry.get()
        celular = self.celular_entry.get()
        email = self.email_entry.get()

        if nome and sobrenome and cpf and cidade and celular and email:
            conn = sqlite3.connect('crm_sebrae.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO clientes (nome, sobrenome, cpf, cidade, celular, email) VALUES (?, ?, ?, ?, ?, ?)",
                          (nome, sobrenome, cpf, cidade, celular, email))
                conn.commit()
                messagebox.showinfo("Success", "Cliente cadastrado com sucesso!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "CPF já cadastrado.")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Todos os campos são obrigatórios.")

    def create_projetos_screen(self):
        tk.Label(self.projetos_frame, text="Nome do Projeto:", bg='#0078D7', fg='white').grid(row=0, column=0, padx=10, pady=10)
        self.projeto_nome_entry = tk.Entry(self.projetos_frame)
        self.projeto_nome_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.projetos_frame, text="Data:", bg='#0078D7', fg='white').grid(row=1, column=0, padx=10, pady=10)
        self.projeto_data_entry = tk.Entry(self.projetos_frame)
        self.projeto_data_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.projetos_frame, text="Local:", bg='#0078D7', fg='white').grid(row=2, column=0, padx=10, pady=10)
        self.projeto_local_entry = tk.Entry(self.projetos_frame)
        self.projeto_local_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.projetos_frame, text="Responsáveis:", bg='#0078D7', fg='white').grid(row=3, column=0, padx=10, pady=10)
        self.projeto_responsaveis_entry = tk.Entry(self.projetos_frame)
        self.projeto_responsaveis_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.projetos_frame, text="Cadastrar Projeto", command=self.cadastrar_projeto, bg='#004A8F', fg='white').grid(row=4, column=0, columnspan=2, pady=10)

    def cadastrar_projeto(self):
        nome = self.projeto_nome_entry.get()
        data = self.projeto_data_entry.get()
        local = self.projeto_local_entry.get()
        responsaveis = self.projeto_responsaveis_entry.get()

        if nome and data and local and responsaveis:
            conn = sqlite3.connect('crm_sebrae.db')
            c = conn.cursor()
            c.execute("INSERT INTO projetos (nome, data, local, responsaveis) VALUES (?, ?, ?, ?)",
                       (nome, data, local, responsaveis))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Projeto cadastrado com sucesso!")
        else:
            messagebox.showerror("Error", "Todos os campos são obrigatórios.")

    def create_agenda_screen(self):
        tk.Label(self.agenda_frame, text="Tipo de Evento:", bg='#0078D7', fg='white').grid(row=0, column=0, padx=10, pady=10)
        self.evento_tipo_entry = tk.Entry(self.agenda_frame)
        self.evento_tipo_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.agenda_frame, text="Descrição:", bg='#0078D7', fg='white').grid(row=1, column=0, padx=10, pady=10)
        self.evento_descricao_entry = tk.Entry(self.agenda_frame)
        self.evento_descricao_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.agenda_frame, text="Data:", bg='#0078D7', fg='white').grid(row=2, column=0, padx=10, pady=10)
        self.evento_data_entry = tk.Entry(self.agenda_frame)
        self.evento_data_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.agenda_frame, text="Participantes:", bg='#0078D7', fg='white').grid(row=3, column=0, padx=10, pady=10)
        self.evento_participantes_entry = tk.Entry(self.agenda_frame)
        self.evento_participantes_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.agenda_frame, text="Adicionar Evento", command=self.adicionar_evento, bg='#004A8F', fg='white').grid(row=4, column=0, columnspan=2, pady=10)

    def adicionar_evento(self):
        tipo = self.evento_tipo_entry.get()
        descricao = self.evento_descricao_entry.get()
        data = self.evento_data_entry.get()
        participantes = self.evento_participantes_entry.get()

        if tipo and descricao and data and participantes:
            conn = sqlite3.connect('crm_sebrae.db')
            c = conn.cursor()
            c.execute("INSERT INTO eventos (tipo, descricao, data, participantes) VALUES (?, ?, ?, ?)",
                       (tipo, descricao, data, participantes))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Evento adicionado com sucesso!")
        else:
            messagebox.showerror("Error", "Todos os campos são obrigatórios.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Iniciar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = CRMSebraeApp(root)
    root.mainloop()