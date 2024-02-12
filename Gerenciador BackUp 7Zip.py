import os
import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton,
                             QFileDialog, QWidget, QTreeView, QMessageBox, QMenu)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6 import QtGui


def buscar_sevenzip_executavel():
    # Obter o caminho do diretório do executável
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    # Construir o caminho para o executável do 7-Zip
    caminho_sevenzip = os.path.join(dir_atual, '7zG.exe')

    # Verificar se o executável do 7-Zip existe
    if os.path.exists(caminho_sevenzip):
        return caminho_sevenzip

    possible_locations = [
        rf"C:\Program Files\7-Zip\7zG.exe",
        rf"C:\Program Files (x86)\7-Zip\7zG.exe",
    ]

    for location in possible_locations:
        if os.path.isfile(location):
            return location

    return None


class CompressaoZIP(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, output_listbox, folder_listbox, compress_as_zip=False,
                 compression_method=None):

        super().__init__()
        self.sevenzip_executable = sevenzip_executable
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_zip = compress_as_zip
        self.compression_method = compression_method

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        compressed_files = []

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                compressed_file_zip = os.path.join(output_path, f"{folder_name}.zip")
                command = f'"{self.sevenzip_executable}" a -r -tzip -mx={self.compression_method} "{compressed_file_zip}" "{folder_path}"'
                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_zip)

        self.finished.emit()


class Compressao7Z(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, output_listbox, folder_listbox, compress_as_7z=False,
                 compression_method=None):

        super().__init__()
        self.sevenzip_executable = sevenzip_executable
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_7z = compress_as_7z
        self.compression_method = compression_method

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        compressed_files = []

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                compressed_file_7z = os.path.join(output_path, f"{folder_name}.7z")
                command = f'"{self.sevenzip_executable}" a -r -t7z -mx={self.compression_method} "{compressed_file_7z}" "{folder_path}"'
                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_7z)

        self.finished.emit()


class CompressaoTAR(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, output_listbox, folder_listbox, compress_as_tar=False,
                 compression_method=None):

        super().__init__()
        self.sevenzip_executable = sevenzip_executable
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_tar = compress_as_tar
        self.compression_method = compression_method

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        compressed_files = []

        for idx in range(self.folder_listbox.count()):
            folder_path = self.folder_listbox.item(idx).text()
            folder_name = os.path.basename(folder_path)

            for output_path in output_paths:
                compressed_file_tar = os.path.join(output_path, f"{folder_name}.tar")
                command = f'"{self.sevenzip_executable}" a -r -ttar "{compressed_file_tar}" "{folder_path}"'
                subprocess.run(command, shell=True)
                compressed_files.append(compressed_file_tar)

        self.finished.emit()


