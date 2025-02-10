import sqlite3
from flet import *
from main import AppBarbearia



class TelaHistoricoVendas():
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

        self.lista_historico = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_historico()

        lista_historico_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_historico],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,
        )

        botao_ver_barbeiros = ElevatedButton(
            text=" Ver Barbeiros ",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            
            on_click=lambda e: self.ver_barbeiros()
        )

        botao_ver_historico_mensal = ElevatedButton(
            text="Ver Histórico Mensal",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_mensal()
        )

        botao_ver_produtos_diarios = ElevatedButton(
            text=" Ver Produtos Diários" , 
            bgcolor= "white",
            color = "black",
            width= 300,
            height= 50,

            on_click= lambda e: self.ver_produtos_diarios()
        )

        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar,
                        ],
                    ), 
                    #cabecalho,
                    lista_historico_container ,
                    Row(
                        controls=[
                            botao_ver_barbeiros, botao_ver_historico_mensal, botao_ver_produtos_diarios
                        ]
                    )
                ],

            ),
        )
        self.atualizar_lista_historico()

    def buscar_historico(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT DATE(data) as dia, SUM(total) as total_diario, COUNT(*) as quantidade_cortes
            FROM RegistroServiços
            GROUP BY DATE(data)
            ORDER BY DATE(data)
            DESC
        ''')
        historico = cursor.fetchall()
        conexao.close()
        return historico


    def atualizar_lista_historico(self):
        historico = self.buscar_historico()
        self.lista_historico.controls.clear()

        for dia, total_diario, quantidade_cortes in historico:
            item = Container(
                content=Row(
                    controls=[
                        Text(f"Dia: {dia}", size=20, color="black",width=280, weight="bold"),
                        Text(f"Receita: R$ {total_diario:.2f}", size=20, color="green",width=280, weight="bold"),
                        Text(f"Cortes: {quantidade_cortes}", size=20, color="blue", width=200, weight="bold")
                    ]
                ),
                padding=5,
                border_radius=5,
                #bgcolor="white"
            )
            self.lista_historico.controls.append(item)
        
        self.page.update()

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def historico_mensal(self):
        self.page.clean()
        ListaDadosMensais(self.page)

    def ver_produtos_diarios(self):
        self.page.clean()
        ListaDadosProdutosDiarios(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)





# Cada class é uma lista diferente que será exibida

class ListaDadosBarbeiros():
    def __init__(self, page:Page):
        self.page = page
        self.setup_interface()

    def setup_interface(self):
        self.page.clean()

        botao_voltar= ElevatedButton(
            text=" ",
            bgcolor="black",
            color="white",
            width=100,
            height=50,
            icon=icons.ARROW_BACK,
            on_click=lambda e: self.voltar()   
        )

        self.lista_dados_barbeiro = ListView (
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_dados_barbeiro()

        lista_dados_barbeiro_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_dados_barbeiro],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,
        )


        botao_ver_historico_diario = ElevatedButton(
            text="Ver Histórico Diário",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_diario()
        )

        botao_ver_historico_mensal = ElevatedButton(
            text="Ver Histórico Mensal",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_mensal()
        )

        botao_ver_produtos_diarios = ElevatedButton(
            text=" Ver Produtos Diários" , 
            bgcolor= "white",
            color = "black",
            width= 300,
            height= 50,

            on_click= lambda e: self.ver_produtos_diarios()
        )


        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar,
                        ],
                    ), 
                    #cabecalho,
                    lista_dados_barbeiro_container ,
                    Row(
                        controls=[
                            botao_ver_historico_diario, botao_ver_historico_mensal, botao_ver_produtos_diarios
                        ]
                    )
                ],

            ),
        )


    def buscar_historico_barbeiro(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT DATE(data) as dia, barbeiro, COUNT(*) as quantidade_cortes, SUM(total) as valor_total
            FROM RegistroServiços
            GROUP BY DATE(data), barbeiro
            ORDER BY DATE(data) DESC, barbeiro ASC
        ''')
        historico = cursor.fetchall()
        conexao.close()

        historico_formatado = {}
        for dia, barbeiro, quantidade_cortes, valor_total in historico:
            if dia not in historico_formatado:
                historico_formatado[dia] = []
            historico_formatado[dia].append({
                "barbeiro": barbeiro,
                "cortes": quantidade_cortes,
                "lucro": valor_total
            })

        return historico_formatado
    


    def atualizar_lista_dados_barbeiro(self):
        historico = self.buscar_historico_barbeiro()
        self.lista_dados_barbeiro.controls.clear()  # Limpa a lista atual

        for dia, registros in historico.items():
            # Adiciona a data apenas uma vez
            self.lista_dados_barbeiro.controls.append(
                Text(f"Dia {dia}", size=20, color="black", weight="bold")
            )
            
            # Adiciona as informações de cada barbeiro
            for registro in registros:
                item = Container(
                    content=Column(
                        controls=[
                            Text(f"Barbeiro: {registro['barbeiro']}", size=18, color="black" , weight="bold"),
                            Text(f"Cortes realizados: {registro['cortes']}", size=18, color="black"),
                            Text(f"Valor total: R$ {registro['lucro']:.2f}", size=18, color="green" , weight="bold"),
                        ]
                    ),
                    padding=10,
                    border_radius=5,
                    bgcolor="white",
                )
                self.lista_dados_barbeiro.controls.append(item)  # Adiciona cada item à lista

        self.page.update()


    def historico_diario(self):
        self.page.clean()
        TelaHistoricoVendas(self.page)

    def historico_mensal(self):
        self.page.clean()
        ListaDadosMensais(self.page)

    def ver_produtos_diarios(self):
        self.page.clean()
        ListaDadosProdutosDiarios(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)


