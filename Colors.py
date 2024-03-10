# O método change_theme(self, theme) é usado para alterar o tema da interface do usuário de um aplicativo PyQt.
# Aqui está uma descrição detalhada:
    # Este é o início da definição do método.
    # Ele recebe um argumento, theme, que é o nome do tema que você deseja aplicar.
def change_theme(self, theme):
    # Este método é usado para definir o estilo do theme_menu (presumivelmente um objeto QMenu no PyQt).
    # O estilo é definido usando uma folha de estilo em cascata (CSS), ...
    # que é uma linguagem usada para descrever a aparência de um documento escrito em HTML ou XML.
    # No caso de PyQt, ele é usado para estilizar widgets.
        # QMenuBar::item:selected { background-color: #90c8f6; } ...
        # QMenu::item:selected { background-color: #90c8f6; } ...
            # altera a cor de fundo dos itens de menu selecionados para #90c8f6 (um tom de azul claro).
        # QMenuBar::item:hover { background-color: #000000; } ...
        # QMenu::item:hover { background-color: #000000; } ...
            # altera a cor de fundo dos itens de menu quando o mouse passa sobre eles para #000000 (um tom de preto).
    submenu_stylesheet = """
        QMenu::item:selected {
            background-color: #90c8f6;
        }
        QMenu::item:hover {
            background-color: #000000;
        }
        QWidget {
            background-color: #f0f0f0;
            color: #333333;
        }
    """
    menubar_stylesheet = """
        QMenuBar::item:selected {
            background-color: #90c8f6;
        }
        QMenuBar::item:hover {
            background-color: #000000;
        }
        QWidget {
            background-color: #f0f0f0;
            color: #333333;
        }
    """
    # Esta linha verifica se o tema passado como argumento é 'Tema Neutro Padrão'.
    # Se for, ele executa o bloco de código a seguir.
    if theme == 'Tema Neutro Padrão':
        pass

    elif theme == 'Tema Claro':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #b3b3b3;
            }
            QMenu::item:hover {
                background-color: #333333;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected { 
                background-color: #b3b3b3; 
            }
            QMenuBar::item:hover { 
                background-color: #333333; 
            }
        """

    elif theme == 'Tema Escuro':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #333333;
            }
            QMenu::item:hover {
                background-color: #b3b3b3;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #333333;
            }
            QMenuBar::item:hover {
                background-color: #b3b3b3;
            }
        """

    elif theme == 'Tema Azul':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #538cc6;
            }
            QMenu::item:hover {
                background-color: #1a3348;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #538cc6;
            }
            QMenuBar::item:hover {
                background-color: #1a3348;
            }
        """

    elif theme == 'Tema Vermelho':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #c65353;
            }
            QMenu::item:hover {
                background-color: #4d1a1a;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #c65353;
            }
            QMenuBar::item:hover {
                background-color: #4d1a1a;
            }
        """

    elif theme == 'Tema Verde':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #53c68c;
            }
            QMenu::item:hover {
                background-color: #1a4d33;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #53c68c;
            }
            QMenuBar::item:hover {
                background-color: #1a4d33;
            }
        """

    elif theme == 'Tema Roxo':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #8c53c6;
            }
            QMenu::item:hover {
                background-color: #331a4d;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #8c53c6;
            }
            QMenuBar::item:hover {
                background-color: #331a4d;
            }
        """

    elif theme == 'Tema Laranja':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #ff751a;
            }
            QMenu::item:hover {
                background-color: #993d00;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #ff751a;
            }
            QMenuBar::item:hover {
                background-color: #993d00;
            }
        """

    elif theme == 'Tema Amarelo':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #ffffb3;
            }
            QMenu::item:hover {
                background-color: #99993d;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #ffffb3;
            }
            QMenuBar::item:hover {
                background-color: #99993d;
            }
        """

    elif theme == 'Tema Rosa':
        submenu_stylesheet = """
            QMenu::item:selected {
                background-color: #ffb3e6;
            }
            QMenu::item:hover {
                background-color: #993d7a;
            }
        """
        menubar_stylesheet = """
            QMenuBar::item:selected {
                background-color: #ffb3e6;
            }
            QMenuBar::item:hover {
                background-color: #993d7a;
            }
        """

    if self.themes_menu is not None:  # Verificando se theme_menu não é None
        self.themes_menu.setStyleSheet(submenu_stylesheet)
    if self.config_menu is not None:  # Verificando se config_menu não é None
        self.config_menu.setStyleSheet(submenu_stylesheet)
    if self.menu_bar is not None:  # Verificando se menu_bar não é None
        self.menu_bar.setStyleSheet(menubar_stylesheet)

def apply_neutral_standart_theme(self):
    self.setStyleSheet("""
    QPushButton {
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
    }
    QListWidget {
        min-width: 150px;
        min-height: 140px;
    }
    """)
    self.change_theme('Tema Neutro Padrão')

# O método apply_light_theme(self) é usado para aplicar um tema claro à interface do usuário de um aplicativo PyQt.
# Ele faz isso definindo uma folha de estilo para o objeto atual (self), ...
# que provavelmente é uma janela ou widget que contém outros widgets.
# Aqui está uma descrição detalhada:
    # QWidget { background-color: #f0f0f0; color: #333333; }:
        # Isso define a cor de fundo de todos os widgets para #f0f0f0 ...
        # (um tom de cinza claro) e a cor do texto para #333333 (um tom de cinza escuro).
    # QPushButton { ... }:
        # Isso define o estilo dos botões (QPushButton).
        # Ele define a cor de fundo, o estilo e a cor da borda, o tamanho da fonte, ...
        # a largura mínima e máxima, o preenchimento e a cor do texto.
    # QPushButton:hover { ... }:
        # Isso define o estilo dos botões quando o mouse passa sobre eles.
        # Ele altera a cor de fundo, a cor da borda e a cor do texto.
    # QLabel { color: #333333; }:
        # Isso define a cor do texto de todos os rótulos (QLabel) para #333333 (um tom de cinza escuro).
    # QListWidget { ... }:
        # Isso define o estilo das listas de widgets (QListWidget).
        # Ele define a cor de fundo, a largura mínima, a altura mínima e a cor do texto.
    ## O método setStyleSheet é usado para aplicar a folha de estilo.
        # As folhas de estilo em PyQt são uma maneira de estilizar widgets; ...
        # elas usam uma sintaxe semelhante à das folhas de estilo em cascata (CSS) usadas em HTML.
