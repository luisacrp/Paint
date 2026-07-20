from tkinter import filedialog
from src.lss_paint.controller.estados import (EstadoRabisco, EstadoLinha, EstadoRetangulo, EstadoOval, EstadoCirculo, EstadoPoligono)

class PaintController:
    """
    Controlador do padrão MVC que intermedeia interações do usuário com as regras do Model.
    
    Responsabilidade: Receber eventos da interface gráfica, manipular instâncias geométricas 
    e gerir operações de cores e persistência utilizando o Padrão State.
    
    @author Luísa Costa, Sarah Beatriz e Sayran Felix
    @version 2.0
    @since 2026-07-19
    """
    def __init__(self, model):
        """
        Construtor da classe PaintController.
        
        @param model: Instância da classe DesenhoModel contendo o estado da aplicação.
        @throws Nenhuma exceção.
        """
        self.model = model
        self.view = None
        
        # Mapeamento do Padrão State
        self.estados = {
            'rabisco': EstadoRabisco(),
            'linha': EstadoLinha(),
            'retangulo': EstadoRetangulo(),
            'oval': EstadoOval(),
            'circulo': EstadoCirculo(),
            'poligono': EstadoPoligono()
        }
        self.estado_atual = self.estados['rabisco']

    def associar_visao(self, view):
        """
        Registra a interface gráfica que o controller irá atualizar.
        
        @param view: Instância da classe JanelaView.
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        self.view = view

    def mudar_ferramenta(self, nova_ferramenta):
        """
        Atualiza a ferramenta ativa e altera o estado (State) do comportamento do mouse.
        
        @param nova_ferramenta: String contendo o nome da ferramenta selecionada.
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        self.model.ferramenta = nova_ferramenta
        
        # Altera o comportamento do controlador baseado no novo estado selecionado
        self.estado_atual = self.estados[nova_ferramenta]
        
        self.view.atualizar_visibilidade_lados(nova_ferramenta == "poligono")

    def mudar_num_lados(self, valor):
        """
        Atualiza a quantidade de lados para a ferramenta Polígono no modelo.
        
        @param valor: String ou Inteiro com a quantidade de lados inserida no Spinbox.
        @return Nenhum.
        @throws ValueError: Tratado internamente se a conversão para inteiro falhar.
        """
        try:
            self.model.num_lados_poligono = max(3, int(valor))
        except ValueError:
            pass

    # ===== Cores =====

    def set_cor_alvo(self, alvo):
        """
        Define o alvo da coloração (borda ou preenchimento).
        
        @param alvo: String "borda" ou "preenchimento".
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        self.model.cor_alvo = alvo
        self.view.atualizar_botoes_cor(alvo)

    def selecionar_cor(self, cor):
        """
        Aplica a cor escolhida da paleta ao alvo selecionado.
        
        @param cor: Código hexadecimal da cor selecionada ou "transparente".
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        cor_real = "" if cor == "transparente" else cor
        cor_botao = "white" if cor == "transparente" else cor

        if self.model.cor_alvo == "borda":
            self.model.cor_atual_borda = cor_real
        else:
            self.model.cor_atual_preenchimento = cor_real

        self.view.atualizar_cor_botao(self.model.cor_alvo, cor_botao)

    # ===== Desenho (Refatorado com Padrão State) =====

    def iniciar_figura(self, event):
        """
        Captura o clique inicial do mouse e delega a criação da figura ao Estado ativo.
        
        @param event: Objeto de evento do Tkinter contendo coordenadas x e y do mouse.
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        x, y = self.view.canvas_coords(event)
        # O comportamento varia conforme o estado atual, sem o uso de "match"
        self.estado_atual.iniciar_figura(self, x, y)

    def atualizar_figura(self, event):
        """
        Ajusta as coordenadas da figura atual através do Estado ativo, simulando preview.
        
        @param event: Objeto de evento do Tkinter com as coordenadas em tempo real.
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        if not self.model.nova_figura:
            return

        x, y = self.view.canvas_coords(event)
        # O comportamento de arrasto é delegado ao estado ativo, sem o uso de "if isinstance"
        self.estado_atual.atualizar_figura(self, x, y)
        self.view.desenhar_preview(self.model.nova_figura)

    def incluir_figura(self, event):
        """
        Finaliza a renderização de uma figura ao soltar o mouse e a salva no modelo global.
        
        @param event: Objeto de evento de release do Tkinter.
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        m = self.model
        if m.nova_figura:
            m.figuras.append(m.nova_figura)
        m.nova_figura = None

        self.view.redesenhar_tudo(m.figuras)

    # ===== Persistência =====
    
    def salvar_desenho(self):
        """
        Aciona a caixa de diálogo do sistema para que o usuário salve os dados persistentes.
        
        @param: Nenhum.
        @return: Nenhum.
        @throws Exception: Exibe pop-up de erro se a gravação do modelo falhar.
        """
        caminho = filedialog.asksaveasfilename(
            defaultextension=".lssp", 
            filetypes=[("LSS Paint Files", "*.lssp"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.model.salvar_arquivo(caminho)

    def abrir_desenho(self):
        """
        Aciona caixa de diálogo do sistema para abrir projetos salvos anteriormente.
        
        @param: Nenhum.
        @return: Nenhum.
        @throws Exception: Exibe pop-up de erro se a leitura do arquivo falhar.
        """
        caminho = filedialog.askopenfilename(
            filetypes=[("LSS Paint Files", "*.lssp"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.model.carregar_arquivo(caminho)
            self.view.redesenhar_tudo(self.model.figuras)