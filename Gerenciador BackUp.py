import os  # Importa o módulo os
import sys  # Importa o módulo sys
# Importa as classes QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
# QListWidget, QPushButton, QWidget QMenu do módulo QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QWidget, QMenu)
# Importa a classe Qt do módulo QtCore
from PyQt6.QtCore import Qt
# Importa a classe QAction do módulo QtGui
from PyQt6.QtGui import QAction
# Importa a classe QtGui do módulo PyQt6
from PyQt6 import QtGui
# Importa a classe GerenciadorInterface do módulo ManagerInterface_7Zip
from ManagerInterface_7Zip import GerenciadorInterface
# Importa a função apply_neutral_standart_theme_2 do módulo Colors
from Colors import apply_neutral_standart_theme_2


# Define uma nova classe chamada InterfaceGrafica que herda de QMainWindow, uma classe do PyQt que representa uma janela.
class InterfaceGrafica(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cria o gerenciador de interface
        self.gerenciador_interface = GerenciadorInterface(self)

        # Cria a barra de menus
        self.menu_bar = self.menuBar()
        if self.menu_bar is None:
            raise Exception("MenuBar não pôde ser criado")

        # Cria a barra de menus
        self.config_menu = self.menu_bar.addMenu('Configurações')
        if self.config_menu is None:
            raise Exception("Menu de Configurações não pôde ser criado")
        
            # Adicionar ação para selecionar método de compressão
        self.compression_method_action = QAction('Selecionar Método de Compressão', self)
            # Conectar a ação a um método
        self.compression_method_action.triggered.connect(self.select_compression_method)
            # Adicionar a ação ao menu
        self.config_menu.addAction(self.compression_method_action)
            # Adiciona evento de entrada e saída para ativar o menu
        self.config_menu.aboutToShow.connect(self.select_compression_method)

        # Chama o método init_ui
        self.init_ui()

    # Define um método chamado select_compression_method
    def select_compression_method(self):
        # Dicionário de legendas para os métodos de compressão
        legends_sevenzip = {
            "0": "0 - Armazenar",
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }

        # Crie um menu para selecionar o método de compressão
        compression_menu = QMenu(self)
        compression_menu.setStyleSheet(self.config_menu.styleSheet())	

        # Adicione submenus para cada método de compressão do WinRAR
        zip_submenu = QMenu('ZIP (0-9)', self)
        zip_submenu.setStyleSheet(self.config_menu.styleSheet())
        zip_methods = ["0", "1", "3", "5", "7", "9"]

        # Adicione submenus para cada método de compressão do 7-Zip
        seven_submenu = QMenu('7Z (0-9)', self)
        seven_submenu.setStyleSheet(self.config_menu.styleSheet())
        seven_methods = ["0", "1", "3", "5", "7", "9"]

        # Adicione submenus para cada método de compressão do 7-Zip
        tar_submenu = QMenu('TAR (0)', self)
        tar_submenu.setStyleSheet(self.config_menu.styleSheet())
        tar_methods = ["0"]
        
        # Adicione ação para cada método de compressão
        for method in zip_methods:
            # Crie uma ação para o método de compressão
            action = QAction(legends_sevenzip[method], self)
            # Conecte a ação a um método, passando o método de compressão como argumento
            action.triggered.connect(lambda checked=False, method=method: self.set_compression_method(checked, method, 'zip'))
            # Adicione a ação ao submenu do 7-Zip
            zip_submenu.addAction(action)
        # Adicione o submenu do 7-Zip ao menu de compressão
        compression_menu.addMenu(zip_submenu)

        for method in seven_methods:
            action = QAction(legends_sevenzip[method], self)
            action.triggered.connect(lambda checked=False, method=method: self.set_compression_method(checked, method, '7z'))
            seven_submenu.addAction(action)
        compression_menu.addMenu(seven_submenu)

        for method in tar_methods:
            action = QAction(legends_sevenzip[method], self)
            action.triggered.connect(lambda checked=False, method=method: self.set_compression_method(checked, method, 'tar'))
            tar_submenu.addAction(action)
        compression_menu.addMenu(tar_submenu)

        # Adicione o menu de compressão como submenu do menu principal
        self.compression_method_action.setMenu(compression_menu)

    # Define um método chamado set_compression_method
    def set_compression_method(self, checked, method, compress_type):
        # Verifica o tipo de compressão
        if compress_type == 'zip':
            # Define o método de compressão para arquivos ZIP
            self.gerenciador_interface.compression_method_zip = method
        elif compress_type == '7z':
            self.gerenciador_interface.compression_method_7z = method
        elif compress_type == 'tar':
            self.gerenciador_interface.compression_method_tar = method

    # Define um método chamado init_ui
    def init_ui(self):
        # Esta linha está definindo o caminho base para buscar arquivos.
        # Se o programa estiver sendo executado como um executável PyInstaller, ...
        # o atributo sys._MEIPASS será definido, que é o caminho para os recursos empacotados.
        # Se não estiver sendo executado como um executável, ele usará o diretório do script atual.
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        # Esta linha está definindo o caminho para a pasta "icones", ...
        # que está localizada no mesmo diretório que o script atual ou no diretório de recursos do PyInstaller, ...
        # dependendo de como o programa está sendo executado.
        icon_path = os.path.join(base_path, "icones")

        main_layout_1 = QHBoxLayout()

        primeiro_quadrante_layout = QVBoxLayout()

        folder_button = QPushButton("Adicionar Pastas")
        folder_button.clicked.connect(lambda: self.gerenciador_interface.browse_folder(self))
        primeiro_quadrante_layout.addWidget(folder_button)

        file_button = QPushButton("Adicionar Arquivos")
        file_button.clicked.connect(lambda: self.gerenciador_interface.browse_file(self))
        primeiro_quadrante_layout.addWidget(file_button)

        test_button = QPushButton("Testar Integridade")
        test_icon_path = os.path.join(icon_path, "teste_integridade2.png")
        test_button.setIcon(QtGui.QIcon(test_icon_path))
        test_button.clicked.connect(self.gerenciador_interface.testar_integridade)
        primeiro_quadrante_layout.addWidget(test_button)

        clear_button_folders = QPushButton("Limpar Entrada")
        limpar_folders_icon_path = os.path.join(icon_path, "clear_button3.png")
        clear_button_folders.setIcon(QtGui.QIcon(limpar_folders_icon_path))
        clear_button_folders.clicked.connect(self.gerenciador_interface.clear_folders)
        primeiro_quadrante_layout.addWidget(clear_button_folders)

        clear_button_output = QPushButton("Limpar Saídas")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        clear_button_output.setIcon(QtGui.QIcon(limpar_output_icon_path))
        clear_button_output.clicked.connect(self.gerenciador_interface.clear_output)
        primeiro_quadrante_layout.addWidget(clear_button_output)

        main_layout_1.addLayout(primeiro_quadrante_layout)
        main_layout_1.setAlignment(primeiro_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        segundo_quadrante_layout = QVBoxLayout()

        folder_label = QLabel("Diretório(s) Pastas e Arquivos:")
        segundo_quadrante_layout.addWidget(folder_label)
        self.gerenciador_interface.folder_listbox = QListWidget()
        segundo_quadrante_layout.addWidget(self.gerenciador_interface.folder_listbox)
        main_layout_1.addLayout(segundo_quadrante_layout)

        main_layout_2 = QHBoxLayout()

        quarto_quadrante_layout = QVBoxLayout()

        output_button_output_ZIP = QPushButton("Especificar Diretório(s) de Saída .ZIP")
        output_button_output_ZIP.clicked.connect(self.gerenciador_interface.output_button_output_ZIP_clicked)
        quarto_quadrante_layout.addWidget(output_button_output_ZIP)

        create_zip_button = QPushButton("Armazenar como .ZIP")
        zip_icon_path = os.path.join(icon_path, "winzip4.png")
        create_zip_button.setIcon(QtGui.QIcon(zip_icon_path))
        create_zip_button.clicked.connect(self.gerenciador_interface.store_as_zip)
        quarto_quadrante_layout.addWidget(create_zip_button)

        output_button_output_7Z = QPushButton("Especificar Diretório(s) de Saída .7Z")
        output_button_output_7Z.clicked.connect(self.gerenciador_interface.output_button_output_7Z_clicked)
        quarto_quadrante_layout.addWidget(output_button_output_7Z)

        create_7z_button = QPushButton("Armazenar como .7Z")
        sevenzip_icon_path = os.path.join(icon_path, "sevenzip4.png")
        create_7z_button.setIcon(QtGui.QIcon(sevenzip_icon_path))
        create_7z_button.clicked.connect(self.gerenciador_interface.store_as_7z)
        quarto_quadrante_layout.addWidget(create_7z_button)

        main_layout_2.addLayout(quarto_quadrante_layout)
        main_layout_2.setAlignment(quarto_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        quinto_quadrante_layout = QVBoxLayout()

        output_label_zip = QLabel("Diretório(s) de saída .ZIP:")
        quinto_quadrante_layout.addWidget(output_label_zip)
        self.gerenciador_interface.output_listbox_zip = QListWidget()
        quinto_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_zip)
        main_layout_2.addLayout(quinto_quadrante_layout)

        sexto_quadrante_layout = QVBoxLayout()

        output_label_7z = QLabel("Diretório(s) de saída .7Z:")
        sexto_quadrante_layout.addWidget(output_label_7z)
        self.gerenciador_interface.output_listbox_7z = QListWidget()
        sexto_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_7z)
        main_layout_2.addLayout(sexto_quadrante_layout)

        main_layout_3 = QHBoxLayout()

        setimo_quadrante_layout = QVBoxLayout()

        output_button_output_TAR = QPushButton("Especificar Diretório(s) de Saída .TAR")
        output_button_output_TAR.clicked.connect(self.gerenciador_interface.output_button_output_TAR_clicked)
        setimo_quadrante_layout.addWidget(output_button_output_TAR)

        create_tar_button = QPushButton("Armazenar como .TAR")
        tar_icon_path = os.path.join(icon_path, "tar1.png")
        create_tar_button.setIcon(QtGui.QIcon(tar_icon_path))
        create_tar_button.clicked.connect(self.gerenciador_interface.store_as_tar)
        setimo_quadrante_layout.addWidget(create_tar_button)

        output_button_output_EXTRACT = QPushButton("Especificar Diretório(s) de Extração")
        output_button_output_EXTRACT.clicked.connect(self.gerenciador_interface.output_button_output_EXTRACT_clicked)
        setimo_quadrante_layout.addWidget(output_button_output_EXTRACT)

        extract_button = QPushButton("Extrair Arquivos e Pastas")
        extracao_icon_path = os.path.join(icon_path, "extracao4.png")
        extract_button.setIcon(QtGui.QIcon(extracao_icon_path))
        extract_button.clicked.connect(self.gerenciador_interface.extract_files)
        setimo_quadrante_layout.addWidget(extract_button)

        main_layout_3.addLayout(setimo_quadrante_layout)
        main_layout_3.setAlignment(setimo_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        oitavo_quadrante_layout = QVBoxLayout()

        output_label_tar = QLabel("Diretório(s) de saída .TAR:")
        oitavo_quadrante_layout.addWidget(output_label_tar)
        self.gerenciador_interface.output_listbox_tar = QListWidget()
        oitavo_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_tar)
        main_layout_3.addLayout(oitavo_quadrante_layout)

        nono_quadrante_layout = QVBoxLayout()

        output_label_extract = QLabel("Diretório(s) para Extração:")
        nono_quadrante_layout.addWidget(output_label_extract)
        self.gerenciador_interface.output_listbox_extract = QListWidget()
        nono_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_extract)
        main_layout_3.addLayout(nono_quadrante_layout)

        widget_1 = QWidget(self)
        widget_1.setLayout(main_layout_1)
        widget_2 = QWidget(self)
        widget_2.setLayout(main_layout_2)
        widget_3 = QWidget(self)
        widget_3.setLayout(main_layout_3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(widget_1)
        main_layout.addWidget(widget_2)
        main_layout.addWidget(widget_3)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.apply_neutral_standart_theme_2()

    def apply_neutral_standart_theme_2(self):
        apply_neutral_standart_theme_2(self)


# Esta linha verifica se o script atual está sendo executado diretamente, e não sendo importado como um módulo.
# Se o script está sendo executado diretamente, o valor de __name__ será "__main__".
if __name__ == "__main__":
    # Esta linha cria uma instância de QApplication, que é a classe principal de qualquer aplicação PyQt.
    # Ela recebe como argumento uma lista de argumentos de linha de comando.
    # Neste caso, uma lista vazia é passada, o que significa que nenhum argumento de linha de comando é usado.
    app = QApplication([])
    # Esta linha cria uma instância da classe InterfaceGrafica.
    # Presumivelmente, esta é uma subclasse de uma das classes de janela do PyQt, ...
    # como QMainWindow ou QWidget, e define a interface do usuário da aplicação.
    window = InterfaceGrafica()
    # Esta linha exibe a janela na tela. Até que este método seja chamado, a janela não será visível.
    window.show()
    # Esta linha inicia o loop de eventos da aplicação.
    # Um loop de eventos é um loop infinito que espera por eventos do sistema, ...
    # como cliques de mouse ou pressionamentos de teclas, e os envia para os objetos apropriados.
    # Este método não retornará até que a aplicação seja encerrada.
    app.exec()

"""
Este código utiliza as seguintes bibliotecas:

- `os`: Uma biblioteca padrão do Python para interagir com o sistema operacional. Permite realizar várias operações no sistema de arquivos e no ambiente do sistema operacional.
- `subprocess`: Uma biblioteca padrão do Python para gerenciar novos processos, conectar a seus pipes de entrada/saída/erro e obter seus códigos de retorno.
- `PyQt6.QtWidgets`: Uma biblioteca de terceiros para criar interfaces gráficas de usuário (GUIs) no Python.
- `Nesta versão`: O empacotamento de compressão e descompressão é feito pelo 7-Zip, fora da Thread Principal.
        Deixando a GUI livre, sem bloquea-la, até que o processo seja concluído.
- `Nesta versão`: Os botões e caixas de texto estão organizados em grade, em três colunas e três linhas.
- `Nesta versão`: O tema é aplicado o tema padrão da biblioteca PyQt6 - Neutral Standart, Light, Dark, Blue, Red, Green, Purple, Orange, Yellow, Pink.

Agradecemos aos desenvolvedores e contribuidores dessas bibliotecas por seu trabalho duro e dedicação, que tornaram possível a criação deste projeto.
"""
