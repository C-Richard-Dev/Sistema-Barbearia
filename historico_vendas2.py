import sqlite3
from flet import *
from main import AppBarbearia

# TELA QUE FALA SOBRE O HISTÓRICO DE PRODUTOS

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

        botao_ver_lista_geral = ElevatedButton(
            text = "Ver Lista de Registro Geral",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_geral()
        )

        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[botao_voltar, Text("Lista de vendas de produtos por dia",color="white", weight="bold",size=25),],
                    ),
                    lista_historico_container,
                    Row(
                        controls=[botao_ver_barbeiros, botao_ver_historico_mensal, botao_ver_lista_geral]
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
        ListaDadosProdutosMensais(self.page)

    def historico_geral(self):
        self.page.clean()
        ListaProdutos(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)

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

        botao_ver_lista_geral = ElevatedButton(
            text = "Ver Lista de Registro Geral",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_geral())

        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar, Text("Lista de produtos por barbeiro",color="white", weight="bold",size=25),
                        ],
                    ), 
                    #cabecalho,
                    lista_dados_barbeiro_container ,
                    Row(
                        controls=[
                            botao_ver_historico_diario, botao_ver_historico_mensal, botao_ver_lista_geral
                        ]
                    )
                ],

            ),
        )

    def buscar_historico_barbeiro(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT DATE(data_produto) as dia, barbeiro_produto, COUNT(*) as quantidade_produto, SUM(total_produto) as valor_total
            FROM Registro_Produtos
            GROUP BY DATE(data_produto), barbeiro_produto
            ORDER BY DATE(data_produto) DESC, barbeiro_produto ASC
        ''')
        historico = cursor.fetchall()
        conexao.close()

        historico_formatado = {}
        for dia, barbeiro, quantidade_produtos, valor_total in historico:
            if dia not in historico_formatado:
                historico_formatado[dia] = []
            historico_formatado[dia].append({
                "barbeiro": barbeiro,
                "produtos": quantidade_produtos,
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
                            Text(f"Produtos vendidos: {registro['produtos']}", size=18, color="black"),
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
        ListaDadosProdutosDiarios(self.page)

    def historico_mensal(self):
        self.page.clean()
        ListaDadosProdutosMensais(self.page)

    def historico_geral(self):
        self.page.clean()
        ListaProdutos(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)

class ListaDadosProdutosMensais():
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

        self.lista_produtos_mensal = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_produtos_mensal()

        lista_produtos_mensal_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_produtos_mensal],
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
            text="Ver Barbeiros",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.ver_barbeiros()
        )

        botao_ver_lista_geral = ElevatedButton(
            text="Ver Lista de Registro Geral",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.historico_geral()
        )

        self.page.add(
            Column(
                controls=[
                    Row(
                        controls=[
                            botao_voltar, 
                            Text("Lista de produtos vendidos por mês", color="white", weight="bold", size=25),
                        ],
                    ), 
                    lista_produtos_mensal_container,
                    Row(
                        controls=[
                            botao_ver_historico_diario, botao_ver_barbeiros, botao_ver_lista_geral
                        ]
                    )
                ],
            ),
        )

    def buscar_historico_produtos_mensal(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT 
                mes, 
                total_lucro AS lucro_mensal, 
                total_cortes AS quantidade_cortes,
                barbeiro_produto,
                SUM(total_produto) AS lucro_barbeiro,
                COUNT(*) AS cortes_barbeiro
            FROM (
                SELECT 
                    strftime('%Y-%m', data_produto) AS mes, 
                    SUM(total_produto) OVER (PARTITION BY strftime('%Y-%m', data_produto)) AS total_lucro, 
                    COUNT(*) OVER (PARTITION BY strftime('%Y-%m', data_produto)) AS total_cortes,
                    barbeiro_produto,
                    total_produto
                FROM Registro_Produtos
            ) AS subquery
            GROUP BY mes, barbeiro_produto
            ORDER BY mes DESC, lucro_barbeiro DESC;
        ''')
        historico = cursor.fetchall()
        conexao.close()
        return historico    

    def atualizar_lista_produtos_mensal(self):
        historico = self.buscar_historico_produtos_mensal()
        self.lista_produtos_mensal.controls.clear()

        dados_por_mes= {}
        for mes, lucro_total, vendas_totais, barbeiro, lucro_barbeiro, vendas_barbeiro in historico:
            if mes not in dados_por_mes:
                dados_por_mes[mes] = {
                    "lucro_total": lucro_total,
                    "vendas_totais":vendas_totais,
                    "barbeiros": []
                }
            dados_por_mes[mes]["barbeiros"].append((barbeiro, vendas_barbeiro, lucro_barbeiro))

        for mes, dados in dados_por_mes.items():
            linha_principal = Row([
                Text(f"Mês: {mes}", size=20, width=150, color="black", weight="bold"),
                Text(f"Lucro Total: R$ {dados['lucro_total']:.2f}", size=20, width=200, color="green", weight="bold"),
                Text(f"Vendas Totais: {dados['vendas_totais']}", size=20, width=200, color="blue", weight="bold"),
            ])
            self.lista_produtos_mensal.controls.append(linha_principal)
            
            for barbeiro, vendas, lucro in dados["barbeiros"]:
                linha_barbeiro = Row([
                    Text(f"Barbeiro: {barbeiro}", size=18, width=200, color="black"),
                    Text(f"{vendas} vendas - R$ {lucro:.2f}", size=18, width=200, color="gray"),
                ])
                self.lista_produtos_mensal.controls.append(linha_barbeiro)
        self.page.update()

    def historico_diario(self):
        self.page.clean()
        ListaDadosProdutosDiarios(self.page)

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def historico_geral(self):
        self.page.clean()
        ListaProdutos(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)

