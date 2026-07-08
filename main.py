import tkinter as tk
from Modelo.desenho import DesenhoModel
from controlador.paintcontroller import PaintController
from Visao.janela import JanelaView

def main():
    root = tk.Tk()

    # 1. Instancia o Modelo (Dados)
    model = DesenhoModel()

    # 2. Instancia o Controlador passando o modelo
    controller = PaintController(model)

    # 3. Instancia a Visão passando a janela e o controlador
    view = JanelaView(root, controller)

    # 4. Faz o controlador conhecer a visão criada
    controller.associar_visao(view)

    # 5. Roda a aplicação
    root.mainloop()

if __name__ == "__main__":
    main()
