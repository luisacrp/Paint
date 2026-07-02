import tkinter as tk
# Modulo das classes criadas
from figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono


# Variáveis de estado global 
figuras = []
nova_figura = None
ferramenta = "rabisco"
cor_atual_borda = "black"
cor_atual_preenchimento = "" 
cor_alvo = "borda"
num_lados_poligono = 6


# Função para atualizar a ferramenta selecionada no menu
def mudarFerramenta(nova_ferramenta):
    global ferramenta
    ferramenta = nova_ferramenta

    # Mostra o controle de lados só quando a ferramenta polígono está ativa
    if nova_ferramenta == "poligono":
        frame_lados.pack(pady=5, fill="x", padx=5, after=frame_ferramentas_botoes)
    else:
        frame_lados.pack_forget()


# Função para atualizar a quantidade de lados do polígono
def mudarNumLados(valor):
    global num_lados_poligono
    try:
        num_lados_poligono = max(3, int(valor))
    except ValueError:
        pass


# Função para definir se é a borda ou o preenchimento que mudará de cor
def setCorAlvo(alvo):
    global cor_alvo
    cor_alvo = alvo
    if alvo == "borda":
        botao_cor_borda.config(relief="sunken")
        botao_cor_preenchimento.config(relief="raised")
    else:
        botao_cor_borda.config(relief="raised")
        botao_cor_preenchimento.config(relief="sunken")

# Função para aplicar a cor selecionada na paleta para a variável de borda ou preenchimento
def selecionarCor(cor):
    global cor_atual_borda, cor_atual_preenchimento
    cor_real = "" if cor == "transparente" else cor
    cor_botao = "white" if cor == "transparente" else cor

    if cor_alvo == "borda":
        cor_atual_borda = cor_real
        botao_cor_borda.config(bg=cor_botao)
    else:
        cor_atual_preenchimento = cor_real
        botao_cor_preenchimento.config(bg=cor_botao)


# Função que marca o ponto inicial (x, y) quando o usuário clica na tela
def iniciarFigura(event):
    global nova_figura
    # ajusta as coordenadas considerando o scroll
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    
    match ferramenta:
        case 'linha':
            nova_figura = Linha([x, y, x, y], cor_atual_borda, cor_atual_preenchimento)
        case 'rabisco':
            nova_figura = Rabisco([(x, y)], cor_atual_borda, cor_atual_preenchimento)
        case 'retangulo':
            nova_figura = Retangulo([x, y, x, y], cor_atual_borda, cor_atual_preenchimento)
        case 'oval':
            nova_figura = Oval([x, y, x, y], cor_atual_borda, cor_atual_preenchimento)
        case 'circulo':
            nova_figura = Circulo([x, y, x, y], cor_atual_borda, cor_atual_preenchimento)
        case 'poligono':
            nova_figura = Poligono([x, y, x, y], cor_atual_borda, cor_atual_preenchimento, num_lados=num_lados_poligono)


# Função que atualiza as coordenadas da figura enquanto o mouse é arrastado (preview)
def atualizarFigura(event):
    global nova_figura
    if not nova_figura: return
        
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    
    # Verifica se a figura é um Rabisco (que usa uma lista de várias tuplas)
    if isinstance(nova_figura, Rabisco):
        nova_figura.coordenadas.append((x, y))
    # Para as outras figuras (que usam [x1, y1, x2, y2])
    else:
        nova_figura.coordenadas[2] = x
        nova_figura.coordenadas[3] = y
            
    # atualiza so o preview pra nao apagar o fundo
    canvas.delete("preview")
    nova_figura.desenhar(canvas, tag="preview")


# Função que salva a figura finalizada na lista global ao soltar o clique do mouse
def incluirFigura(event):
    global nova_figura
    if nova_figura:
        figuras.append(nova_figura)
    nova_figura = None
    
    canvas.delete("preview")
    canvas.delete("definitivo")
    for figura in figuras:
        # chama o método da própria classe
        figura.desenhar(canvas, tag="definitivo")



# INTERFACE GRÁFICA
root = tk.Tk()
root.title("LSS Paint")
root.geometry("800x600")


# Divide as sessões da aplicação
# O borderwidth é a grossura da borda. 
frame_esquerda = tk.Frame(root, width=80, bg="#e0e0e0", relief="raised", borderwidth=2)
frame_esquerda.pack(side="left", fill="y")

