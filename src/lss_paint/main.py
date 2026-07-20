"""
Módulo de inicialização do sistema LSS Paint.
Responsável por instanciar os componentes do padrão MVC e iniciar o loop da interface gráfica.

@author Luísa Costa, Sarah Beatriz e Sayran Felix
@version 1.0
@since 2026-07-13
"""

import tkinter as tk
from src.lss_paint.model.desenho import DesenhoModel
from src.lss_paint.controller.paintController import PaintController
from src.lss_paint.view.janela import JanelaView

def main():
    """
    Função principal que orquestra a criação e injeção de dependências do MVC.
    
    @param: Nenhum
    @return: Nenhum
    @throws: Nenhuma exceção tratada especificamente.
    """
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

