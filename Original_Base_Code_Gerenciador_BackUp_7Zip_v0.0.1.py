import os  # Importa o módulo os
import sys  # Importa o módulo sys
import subprocess  # Importa o módulo subprocess
# Importa as classes QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, ...
# QFileDialog, QWidget, QTreeView, QMessageBox, QMenu do módulo QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton,
                             QFileDialog, QWidget, QTreeView, QMessageBox, QMenu)
# Importa as classes Qt, QThread, pyqtSignal do módulo QtCore
from PyQt6.QtCore import Qt, QThread, pyqtSignal
# Importa a classe QAction do módulo QtGui
from PyQt6.QtGui import QAction
# Importa a classe QtGui do módulo PyQt6
from PyQt6 import QtGui


### AS LINHAS DE COMENTÁRIO SEMPRE FARÃO REFERÊNCIA A LINHA DE CÓDIGO QUE AS SUSCEDE, LOGO ABAIXO ###

# Define a função de chamada, que busca o executável. Essa função não recebe nenhum argumento.
def buscar_sevenzip_executavel():
    # Obter o caminho do diretório do executável
    dir_atual = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))

    sevenzip_path = os.path.join(dir_atual, "7-Zip")

    # Construir o caminho para o executável do 7-Zip
    # Ela usa a função os.path.join() para combinar o diretório atual (dir_atual) com o nome do arquivo (7zG.exe).
    caminho_sevenzip = os.path.join(sevenzip_path, '7zG.exe')

    # Verificar se o executável do 7-Zip existe
    if os.path.exists(caminho_sevenzip):
        return caminho_sevenzip

    # Esta linha define uma lista de possíveis localizações para o executável do 7-Zip.
    # Essas localizações são caminhos absolutos para os diretórios onde o 7-Zip pode estar instalado.
    possible_locations = [
        rf"C:\Program Files\7-Zip\7zG.exe",
        rf"C:\Program Files (x86)\7-Zip\7zG.exe",
    ]

    # Esta linha inicia um loop que percorre cada localização na lista possible_locations.
    for location in possible_locations:
        if os.path.isfile(location):
            return location

    # Se o arquivo do executável do 7-Zip não for encontrado em nenhuma das localizações, ...
    # esta linha retorna None, indicando que o executável não foi encontrado.
    return None


# Define uma nova classe chamada class CompressaoZIP(QThread): que herda de QThread, uma classe do PyQt que permite a criação de threads.
class CompressaoZIP(QThread):
    # Define um sinal chamado finished que pode ser emitido quando a thread terminar.
    finished = pyqtSignal()

    # Esta linha define o método especial __init__, que é o construtor da classe.
    # Ele é chamado quando um novo objeto da classe é criado.
    # O construtor recebe vários parâmetros: sevenzip_executable, output_listbox, folder_listbox, compress_as_zip e compression_method.
    def __init__(self, sevenzip_executable, output_listbox, folder_listbox, compress_as_zip=False, compression_method=None):

        # Esta linha chama o construtor da classe pai.
        # Ela garante que o construtor da classe pai seja executado antes do código no construtor da classe atual.
        super().__init__()
        # Esta linha atribui o valor do parâmetro sevenzip_executable ao atributo sevenzip_executable do objeto atual.
        # O atributo self.sevenzip_executable será usado posteriormente no código.
        # O mesmo vale para os outros atributos.
        self.sevenzip_executable = sevenzip_executable
        self.output_listbox = output_listbox
        self.folder_listbox = folder_listbox
        self.compress_as_zip = compress_as_zip
        self.compression_method = compression_method

    # Define o método run, que é chamado quando a thread é iniciada. Este método não recebe argumentos além de self.
    def run(self):
        # Nesta linha, uma lista chamada output_paths é criada.
        # Ela contém os textos de cada item da output_listbox, que é uma caixa de listagem de saída.
        # O loop for percorre os índices de 0 até o número de itens na output_listbox, e o método text() é usado para obter o texto de cada item.
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        # Esta linha verifica se a lista output_paths está vazia. Se estiver vazia, o código retorna imediatamente, interrompendo a execução do método.
        if not output_paths:
            return

        # Aqui, uma lista vazia chamada compressed_files é criada.
        # Essa lista será usada para armazenar os caminhos dos arquivos comprimidos.
        compressed_files = []

        # Este loop for percorre os índices de 0 até o número de itens na folder_listbox, que é outra caixa de listagem.
        for idx in range(self.folder_listbox.count()):
            # Nesta linha, o texto do item da folder_listbox correspondente ao índice atual é obtido e atribuído à variável folder_path.
            # Essa variável representa o caminho da pasta.
            folder_path = self.folder_listbox.item(idx).text()
            # Aqui, o nome da pasta é extraído do caminho completo da pasta usando a função basename do módulo os.
            # O nome da pasta é armazenado na variável folder_name.
            folder_name = os.path.basename(folder_path)

            # Este loop for percorre cada caminho de saída na lista output_paths.
            for output_path in output_paths:
                # Nesta linha, o caminho completo do arquivo comprimido é construído usando a função join do módulo os.
                # O caminho de saída e o nome da pasta são combinados com a extensão .rar para formar o caminho completo do arquivo comprimido.
                # O caminho é armazenado na variável compressed_file_zip.
                compressed_file_zip = os.path.join(output_path, f"{folder_name}.zip")
                # Aqui, uma string command é construída para representar o comando que será executado para comprimir a pasta.
                # O comando inclui o executável do 7-Zip, opções de compressão e os caminhos do arquivo comprimido e da pasta.
                command = f'"{self.sevenzip_executable}" a -r -tzip -mx={self.compression_method} "{compressed_file_zip}" "{folder_path}"'
                # Nesta linha, o comando construído anteriormente é executado usando o módulo subprocess.
                # O parâmetro shell=True indica que o comando deve ser executado em um shell.
                subprocess.run(command, shell=True)
                # Aqui, o caminho do arquivo comprimido é adicionado à lista compressed_files.
                compressed_files.append(compressed_file_zip)

        # Por fim, o sinal finished é emitido.
        # Isso indica que o metodo run foi concluído e pode ser usado para notificar outros componentes ou partes do código sobre o término da execução.
        self.finished.emit()


