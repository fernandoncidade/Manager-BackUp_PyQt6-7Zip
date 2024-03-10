# Importa as classes QListWidget, QFileDialog, QWidget, QTreeView, QMessageBox do módulo QtWidgets
from PyQt6.QtWidgets import (QListWidget, QFileDialog, QWidget, QTreeView, QMessageBox)
# Importa a classe QThread do módulo QtCore
from PyQt6.QtCore import QThread
# Importa as classes CompressaoZIP, Compressao7Z, CompressaoTAR, TesteIntegridade, Extracao do módulo CompressionMotors_7Zip
from CompressionMotors_7Zip import (buscar_sevenzip_executavel, CompressaoZIP, Compressao7Z, CompressaoTAR, TesteIntegridade, Extracao)


# Define uma nova classe chamada GerenciadorInterface que herda de QThread, uma classe do PyQt que permite a criação de threads.
class GerenciadorInterface(QThread):
    # Define o método inicializador da classe, que é chamado quando um objeto da classe é criado.
    def __init__(self, main_window):
        # Chama o método inicializador da classe pai (QThread), que é necessário para a correta inicialização da thread.
        super().__init__()
        self.main_window = main_window

            # Definir variáveis para armazenar o método de compressão selecionado para cada tipo de arquivo.
        self.compression_method_rar = None # Método de compressão para arquivos RAR
        self.compression_method_zip = None
        self.compression_method_7z = None
        self.compression_method_tar = None

        # Atribuir o caminho do executável do 7zip à variável sevenzip_executable.
        self.sevenzip_executable = buscar_sevenzip_executavel()

        # Verificar se o executável do WinRAR ou do 7zip foi encontrado.
        if not self.sevenzip_executable:
            print("WinRAR não encontrado. Por favor, instale e tente novamente.")
            # Se nenhum dos executáveis for encontrado, o programa é encerrado.
            exit(1)

            # Crie listas separadas para cada tipo de compressão
        self.output_listbox_zip = QListWidget() # Lista de saída para arquivos ZIP
        self.output_listbox_7z = QListWidget()
        self.output_listbox_tar = QListWidget()
        self.output_listbox = QListWidget() # Lista de saída para arquivos a serem comprimidos
        self.folder_listbox = QListWidget() # Lista de entrada para arquivos a serem comprimidos
        self.output_listbox_extract = QListWidget() # Lista de saída para extração de arquivos
        self.compressed_files = [] # Lista de arquivos comprimidos

        # Esta linha está criando uma nova instância da classe CompressaoZIP, passando três argumentos para o construtor:
        # self.sevenzip_executable (o caminho para o executável do 7zip);
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
    def browse_folder(self, main_window):
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

    def browse_file(self, main_window):
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

    def browse_output(self, main_window):
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
    def select_output_path(self, output_listbox, main_window):
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

    # Define um método chamado output_button_output_ZIP_clicked.
    def output_button_output_ZIP_clicked(self):
        # Chama o método select_output_path, passando o ListBox de saída correspondente como argumento.
        self.select_output_path(self.output_listbox_zip, self.main_window)

    def output_button_output_7Z_clicked(self):
        self.select_output_path(self.output_listbox_7z, self.main_window)

    def output_button_output_TAR_clicked(self):
        self.select_output_path(self.output_listbox_tar, self.main_window)

    def output_button_output_EXTRACT_clicked(self):
        self.select_output_path(self.output_listbox_extract, self.main_window)

    # Define um método chamado store_as_zip.
    def store_as_zip(self):
        # Verifica se um método de compressão foi selecionado.
        if self.compression_method_zip is not None:
            # Cria uma nova instância da classe CompressaoZIP, passando os argumentos necessários para o construtor.
            self.compress_thread_zip = CompressaoZIP(
                # O caminho para o executável do 7zip.
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
            # Obtém a janela pai do objeto atual.
            parent = self.parent()
            # Verifica se a janela pai é um objeto QWidget.
            if isinstance(parent, QWidget):
                # Se a janela pai for um objeto QWidget, exibe uma mensagem de aviso.
                QMessageBox.warning(parent, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")
            else:
                # Se a janela pai não for um objeto QWidget, exibe uma mensagem de aviso.
                QMessageBox.warning(None, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def store_as_7z(self):
        if self.compression_method_7z is not None:
            self.compress_thread_7z = Compressao7Z(
                self.sevenzip_executable, self.output_listbox_7z, self.folder_listbox,
                compress_as_7z=True, compression_method=self.compression_method_7z
            )
            self.compress_thread_7z.finished.connect(self.on_compress_finished)
            self.compress_thread_7z.start()
        else:
            # Obtém a janela pai do objeto atual.
            parent = self.parent()
            # Verifica se a janela pai é um objeto QWidget.
            if isinstance(parent, QWidget):
                # Se a janela pai for um objeto QWidget, exibe uma mensagem de aviso.
                QMessageBox.warning(parent, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")
            else:
                # Se a janela pai não for um objeto QWidget, exibe uma mensagem de aviso.
                QMessageBox.warning(None, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    def store_as_tar(self):
        if self.compression_method_tar is not None:
            self.compress_thread_tar = CompressaoTAR(
                self.sevenzip_executable, self.output_listbox_tar, self.folder_listbox,
                compress_as_tar=True, compression_method=self.compression_method_tar
            )
            self.compress_thread_tar.finished.connect(self.on_compress_finished)
            self.compress_thread_tar.start()
        else:
            # Obtém a janela pai do objeto atual.
            parent = self.parent()
            # Verifica se a janela pai é um objeto QWidget.
            if isinstance(parent, QWidget):
                # Se a janela pai for um objeto QWidget, exibe uma mensagem de aviso.
                QMessageBox.warning(parent, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")
            else:
                # Se a janela pai não for um objeto QWidget, exibe uma mensagem de aviso.
                QMessageBox.warning(None, "Aviso", "Por favor, selecione um método de compressão antes de prosseguir.")

    # Define um método chamado testar_integridade.
    def testar_integridade(self):
        # Obtém a lista de arquivos selecionados pelo usuário.
        selected_files = []
        for idx in range(self.folder_listbox.count()):
            item = self.folder_listbox.item(idx)
            if item is not None:
                selected_files.append(item.text())
        
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
            parent = self.parent()
            if isinstance(parent, QWidget):
                QMessageBox.warning(parent, "Aviso", "Por favor, selecione um arquivo para testar a integridade.")
            else:
                QMessageBox.warning(None, "Aviso", "Por favor, selecione um arquivo para testar a integridade.")

    # Define um método chamado extract_files.
    def extract_files(self):
        # Verifica se o executável do 7zip foi encontrado.
        if self.sevenzip_executable:
            # Cria uma nova instância da classe Extracao, passando os argumentos necessários para o construtor.
            self.extract_thread = Extracao(
                self.sevenzip_executable, self.winrar_executable,
                self.output_listbox_extract, self.folder_listbox
            )
            # Conecta o sinal finished da instância Extracao ao método self.on_extract_finished.
            self.extract_thread.finished.connect(self.on_extract_finished)
            # Inicia a thread.
            self.extract_thread.start()
        # Se nenhum dos programas for encontrado, exibe uma mensagem de aviso.
        else:
            parent = self.parent()
            if isinstance(parent, QWidget):
                QMessageBox.warning(parent, "Aviso", "Nenhum dos programas (WinRAR ou 7-Zip) encontrado. Por favor, instale um deles e tente novamente.")
            else:
                QMessageBox.warning(None, "Aviso", "Nenhum dos programas (WinRAR ou 7-Zip) encontrado. Por favor, instale um deles e tente novamente.")

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
