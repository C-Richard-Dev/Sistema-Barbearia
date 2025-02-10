from main import AppBarbearia
from flet import *
from datetime import datetime 
import sqlite3



class TelaVendaServico():
    def __init__(self, page: Page):
        self.page = page
        self.carrinho = []
        self.setup_interface()


    def setup_interface(self):
        self.page.clean()

        # Elementos da tela 1:------------------------------------------------------------------------------------------------------------------

        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()

        barbeiros = [row[0] for row in cursor.execute("SELECT nome_barbeiro FROM Barbeiros").fetchall()]
        self.barbeiro = Dropdown(
            label="Barbeiro",
            label_style=TextStyle(color="white"),
            options=[dropdown.Option(nome) for nome in barbeiros],
            border_color="white",
            color="white",
            bgcolor="black",
            width=400,
        )
        conexao.close()

        self.pagamento = Dropdown(
            label="Forma de Pagamento",
            label_style=TextStyle(color="white"),
            options=[
                dropdown.Option(key="pix", text="Pix"),
                dropdown.Option(key="dinheiro", text="Dinheiro"),
                dropdown.Option(key="cartao_debito", text="Cartão de Débito"),
                dropdown.Option(key="cartao_credito", text="Cartão de Crédito"),
            ],
            border_color="white",
            color="white",
            bgcolor="black",
            width=300,
        )

        self.cliente = TextField(
            label="Cliente",
            label_style=TextStyle(color="white"),
            hint_text="Nome do cliente",
            border_color="white",
            color="white",
            bgcolor="black"
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
            height=510,  # Defina a altura máxima para ativar a rolagem
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
                            self.cliente,
                            self.barbeiro,
                            self.pagamento,
                            ]
                    ),
                    cabecalho_produtos,
                    self.lista_produtos_container,
                ]
            )
        )

    #Elementos tela 2-------------------------------------------------------------------------------------------------------------------------------
        self.lista_carrinho = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True,
        )

        carrinho_container = Container(
            bgcolor="black",
            border_radius=15,
            padding=10,
            height=400,  
            
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_carrinho],
                scroll="adaptive",
                width=360,
                height=300,
                
            ),
            
            
        )

        botao_registrar_compra = ElevatedButton(
            text="Finalizar",
            bgcolor="yellow",
            color="white",
            width=250,
            height=50,
            on_click= self.finalizar_venda_produto
            )


        self.total = 0.00 #tipo float
        # texto que exibe o total
        self.total_label = Text(f"R$ {self.total:.2f}", size=20, color="green", weight="bold")



        #Conteúdo da segunda tela
        tela2 = Container(
            width=410,
            height=700,
            bgcolor="white",
            border_radius=20,
            border=border.all(2,"black"),
            padding=15,
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
                    ),
                    Row(
                        controls=[
                            carrinho_container
                        ]
                    ),
                    Row(
                        controls=[
                            Text("TOTAL",
                                
                                size=20,
                                color="black",
                                )
                        ],
                    alignment="left"
                    ),
                    Row(
                        controls=[
                            self.total_label
                        ]
                    ),
                    Row(
                        controls=[
                            botao_registrar_compra
                        ],
                    alignment="end"
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
        self.atualizar_lista_produtos()

    def atualizar_lista_produtos(self):  # Função para manter atualizada a lista de produtos
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, produto, preco_produto, quantidade_produto FROM Produtos")
        produtos = cursor.fetchall()
        conexao.close()

        self.lista_produtos.controls.clear()

        for produto in produtos:
            produto_id, nome_produto, preco_produto, quantidade_produto = produto
            item = Row(
                controls=[
                    Text(f"{nome_produto}", size=20, color="black", width=200),
                    Text(f"R${preco_produto}", size=20, color="black", width=150),
                    Text(f"Qtd: {quantidade_produto}", size=20, color="black", width=150),
                    ElevatedButton(
                        "Adicionar",
                        color="white",
                        bgcolor="green",
                        on_click=lambda e, nome_produto=nome_produto, preco_produto=preco_produto: self.adicionar_ao_carrinho(nome_produto, preco_produto)
                    ),
                ],
                spacing=15
            )
            self.lista_produtos.controls.append(item)
        
        self.page.update()

    def adicionar_ao_carrinho(self, nome_produto, preco_produto):
        self.carrinho.append({
            "nome": nome_produto,
            "preco": preco_produto
        })
        self.atualizar_carrinho()
        print(f"O produto {nome_produto} foi adicionado ao carrinho com o preço de R${preco_produto}")

        self.total += preco_produto
        self.total_label.value = f"R$ {self.total:.2f}"
        self.page.update()

    def remover_do_carrinho(self, index, preco_produto):
        if isinstance(index, int) and 0 <= index < len(self.carrinho):
            self.carrinho.pop(index)
            self.atualizar_carrinho()

        self.total -= preco_produto
        self.total_label.value = f"R$ {self.total:.2f}"
        self.page.update()

    def atualizar_carrinho(self):
        self.lista_carrinho.controls.clear()

        for index, produto in enumerate(self.carrinho):
            item = Row(
                controls=[
                    Text(f"{produto['nome']}", size=20, color="white", width=130),
                    Text(f"R${produto['preco']}", size=20, color="green", width=130),
                    ElevatedButton(
                        "X",
                        color="white",
                        bgcolor="red",
                        width=50,
                        on_click=lambda e, idx=index: self.remover_do_carrinho(idx, self.carrinho[idx]["preco"])
                    )
                ],
            )
            self.lista_carrinho.controls.append(item)
        self.page.update()

    def fechar_dialog(self,e):
        self.page.dialog.open=False
        self.page.clean()
        TelaVendaServico(self.page)
        self.page.update()   

    def finalizar_venda_produto(self, e):
        if not self.carrinho:
            alert_dialog = AlertDialog(
                modal=True,
                content=Text("Preencha todos os campos de informação, por favor."),
                actions=[
                    ElevatedButton(
                        text="Ok",
                        on_click=self.fechar_dialog
                    )
                ]
            )
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()
        else:
            total = self.total
            cliente = self.cliente.value
            barbeiro = self.barbeiro.value
            forma_pagamento = self.pagamento.value
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Registrar a venda na tabela RegistroProdutos
            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Registro_Produtos (total_produto, cliente_produto, barbeiro_produto, pagamento_produto, data_produto) 
                            VALUES (?, ?, ?, ?, ?)''',
                        (total, cliente, barbeiro, forma_pagamento, data))
            conn.commit()

            # Contar a quantidade de cada produto no carrinho
            produtos_vendidos = {}
            for produto in self.carrinho:
                nome_produto = produto["nome"]
                if nome_produto in produtos_vendidos:
                    produtos_vendidos[nome_produto] += 1
                else:
                    produtos_vendidos[nome_produto] = 1

            # Atualizar o estoque no banco de dados
            for nome_produto, quantidade_vendida in produtos_vendidos.items():
                cursor.execute('''UPDATE Produtos SET quantidade_produto = quantidade_produto - ? WHERE produto = ?''', 
                            (quantidade_vendida, nome_produto))
            conn.commit()
            conn.close()

            # Exibir a mensagem de sucesso
            alert_dialog = AlertDialog(
                modal=True,
                content=Text("Venda finalizada com sucesso!"),
                actions=[
                    ElevatedButton(
                        text="Ok",
                        on_click=self.fechar_dialog
                    )
                ]
            )

            # Limpar o carrinho e atualizar o total
            self.carrinho.clear()
            self.atualizar_carrinho()
            self.total = 0.00
            self.total_label.value = f"R$ {self.total:.2f}"

            # Mostrar o dialog
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)