frame_base = tk.Frame(root, height=60, bg="#e0e0e0", relief="raised", borderwidth=2)
frame_base.pack(side="bottom", fill="x")

frame_canva = tk.Frame(root)
frame_canva.pack(side="right", fill="both", expand=True)


# Barrinhas de rolagem :)
scroll_y = tk.Scrollbar(frame_canva, orient="vertical")
scroll_x = tk.Scrollbar(frame_canva, orient="horizontal")

canvas = tk.Canvas(frame_canva, bg="white", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, scrollregion=(0,0,1000,1000))
scroll_y.config(command=canvas.yview)
scroll_x.config(command=canvas.xview)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)


# Vinculando ações do mouse às funções (Ajustar)
canvas.bind('<ButtonPress-1>', iniciarFigura)
canvas.bind('<B1-Motion>', atualizarFigura)
canvas.bind('<ButtonRelease-1>', incluirFigura)


# Menu de Ferramentas
tk.Label(frame_esquerda, text="FERRAMENTAS", bg="#e0e0e0", font=("Verdana", 8, "bold")).pack(pady=5)

frame_ferramentas_botoes = tk.Frame(frame_esquerda, bg="#e0e0e0")
frame_ferramentas_botoes.pack(fill="x")

ferramentas = [("Lápis", "rabisco"), ("Linha", "linha"), ("Retângulo", "retangulo"), ("Oval", "oval"), ("Círculo", "circulo"), ("Polígono", "poligono")]
for texto, val in ferramentas:
    tk.Button(frame_ferramentas_botoes, text=texto, command=lambda v=val: mudarFerramenta(v), width=10).pack(pady=2)

# Controle de número de lados do polígono (fica escondido até a ferramenta ser selecionada)
frame_lados = tk.Frame(frame_esquerda, bg="#e0e0e0")
tk.Label(frame_lados, text="Lados:", bg="#e0e0e0", font=("Verdana", 8)).pack(side="left")
spin_lados = tk.Spinbox(
    frame_lados, from_=3, to=12, width=4,
    command=lambda: mudarNumLados(spin_lados.get())
)
spin_lados.delete(0, "end")
spin_lados.insert(0, str(num_lados_poligono))
spin_lados.pack(side="left", padx=5)
# Também atualiza se o usuário digitar o número direto no campo
spin_lados.bind("<KeyRelease>", lambda e: mudarNumLados(spin_lados.get()))

tk.Label(frame_esquerda, text="\nCORES", bg="#e0e0e0", font=("Verdana", 8, "bold")).pack()
botao_cor_borda = tk.Button(frame_esquerda, text="Cor da Borda", bg="black", fg="white", relief="sunken", command=lambda: setCorAlvo("borda"))
botao_cor_borda.pack(pady=2, fill="x", padx=5)

botao_cor_preenchimento = tk.Button(frame_esquerda, text="Cor do Fundo", bg="white", relief="raised", command=lambda: setCorAlvo("preenchimento"))
botao_cor_preenchimento.pack(pady=2, fill="x", padx=5)

# Menu com Paleta de Cores
tk.Label(frame_base, text="PALETA:", bg="#e0e0e0", font=("Verdana", 8, "bold")).pack(side="left", padx=5)
tk.Button(frame_base, text="X", bg="white", width=3, command=lambda: selecionarCor("transparente")).pack(side="left", padx=2, pady=5)

frame_paleta = tk.Frame(frame_base, bg="#e0e0e0")
frame_paleta.pack(side="left", padx=5)

cores_paleta = [
    "#000000", "#404040", "#808080", "#FFFFFF", "#FF0000", "#FF3C00", 
    "#FF5E00", "#FF7B00", "#F5D000", "#9DFF00", "#09FF00", "#008300", 
    "#00FFC8", "#0077FF", "#001AFF", "#000080", "#7700FF", "#E100FF", 
    "#FF00D4", "#FF0062", "#7A012A", "#710080", "#5E3201", "#745500"
]

# Cria os botões da paleta com as 24 cores na linha 0
for coluna, cor in enumerate(cores_paleta):
    tk.Button(frame_paleta, bg=cor, width=2, height=1, relief="sunken", bd=1, command=lambda c=cor: selecionarCor(c)).grid(row=0, column=coluna, padx=1, pady=1)

root.mainloop()