def apply_light_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #f0f0f0;
        color: #333333;
    }
    QPushButton {
        background-color: #e0e0e0;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #b3b3b3;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #333333;
    }
    QPushButton:hover {
        background-color: #b3b3b3;
        border-color: #333333;
        color: #f0f0f0;
    }
    QLabel {
        color: #333333;
    }
    QListWidget {
        background-color: #e0e0e0;
        min-width: 150px;
        min-height: 140px;
        color: #333333;
    }
    """)
    self.change_theme('Tema Claro')

def apply_dark_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
        color: #b3b3b3;
    }
    QPushButton {
        background-color: #333333;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #1e1e1e;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #b3b3b3;
    }
    QPushButton:hover {
        background-color: #1e1e1e;
        border-color: #b3b3b3;
        color: #f0f0f0;
    }
    QLabel {
        color: #f0f0f0;
    }
    QListWidget {
        background-color: #333333;
        min-width: 150px;
        min-height: 140px;
        color: #f0f0f0;
    }
    """)
    self.change_theme('Tema Escuro')

def apply_blue_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #336699;
        color: #ffffff;
    }
    QPushButton {
        background-color: #264d73;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #1a3348;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #1a3348;
        border-color: #ffffff;
        color: #b3d1ff;
    }
    QLabel {
        color: #ffffff;
    }
    QListWidget {
        background-color: #264d73;
        min-width: 150px;
        min-height: 140px;
        color: #ffffff;
    }
    """)
    self.change_theme('Tema Azul')

def apply_red_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #993333;
        color: #ffffff;
    }
    QPushButton {
        background-color: #732626;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #4d1a1a;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #4d1a1a;
        border-color: #ffffff;
        color: #ff9999;
    }
    QLabel {
        color: #ffffff;
    }
    QListWidget {
        background-color: #732626;
        min-width: 150px;
        min-height: 140px;
        color: #ffffff;
    }
    """)
    self.change_theme('Tema Vermelho')

def apply_green_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #339966;
        color: #ffffff;
    }
    QPushButton {
        background-color: #26734d;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #1a4d33;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #1a4d33;
        border-color: #ffffff;
        color: #99ffcc;
    }
    QLabel {
        color: #ffffff;
    }
    QListWidget {
        background-color: #26734d;
        min-width: 150px;
        min-height: 140px;
        color: #ffffff;
    }
    """)
    self.change_theme('Tema Verde')

def apply_purple_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #663399;
        color: #ffffff;
    }
    QPushButton {
        background-color: #4d2673;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #331a4d;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #331a4d;
        border-color: #ffffff;
        color: #b399ff;
    }
    QLabel {
        color: #ffffff;
    }
    QListWidget {
        background-color: #4d2673;
        min-width: 150px;
        min-height: 140px;
        color: #ffffff;
    }
    """)
    self.change_theme('Tema Roxo')

def apply_orange_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #ff6600;
        color: #ffffff;
    }
    QPushButton {
        background-color: #cc5200;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #993d00;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #993d00;
        border-color: #ffffff;
        color: #ffcc99;
    }
    QLabel {
        color: #ffffff;
    }
    QListWidget {
        background-color: #cc5200;
        min-width: 150px;
        min-height: 140px;
        color: #ffffff;
    }
    """)
    self.change_theme('Tema Laranja')

def apply_yellow_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #ffff66;
        color: #333333;
    }
    QPushButton {
        background-color: #cccc52;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #99993d;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #333333;
    }
    QPushButton:hover {
        background-color: #99993d;
        border-color: #333333;
        color: #ffffcc;
    }
    QLabel {
        color: #333333;
    }
    QListWidget {
        background-color: #cccc52;
        min-width: 150px;
        min-height: 140px;
        color: #333333;
    }
    """)
    self.change_theme('Tema Amarelo')

def apply_pink_theme(self):
    self.setStyleSheet("""
    QWidget {
        background-color: #ff66cc;
        color: #ffffff;
    }
    QPushButton {
        background-color: #cc52a3;
        border-style: outset;
        border-width: 2px;
        border-radius: 5px;
        border-color: #993d7a;
        font: bold 12px;
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #993d7a;
        border-color: #ffffff;
        color: #ffccf2;
    }
    QLabel {
        color: #ffffff;
    }
    QListWidget {
        background-color: #cc52a3;
        min-width: 150px;
        min-height: 140px;
        color: #ffffff;
    }
    """)
    self.change_theme('Tema Rosa')

def apply_neutral_standart_theme_2(self):
    self.setStyleSheet("""
    QPushButton {
        min-width: 14em;
        max-width: 14em;
        padding: 2px;
    }
    QListWidget {
        min-width: 150px;
        min-height: 140px;
    }
    QMenu::item:selected {
        background-color: #90c8f6;
    }
    QMenu::item:hover {
        background-color: #000000;
    }
    QMenuBar::item:selected {
        background-color: #90c8f6;
    }
    QMenuBar::item:hover {
        background-color: #000000;
    }
    """)
    