class Compressao7Z(QThread):
    finished = pyqtSignal()

    def __init__(self, sevenzip_executable, output_listbox, folder_listbox, compress_as_7z=False, compression_method=None):

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

    def __init__(self, sevenzip_executable, output_listbox, folder_listbox, compress_as_tar=False, compression_method=None):

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


# Define uma nova classe chamada TesteIntegridade que herda de QThread, uma classe do PyQt que permite a criação de threads.
class TesteIntegridade(QThread):
    # Define um sinal chamado finished que pode ser emitido quando a thread terminar.
    finished = pyqtSignal()

    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    # Ele recebe três argumentos:
    # self (uma referência ao objeto sendo criado),\;
    # sevenzip_executable (o caminho para o executável do 7zip), e;
    # compressed_files (uma lista de arquivos comprimidos para verificar).
    def __init__(self, sevenzip_executable, compressed_files):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super().__init__()
        # Armazena o caminho para o executável do 7zip no objeto.
        self.sevenzip_executable = sevenzip_executable
        # Armazena a lista de arquivos comprimidos no objeto.
        self.compressed_files = compressed_files

    # Define o método run, que é chamado quando a thread é iniciada. Este método não recebe argumentos além de self.
    def run(self):
        # Inicia um loop que itera sobre cada arquivo na lista de arquivos comprimidos.
        for compressed_file in self.compressed_files:
            # Verifica se o nome do arquivo termina com ".zip", indicando que é um arquivo ZIP.
            if compressed_file.endswith(".zip"):
                # Define o comando que será executado para verificar a integridade do arquivo.
                # O comando usa o executável do 7zip e o nome do arquivo.
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                # Executa o comando definido na linha anterior.
                # O argumento shell=True permite que o comando seja executado em um shell,
                # enquanto check=True faz com que uma exceção seja lançada se o comando falhar.
                result = subprocess.run(command, shell=True, check=True)
                # Verifica se o comando retornou um código de erro (qualquer coisa diferente de 0).
                if result.returncode != 0:
                    # Se o comando retornou um código de erro, ...
                    # uma exceção é lançada com uma mensagem indicando ...
                    # que a verificação da integridade do arquivo falhou.
                    raise Exception("A verificação da integridade do arquivo falhou")

            # Verifica se o nome do arquivo termina com ".7z", indicando que é um arquivo 7z.
            elif compressed_file.endswith(".7z"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

            # Verifica se o nome do arquivo termina com ".tar", indicando que é um arquivo TAR.
            elif compressed_file.endswith(".tar"):
                command = f'"{self.sevenzip_executable}" t "{compressed_file}"'
                result = subprocess.run(command, shell=True, check=True)
                if result.returncode != 0:
                    raise Exception("A verificação da integridade do arquivo falhou")

        # Emite o sinal finished, indicando que a thread terminou.
        self.finished.emit()


# Define uma nova classe chamada Extracao que herda de QThread, uma classe do PyQt que permite a criação de threads.
class Extracao(QThread):
    # Define um sinal chamado finished que pode ser emitido quando a thread terminar.
    finished = pyqtSignal()

    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    # Ele recebe cinco argumentos:
    # self (uma referência ao objeto sendo criado);
    # sevenzip_executable (o caminho para o executável do 7-Zip);
    # output_listbox (um objeto ListBox que contém os caminhos de saída);
    # e folder_listbox (um objeto ListBox que contém os caminhos dos arquivos a serem extraídos).
    def __init__(self, sevenzip_executable, output_listbox, folder_listbox):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super().__init__()
        # Armazena o caminho para o executável do 7zip no objeto.
        self.sevenzip_executable = sevenzip_executable
        # Armazena o objeto ListBox que contém os caminhos de saída no objeto.
        self.output_listbox = output_listbox
        # Armazena o objeto ListBox que contém os caminhos dos arquivos a serem extraídos no objeto.
        self.folder_listbox = folder_listbox

    # Define o método run, que é chamado quando a thread é iniciada. Este método não recebe argumentos além de self.
    def run(self):
        # Cria uma lista de caminhos de saída, obtendo o texto de cada item no ListBox de saída.
        output_paths = [self.output_listbox.item(idx).text() for idx in range(self.output_listbox.count())]
        # Verifica se a lista de caminhos de saída está vazia.
        if not output_paths:
            # Se a lista de caminhos de saída está vazia, o método run é encerrado.
            return

        # Inicia um loop que itera sobre cada item no ListBox de pastas.
        for idx in range(self.folder_listbox.count()):
            # Obtém o caminho do arquivo a ser extraído do item atual no ListBox de pastas.
            archive_path = self.folder_listbox.item(idx).text()
            # Inicia um loop que itera sobre cada caminho de saída na lista de caminhos de saída.
            for output_path in output_paths:
                # Verifica se o nome do arquivo termina com ".zip", indicando que é um arquivo RAR.
                if archive_path.endswith(".zip"):
                    # Define o comando que será executado para extrair o arquivo.
                    # O comando usa o executável do 7-Zip e o nome do arquivo.
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".7z"):
                    # Define o comando que será executado para extrair o arquivo.
                    # O comando usa o executável do 7zip e o nome do arquivo.
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

                elif archive_path.endswith(".tar"):
                    # Define o comando que será executado para extrair o arquivo.
                    # O comando usa o executável do 7zip e o nome do arquivo.
                    command = f'"{self.sevenzip_executable}" x -y "{archive_path}" -o"{output_path}"'
                    # Executa o comando definido na linha anterior.
                    # O argumento shell=True permite que o comando seja executado em um shell.
                    subprocess.run(command, shell=True)

        # Emite o sinal finished, indicando que a thread terminou.
        self.finished.emit()


