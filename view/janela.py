import tkinter as tk


class JanelaView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("LSS Paint")
        self.root.geometry("800x600")

        self._montar_layout()
        self._montar_canvas()
        self._montar_menu_ferramentas()
        self._montar_menu_cores()
        self._montar_paleta()

    # ===== Montagem da interface =====

    def _montar_layout(self):
        self.frame_esquerda = tk.Frame(self.root, width=80, bg="#e0e0e0", relief="raised", borderwidth=2)
        self.frame_esquerda.pack(side="left", fill="y")

        self.frame_base = tk.Frame(self.root, height=60, bg="#e0e0e0", relief="raised", borderwidth=2)
        self.frame_base.pack(side="bottom", fill="x")

        self.frame_canva = tk.Frame(self.root)
        self.frame_canva.pack(side="right", fill="both", expand=True)

    def _montar_canvas(self):
        scroll_y = tk.Scrollbar(self.frame_canva, orient="vertical")
        scroll_x = tk.Scrollbar(self.frame_canva, orient="horizontal")

        self.canvas = tk.Canvas(
            self.frame_canva, bg="white",
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set,
            scrollregion=(0, 0, 1000, 1000)
        )
        scroll_y.config(command=self.canvas.yview)
        scroll_x.config(command=self.canvas.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind('<ButtonPress-1>', self.controller.iniciar_figura)
        self.canvas.bind('<B1-Motion>', self.controller.atualizar_figura)
        self.canvas.bind('<ButtonRelease-1>', self.controller.incluir_figura)

    def _montar_menu_ferramentas(self):
        tk.Label(self.frame_esquerda, text="FERRAMENTAS", bg="#e0e0e0", font=("Verdana", 8, "bold")).pack(pady=5)

        self.frame_ferramentas_botoes = tk.Frame(self.frame_esquerda, bg="#e0e0e0")
        self.frame_ferramentas_botoes.pack(fill="x")

        ferramentas = [
            ("Lápis", "rabisco"), ("Linha", "linha"), ("Retângulo", "retangulo"),
            ("Oval", "oval"), ("Círculo", "circulo"), ("Polígono", "poligono")
        ]
        for texto, val in ferramentas:
            tk.Button(
                self.frame_ferramentas_botoes, text=texto, width=10,
                command=lambda v=val: self.controller.mudar_ferramenta(v)
            ).pack(pady=2)

        self.frame_lados = tk.Frame(self.frame_esquerda, bg="#e0e0e0")
        tk.Label(self.frame_lados, text="Lados:", bg="#e0e0e0", font=("Verdana", 8)).pack(side="left")
        self.spin_lados = tk.Spinbox(
            self.frame_lados, from_=3, to=12, width=4,
            command=lambda: self.controller.mudar_num_lados(self.spin_lados.get())
        )
        self.spin_lados.delete(0, "end")
        self.spin_lados.insert(0, str(self.controller.model.num_lados_poligono))
        self.spin_lados.pack(side="left", padx=5)
        self.spin_lados.bind("<KeyRelease>", lambda e: self.controller.mudar_num_lados(self.spin_lados.get()))

    def _montar_menu_cores(self):
        tk.Label(self.frame_esquerda, text="\nCORES", bg="#e0e0e0", font=("Verdana", 8, "bold")).pack()

        self.botao_cor_borda = tk.Button(
            self.frame_esquerda, text="Cor da Borda", bg="black", fg="white", relief="sunken",
            command=lambda: self.controller.set_cor_alvo("borda")
        )
        self.botao_cor_borda.pack(pady=2, fill="x", padx=5)

        self.botao_cor_preenchimento = tk.Button(
            self.frame_esquerda, text="Cor do Fundo", bg="white", relief="raised",
            command=lambda: self.controller.set_cor_alvo("preenchimento")
        )
        self.botao_cor_preenchimento.pack(pady=2, fill="x", padx=5)

    def _montar_paleta(self):
        tk.Label(self.frame_base, text="PALETA:", bg="#e0e0e0", font=("Verdana", 8, "bold")).pack(side="left", padx=5)
        tk.Button(
            self.frame_base, text="X", bg="white", width=3,
            command=lambda: self.controller.selecionar_cor("transparente")
        ).pack(side="left", padx=2, pady=5)

        frame_paleta = tk.Frame(self.frame_base, bg="#e0e0e0")
        frame_paleta.pack(side="left", padx=5)

        cores_paleta = [
            "#000000", "#404040", "#808080", "#FFFFFF", "#FF0000", "#FF3C00",
            "#FF5E00", "#FF7B00", "#F5D000", "#9DFF00", "#09FF00", "#008300",
            "#00FFC8", "#0077FF", "#001AFF", "#000080", "#7700FF", "#E100FF",
            "#FF00D4", "#FF0062", "#7A012A", "#710080", "#5E3201", "#745500"
        ]

        for coluna, cor in enumerate(cores_paleta):
            tk.Button(
                frame_paleta, bg=cor, width=2, height=1, relief="sunken", bd=1,
                command=lambda c=cor: self.controller.selecionar_cor(c)
            ).grid(row=0, column=coluna, padx=1, pady=1)

    # ===== Métodos chamados pelo controller para atualizar a tela =====

    def canvas_coords(self, event):
        return self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

    def atualizar_visibilidade_lados(self, mostrar):
        if mostrar:
            self.frame_lados.pack(pady=5, fill="x", padx=5, after=self.frame_ferramentas_botoes)
        else:
            self.frame_lados.pack_forget()

    def atualizar_botoes_cor(self, alvo):
        if alvo == "borda":
            self.botao_cor_borda.config(relief="sunken")
            self.botao_cor_preenchimento.config(relief="raised")
        else:
            self.botao_cor_borda.config(relief="raised")
            self.botao_cor_preenchimento.config(relief="sunken")

    def atualizar_cor_botao(self, alvo, cor):
        if alvo == "borda":
            self.botao_cor_borda.config(bg=cor)
        else:
            self.botao_cor_preenchimento.config(bg=cor)

    def desenhar_preview(self, figura):
        self.canvas.delete("preview")
        if figura:
            figura.desenhar(self.canvas, tag="preview")

    def redesenhar_tudo(self, figuras):
        self.canvas.delete("preview")
        self.canvas.delete("definitivo")
        for figura in figuras:
            figura.desenhar(self.canvas, tag="definitivo")