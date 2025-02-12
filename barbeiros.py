import sqlite3
from flet import *
from main import AppBarbearia

class TelaBarbeiros:
    def __init__(self, page: Page):
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
            "Barbeiros Cadastrados",
            size=30,
            color="white",
            weight="bold"
        )

        botao_cadastrar_barbeiro = ElevatedButton(
            text="Cadastrar",
            bgcolor="black",
            color="white",
            width=250,
            height=50,
            icon=icons.ADD,
            on_click=self.tela_cadastrar_barbeiro
        )

        cabecalho = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Nome", size=20, color="black", width=280, weight="bold"),
                    Text("Contato", size=20, color="black", width=280, weight="bold"),
                    Text("Cortes Realizados", size=20, color="black", width=280, weight="bold"),
                ],
            ),
            expand=True
        )

        self.lista_barbeiros = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_barbeiros()

        lista_barbeiros_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_barbeiros],
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
                            botao_cadastrar_barbeiro
                        ]
                    ),
                    cabecalho,
                    lista_barbeiros_container,
                ]
            )
        )
        self.atualizar_lista_barbeiros()

    def excluir_barbeiro(self, barbeiro_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Barbeiros WHERE rowid = ?", (barbeiro_id,))
        conexao.commit()
        conexao.close()
        self.atualizar_lista_barbeiros()

    def atualizar_lista_barbeiros(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, nome_barbeiro, contato_barbeiro FROM Barbeiros")
        barbeiros = cursor.fetchall()
        conexao.close()

        self.lista_barbeiros.controls.clear()

        for barbeiro in barbeiros:
            barbeiro_id, nome_barbeiro, contato_barbeiro = barbeiro
            item = Row(
                controls=[
                    Text(f"{nome_barbeiro}", size=20, color="black", width=280),
                    Text(f"{contato_barbeiro}", size=20, color="black", width=280),
                    ElevatedButton(
                        "Excluir",
                        bgcolor="red",
                        color="white",
                        on_click=lambda e, barbeiro_id=barbeiro_id: self.excluir_barbeiro(barbeiro_id)
                    ),
                ],
                spacing=25
            )
            self.lista_barbeiros.controls.append(item)
        self.page.update()

    def salvar_barbeiro(self, nome_barbeiro, contato_barbeiro):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Barbeiros (nome_barbeiro, contato_barbeiro) VALUES (?, ?)", (nome_barbeiro, contato_barbeiro))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_barbeiros()

        print(f"O barbeiro {nome_barbeiro} foi salvo no BD com o contato: {contato_barbeiro}")

    def tela_cadastrar_barbeiro(self, e):
        nome_barbeiro = TextField(label="Nome", hint_text="Escreva o nome do barbeiro")
        contato_barbeiro = TextField(label="Contato", hint_text="Escreva o número do barbeiro")

        overlay = Container(
            bgcolor='white',
            border_radius=20,
            border=border.all(2,"black"),
            content=Column(
                controls=[
                    Text("Cadastrar Barbeiro", size=25, color="black"),
                    nome_barbeiro,
                    contato_barbeiro,

                    Row(
                        controls=[
                            ElevatedButton(
                                "Cadastrar",
                                color="white",
                                bgcolor="green",
                                on_click=lambda e: (
                                    self.salvar_barbeiro(nome_barbeiro.value, contato_barbeiro.value),
                                    e.page.overlay.remove(centered_overlay),
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
                            )
                        ],
                        alignment="end"
                    )
                ]
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
