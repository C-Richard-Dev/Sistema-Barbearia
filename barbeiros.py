from flet import *
import sqlite3
from main import AppBarbearia


class TelaBarbeiros:
    def __init__(self, page: Page):
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
            on_click= self.tela_cadastrar_barbeiro
        )
        cabecalho = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Nome", size=20, color="black",width=280, weight="bold"),
                    Text("Contato", size=20, color="black",width=280, weight="bold"),
                    Text("Cortes Realizados", size=20, color="black",width=280, weight="bold"),
                ],
            ),
            expand=True
        )


        self.page.add(Column(
            controls=[
                Row(
                    controls=[
                        botao_voltar,
                        titulo,
                        botao_cadastrar_barbeiro

                        ]
                ),
                cabecalho,
            ]
        ))

    def tela_cadastrar_barbeiro(self,e):
        nome_barbeiro = TextField(label="Nome", hint_text="Escreva o nome do barbeiro")
        contato_barbeiro = TextField(label="Contato", hint_text="Escreva o número do barbeiro")

        overlay = Container(
            bgcolor='white',
            border_radius=20,
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
                                    e.page.overlay.remove(centered_overlay),
                                    e.page.update())


                            ),
                            ElevatedButton(
                                "Cancelar",
                                color="white",
                                bgcolor="red",
                                on_click=lambda e: (
                                    e.page.overlay.remove(centered_overlay),
                                    e.page.update())
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