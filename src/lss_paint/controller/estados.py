"""
Módulo contendo a implementação do Padrão State para as ferramentas de desenho.

Responsabilidade: Isolar o comportamento de inicialização e atualização de cada 
ferramenta, eliminando condicionais complexas no controlador.

@author Luísa Costa, Sarah Beatriz e Sayran Felix
@version 1.0
@since 2026-07-19
"""

from abc import ABC, abstractmethod
from src.lss_paint.model.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono

class EstadoFerramenta(ABC):
    """Classe abstrata (State) que define a interface para os comportamentos do mouse."""
    
    @abstractmethod
    def iniciar_figura(self, controller, x, y):
        """
        Define o comportamento ao clicar na tela.
        
        @param controller: Instância do PaintController.
        @param x: Coordenada X do clique.
        @param y: Coordenada Y do clique.
        """
        pass
        
    @abstractmethod
    def atualizar_figura(self, controller, x, y):
        """Define o comportamento ao arrastar o mouse na tela."""
        pass

class EstadoRabisco(EstadoFerramenta):
    """Estado concreto para o comportamento da ferramenta de Rabisco livre."""
    
    def iniciar_figura(self, controller, x, y):
        m = controller.model
        m.nova_figura = Rabisco([(x, y)], m.cor_atual_borda, m.cor_atual_preenchimento)

    def atualizar_figura(self, controller, x, y):
        m = controller.model
        if m.nova_figura:
            m.nova_figura.coordenadas.append((x, y))

class EstadoFormaSimples(EstadoFerramenta):
    """Estado concreto base que encapsula a lógica de arrasto para formas de 2 pontos (x2, y2)."""
    
    def atualizar_figura(self, controller, x, y):
        m = controller.model
        if m.nova_figura:
            m.nova_figura.coordenadas[2] = x
            m.nova_figura.coordenadas[3] = y

class EstadoLinha(EstadoFormaSimples):
    """Estado concreto para criação de Linhas."""
    def iniciar_figura(self, controller, x, y):
        m = controller.model
        m.nova_figura = Linha([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)

class EstadoRetangulo(EstadoFormaSimples):
    """Estado concreto para criação de Retângulos."""
    def iniciar_figura(self, controller, x, y):
        m = controller.model
        m.nova_figura = Retangulo([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)

class EstadoOval(EstadoFormaSimples):
    """Estado concreto para criação de Ovais."""
    def iniciar_figura(self, controller, x, y):
        m = controller.model
        m.nova_figura = Oval([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)

class EstadoCirculo(EstadoFormaSimples):
    """Estado concreto para criação de Círculos perfeitos."""
    def iniciar_figura(self, controller, x, y):
        m = controller.model
        m.nova_figura = Circulo([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)

class EstadoPoligono(EstadoFormaSimples):
    """Estado concreto para criação de Polígonos baseados em número de lados."""
    def iniciar_figura(self, controller, x, y):
        m = controller.model
        m.nova_figura = Poligono([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento, num_lados=m.num_lados_poligono)