import pickle
from src.lss_paint.model.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono

class DesenhoModel:
    """
    Classe do Modelo responsável por armazenar o estado global e os dados da aplicação.
    
    Responsabilidade: Manter a lista de figuras desenhadas, opções de ferramentas e cores atuais, 
    além de lidar com a persistência de dados em disco.
    
    @author Luísa Costa, Sarah Beatriz e Sayran Felix
    @version 1.0
    @since 2026-07-13
    """
    
    def __init__(self):
        """
        Inicializa as variáveis de estado com seus valores padrão.
        
        @throws Nenhuma exceção.
        """
        self.figuras = []
        self.nova_figura = None
        self.ferramenta = "rabisco"
        self.cor_atual_borda = "black"
        self.cor_atual_preenchimento = "" 
        self.cor_alvo = "borda"
        self.num_lados_poligono = 6

    def salvar_arquivo(self, caminho):
        """
        Salva o estado atual das figuras em um arquivo serializado.
        
        @param caminho: Caminho completo escolhido pelo usuário para salvar o arquivo.
        @return Nenhum.
        @throws Exception: Caso ocorra erro de permissão ou falha ao gravar o arquivo.
        @see pickle.dump
        """
        with open(caminho, 'wb') as f:
            pickle.dump(self.figuras, f)

    def carregar_arquivo(self, caminho):
        """
        Carrega as figuras de um arquivo serializado para a memória do modelo.
        
        @param caminho: Caminho completo do arquivo a ser lido.
        @return Nenhum.
        @throws Exception: Caso o arquivo esteja corrompido ou o caminho seja inválido.
        @see pickle.load
        """
        with open(caminho, 'rb') as f:
            self.figuras = pickle.load(f)

