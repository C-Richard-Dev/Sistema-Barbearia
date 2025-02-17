import sqlite3
from flet import *
from main import AppBarbearia

#TELA QUE FALA SOBRE O HISTÓRICO DE SERVIÇOS

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
                        controls=[
                            botao_voltar, Text("Lista Diária de Serviços",color="white", weight="bold",size=25),
                        ],
                    ), 
                    #cabecalho,
                    lista_historico_container ,
                    Row(
                        controls=[
                            botao_ver_barbeiros, botao_ver_historico_mensal, botao_ver_lista_geral
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

    def historico_geral(self):
        self.page.clean()
        ListaRegistroGeral(self.page)

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
                            botao_voltar, Text("Lista de cortes por barbeiro",color="white", weight="bold",size=25),
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


    def historico_geral(self):
        self.page.clean()
        ListaRegistroGeral(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)


class ListaDadosMensais():
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
                scroll="auto",  # Permite scroll horizontal e vertical
            ),
            bgcolor="white",
            border_radius=15,
            padding=10,
            height=400,
            width=True ,  # Aumenta largura para acomodar as colunas extras
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
                            Text("Lista de receitas mensais", color="white", weight="bold", size=25),
                        ],
                    ),
                    lista_mensal_container,
                    Row(
                        controls=[botao_ver_historico_diario, botao_ver_barbeiros, botao_ver_lista_geral]
                    )
                ],
            ),
        )

    def buscar_historico_mensal(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT 
                mes, 
                total_lucro AS lucro_mensal, 
                total_cortes AS quantidade_cortes,
                barbeiro,
                SUM(total) AS lucro_barbeiro,
                COUNT(*) AS cortes_barbeiro
            FROM (
                SELECT 
                    strftime('%Y-%m', data) AS mes, 
                    SUM(total) OVER (PARTITION BY strftime('%Y-%m', data)) AS total_lucro, 
                    COUNT(*) OVER (PARTITION BY strftime('%Y-%m', data)) AS total_cortes,
                    barbeiro,
                    total
                FROM RegistroServiços
            ) AS subquery
            GROUP BY mes, barbeiro
            ORDER BY mes DESC, lucro_barbeiro DESC;
        ''')
        historico = cursor.fetchall()
        conexao.close()
        return historico    

    def atualizar_lista_mensal(self):
        historico = self.buscar_historico_mensal()
        self.lista_mensal.controls.clear()

        dados_por_mes = {}
        for mes, lucro_total, cortes_totais, barbeiro, lucro_barbeiro, cortes_barbeiro in historico:
            if mes not in dados_por_mes:
                dados_por_mes[mes] = {
                    "lucro_total": lucro_total,
                    "cortes_totais": cortes_totais,
                    "barbeiros": []
                }
            dados_por_mes[mes]["barbeiros"].append((barbeiro, cortes_barbeiro, lucro_barbeiro))

        for mes, dados in dados_por_mes.items():
            linha_principal = Row([
                Text(f"Mês: {mes}", size=20, width=150, color="black", weight="bold"),
                Text(f"Lucro Total: R$ {dados['lucro_total']:.2f}", size=20, width=200, color="green", weight="bold"),
                Text(f"Cortes Totais: {dados['cortes_totais']}", size=20, width=200, color="blue", weight="bold"),
            ])
            self.lista_mensal.controls.append(linha_principal)

            for barbeiro, cortes_barbeiro, lucro_barbeiro in dados["barbeiros"]:
                linha_barbeiro = Row([
                    Text(f"Barbeiro: {barbeiro}", size=18, width=200, color="black"),
                    Text(f"{cortes_barbeiro} cortes - R$ {lucro_barbeiro:.2f}", size=18, width=200, color="gray"),
                ])
                self.lista_mensal.controls.append(linha_barbeiro)

        self.page.update()

    def historico_diario(self):
        self.page.clean()
        TelaHistoricoVendas(self.page)

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def historico_geral(self):
        self.page.clean()
        ListaRegistroGeral(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)


class ListaRegistroGeral():
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
            text="Limpar Lista de Dados",
            bgcolor="white",
            color="black",
            width=300,
            height=50,
            on_click=lambda e: self.open_popup()
        )

        self.lista_registros = ListView(
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.atualizar_lista_registros()

        lista_registros_container = Container(
            content=Column(
                spacing=25,
                alignment="start",
                controls=[self.lista_registros],
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
                    Row(controls=[botao_voltar,Text("Lista Geral de Serviços",color="white", weight="bold",size=25), botao_limpar_dados]), 
                    lista_registros_container,
                    Row(
                        controls=[botao_ver_historico_diario, botao_ver_barbeiros, botao_ver_historico_mensal]
                    )
                ],
            ),
        )
        self.atualizar_lista_registros()

    def buscar_registros(self):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT id, total, cliente, barbeiro, pagamento, DATE(data)
            FROM RegistroServiços
            ORDER BY DATE(data) DESC
        ''')
        registros = cursor.fetchall()
        conexao.close()
        return registros

    def excluir_registro(self, registro_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM RegistroServiços WHERE id = ?', (registro_id,))
        conexao.commit()
        conexao.close()
        self.atualizar_lista_registros()

    def atualizar_lista_registros(self):
        registros = self.buscar_registros()
        self.lista_registros.controls.clear()

        for registro in registros:
            registro_id, total, cliente, barbeiro, pagamento, data = registro
            item = Container(
                content=Row(
                    controls=[
                        Text(f"Cliente: {cliente}", size=18, color="black", width=280, weight="bold"),
                        Text(f"Barbeiro: {barbeiro}", size=18, color="blue", width=280, weight="bold"),
                        Text(f"Total: R$ {total:.2f}", size=18, color="green", width=280, weight="bold"),
                        Text(f"Pagamento: {pagamento}", size=18, color="gray", width=280, weight="bold"),
                        Text(f"Data: {data}", size=18, color="black", width=180, weight="bold"),
                        IconButton(
                            icon=icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, rid=registro_id: self.excluir_registro(rid)
                        )
                    ]
                ),
                padding=10,
                border_radius=5,
            )
            self.lista_registros.controls.append(item)

        self.page.update()

    def open_popup(self):
        alert_dialog = AlertDialog(
            modal=True,
            content=Text("ATENÇÃO: ao limpar o dados, eles não poderão mais ser recuperados!"),
            actions=[
                ElevatedButton(
                    text="Voltar",
                    on_click= self.fechar_dialog
                ),
                ElevatedButton(
                    text="Limpar",
                    bgcolor="red",
                    color="white",
                    on_click= self.fechar_dialog
                )
            ]
        )
        self.page.dialog = alert_dialog
        alert_dialog.open = True
        self.page.update()

    def fechar_dialog(self,e):
        self.page.dialog.open=False
        self.page.clean()
        ListaRegistroGeral(self.page)
        self.page.update()

    def limpar_lista(self,e):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE From RegistroServiços")
        conexao.commit()
        conexao.close()

        self.page.dialog.open = False 
        self.atualizar_lista_registros()
        self.page.update

    def historico_diario(self):
        self.page.clean()
        TelaHistoricoVendas(self.page)

    def ver_barbeiros(self):
        self.page.clean()
        ListaDadosBarbeiros(self.page)

    def historico_mensal(self):
        self.page.clean()
        ListaDadosMensais(self.page)

    def voltar(self):
        self.page.clean()
        AppBarbearia(self.page)

