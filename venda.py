from main import AppBarbearia
from flet import *
from datetime import datetime 
import sqlite3


class TelaVendas():
    def __init__(self, page:Page ):
        self.page=page 
        self.carrinho = []
        self.setup_interface()


    def setup_interface(self):
        self.page.clean

#Elementos da tela 1:------------------------------------------------------------------------------------------------------------------

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

        self.cliente = TextField(label="Cliente",label_style=TextStyle(color="white"), hint_text="Nome do cliente", border_color="white", color="white",bgcolor="black")

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
            height=510,  # Defina a altura máxima para ativar a rolagem
            
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_servicos],
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
                    cabecalho_servicos,
                    self.lista_servicos_container,
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
            on_click= self.finalizar_venda_servico
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
        self.atualizar_lista_servicos()

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
                    ElevatedButton(
                        "Adicionar",
                        color="white",
                        bgcolor="green",
                        on_click= lambda e, nome_servico=nome_servico, preco_servico=preco_servico: self.adicionar_ao_carrinho(nome_servico,preco_servico) 
                    ),
                ],

                spacing=15
            )
            self.lista_servicos.controls.append(item)
            self.page.update()

    

    def adicionar_ao_carrinho(self, nome_servico, preco_servico):
        self.carrinho.append({
            "nome": nome_servico,
            "preco": preco_servico
        })
        self.atualizar_carrinho()
        print(f"o serviço {nome_servico} foi adicionado ao carrinho com o preço de R${preco_servico}")

        self.total += preco_servico
        self.total_label.value = f"R$ {self.total:.2f}"
        self.page.update()

    def remover_do_carrinho(self,index, preco_servico):
        if isinstance(index, int) and 0 <= index < len(self.carrinho):
            self.carrinho.pop(index)
            self.atualizar_carrinho()

        self.total -= preco_servico
        self.total_label.value = f"R$ {self.total:.2f}"
        self.page.update()



    def atualizar_carrinho (self):
        self.lista_carrinho.controls.clear()
        #self.carrinho.sort(key= lambda servico: float(servico["preco"]))

        for index, servico in enumerate (self.carrinho):
            item = Row(
                controls=[
                    Text(f"{servico['nome']}", size=20, color="white", width=130),
                    Text(f"R${servico['preco']}", size=20, color="green", width=130),
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
        self.page.update()

    def finalizar_venda_servico(self,e):
        if not self.carrinho:
            alert_dialog = AlertDialog(
            modal=True,
            content=Text("Preencha todos os campos de informação, por favor."),
            actions=[
                ElevatedButton(
                    text="Ok",
                    on_click= self.fechar_dialog
                )
            ]
        )
        else:
            total = self.total
            cliente = self.cliente.value
            barbeiro = self.barbeiro.value
            forma_pagamento = self.pagamento.value
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO RegistroServiços (total, cliente, barbeiro, pagamento, data) VALUES (?,?,?,?,?)''',
                           (total, cliente, barbeiro, forma_pagamento, data))
            conn.commit()
            conn.close()

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
            self.carrinho.clear()
            self.atualizar_carrinho()
            self.total = 0.00
            self.total_label.value = f"R$ {self.total:.2f}"


            
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()

            

        self.page.dialog = alert_dialog
        alert_dialog.open = True
        self.page.update()
    
        
    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)