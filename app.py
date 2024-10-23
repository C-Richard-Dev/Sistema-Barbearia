from flet import *
import sqlite3



    



# CÓDIGO DA TELA DE SERVIÇOS -------------------------------------------------------------------------------------------------------------
def tela_servicos(e):
    # Limpar a tela atual
    e.page.clean()
    
    titulo_servicos = Text(
        "Lista de Serviços",
        size= 30,
        color= "white",
        weight="bold",
        
    )

    botao_voltar = ElevatedButton(
        text= " ",
        bgcolor="black",
        color="white",
        width=100,
        height=50,
        icon=icons.ARROW_BACK,
        on_click= lambda e:voltar(e.page)
    )

    def salvar_servico(nome_servico, preco_servico):
        conexao = sqlite3.connect("meubanco.db") #Inicio a conexão ao meu DB
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Serviços (serviço, preço_serviço) VALUES (?,?)",(nome_servico, preco_servico))
        conexao.commit() #Salvo as alterações feitas no DB
        conexao.close() #Fecho a conexão ao DB

        atualizar_lista_servicos()

        print(f"O Serviço {nome_servico} foi salvo com o preço de {preco_servico} no banco de dados!")

    def excluir_servico(servico_id):
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Serviços WHERE rowid = ?", (servico_id,))
        conexao.commit()
        conexao.close()
        atualizar_lista_servicos()

    def atualizar_lista_servicos():
        conexao = sqlite3.connect("meubanco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT rowid, serviço, preço_serviço FROM Serviços")
        servicos = cursor.fetchall() #retorna todos os serviços
        conexao.close()

        lista_servicos.controls.clear()

        for servico in servicos:
            servico_id, nome_servico, preco_servico = servico
            item = Row(
                controls=[
                    Text(f"{nome_servico}", size=20, color="white"),
                    Text(f"(R$ {preco_servico})", size=20, color="white",width=100),
                    ElevatedButton(
                        "Excluir",
                        color="white",
                        bgcolor="red",
                        on_click=lambda e, servico_id=servico_id: excluir_servico(servico_id)
                    ),
                ],
                
                spacing=15
            )
            lista_servicos.controls.append(item),
            e.page.update()
            


    def tela_adicionar_servico(e):

        nome_servico = TextField(label="Nome do serviço", hint_text="Digite o nome do serviço")
        preco_servico = TextField(label="Preço", hint_text="Digite o preço do serviço", keyboard_type="number")

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
                        ElevatedButton("Adicionar",color="white",bgcolor="green", on_click=lambda e: (salvar_servico(nome_servico.value , preco_servico.value),e.page.overlay.remove(centered_overlay),
                                                                                                      e.page.update())),
                        ElevatedButton("Cancelar",color="white",bgcolor="red",on_click=lambda e: (e.page.overlay.remove(centered_overlay),e.page.update())),
                    ],
                    alignment="end",
                ),
            ],
            
            spacing=10,
            alignment= "start",
            horizontal_alignment= "center"
        ),
        width=400,  # Largura do container
        height=300,  # Altura do container
        padding=20,  # Padding interno
        
    )
        centered_overlay = Container(
        expand=True, 
        alignment=alignment.center,
        content=overlay,  # O conteúdo que será centralizado
    )
    
        e.page.overlay.append(centered_overlay)
        e.page.update()  

    botao_adicionar = ElevatedButton(
        text="Adicionar Serviço",
        bgcolor="black",
        color="white",
        width= 250,
        height=50,
        icon=icons.ADD,
        on_click= tela_adicionar_servico
    )

    cabecalho = Container(
        bgcolor="white",
        padding=10,
        border_radius=15,
        content=Row(
            controls=[
                Text("SERVIÇOS",size=20,color="black", weight="bold" ),               
            ],
        ),
       expand=True
    ) 

    lista_servicos= Column(  
        spacing=25,
        alignment="start",
        scroll= "adaptative",
        

    )

    lista_servicos_container = Container(
    content=Column(
        
        spacing=25,
        alignment="start",
        controls=[
            lista_servicos
        ],
        scroll="adaptive",  # Adiciona rolagem adaptativa
    ),
    height=400,  # Defina a altura máxima para ativar a rolagem
)


    

    #Elementos da tela sao adicionados aqui
    e.page.add(Column(
        controls=[
            Row(
                controls=[
                    botao_voltar,
                    titulo_servicos,
                    botao_adicionar
                ],
            ),
        cabecalho,
        lista_servicos_container,
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=30
        
    ))
    atualizar_lista_servicos()
  #----------------------------------------------------------------------------------------------------------------------------------------  
    
    
def voltar(page):# função para voltar a pagina inicial (serve para qualquer def)
    page.clean()
    main(page)

# FUNÇÃO PRINCIPAL DO CÓDIGO ----------------------------------------------------------------------------------------------------------------------
def main(page: Page):
    
    page.bgcolor = "black"

    
    titulo = Text(
        "Barbearia",
        size=30,
        color="white",
        weight="bold",  # Negrito
    )

    # container para o título
    titulo_container = Container(
        content=titulo,
        alignment=alignment.center,  #centraliza o conteúdo dentro do container
        padding=20  # Adiciona um pouco de espaço em volta
    )

    #Container com a página inicial
    container = Container(
        Column(
            controls=[
                    titulo_container,
                    ElevatedButton(text="Serviços",
                                     bgcolor="white",
                                     color="black",
                                     width=500,
                                     height=50,
                                     on_click= tela_servicos),
                    ElevatedButton(text="Estoque de Produtos",
                                     bgcolor="white",
                                     color="black",
                                     width=500,
                                     height=50,
                                     on_click= tela_estoque),
                    ElevatedButton(text="Barbeiros",
                                     bgcolor="white",
                                     color="black",
                                     width=500,
                                     height=50),
                    ElevatedButton(text="Clientes",
                                     bgcolor="white",
                                     color="black",
                                     width=500,
                                     height=50),
                    ElevatedButton(text="Registrar Corte",
                                     bgcolor="white",
                                     color="black",
                                     width=500,
                                     height=50),
                     ElevatedButton(text="Registrar Venda",
                                     bgcolor="white",
                                     color="black",
                                     width=500,
                                     height=50)
                      ],
            alignment="start",  # Alinhar ao topo
            horizontal_alignment="center", 
            expand=True
            ) 
    )

    
    page.add(container)

app(target=main)

