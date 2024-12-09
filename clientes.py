import sqlite3
from flet import *
from main import AppBarbearia


class TelaClientes():
    def __init__(self, page:Page):
        self.page = page
        self.setup_interface()

    def setup_interface(self):
        self.page.clean()

        botao_voltar = ElevatedButton(
            text=" ",
            bgcolor="black",
            color="white",
            width=100,
            height=50,
            icon=icons.ARROW_BACK,
            on_click=lambda e: self.voltar()
            )
        
        titulo = Text(
            "Lista de Clientes",
            size=30,
            color="white",
            weight="bold"
        )

        botao_cadastrar_cliente = ElevatedButton(
            text="Cadastrar",
            bgcolor="black",
            color="white",
            width=250,
            height=50,
            icon=icons.ADD,
            on_click=self.tela_cadastrar_cliente
        )

        cabecalho = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Nome", size=20, color="black", width=280, weight="bold"),
                    Text("Contato", size=20, color="black", width=280, weight="bold"),
                ]
            )
            
        )
        self.lista_clientes = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_clientes()

        lista_clientes_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_clientes],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,  # Defina a altura máxima para ativar a rolagem
            
        )


        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar,
                            titulo,
                            botao_cadastrar_cliente,
                        ]
                        ),
                        cabecalho,
                        lista_clientes_container,
                    ]
                )
            ),
        self.atualizar_lista_clientes()
        
    def excluir_cliente(self, cliente_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Clientes WHERE rowid = ?", (cliente_id,))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_clientes()

        
    def atualizar_lista_clientes(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, nome_cliente, contato_cliente FROM Clientes")
        clientes = cursor.fetchall()
        conexao.close()

        self.lista_clientes.controls.clear()

        for cliente in clientes:
            cliente_id, nome_cliente, contato_cliente = cliente
            item = Row(
                controls=[
                    Text(f"{nome_cliente}", size=20, color="black", width=280),
                    Text(f"{contato_cliente}",size=20, color="black", width=280),
                    ElevatedButton(
                        "Excluir",
                        bgcolor="red",
                        color="white",
                        on_click= lambda e, cliente_id=cliente_id: self.excluir_cliente(cliente_id)
                    ),
                ],
                spacing=25
            )
            self.lista_clientes.controls.append(item)
        self.page.update()


        
    def salvar_cliente(self, nome_cliente, contato_cliente):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Clientes (nome_cliente, contato_cliente) VALUES (?,?)",(nome_cliente, contato_cliente))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_clientes()

        print(f"O cliente {nome_cliente} foi cadastrado com sucesso no BD!")
    
        
    def tela_cadastrar_cliente(self,e):
        nome_cliente = TextField(label="Nome",label_style=TextStyle(color="white"), hint_text="Escreva o nome do cliente",border_color="white", color="white", bgcolor="black")
        contato_cliente = TextField(label="Contato",label_style=TextStyle(color="white"), hint_text="Número",border_color="white", color="white", bgcolor="black")
        
        overlay = Container(
            bgcolor="black",
            border_radius=20,
            border=border.all(2,"white"),
            content=Column(
                controls=[
                    Text("Cadastrar Cliente", size=25, color="white"),
                    nome_cliente,
                    contato_cliente,

                    Row(
                        controls=[
                            ElevatedButton(
                                "Cadastrar",
                                color="white",
                                bgcolor="green",
                                on_click= lambda e :(
                                    self.salvar_cliente(nome_cliente.value , contato_cliente.value),
                                    e.page.overlay.remove(centered_overlay),
                                    e.page.update()
                                )
                            ),
                            ElevatedButton(
                                "Cancelar",
                                color="white",
                                bgcolor="red",
                                on_click= lambda e: (
                                    e.page.overlay.remove(centered_overlay),
                                    e.page.update()
                                )
                            )
                        ],
                        alignment= "end",
                    )
                ],
    
            ),
            width=400,
            height=350,
            padding=20,
        )
        centered_overlay = Container(
            expand=True,
            alignment=alignment.center,
            content=overlay,
        )

        e.page.overlay.append(centered_overlay)
        e.page.update()

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)