class TesteIntegridadeCentral(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, compressed_files):
        super().__init__()
        self.sevenzip_executable = sevenzip_executable
        self.compressed_files = compressed_files

    def run(self):
        for compressed_file in self.compressed_files:
            if compressed_file.endswith(".zip"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            elif compressed_file.endswith(".7z"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            elif compressed_file.endswith(".tar"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

        self.finished.emit()


class ExtracaoCentral(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, output_listbox, folder_listbox):
        super().__init__()
        self.sevenzip_executable = sevenzip_executable
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox

    def run(self):
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        if not output_paths:
            return

        for idx in range(self.folder_listbox.count()):
            archive_path = self.folder_listbox.item(idx).text()
            for output_path in output_paths:
                if archive_path.endswith(".zip"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".7z"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".tar"):
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    subprocess.run(command, shell=True)

        self.finished.emit()


class PastaAppEmapacotamento(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sevenzip_executable = buscar_sevenzip_executavel()

        if not self.sevenzip_executable:
            print("7-Zip não encontrado. Por favor, instale e tente novamente.")
            exit(1)

            # Crie listas separadas para cada tipo de compressão
        self.output_listbox_zip = QListWidget()
        self.output_listbox_7z = QListWidget()
        self.output_listbox_tar = QListWidget()
        self.output_listbox = QListWidget()
        self.folder_listbox = QListWidget()
        self.output_listbox_extract = QListWidget()
        self.compressed_files = []

        self.compress_thread_zip = CompressaoZIP(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.compress_thread_zip.finished.connect(self.on_compress_finished)

        self.compress_thread_7z = Compressao7Z(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.compress_thread_7z.finished.connect(self.on_compress_finished)

        self.compress_thread_tar = CompressaoTAR(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.compress_thread_tar.finished.connect(self.on_compress_finished)

        self.teste_integridade_thread = TesteIntegridadeCentral(self.sevenzip_executable, self.compressed_files)
        self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)

        self.extract_thread = ExtracaoCentral(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.extract_thread.finished.connect(self.on_extract_finished)

        # Cria a barra de menus
        self.menu_bar = self.menuBar()

        # Criar menu de configurações
        self.config_menu = self.menu_bar.addMenu('Configurações')

        # Adicionar ação para selecionar método de compressão
        self.compression_method_action = QAction('Selecionar Método de Compressão', self)
        self.compression_method_action.triggered.connect(self.select_compression_method)
        self.config_menu.addAction(self.compression_method_action)
        # Definir variáveis para armazenar o método de compressão selecionado para cada tipo
        self.compression_method_rar = None
        self.compression_method_zip = None
        self.compression_method_7z = None
        self.compression_method_tar = None
        # Adiciona evento de entrada e saída para ativar o menu
        self.config_menu.aboutToShow.connect(self.select_compression_method)

        # Cria o menu de temas
        self.theme_menu = self.menu_bar.addMenu('Temas')

        # Cria a ação para o tema neutro padrão
        self.neutral_theme_action = QAction('Tema Neutro Padrão', self)
        self.neutral_theme_action.triggered.connect(self.apply_neutral_standart_theme)
        self.neutral_theme_action.triggered.connect(lambda: self.change_theme('Tema Neutro Padrão'))
        self.theme_menu.addAction(self.neutral_theme_action)

        # Cria a ação para o tema claro
        self.light_theme_action = QAction('Tema Claro', self)
        self.light_theme_action.triggered.connect(self.apply_light_theme)
        self.light_theme_action.triggered.connect(lambda: self.change_theme('Tema Claro'))
        self.theme_menu.addAction(self.light_theme_action)

        # Cria a ação para o tema escuro
        self.dark_theme_action = QAction('Tema Escuro', self)
        self.dark_theme_action.triggered.connect(self.apply_dark_theme)
        self.dark_theme_action.triggered.connect(lambda: self.change_theme('Tema Escuro'))
        self.theme_menu.addAction(self.dark_theme_action)

        # Cria a ação para o tema azul
        self.blue_theme_action = QAction('Tema Azul', self)
        self.blue_theme_action.triggered.connect(self.apply_blue_theme)
        self.blue_theme_action.triggered.connect(lambda: self.change_theme('Tema Azul'))
        self.theme_menu.addAction(self.blue_theme_action)

        # Cria a ação para o tema vermelho
        self.red_theme_action = QAction('Tema Vermelho', self)
        self.red_theme_action.triggered.connect(self.apply_red_theme)
        self.red_theme_action.triggered.connect(lambda: self.change_theme('Tema Vermelho'))
        self.theme_menu.addAction(self.red_theme_action)

        # Cria a ação para o tema verde
        self.green_theme_action = QAction('Tema Verde', self)
        self.green_theme_action.triggered.connect(self.apply_green_theme)
        self.green_theme_action.triggered.connect(lambda: self.change_theme('Tema Verde'))
        self.theme_menu.addAction(self.green_theme_action)

        # Cria a ação para o tema roxo
        self.purple_theme_action = QAction('Tema Roxo', self)
        self.purple_theme_action.triggered.connect(self.apply_purple_theme)
        self.purple_theme_action.triggered.connect(lambda: self.change_theme('Tema Roxo'))
        self.theme_menu.addAction(self.purple_theme_action)

        # Cria a ação para o tema laranja
        self.orange_theme_action = QAction('Tema Laranja', self)
        self.orange_theme_action.triggered.connect(self.apply_orange_theme)
        self.orange_theme_action.triggered.connect(lambda: self.change_theme('Tema Laranja'))
        self.theme_menu.addAction(self.orange_theme_action)

        # Cria a ação para o tema amarelo
        self.yellow_theme_action = QAction('Tema Amarelo', self)
        self.yellow_theme_action.triggered.connect(self.apply_yellow_theme)
        self.yellow_theme_action.triggered.connect(lambda: self.change_theme('Tema Amarelo'))
        self.theme_menu.addAction(self.yellow_theme_action)

        # Cria a ação para o tema rosa
        self.pink_theme_action = QAction('Tema Rosa', self)
        self.pink_theme_action.triggered.connect(self.apply_pink_theme)
        self.pink_theme_action.triggered.connect(lambda: self.change_theme('Tema Rosa'))
        self.theme_menu.addAction(self.pink_theme_action)

        self.init_ui()

    def change_theme(self, theme):
        if theme == 'Tema Neutro Padrão':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #333333; 
                }
                QMenu::item:hover { 
                    background-color: #b3b3b3; 
                }
            """)
        elif theme == 'Tema Claro':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #b3b3b3; 
                }
                QMenu::item:hover { 
                    background-color: #333333; 
                }
            """)
        elif theme == 'Tema Escuro':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #333333; 
                }
                QMenu::item:hover { 
                    background-color: #b3b3b3; 
                }
            """)
        elif theme == 'Tema Azul':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #b3d1ff; 
                }
                QMenu::item:hover { 
                    background-color: #1a3348; 
                }
            """)
        elif theme == 'Tema Vermelho':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #ff9999; 
                }
                QMenu::item:hover { 
                    background-color: #4d1a1a; 
                }
            """)
        elif theme == 'Tema Verde':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #99ffcc; 
                }
                QMenu::item:hover { 
                    background-color: #1a4d33; 
                }
            """)
        elif theme == 'Tema Roxo':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #b399ff; 
                }
                QMenu::item:hover { 
                    background-color: #331a4d; 
                }
            """)
        elif theme == 'Tema Laranja':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #ffcc99; 
                }
                QMenu::item:hover { 
                    background-color: #993d00; 
                }
            """)
        elif theme == 'Tema Amarelo':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #ffffcc; 
                }
                QMenu::item:hover { 
                    background-color: #99993d; 
                }
            """)
        elif theme == 'Tema Rosa':
            self.theme_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #ffccf2; 
                }
                QMenu::item:hover { 
                    background-color: #993d7a; 
                }
            """)

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

    def init_ui(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        # Adicione a pasta "icones" ao caminho base
        icon_path = os.path.join(base_path, "icones")

        self.setWindowTitle("Gerenciador de BackUp-7Zip")
        icon_title_path = os.path.join(icon_path, "Manager-BackUp.ico")
        self.setWindowIcon(QtGui.QIcon(icon_title_path))

        ### Primeiro layout horizontal ###
        main_layout_1 = QHBoxLayout()

        # Primeiro quadrante (topo esquerdo)
        primeiro_quadrante_layout = QVBoxLayout()

        folder_button = QPushButton("Adicionar Pastas")
        folder_button.clicked.connect(self.browse_folder)
        primeiro_quadrante_layout.addWidget(folder_button)
        file_button = QPushButton("Adicionar Arquivos")
        file_button.clicked.connect(self.browse_file)
        primeiro_quadrante_layout.addWidget(file_button)

        test_button = QPushButton("Testar Integridade")
        test_icon_path = os.path.join(icon_path, "teste_integridade2.png")
        test_button.setIcon(QtGui.QIcon(test_icon_path))
        test_button.clicked.connect(self.testar_integridade)
        primeiro_quadrante_layout.addWidget(test_button)

        clear_button_folders = QPushButton("Limpar Entrada")
        limpar_folders_icon_path = os.path.join(icon_path, "clear_button3.png")
        clear_button_folders.setIcon(QtGui.QIcon(limpar_folders_icon_path))
        clear_button_folders.clicked.connect(self.clear_folders)
        primeiro_quadrante_layout.addWidget(clear_button_folders)
        clear_button_output = QPushButton("Limpar Saídas")
        limpar_output_icon_path = os.path.join(icon_path, "clear_button2.png")
        clear_button_output.setIcon(QtGui.QIcon(limpar_output_icon_path))
        clear_button_output.clicked.connect(self.clear_output)
        primeiro_quadrante_layout.addWidget(clear_button_output)

        main_layout_1.addLayout(primeiro_quadrante_layout)
        main_layout_1.setAlignment(primeiro_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        # Segundo + Terceiro quadrante (topo centro e direito)
        segundo_quadrante_layout = QVBoxLayout()

        folder_label = QLabel("Diretório(s) Pastas e Arquivos:")
        segundo_quadrante_layout.addWidget(folder_label)
        self.folder_listbox = QListWidget()
        segundo_quadrante_layout.addWidget(self.folder_listbox)
        main_layout_1.addLayout(segundo_quadrante_layout)

        ### Segundo layout horizontal ###
        main_layout_2 = QHBoxLayout()

        # Quarto quadrante (centro esquerdo)
        quarto_quadrante_layout = QVBoxLayout()

        output_button_output_ZIP = QPushButton("Especificar Diretório(s) de Saída .ZIP")
        output_button_output_ZIP.clicked.connect(self.output_button_output_ZIP_clicked)
        quarto_quadrante_layout.addWidget(output_button_output_ZIP)

        create_zip_button = QPushButton("Armazenar como .ZIP")
        zip_icon_path = os.path.join(icon_path, "winzip4.png")
        create_zip_button.setIcon(QtGui.QIcon(zip_icon_path))
        create_zip_button.clicked.connect(self.store_as_zip)
        quarto_quadrante_layout.addWidget(create_zip_button)

        output_button_output_7Z = QPushButton("Especificar Diretório(s) de Saída .7Z")
        output_button_output_7Z.clicked.connect(self.output_button_output_7Z_clicked)
        quarto_quadrante_layout.addWidget(output_button_output_7Z)

        create_7z_button = QPushButton("Armazenar como .7Z")
        sevenzip_icon_path = os.path.join(icon_path, "sevenzip4.png")
        create_7z_button.setIcon(QtGui.QIcon(sevenzip_icon_path))
        create_7z_button.clicked.connect(self.store_as_7z)
        quarto_quadrante_layout.addWidget(create_7z_button)

        main_layout_2.addLayout(quarto_quadrante_layout)
        main_layout_2.setAlignment(quarto_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        # Quinto quadrante (centro centro)
        quinto_quadrante_layout = QVBoxLayout()

        output_label_zip = QLabel("Diretório(s) de saída .ZIP:")
        quinto_quadrante_layout.addWidget(output_label_zip)
        self.output_listbox_zip = QListWidget()
        quinto_quadrante_layout.addWidget(self.output_listbox_zip)
        main_layout_2.addLayout(quinto_quadrante_layout)

        # Sexto quadrante (centro direito)
        sexto_quadrante_layout = QVBoxLayout()

        output_label_7z = QLabel("Diretório(s) de saída .7Z:")
        sexto_quadrante_layout.addWidget(output_label_7z)
        self.output_listbox_7z = QListWidget()
        sexto_quadrante_layout.addWidget(self.output_listbox_7z)
        main_layout_2.addLayout(sexto_quadrante_layout)

        ### Terceiro layout horizontal ###
        main_layout_3 = QHBoxLayout()

        # Sétimo quadrante (inferior esquerdo)
        setimo_quadrante_layout = QVBoxLayout()

        output_button_output_TAR = QPushButton("Especificar Diretório(s) de Saída .TAR")
        output_button_output_TAR.clicked.connect(self.output_button_output_TAR_clicked)
        setimo_quadrante_layout.addWidget(output_button_output_TAR)

        create_tar_button = QPushButton("Armazenar como .TAR")
        tar_icon_path = os.path.join(icon_path, "tar1.png")
        create_tar_button.setIcon(QtGui.QIcon(tar_icon_path))
        create_tar_button.clicked.connect(self.store_as_tar)
        setimo_quadrante_layout.addWidget(create_tar_button)

        output_button_output_EXTRACT = QPushButton("Especificar Diretório(s) de Extração")
        output_button_output_EXTRACT.clicked.connect(self.output_button_output_EXTRACT_clicked)
        setimo_quadrante_layout.addWidget(output_button_output_EXTRACT)

        extract_button = QPushButton("Extrair Arquivos e Pastas")
        extracao_icon_path = os.path.join(icon_path, "extracao4.png")
        extract_button.setIcon(QtGui.QIcon(extracao_icon_path))
        extract_button.clicked.connect(self.extract_files)
        setimo_quadrante_layout.addWidget(extract_button)

        main_layout_3.addLayout(setimo_quadrante_layout)
        main_layout_3.setAlignment(setimo_quadrante_layout, Qt.AlignmentFlag.AlignBottom)

        # Oitavo quadrante (inferior centro)
        oitavo_quadrante_layout = QVBoxLayout()

        output_label_tar = QLabel("Diretório(s) de saída .TAR:")
        oitavo_quadrante_layout.addWidget(output_label_tar)
        self.output_listbox_tar = QListWidget()
        oitavo_quadrante_layout.addWidget(self.output_listbox_tar)
        main_layout_3.addLayout(oitavo_quadrante_layout)

        # Nono quadrante (inferior direito)
        nono_quadrante_layout = QVBoxLayout()

        output_label_extract = QLabel("Diretório(s) para Extração:")
        nono_quadrante_layout.addWidget(output_label_extract)
        self.output_listbox_extract = QListWidget()
        nono_quadrante_layout.addWidget(self.output_listbox_extract)
        main_layout_3.addLayout(nono_quadrante_layout)

        # Criar dois widgets para acomodar os layouts horizontais
        widget_1 = QWidget(self)
        widget_1.setLayout(main_layout_1)

        widget_2 = QWidget(self)
        widget_2.setLayout(main_layout_2)

        widget_3 = QWidget(self)
        widget_3.setLayout(main_layout_3)

        # Adicionar os widgets ao layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(widget_1)
        main_layout.addWidget(widget_2)
        main_layout.addWidget(widget_3)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.apply_pink_theme()

        self.apply_yellow_theme()

        self.apply_orange_theme()

        self.apply_purple_theme()

        self.apply_green_theme()

        self.apply_red_theme()

        self.apply_blue_theme()

        self.apply_dark_theme()

        self.apply_light_theme()

        self.apply_neutral_standart_theme()

        self.change_theme(theme='Tema Neutro Padrão')

    def browse_folder(self):
        folder_dialog = QFileDialog(self, "Selecionar Pastas")
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        folder_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        folder_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        folder_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        folder_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")

        tree_view = folder_dialog.findChild(QTreeView)
        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if folder_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_folders = folder_dialog.selectedFiles()
            self.folder_listbox.addItems(selected_folders)

    def browse_file(self):
        file_dialog = QFileDialog(self, "Selecionar Arquivos")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Todos os Arquivos (*.*)")
        # file_dialog.setNameFilter("Arquivos Compactados (*.rar *.zip *.7z *.tar)")
        file_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        file_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        file_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        file_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        file_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")

        tree_view = file_dialog.findChild(QTreeView)
        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.folder_listbox.addItems(selected_files)

    def clear_folders(self):
        self.folder_listbox.clear()

    def browse_output(self):
        output_dialog = QFileDialog(self, "Selecionar Pasta de Saída")
        output_dialog.setFileMode(QFileDialog.FileMode.Directory)
        output_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        output_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        output_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        output_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        output_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        output_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        output_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")

        tree_view = output_dialog.findChild(QTreeView)
        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if output_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_output = output_dialog.selectedFiles()
            self.output_listbox.addItems(selected_output)
            self.output_listbox_zip.addItems(selected_output)
            self.output_listbox_7z.addItems(selected_output)
            self.output_listbox_tar.addItems(selected_output)
            self.output_listbox_extract.addItems(selected_output)

    def clear_output(self):
        self.output_listbox.clear()
        self.output_listbox_zip.clear()
        self.output_listbox_7z.clear()
        self.output_listbox_tar.clear()
        self.output_listbox_extract.clear()

    def select_output_path(self, output_listbox):
        output_dialog = QFileDialog(self, "Selecionar Pasta de Saída")
        output_dialog.setFileMode(QFileDialog.FileMode.Directory)
        output_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        output_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        output_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        output_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        output_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        output_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        output_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")

        tree_view = output_dialog.findChild(QTreeView)
        if tree_view:
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        if output_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_output = output_dialog.selectedFiles()
            output_listbox.addItems(selected_output)

    def output_button_output_ZIP_clicked(self):
        self.select_output_path(self.output_listbox_zip)

    def output_button_output_7Z_clicked(self):
        self.select_output_path(self.output_listbox_7z)

    def output_button_output_TAR_clicked(self):
        self.select_output_path(self.output_listbox_tar)

    def output_button_output_EXTRACT_clicked(self):
        self.select_output_path(self.output_listbox_extract)

    def select_compression_method(self):
        legends_sevenzip = {
            "0": "0 - Armazena sem compressão",
            "1": "1 - Mais Rápido",
            "3": "3 - Rápido",
            "5": "5 - Normal",
            "7": "7 - Máximo",
            "9": "9 - Ultra"
        }

        compression_menu = QMenu(self)

        sevenzip_submenu = QMenu("7-Zip", self)
        sevenzip_methods = ["0", "1", "3", "5", "7", "9"]
        for method in sevenzip_methods:
            action = QAction(legends_sevenzip[method], self)
            # Para 7z
            action.triggered.connect(
                lambda checked=False, method=method: self.set_compression_method(checked, method, '7z'))
            # Para zip
            action.triggered.connect(
                lambda checked=False, method=method: self.set_compression_method(checked, method, 'zip'))
            # Para tar
            action.triggered.connect(
                lambda checked=False, method=method: self.set_compression_method(checked, method, 'tar'))
            sevenzip_submenu.addAction(action)
        compression_menu.addMenu(sevenzip_submenu)

        self.compression_method_action.setMenu(compression_menu)

    def set_compression_method(self, checked, method, compress_type):
        if compress_type == 'zip':
            self.compression_method_zip = method
        elif compress_type == '7z':
            self.compression_method_7z = method
        elif compress_type == 'tar':
            self.compression_method_tar = method

    def store_as_zip(self):
        if self.compression_method_zip is not None:
            self.compress_thread_zip = CompressaoZIP(
                self.sevenzip_executable, self.output_listbox_zip, self.folder_listbox,
                compress_as_zip=True, compression_method=self.compression_method_zip
            )
            self.compress_thread_zip.finished.connect(self.on_compress_finished)
            self.compress_thread_zip.start()
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def store_as_7z(self):
        if self.compression_method_7z is not None:
            self.compress_thread_7z = Compressao7Z(
                self.sevenzip_executable, self.output_listbox_7z, self.folder_listbox,
                compress_as_7z=True, compression_method=self.compression_method_7z
            )
            self.compress_thread_7z.finished.connect(self.on_compress_finished)
            self.compress_thread_7z.start()
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def store_as_tar(self):
        if self.compression_method_tar is not None:
            self.compress_thread_tar = CompressaoTAR(
                self.sevenzip_executable, self.output_listbox_tar, self.folder_listbox,
                compress_as_tar=True, compression_method=self.compression_method_tar
            )
            self.compress_thread_tar.finished.connect(self.on_compress_finished)
            self.compress_thread_tar.start()
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def testar_integridade(self):
        selected_files = [self.folder_listbox.item(idx).text() for idx in range(self.folder_listbox.count())]
        self.teste_integridade_thread = TesteIntegridadeCentral(self.sevenzip_executable, selected_files)
        self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)
        self.teste_integridade_thread.start()

    def extract_files(self):
        if self.sevenzip_executable:
            self.extract_thread = ExtracaoCentral(
                self.sevenzip_executable, self.output_listbox_extract, self.folder_listbox)
            self.extract_thread.finished.connect(self.on_extract_finished)
            self.extract_thread.start()
        else:
            print("Nenhum programa (WinRAR ou 7-Zip) encontrado para extração.")

    def on_compress_finished(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Empacotamento Concluído")
        msg_box.setText("O Empacotamento dos arquivos foi concluído com sucesso!")
        msg_box.exec()

    def on_teste_integridade_finished(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Teste de Integridade Concluído")
        msg_box.setText("O teste de integridade dos arquivos foi concluído com sucesso!")
        msg_box.exec()

    def on_extract_finished(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Extração Concluída")
        msg_box.setText("A Extração dos arquivos foi concluída com sucesso!")
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = PastaAppEmapacotamento()
    window.show()
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
