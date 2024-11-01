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
                        text="Clientes",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                    ),
                    ElevatedButton(
                        text="Registrar Corte",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
                    ),
                    ElevatedButton(
                        text="Registrar Venda",
                        bgcolor="white",
                        color="black",
                        width=500,
                        height=50,
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


if __name__ == "__main__":  #definindo a class principal do meu projeto
    app(target=AppBarbearia)