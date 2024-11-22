from flet import *
import flet as ft
import sqlite3
from main import AppBarbearia 

class TelaProdutos:
    def __init__(self, page:Page):
        self.page = page
        self.setup_interface()

    def setup_interface(self):
        self.page.clean()

        botao_adicionar_produto = ElevatedButton(
            text="Adicionar Produto",
            bgcolor="black",
            color="white",
            width=250,
            height=50,
            icon=icons.ADD,
            on_click= self.tela_adicionar_produto
        )

        titulo_produtos = Text(
            "Lista de Produtos",
            size=30,
            color="white",
            weight="bold",
        )

        botao_voltar = ElevatedButton(
            text=" ",
            bgcolor="black",
            color="white",
            width=100,
            height=50,
            icon=icons.ARROW_BACK,
            on_click=lambda e: self.voltar()
        )

        cabecalho = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Nome", size=20, color="black",width=280, weight="bold"),
                    Text("Preço", size=20, color="black",width=280, weight="bold"),
                    Text("Quantidade", size=20, color="black",width=280, weight="bold"),
                    Text("Observação", size=20, color="black",width=280, weight="bold"),
                ],
            ),
            expand=True
        )

        self.lista_produtos = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True 
        )
        self.atualizar_lista_produtos()

        lista_produtos_container = Container(       
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_produtos],
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
                            titulo_produtos,
                            botao_adicionar_produto
                        ],
                    ), 
                    cabecalho,
                    lista_produtos_container 
                ],
            ),
        )
        self.atualizar_lista_produtos()
    

    def salvar_produto(self, nome_produto, preco_produto, quantidade_produto, obs_produto):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Produtos (produto, preco_produto, quantidade_produto, obs_produto) VALUES (?,?,?,?)", (nome_produto, preco_produto, quantidade_produto, obs_produto))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_produtos()

        print(f"O produto {nome_produto} foi salvo no banco de dados!")

    def excluir_produto(self,produto_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Produtos WHERE rowid = ?", (produto_id,))
        conexao.commit()
        conexao.close()
        self.atualizar_lista_produtos()

    def atualizar_lista_produtos(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, produto, preco_produto, quantidade_produto, obs_produto FROM Produtos")
        produtos = cursor.fetchall()
        conexao.close()

        self.lista_produtos.controls.clear()

        for produto in produtos:
            produto_id, nome_produto, preco_produto, quantidade_produto, obs_produto = produto
            item = Row(
                controls=[
                    Text(f"{nome_produto}", size=20, color="black", width=280),
                    Text(f"R${preco_produto}", size=20, color="black", width=280),
                    Text(f"{quantidade_produto}", size=20, color="black", width=280),
                    Text(f"{obs_produto}", size=20, color="black", width=250),
                    ElevatedButton(
                        "Excluir",
                        color="white",
                        bgcolor="red",
                        on_click=lambda e, produto_id=produto_id: self.excluir_produto(produto_id)
                    ),
                ],
                

                spacing=25
            )
            self.lista_produtos.controls.append(item)
            self.page.update()


    def tela_adicionar_produto(self,e):

        nome_produto= TextField(label="Nome do produto", hint_text="Digite o nome do produto") #texto
        preco_produto= TextField(label="Preço do produto", hint_text="Digite o preço do produto", keyboard_type="number")#número
        quantidade_produto= TextField(label="Quantidade do produto", hint_text="Digite a quantidade do produto", keyboard_type="number")#número
        obs_produto= TextField(label="Observação", hint_text="Digite uma observação para esse produto")#Texto

        def validar(preco_produto, quantidade_produto):
            try:
                return float(preco_produto), float(quantidade_produto)
            except ValueError:
                return None

        overlay = Container( #popup - conteúdo e aparencia do popup
            bgcolor='white',
            border_radius=20,
            border=border.all(2,"black"),
            content=Column(
                controls=[
                    Text("Adicionar Produto", size=25, color="black"),
                    nome_produto,
                    preco_produto,
                    quantidade_produto,
                    obs_produto,
                    Row(
                        controls=[
                            ElevatedButton(
                                "Adicionar",
                                color="white",
                                bgcolor="green",
                                on_click=lambda e:(
                                    self.salvar_produto(nome_produto.value, preco_produto.value, quantidade_produto.value, obs_produto.value) 
                                    if validar(preco_produto.value, quantidade_produto.value) else None,

                                    e.page.overlay.remove(centered_overlay) if validar(preco_produto.value, quantidade_produto.value) is not None else None,
                                    e.page.update()
                                )
                            ),
                       

                            ElevatedButton(
                                "Cancelar",
                                color="white",
                                bgcolor="red",
                                on_click=lambda e: (
                                    e.page.overlay.remove(centered_overlay),
                                    e.page.update()
                                )
                            ),
                        ],
                        alignment="end",
                    ),
                ],
                spacing=10,
                alignment="start",
                horizontal_alignment="center"
            ),
            width=400,
            height=500,
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