# Define uma nova classe chamada GerenciadorInterface que herda de QThread, uma classe do PyQt que permite a criação de threads.
class GerenciadorInterface(QThread):
    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    def __init__(self):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super().__init__()

        # Definir variáveis para armazenar o método de compressão selecionado para cada tipo de arquivo.
        self.compression_method_zip = None    # Método de compressão para arquivos ZIP
        self.compression_method_7z = None
        self.compression_method_tar = None

        # Atribuir o caminho do executável do 7zip à variável sevenzip_executable.
        self.sevenzip_executable = buscar_sevenzip_executavel()

        # Verificar se o executável 7zip foi encontrado.
        if not self.sevenzip_executable:
            print("7-Zip não encontrado. Por favor, instale e tente novamente.")
            # Se nenhum dos executáveis for encontrado, o programa é encerrado.
            exit(1)

            # Crie listas separadas para cada tipo de compressão
        self.output_listbox_zip = QListWidget()    # Lista de saída para arquivos ZIP
        self.output_listbox_7z = QListWidget()
        self.output_listbox_tar = QListWidget()
        self.output_listbox = QListWidget()  # Lista de saída para arquivos a serem comprimidos
        self.folder_listbox = QListWidget()  # Lista de entrada para arquivos a serem comprimidos
        self.output_listbox_extract = QListWidget()  # Lista de saída para extração de arquivos
        self.compressed_files = []  # Lista de arquivos comprimidos

        # Esta linha está criando uma nova instância da classe CompressaoZIP, passando três argumentos para o construtor:
        # self.sevenzip_executable (o caminho para o executável do 7-Zip);
        # self.output_listbox (um objeto ListBox que contém os caminhos de saída) e;
        # self.folder_listbox (um objeto ListBox que contém os caminhos dos arquivos a serem comprimidos).
        # A nova instância é armazenada na variável self.compress_thread_zip.
        self.compress_thread_zip = CompressaoZIP(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        # Esta linha está conectando o sinal finished da instância CompressaoZIP ao método self.on_compress_finished.
        # Isso significa que quando o sinal finished for emitido (ou seja, quando a compressão estiver concluída);
        # o método self.on_compress_finished será chamado automaticamente.
        self.compress_thread_zip.finished.connect(self.on_compress_finished)

        self.compress_thread_7z = Compressao7Z(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.compress_thread_7z.finished.connect(self.on_compress_finished)

        self.compress_thread_tar = CompressaoTAR(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.compress_thread_tar.finished.connect(self.on_compress_finished)

        self.teste_integridade_thread = TesteIntegridade(self.sevenzip_executable, self.compressed_files)
        self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)

        self.extract_thread = Extracao(self.sevenzip_executable, self.output_listbox, self.folder_listbox)
        self.extract_thread.finished.connect(self.on_extract_finished)

    # Define um método chamado browse_folder.
    # Este método não recebe argumentos além de self (uma referência ao objeto que o método foi chamado).
    def browse_folder(self):
        # Obtém o objeto pai do objeto atual (geralmente a janela principal da aplicação) e armazena em main_window.
        main_window = self.parent()
        # Cria um novo diálogo de seleção de arquivos com o título "Selecionar Pastas". O diálogo é filho da janela principal.
        folder_dialog = QFileDialog(main_window, "Selecionar Pastas")
        # Define o modo do diálogo para permitir apenas a seleção de diretórios.
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        # Define a opção para mostrar apenas diretórios no diálogo.
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        # Define a opção para tornar o diálogo somente leitura.
        folder_dialog.setOption(QFileDialog.Option.ReadOnly, True)
        # Define a opção para ocultar detalhes do filtro de nome no diálogo.
        folder_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
        # Define a opção para não usar o diálogo nativo do sistema operacional.
        folder_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        # Define a opção para não resolver links simbólicos no diálogo.
        folder_dialog.setOption(QFileDialog.Option.DontResolveSymlinks, True)
        # Define o texto do botão de aceitação do diálogo para "Selecionar".
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Selecionar")
        # Define o texto do botão de rejeição do diálogo para "Cancelar".
        folder_dialog.setLabelText(QFileDialog.DialogLabel.Reject, "Cancelar")

        # Procura por um objeto QTreeView filho do diálogo e armazena em tree_view.
        tree_view = folder_dialog.findChild(QTreeView)
        # Verifica se tree_view não é None (ou seja, se um objeto QTreeView foi encontrado).
        if tree_view:
            # Define o modo de seleção do QTreeView para permitir a seleção de múltiplos itens.
            tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

        # Exibe o diálogo e verifica se o usuário clicou no botão de aceitar.
        if folder_dialog.exec() == QFileDialog.DialogCode.Accepted:
            # Obtém a lista de diretórios selecionados pelo usuário.
            selected_folders = folder_dialog.selectedFiles()
            # Adiciona os diretórios selecionados ao ListBox de pastas.
            self.folder_listbox.addItems(selected_folders)

    def browse_file(self):
        main_window = self.parent()
        file_dialog = QFileDialog(main_window, "Selecionar Arquivos")
        # Define o modo do diálogo para permitir a seleção de arquivos.
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        # Define o filtro de nome do diálogo para "Todos os Arquivos (*.*)".
        file_dialog.setNameFilter("Todos os Arquivos (*.*)")
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
            # Obtém a lista de arquivos selecionados pelo usuário.
            selected_files = file_dialog.selectedFiles()
            # Adiciona os arquivos selecionados ao ListBox de pastas.
            self.folder_listbox.addItems(selected_files)

    # Define um método chamado clear_folders.
    def clear_folders(self):
        # Limpa o conteúdo do ListBox de pastas.
        self.folder_listbox.clear()

    def browse_output(self):
        main_window = self.parent()
        output_dialog = QFileDialog(main_window, "Selecionar Pasta de Saída")
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
            # Obtém a lista de diretórios selecionados pelo usuário.
            selected_output = output_dialog.selectedFiles()
            # Adiciona os diretórios selecionados ao ListBox de saída.
            self.output_listbox.addItems(selected_output)
            # Adiciona os diretórios selecionados aos ListBox de saída para cada tipo de compressão.
            self.output_listbox_zip.addItems(selected_output)
            self.output_listbox_7z.addItems(selected_output)
            self.output_listbox_tar.addItems(selected_output)
            # Adiciona os diretórios selecionados ao ListBox de saída para extração.
            self.output_listbox_extract.addItems(selected_output)

    # Define um método chamado clear_output.
    def clear_output(self):
        # Limpa o conteúdo do ListBox de saída.
        self.output_listbox.clear()
        self.output_listbox_zip.clear()
        self.output_listbox_7z.clear()
        self.output_listbox_tar.clear()
        self.output_listbox_extract.clear()

    # Define um método chamado select_output_path.
    def select_output_path(self, output_listbox):
        main_window = self.parent()
        output_dialog = QFileDialog(main_window, "Selecionar Pasta de Saída")
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
            # Obtém a lista de diretórios selecionados pelo usuário.
            selected_output = output_dialog.selectedFiles()
            # Adiciona os diretórios selecionados ao ListBox de saída correspondente.
            output_listbox.addItems(selected_output)

    # Define um método chamado output_button_output_RAR_clicked.
    def output_button_output_ZIP_clicked(self):
        # Chama o método select_output_path, passando o ListBox de saída correspondente como argumento.
        self.select_output_path(self.output_listbox_zip)

    def output_button_output_7Z_clicked(self):
        self.select_output_path(self.output_listbox_7z)

    def output_button_output_TAR_clicked(self):
        self.select_output_path(self.output_listbox_tar)

    def output_button_output_EXTRACT_clicked(self):
        self.select_output_path(self.output_listbox_extract)

    # Define um método chamado store_as_zip.
    def store_as_zip(self):
        # Verifica se um método de compressão foi selecionado.
        if self.compression_method_zip is not None:
            # Cria uma nova instância da classe CompressaoZIP, passando os argumentos necessários para o construtor.
            self.compress_thread_zip = CompressaoZIP(
                # O caminho para o executável do 7-Zip.
                # O ListBox de saída correspondente.
                # O ListBox de pastas.
                # O valor True para o parâmetro compress_as_zip.
                # O método de compressão selecionado.
                self.sevenzip_executable, self.output_listbox_zip, self.folder_listbox,
                compress_as_zip=True, compression_method=self.compression_method_zip
            )
            # Conecta o sinal finished da instância CompressaoZIP ao método self.on_compress_finished.
            self.compress_thread_zip.finished.connect(self.on_compress_finished)
            # Inicia a thread.
            self.compress_thread_zip.start()
        # Se nenhum método de compressão foi selecionado, exibe uma mensagem de aviso.
        else:
            QMessageBox.warning(self.parent(), "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def store_as_7z(self):
        if self.compression_method_7z is not None:
            self.compress_thread_7z = Compressao7Z(
                self.sevenzip_executable, self.output_listbox_7z, self.folder_listbox,
                compress_as_7z=True, compression_method=self.compression_method_7z
            )
            self.compress_thread_7z.finished.connect(self.on_compress_finished)
            self.compress_thread_7z.start()
        else:
            QMessageBox.warning(self.parent(), "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def store_as_tar(self):
        if self.compression_method_tar is not None:
            self.compress_thread_tar = CompressaoTAR(
                self.sevenzip_executable, self.output_listbox_tar, self.folder_listbox,
                compress_as_tar=True, compression_method=self.compression_method_tar
            )
            self.compress_thread_tar.finished.connect(self.on_compress_finished)
            self.compress_thread_tar.start()
        else:
            QMessageBox.warning(self.parent(), "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    # Define um método chamado testar_integridade.
    def testar_integridade(self):
        # Obtém a lista de arquivos selecionados pelo usuário.
        selected_files = [self.folder_listbox.item(idx).text() for idx in range(self.folder_listbox.count())]
        # Verifica se a lista de arquivos selecionados não está vazia.
        if self.sevenzip_executable and selected_files:
            # Cria uma nova instância da classe TesteIntegridade, passando os argumentos necessários para o construtor.
            self.teste_integridade_thread = TesteIntegridade(self.sevenzip_executable, selected_files)
            # Conecta o sinal finished da instância TesteIntegridade ao método self.on_teste_integridade_finished.
            self.teste_integridade_thread.finished.connect(self.on_teste_integridade_finished)
            # Inicia a thread.
            self.teste_integridade_thread.start()
        # Se a lista de arquivos selecionados estiver vazia, exibe uma mensagem de aviso.
        else:
            QMessageBox.warning(self.parent(), "Aviso", "Por favor, selecione um arquivo para testar a integridade.")

    # Define um método chamado extract_files.
    def extract_files(self):
        # Verifica se o executável do 7zip foi encontrado.
        if self.sevenzip_executable:
            # Cria uma nova instância da classe Extracao, passando os argumentos necessários para o construtor.
            self.extract_thread = Extracao(
                self.sevenzip_executable, self.output_listbox_extract, self.folder_listbox
            )
            # Conecta o sinal finished da instância Extracao ao método self.on_extract_finished.
            self.extract_thread.finished.connect(self.on_extract_finished)
            # Inicia a thread.
            self.extract_thread.start()
        # Se nenhum dos programas for encontrado, exibe uma mensagem de aviso.
        else:
            QMessageBox.warning(self.parent(), "Aviso", "7-Zip não encontrado. Por favor, instale e tente novamente.")

    # Define um método chamado on_compress_finished.
    def on_compress_finished(self):
        # Cria uma nova instância da classe QMessageBox.
        msg_box = QMessageBox()
        # Define o ícone da caixa de mensagem como um ícone de informação.
        msg_box.setIcon(QMessageBox.Icon.Information)
        # Define o título da caixa de mensagem como "Empacotamento Concluído".
        msg_box.setWindowTitle("Empacotamento Concluído")
        # Define o texto da caixa de mensagem como "O Empacotamento dos arquivos foi concluído com sucesso!".
        msg_box.setText("O Empacotamento dos arquivos foi concluído com sucesso!")
        # Exibe a caixa de mensagem.
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


# Define uma nova classe chamada InterfaceGrafica que herda de QMainWindow, uma classe do PyQt que representa uma janela.
class InterfaceGrafica(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cria o gerenciador de interface
        self.gerenciador_interface = GerenciadorInterface()

        # Cria a barra de menus
        self.menu_bar = self.menuBar()

        # Cria a barra de menus
        self.settings_menu = self.menuBar().addMenu('Configurações')
        # Adicionar ação para selecionar método de compressão
        self.compression_method_action = QAction('Selecionar Método de Compressão', self)
        # Conectar a ação a um método
        self.compression_method_action.triggered.connect(self.select_compression_method)
        # Adicionar a ação ao menu
        self.settings_menu.addAction(self.compression_method_action)
        # Adiciona evento de entrada e saída para ativar o menu
        self.settings_menu.aboutToShow.connect(self.select_compression_method)

        # Cria o menu de temas
        self.themes_menu = QMenu('Temas', self)
        # Adiciona o menu de temas ao menu de configurações
        self.settings_menu.addMenu(self.themes_menu)

        # Define um dicionário de ações de tema
        self.theme_actions = {
            'Tema Neutro Padrão': self.apply_neutral_standart_theme,
            'Tema Claro': self.apply_light_theme,
            'Tema Escuro': self.apply_dark_theme,
            'Tema Azul': self.apply_blue_theme,
            'Tema Vermelho': self.apply_red_theme,
            'Tema Verde': self.apply_green_theme,
            'Tema Roxo': self.apply_purple_theme,
            'Tema Laranja': self.apply_orange_theme,
            'Tema Amarelo': self.apply_yellow_theme,
            'Tema Rosa': self.apply_pink_theme
        }

        # Adiciona ação para cada tema
        for theme_name, theme_method in self.theme_actions.items():
            theme_action = QAction(theme_name, self)
            theme_action.triggered.connect(theme_method)
            theme_action.triggered.connect(lambda checked, name=theme_name: self.change_theme(name))
            self.themes_menu.addAction(theme_action)

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
        compression_menu.setStyleSheet(self.themes_menu.styleSheet())

        # Adicione submenus para cada método de compressão do 7-Zip
        zip_submenu = QMenu('ZIP (0-9)', self)
        zip_submenu.setStyleSheet(self.themes_menu.styleSheet())
        zip_methods = ["0", "1", "3", "5", "7", "9"]

        # Adicione submenus para cada método de compressão do 7-Zip
        seven_submenu = QMenu('7Z (0-9)', self)
        seven_submenu.setStyleSheet(self.themes_menu.styleSheet())
        seven_methods = ["0", "1", "3", "5", "7", "9"]

        # Adicione submenus para cada método de compressão do 7-Zip
        tar_submenu = QMenu('TAR (0)', self)
        tar_submenu.setStyleSheet(self.themes_menu.styleSheet())
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
            # Define o método de compressão para arquivos RAR
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

        # Define o título da janela
        self.setWindowTitle("Gerenciador de BackUp")
        # Esta linha está definindo o caminho completo para o arquivo de ícone "Manager-BackUp.ico", que está localizado na pasta "icones".
        icon_title_path = os.path.join(icon_path, "Manager-BackUp.ico")
        # Esta linha está definindo o ícone da janela para o ícone especificado pelo caminho icon_title_path.
        # O método setWindowIcon é um método de um objeto de janela PyQt, e QtGui.QIcon é uma classe que encapsula um ícone.
        self.setWindowIcon(QtGui.QIcon(icon_title_path))

        ### Primeiro layout horizontal ###
        main_layout_1 = QHBoxLayout()

        # Primeiro quadrante (topo esquerdo)
        primeiro_quadrante_layout = QVBoxLayout()

        folder_button = QPushButton("Adicionar Pastas")
        folder_button.clicked.connect(self.gerenciador_interface.browse_folder)
        primeiro_quadrante_layout.addWidget(folder_button)
        file_button = QPushButton("Adicionar Arquivos")
        file_button.clicked.connect(self.gerenciador_interface.browse_file)
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

        # Segundo + Terceiro quadrante (topo centro e direito)
        segundo_quadrante_layout = QVBoxLayout()

        folder_label = QLabel("Diretório(s) Pastas e Arquivos:")
        segundo_quadrante_layout.addWidget(folder_label)
        self.gerenciador_interface.folder_listbox = QListWidget()
        segundo_quadrante_layout.addWidget(self.gerenciador_interface.folder_listbox)
        main_layout_1.addLayout(segundo_quadrante_layout)

        ### Segundo layout horizontal ###
        main_layout_2 = QHBoxLayout()

        # Quarto quadrante (centro esquerdo)
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

        # Quinto quadrante (centro centro)
        quinto_quadrante_layout = QVBoxLayout()

        output_label_zip = QLabel("Diretório(s) de saída .ZIP:")
        quinto_quadrante_layout.addWidget(output_label_zip)
        self.gerenciador_interface.output_listbox_zip = QListWidget()
        quinto_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_zip)
        main_layout_2.addLayout(quinto_quadrante_layout)

        # Sexto quadrante (centro direito)
        sexto_quadrante_layout = QVBoxLayout()

        output_label_7z = QLabel("Diretório(s) de saída .7Z:")
        sexto_quadrante_layout.addWidget(output_label_7z)
        self.gerenciador_interface.output_listbox_7z = QListWidget()
        sexto_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_7z)
        main_layout_2.addLayout(sexto_quadrante_layout)

        ### Terceiro layout horizontal ###
        main_layout_3 = QHBoxLayout()

        # Sétimo quadrante (inferior esquerdo)
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

        # Oitavo quadrante (inferior centro)
        oitavo_quadrante_layout = QVBoxLayout()

        output_label_tar = QLabel("Diretório(s) de saída .TAR:")
        oitavo_quadrante_layout.addWidget(output_label_tar)
        self.gerenciador_interface.output_listbox_tar = QListWidget()
        oitavo_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_tar)
        main_layout_3.addLayout(oitavo_quadrante_layout)

        # Nono quadrante (inferior direito)
        nono_quadrante_layout = QVBoxLayout()

        output_label_extract = QLabel("Diretório(s) para Extração:")
        nono_quadrante_layout.addWidget(output_label_extract)
        self.gerenciador_interface.output_listbox_extract = QListWidget()
        nono_quadrante_layout.addWidget(self.gerenciador_interface.output_listbox_extract)
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

        # O método self.apply_pink_theme() é uma chamada de função em Python.
        # self é uma referência à instância atual da classe e apply_pink_theme é presumivelmente um método definido dentro dessa classe.
        # Este método, como o nome sugere, provavelmente aplica um tema rosa à interface do usuário atual.
        # No entanto, sem ver a implementação do método apply_pink_theme, não posso fornecer detalhes específicos sobre o que exatamente ele faz.
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

        self.apply_neutral_standart_theme()

        # O método self.change_theme(theme='Tema Neutro Padrão') é uma chamada de função em Python.
        # self é uma referência à instância atual da classe e change_theme é presumivelmente um método definido dentro dessa classe.
        # O método change_theme recebe um argumento nomeado theme, que neste caso é definido como 'Tema Neutro Padrão'.
        # Isso sugere que o método change_theme é usado para alterar o tema da interface do usuário para o tema especificado.
        self.change_theme(theme='Tema Neutro Padrão')

    # O método change_theme(self, theme) é usado para alterar o tema da interface do usuário de um aplicativo PyQt.
    # Aqui está uma descrição detalhada:
    # Este é o início da definição do método.
    # Ele recebe um argumento, theme, que é o nome do tema que você deseja aplicar.
    def change_theme(self, theme):
        # Esta linha verifica se o tema passado como argumento é 'Tema Neutro Padrão'.
        # Se for, ele executa o bloco de código a seguir.
        if theme == 'Tema Neutro Padrão':
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
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected {3 
                    background-color: #90c8f6; 
                }
                QMenuBar::item:hover { 
                    background-color: #000000; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #90c8f6;
                }
                QMenu::item:hover {
                    background-color: #000000;
                }
            """)

        elif theme == 'Tema Claro':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #b3b3b3; 
                }
                QMenuBar::item:hover { 
                    background-color: #333333; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #b3b3b3;
                }
                QMenu::item:hover {
                    background-color: #333333;
                }
            """)

        elif theme == 'Tema Escuro':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #333333; 
                }
                QMenuBar::item:hover { 
                    background-color: #b3b3b3; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #333333;
                }
                QMenu::item:hover {
                    background-color: #b3b3b3;
                }
            """)

        elif theme == 'Tema Azul':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #b3d1ff; 
                }
                QMenuBar::item:hover { 
                    background-color: #1a3348; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #b3d1ff;
                }
                QMenu::item:hover {
                    background-color: #1a3348;
                }
            """)

        elif theme == 'Tema Vermelho':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #ff9999; 
                }
                QMenuBar::item:hover { 
                    background-color: #4d1a1a; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #ff9999;
                }
                QMenu::item:hover {
                    background-color: #4d1a1a;
                }
            """)

        elif theme == 'Tema Verde':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #99ffcc; 
                }
                QMenuBar::item:hover { 
                    background-color: #1a4d33; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #99ffcc;
                }
                QMenu::item:hover {
                    background-color: #1a4d33;
                }
            """)

        elif theme == 'Tema Roxo':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #b399ff; 
                }
                QMenuBar::item:hover { 
                    background-color: #331a4d; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #b399ff;
                }
                QMenu::item:hover {
                    background-color: #331a4d;
                }
            """)

        elif theme == 'Tema Laranja':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #ffcc99; 
                }
                QMenuBar::item:hover { 
                    background-color: #993d00; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #ffcc99;
                }
                QMenu::item:hover {
                    background-color: #993d00;
                }
            """)

        elif theme == 'Tema Amarelo':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #ffffcc; 
                }
                QMenuBar::item:hover { 
                    background-color: #99993d; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected {
                    background-color: #ffffcc;
                }
                QMenu::item:hover {
                    background-color: #99993d;
                }
            """)

        elif theme == 'Tema Rosa':
            self.menu_bar.setStyleSheet("""
                QMenuBar::item:selected { 
                    background-color: #ffccf2; 
                }
                QMenuBar::item:hover { 
                    background-color: #993d7a; 
                }
            """)
            self.themes_menu.setStyleSheet("""
                QMenu::item:selected { 
                    background-color: #ffccf2; 
                }
                QMenu::item:hover { 
                    background-color: #993d7a; 
                }
            """)

        self.settings_menu.setStyleSheet(self.themes_menu.styleSheet())

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
