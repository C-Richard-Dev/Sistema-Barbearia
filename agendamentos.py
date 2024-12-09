import sqlite3
from flet import *
from main import AppBarbearia

class TelaAgendamentos():
    def __init__(self,page:Page):
        self.page = page
        self.setup_interface()

    def setup_interface(self):
        self.page.clean

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
                    Text("Cliente", size=20, color="black", width=280, weight="bold"),
                    Text("Barbeiro", size=20, color="black", width=280, weight="bold"),
                    Text("Serviço", size=20, color="black", width=280, weight="bold"),
                    Text("Data", size=20, color="black", width=280, weight="bold"),
                    Text("Horário", size=20, color="black", width=280, weight="bold"),
                ]
            )
        )
        

        titulo = Text(
            "Agendamentos",
            size=30,
            color="white",
            weight="bold"
        )

        self.lista_agendamentos = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True,
        )
        #self.atualizar_lista_agendamentos()

        lista_agendamentos_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_agendamentos],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,  # Defina a altura máxima para ativar a rolagem
            
        )

        botao_adicionar_agendamento =  ElevatedButton(
            text="Novo Agendamento",
            bgcolor="black",
            color="white",
            width=250,
            height=50,
            icon=icons.ADD,
            on_click=self.tela_novo_agendamento
        )



        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar,
                        ],

                    )
                ]
            ),
            Column(
                controls=[
                    Row(
                        controls=[
                            titulo
                        ],
                        alignment= "center"

                    ),
                    cabecalho,
                    lista_agendamentos_container,
                ],
            ),
            Row(
                controls=[
                    botao_adicionar_agendamento
                ]
            )

        )

        self.atualizar_lista_agendamentos()


    def excluir_agendamento(self, dado_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Agendamentos WHERE rowid = ?", (dado_id,))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_agendamentos()


    def atualizar_lista_agendamentos(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid , cliente, barbeiro, servico, data, hora FROM Agendamentos")
        agendamentos = cursor.fetchall()
        conexao.close()

        self.lista_agendamentos.controls.clear()

        for dado in agendamentos:
            dado_id , cliente, barbeiro, servico, data, hora = dado
            item = Row(
                controls=[
                    Text(f"{cliente}", size=20, color="black", width=280),
                    Text(f"{barbeiro}", size=20, color="black", width=280),
                    Text(f"{servico}", size=20, color="black", width=280),
                    Text(f"{data}", size=20, color="black", width=280),
                    Text(f"{hora}", size=20, color="black", width=280),
                    ElevatedButton(
                        "Apagar",
                        bgcolor="red",
                        color="white",
                        on_click= lambda e, dado_id=dado_id: self.excluir_agendamento(dado_id)
                    ),
                ],
                spacing=3,
            )
            self.lista_agendamentos.controls.append(item)
        self.page.update()



    def salvar_agendamento(self,cliente,barbeiro,servico,data,hora):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Agendamentos (cliente, barbeiro, servico, data, hora) VALUES (?,?,?,?,?)",(cliente,barbeiro,servico,data,hora))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_agendamentos()

        print(f"O agendamento do cliente {cliente} foi marcada para o dia {data} ás {hora}.")




    def tela_novo_agendamento(self,e):

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

        servicos = [row[0] for row in cursor.execute("SELECT serviço FROM Serviços").fetchall()]
        servico = Dropdown(
            label="Serviço",
            label_style=TextStyle(color="white"),
            options=[dropdown.Option(servico) for servico in servicos],
            border_color="white",
            color="white",
            bgcolor="black",
            width=400,
        ) 

        conexao.close()

        cliente = TextField(label="Cliente",label_style=TextStyle(color="white"), hint_text="Nome do cliente", border_color="white", color="white",bgcolor="black")
        data = TextField(label="Data",label_style=TextStyle(color="white"), hint_text="dia/mês",border_color="white", color="white", bgcolor="black")
        hora = TextField(label="Horário",label_style=TextStyle(color="white"), hint_text="Hora marcada",border_color="white", color="white", bgcolor="black")


        overlay = Container(
            bgcolor="black",
            border_radius=20,
            border=border.all(2,"white"),
            content=Column(
                controls=[
                    Text("Novo Agendamento", size=25, color="white"),
                    cliente,
                    barbeiro,
                    servico,
                    data,
                    hora,

                    Row(
                        controls=[
                            ElevatedButton(
                                "Cadastrar",
                                color="white",
                                bgcolor="green",
                                on_click= lambda e :(
                                    self.salvar_agendamento(cliente.value, barbeiro.value, servico.value, data.value, hora.value),
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
            width=800,
            height=700,
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
        