class ListaProdutos():
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

        botao_limpar_dados = ElevatedButton(
            text="Limpar Lista de Produtos",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.open_popup()
        )

        botao_ver_barbeiros = ElevatedButton(
            text="Ver Barbeiros",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.ver_barbeiros()
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
            height=400,
        )

        self.page.add(
            Column(
                controls=[
                    Row(controls=[botao_voltar, Text("Lista de Produtos", color="white", weight="bold", size=25), botao_limpar_dados]), 
                    lista_produtos_container,
                    Row(controls=[
                        botao_ver_historico_mensal, botao_ver_historico_diario, botao_ver_barbeiros
                    ])
                ],
            ),
        )
        self.atualizar_lista_produtos()

    def buscar_produtos(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT id, total_produto, cliente_produto, barbeiro_produto, pagamento_produto, DATE(data_produto) AS data
            FROM Registro_Produtos
            ORDER BY DATE(data_produto) DESC
        ''')
        produtos = cursor.fetchall()
        conexao.close()
        return produtos

    def excluir_produto(self, produto_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM Registro_Produtos WHERE id = ?', (produto_id,))
        conexao.commit()
        conexao.close()
        self.atualizar_lista_produtos()

    def atualizar_lista_produtos(self):
        produtos = self.buscar_produtos()
        self.lista_produtos.controls.clear()

        for produto in produtos:
            produto_id, total, cliente, barbeiro, pagamento, data = produto
            item = Container(
                content=Row(
                    controls=[
                        Text(f"Cliente: {cliente}", size=18, color="black", width=280, weight="bold"),
                        Text(f"Barbeiro: {barbeiro}", size=18, color="black", width=280, weight="bold"),
                        Text(f"Total: R${total}", size=18, color="green", width=280, weight="bold"),
                        Text(f"Pagamento: {pagamento}", size=18, color="gray", width=280, weight="bold"),
                        Text(f"Data: {data}", size=18, color="black", width=180, weight="bold"),
                        IconButton(
                            icon=icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, pid=produto_id: self.excluir_produto(pid)
                        )
                    ]
                ),
                padding=10,
                border_radius=5,
            )
            self.lista_produtos.controls.append(item)

        self.page.update()

    def open_popup(self):
        alert_dialog = AlertDialog(
            modal=True,
            content=Text("ATENÇÃO: ao limpar os dados, eles não poderão mais ser recuperados!"),
            actions=[
                ElevatedButton(
                    text="Voltar",
                    on_click=self.fechar_dialog
                ),
                ElevatedButton(
                    text="Limpar",
                    bgcolor="red",
                    color="white",
                    on_click=self.limpar_lista
                )
            ]
        )
        self.page.dialog = alert_dialog
        alert_dialog.open = True
        self.page.update()

    def fechar_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def limpar_lista(self,e):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Registro_Produtos")
        conexao.commit()
        conexao.close()

        self.page.dialog.open = False
        self.atualizar_lista_produtos()
        self.page.update()

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def historico_diario(self):
        self.page.clean()
        ListaDadosProdutosDiarios(self.page)

    def historico_mensal(self):
        self.page.clean()
        ListaDadosProdutosMensais(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)