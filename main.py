from flet import *

class AppBarbearia:
    def __init__(self, page: Page):
        self.page = page
        self.page.bgcolor = "black"
        
        self.setup_interface()

    def setup_interface(self):
        titulo = Text(
            "Barbearia",
            size=30,
            color="white",
            weight="bold",  
        )


        titulo_container = Container(
            content=titulo,
            alignment=alignment.center,  
            padding=20  
        )


        container = Container(
            Column(
                controls=[
                    titulo_container,
                    ElevatedButton(
                        text="Serviços",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click=self.tela_servicos
                    ),
                    ElevatedButton(
                        text="Produtos",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.tela_produtos
                    ),
                    ElevatedButton(
                        text="Barbeiros",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.tela_barbeiros
                    ),
                    ElevatedButton(
                        text="Clientes",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.tela_clientes
                    ),
                    ElevatedButton(
                        text="Agendamentos",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.tela_agendamentos
                    ),
                    ElevatedButton(
                        text="Registrar Venda",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.tela_venda
                    ),
                    ElevatedButton(
                        text="Registrar Venda de Produto",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.tela_vendaproduto
                    ),
                    ElevatedButton(
                        text="Ver Histórico de Vendas",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                        on_click= self.ver_historico
                    )
                ],
                alignment="start",
                horizontal_alignment="center",
                expand=True
            )
        )


        self.page.add(container)


    def tela_servicos(self, e):
        from servicos import TelaServicos # É importante que seja importada apenas aqui para evitar problema de importação circular
        self.page.clean()  
        TelaServicos(self.page)


    def tela_produtos(self,e):
        from produtos import TelaProdutos
        self.page.clean()
        TelaProdutos(self.page)


    def tela_barbeiros(self,e):
        from barbeiros import TelaBarbeiros
        self.page.clean()
        TelaBarbeiros(self.page)


    def tela_clientes(self,e):
        from clientes import TelaClientes
        self.page.clean()
        TelaClientes(self.page)

    def tela_agendamentos(self,e):
        from agendamentos import TelaAgendamentos
        self.page.clean()
        TelaAgendamentos(self.page)

    def tela_venda(self,e):
        from venda import TelaVendas
        self.page.clean()
        TelaVendas(self.page)

    def tela_vendaproduto(self,e):
        from vendaservico import TelaVendaServico
        self.page.clean()
        TelaVendaServico(self.page)

    def ver_historico(self,e):
        from historico_vendas import TelaHistoricoVendas
        self.page.clean()
        TelaHistoricoVendas(self.page)
        




if __name__ == "__main__":  #definindo a class principal do meu projeto
    app(target=AppBarbearia)