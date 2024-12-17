from main import AppBarbearia
from flet import *
import sqlite3

class TelaVendas():
    def __init__(self, page:Page ):
        self.page=page 
        self.setup_interface()

    def setup_interface(self):
        self.page.clean

#Elementos da tela 1:------------------------------------------------------------------------------------------------------------------

        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()

        barbeiros = [row[0] for row in cursor.execute("SELECT nome_barbeiro FROM Barbeiros").fetchall()]
        barbeiro = Dropdown(
            label="Barbeiro",
            label_style=TextStyle(color="white"),
            options=[dropdown.Option(nome) for nome in barbeiros],
            border_color="white",
            color="white",
            bgcolor="black",
            width=400,
        ) 
        conexao.close()

        pagamento = Dropdown(
            label="Forma de Pagamento",
            label_style=TextStyle(color="white"),
            options=[
                dropdown.Option(key="pix",text="Pix"),
                dropdown.Option(key="dinheiro",text="Dinheiro"),
                dropdown.Option(key="cartao_debito",text="Cartão de Débito"),
                dropdown.Option(key="cartao_credito",text="Cartão de Crédito"),
            ],
            border_color="white",
            color="white",
            bgcolor="black",
            width=300,
        )

        cliente = TextField(label="Cliente",label_style=TextStyle(color="white"), hint_text="Nome do cliente", border_color="white", color="white",bgcolor="black")

        cabecalho_servicos = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Serviços", size=20, color="black", width=280, weight="bold"),
                ]
            )
        )

        self.lista_servicos = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True,
        )
        self.lista_servicos_container = Container(
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=220,  # Defina a altura máxima para ativar a rolagem
            
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_servicos],
                scroll="adaptive",
            ),
            
            
        )

        cabecalho_produtos = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Produtos", size=20, color="black", width=280, weight="bold"),
                ]
            )
        )
        self.lista_produtos = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True,
        )
        self.lista_produtos_container = Container(
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=220,  
            
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_produtos],
                scroll="adaptive",
            ),
            
            
        )


        #Tela principal (onde são colocados as variáveis acima)
        tela1 = Container(
            width=1100,
            height=700,
            bgcolor="black",
            border_radius=20,
            border=border.all(2,"white"),
            padding=15,
            content= Column(
                controls=[
                    Row(
                        controls=[
                            Text("Dados da Venda",
                                size=20,
                                color="white"
                                )
                        ],
                        alignment= "center"
                    ),
                    Row(
                        controls=[
                            cliente,
                            barbeiro,
                            pagamento,
                            ]
                    ),
                    cabecalho_servicos,
                    self.lista_servicos_container,
                    cabecalho_produtos,
                    self.lista_produtos_container
                ]
            )
        )

    #-----------------------------------------------------------------------------------------------------------------------------------

        tela2 = Container(
            width=410,
            height=700,
            bgcolor="white",
            border_radius=20,
            border=border.all(2,"black"),
            content= Column(
                controls=[
                    Row(
                        controls=[
                            Text("Carrinho",
                                size=20,
                                color="black",
                                )
                        ],
                    alignment="center"
                    )
                ]
            )

        )


        botao_voltar = ElevatedButton(
            text="Voltar",
            bgcolor="white",
            color="black",
            width=250,
            height=50,
            icon=icons.ARROW_BACK,
            on_click=lambda e: self.voltar()
            )

        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            tela1,
                            tela2
                        ]
                    ),
                    Row(
                        controls=[
                            botao_voltar,
                        ]
                    )
                ]
            )
        )
        self.page.update()
        self.atualizar_lista_servicos()
        self.atualizar_lista_produtos()

#---------------------------------------------------------------------------------------------------------------------
    def atualizar_lista_servicos(self): #Função para manter atualizado a lista de serviços
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, serviço, preço_serviço FROM Serviços")
        servicos = cursor.fetchall()
        conexao.close()

        self.lista_servicos.controls.clear()

        for servico in servicos:
            servico_id, nome_servico, preco_servico = servico
            item = Row(
                controls=[
                    Text(f"{nome_servico}", size=20, color="black",width=280 ),
                    Text(f"R${preco_servico}", size=20, color="black", width=280),
                    Text(f"R${preco_servico}", size=20, color="black", width=280),
                    TextField(
                        label="Quantidade",
                        label_style=TextStyle(color="black"), 
                        hint_text="Quantidade", 
                        border_color="white", 
                        color="black",
                        bgcolor="grey",
                        width=150

                    ),
                    ElevatedButton(
                        "Adicionar",
                        color="white",
                        bgcolor="green",
                       #implementar a função on_click
                    ),
                ],

                spacing=15
            )
            self.lista_servicos.controls.append(item)
            self.page.update()

    def atualizar_lista_produtos(self): #Função para manter atualizado a lista de produtos
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, produto, preco_produto FROM Produtos")
        produtos = cursor.fetchall()
        conexao.close()

        self.lista_produtos.controls.clear()

        for produto in produtos:
            produto_id, nome_produto, preco_produto = produto
            item = Row(
                controls=[
                    Text(f"{nome_produto}", size=20, color="black",width=280 ),
                    Text(f"R${preco_produto}", size=20, color="black", width=280),
                    TextField(
                        label="Quantidade",
                        label_style=TextStyle(color="black"), 
                        hint_text="Quantidade", 
                        border_color="white", 
                        color="black",
                        bgcolor="grey",
                        width=150

                    ),
                    ElevatedButton(
                        "Adicionar",
                        color="white",
                        bgcolor="green",
                       #implementar a função on_click
                    ),
                ],

                spacing=15
            )
            self.lista_produtos.controls.append(item)
            self.page.update()



    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)
