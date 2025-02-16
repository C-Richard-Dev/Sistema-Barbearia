from flet import *
import sqlite3
from main import AppBarbearia 

class TelaServicos:
    def __init__(self, page: Page):
        self.page = page
        self.lista_servicos = None
        self.setup_interface()

    def setup_interface(self):
        self.page.clean()
        

        titulo_servicos = Text(
            "Lista de Serviços",
            size=30,
            color="white",
            weight="bold",
        )

        # Botão de voltar
        botao_voltar = ElevatedButton(
            text=" ",
            bgcolor="black",
            color="white",
            width=100,
            height=50,
            icon=icons.ARROW_BACK,
            on_click=lambda e: self.voltar()
        )

        # Botão de adicionar serviço
        botao_adicionar = ElevatedButton(
            text="Adicionar Serviço",
            bgcolor="black",
            color="white",
            width=250,
            height=50,
            icon=icons.ADD,
            on_click=self.tela_adicionar_servico
        )

        # Cabeçalho
        cabecalho = Container(
            bgcolor="white",
            padding=10,
            border_radius=15,
            content=Row(
                controls=[
                    Text("Nome", size=20, color="black", weight="bold", width=250),
                    Text("Preço" , size=20, color="black", weight="bold", width=250),
                ],
            ),
            expand=True
        )

        # Lista de serviços
        self.lista_servicos = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )

        lista_servicos_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_servicos],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,  # Defina a altura máxima para ativar a rolagem
        )
        self.atualizar_lista_servicos()

        #para adicionar os elementos da tela
        self.page.add(Column(
            controls=[
                Row(
                    controls=[botao_voltar, titulo_servicos, botao_adicionar],
                ),
                cabecalho,
                lista_servicos_container,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=30
        ))

        self.atualizar_lista_servicos()

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)
        

    def salvar_servico(self, nome_servico, preco_servico):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Serviços (serviço, preço_serviço) VALUES (?,?)", (nome_servico, preco_servico))
        conexao.commit()
        conexao.close()

        self.atualizar_lista_servicos()

        print(f"O Serviço {nome_servico} foi salvo com o preço de {preco_servico} no banco de dados!")

    def excluir_servico(self, servico_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Serviços WHERE rowid = ?", (servico_id,))
        conexao.commit()
        conexao.close()
        self.atualizar_lista_servicos()

    def atualizar_lista_servicos(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, serviço, preço_serviço FROM Serviços")
        servicos = cursor.fetchall()
        conexao.close()

        # Limpa a lista atual
        self.lista_servicos.controls.clear()

        # Adiciona cada serviço
        for servico in servicos:
            servico_id, nome_servico, preco_servico = servico
            item = Row(
                controls=[
                    Text(f"{nome_servico}", size=20, color="black",width=280 ),
                    Text(f"R${preco_servico}", size=20, color="black", width=280),
                    ElevatedButton(
                        "Excluir",
                        color="white",
                        bgcolor="red",
                        on_click=lambda e, servico_id=servico_id: self.excluir_servico(servico_id)
                    ),
                ],

                spacing=25
            )
            self.lista_servicos.controls.append(item)
            self.page.update()

    def tela_adicionar_servico(self, e): #Exibe o popup para adicionar serviço
        nome_servico = TextField(label="Nome do serviço", hint_text="Digite o nome do serviço")
        preco_servico = TextField(label="Preço", hint_text="Digite o preço do serviço", keyboard_type="number")

        def validar_preco(preco_servico):
            try:
                return float(preco_servico)
            except ValueError:
                return None

        overlay = Container(
            bgcolor='white',
            border_radius=20,
            content=Column(
                controls=[
                    Text("Adicionar Serviço", size=25, color="black"),
                    nome_servico,
                    preco_servico,
                    Row(
                        controls=[
                            ElevatedButton(
                                "Adicionar",
                                color="white",
                                bgcolor="green",
                                on_click=lambda e: (
                                    self.salvar_servico(nome_servico.value, validar_preco(preco_servico.value))
                                    if validar_preco(preco_servico.value) is not None else None,

                                e.page.overlay.remove(centered_overlay) if validar_preco(preco_servico.value) is not None else None,
                                e.page.update()
                            ),
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
            height=300,
            padding=20,
        )

        centered_overlay = Container(
            expand=True,
            alignment=alignment.center,
            content=overlay,
        )

        e.page.overlay.append(centered_overlay)
        e.page.update()