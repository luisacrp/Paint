import tkinter as tk


# Variáveis de estado global 
figuras = []
nova_figura = None
ferramenta = "rabisco"


# Função para atualizar a ferramenta selecionada no menu
def mudarFerramenta(nova_ferramenta):
    global ferramenta
    ferramenta = nova_ferramenta


# Função que marca o ponto inicial (x, y) quando o usuário clica na tela
def iniciarFigura(event):
    global nova_figura
    # ajusta as coordenadas considerando o scroll
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    
    match ferramenta:
        case 'linha':
            nova_figura = ("linha", [x, y, x, y])
        case 'rabisco':
            nova_figura = ("rabisco", [(x, y)])


# Função que atualiza as coordenadas da figura enquanto o mouse é arrastado (preview)
def atualizarFigura(event):
    global nova_figura
    if not nova_figura: return
        
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    
    tipo, coordenadas = nova_figura
    
    match tipo:
        case "rabisco":
            coordenadas.append((x, y))
        case _:
            coordenadas[2] = x
            coordenadas[3] = y
            
    # atualiza so o preview pra nao apagar o fundo
    canvas.delete("preview")
    desenharFigura(nova_figura, tag="preview")


# Função que salva a figura finalizada na lista global ao soltar o clique do mouse
def incluirFigura(event):
    global nova_figura
    if nova_figura:
        figuras.append(nova_figura)
    nova_figura = None
    
    canvas.delete("preview")
    canvas.delete("definitivo")
    for figura in figuras:
        desenharFigura(figura, tag="definitivo")


# Função desenhar na tela baseada no tipo
def desenharFigura(figura, tag=""):
    tipo, coordenadas = figura
    tracejado = (4, 2) if tag == "preview" else None
    
    # Cor e estilo opcionais
    kwargs = {'tags': tag}
    if tracejado: kwargs['dash'] = tracejado

    match tipo:
        case "linha":
            canvas.create_line(coordenadas[0], coordenadas[1], coordenadas[2], coordenadas[3], **kwargs)        
        case "rabisco":
            canvas.create_line(coordenadas, **kwargs)


# INTERFACE GRÁFICA
root = tk.Tk()
root.title("Paint - Luísa, Sarah e Sayran")
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
tk.Label(frame_esquerda, text="Ferramentas", bg="#e0e0e0", font=("Verdana", 10, "bold")).pack(pady=5)
ferramentas = [("Lápis", "rabisco"), ("Linha", "linha")]
for texto, val in ferramentas:
    tk.Button(frame_esquerda, text=texto, command=lambda v=val: mudarFerramenta(v), width=10).pack(pady=2)

root.mainloop()