class ListaDadosMensais():
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

        self.lista_mensal = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_mensal()

        lista_mensal_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_mensal],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,
        )

        botao_ver_historico_diario = ElevatedButton(
            text="Ver Histórico Diário",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_diario()
        )

        botao_ver_barbeiros = ElevatedButton(
            text=" Ver Barbeiros ",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            
            on_click=lambda e: self.ver_barbeiros()
        )

        botao_ver_produtos_diarios = ElevatedButton(
            text=" Ver Produtos Diários" , 
            bgcolor= "white",
            color = "black",
            width= 300,
            height= 50,

            on_click= lambda e: self.ver_produtos_diarios()
        )


        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar,
                        ],
                    ), 
                    #cabecalho,
                    lista_mensal_container ,
                    Row(
                        controls=[
                            botao_ver_historico_diario, botao_ver_barbeiros, botao_ver_produtos_diarios
                        ]
                    )
                ],

            ),
        )

    def buscar_historico_mensal(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', data) AS mes, 
                SUM(total) AS lucro_mensal, 
                COUNT(*) AS quantidade_cortes
            FROM RegistroServiços
            GROUP BY mes
            ORDER BY mes DESC;
        ''')
        historico = cursor.fetchall()
        conexao.close()
        return historico    

    def atualizar_lista_mensal(self):
        historico = self.buscar_historico_mensal()
        self.lista_mensal.controls.clear()

        for mes, lucro, cortes in historico:
            self.lista_mensal.controls.append(
                Row([
                Text(f"Mês: {mes}", size=20, width= 200 ,color="black", weight="bold"),
                Text(f"Lucro: R$ {lucro:.2f}", size=20, width= 200 , color="green", weight="bold"),
                Text(f"Cortes: {(cortes)}", size=20, width= 200 ,color="blue", weight="bold"),
                ])
            )
        self.page.update()


    def historico_diario(self):
        self.page.clean()
        TelaHistoricoVendas(self.page)

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def ver_produtos_diarios(self):
        self.page.clean()
        ListaDadosProdutosDiarios(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)


class ListaDadosProdutosDiarios():
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

        self.lista_historico = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_historico()

        lista_historico_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_historico],
                scroll="adaptive",
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,
        )

        botao_ver_barbeiros = ElevatedButton(
            text=" Ver Barbeiros ",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.ver_barbeiros()
        )

        botao_ver_historico_mensal = ElevatedButton(
            text="Ver Histórico Mensal",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_mensal()
        )

        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[botao_voltar],
                    ),
                    lista_historico_container,
                    Row(
                        controls=[botao_ver_barbeiros, botao_ver_historico_mensal]
                    )
                ],
            ),
        )
        self.atualizar_lista_historico()

    def buscar_historico(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT DATE(data_produto) as dia, SUM(total_produto) as total_diario, COUNT(*) as quantidade_vendas
            FROM Registro_Produtos
            GROUP BY DATE(data_produto)
            ORDER BY DATE(data_produto) DESC
        ''')
        historico = cursor.fetchall()
        conexao.close()
        return historico

    def atualizar_lista_historico(self):
        historico = self.buscar_historico()
        self.lista_historico.controls.clear()

        for dia, total_diario, quantidade_vendas in historico:
            item = Container(
                content=Row(
                    controls=[
                        Text(f"Dia: {dia}", size=20, color="black", width=280, weight="bold"),
                        Text(f"Receita: R$ {total_diario:.2f}", size=20, color="green", width=280, weight="bold"),
                        Text(f"Vendas: {quantidade_vendas}", size=20, color="blue", width=200, weight="bold")
                    ]
                ),
                padding=5,
                border_radius=5,
            )
            self.lista_historico.controls.append(item)
        
        self.page.update()

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def historico_mensal(self):
        self.page.clean()
        ListaDadosMensais(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)
        