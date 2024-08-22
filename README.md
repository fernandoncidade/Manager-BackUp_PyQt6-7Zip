# Manager-BackUp_PyQt6-7Zip
# Gerenciador de Backup

Este projeto é uma aplicação de interface gráfica (GUI) desenvolvida em Python utilizando a biblioteca **PyQt6**. A aplicação foi projetada para facilitar a gestão de backups de arquivos e diretórios, oferecendo funcionalidades como compressão e extração de arquivos em diversos formatos, como .ZIP, .7Z e .TAR.

## Funcionalidades

- **Adicionar Pastas/Arquivos**: Permite ao usuário selecionar e adicionar pastas e arquivos à lista de backup.
- **Especificar Diretório(s) de Extração**: Define o diretório de destino onde os arquivos serão extraídos.
- **Extrair Arquivos e Pastas**: Extrai arquivos e pastas para o diretório especificado.
- **Testar Integridade**: Verifica a integridade dos arquivos selecionados.
- **Armazenar como .ZIP, .7Z, .TAR**: Comprime os arquivos selecionados nos formatos mencionados.
- **Especificar Diretório(s) de Saída**: Define o diretório onde os arquivos comprimidos serão salvos.
- **Limpar Entrada/Saída**: Limpa as listas de arquivos e diretórios de entrada ou saída.

## Estrutura do Projeto

- **ManagerInterface.py**: Contém a classe `GerenciadorInterface`, responsável por gerenciar as operações relacionadas à interface do usuário, como navegação de arquivos, execução de compressão e extração, e manipulação de eventos da GUI.
- **CompressionMethod.py**: Define a classe `MetodoCompressao`, que implementa os métodos de compressão para os diferentes formatos de arquivos suportados (.ZIP, .7Z, .TAR).
- **Colors.py**: Fornece a função `apply_neutral_standart_theme`, que aplica um tema padrão neutro à aplicação, garantindo uma aparência consistente e agradável.

## Requisitos

- **Python 3.x**
- **PyQt6**
- Outros módulos necessários estão listados no arquivo `requirements.txt` (se aplicável).

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/fernandoncidade/Manager-BackUp_PyQt6-7Zip
   cd Manager-BackUp_PyQt6-7Zip
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python Gerenciador_BackUp_7Zip_Standart_v3.py
   ```

## Uso

Após a instalação, ao executar o programa, uma janela gráfica será exibida, permitindo ao usuário interagir com as diversas funcionalidades do gerenciador de backup.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

INFORMAÇÕES EXTRAS SOBRE A LICENÇA:

  7-Zip
  ~~~~~
  License for use and distribution
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  7-Zip Copyright (C) 1999-2023 Igor Pavlov.

  The licenses for files are:

    1) 7z.dll:
         - The "GNU LGPL" as main license for most of the code
         - The "GNU LGPL" with "unRAR license restriction" for some code
         - The "BSD 3-clause License" for some code
    2) All other files: the "GNU LGPL".

  Redistributions in binary form must reproduce related license information from this file.

  Note:
    You can use 7-Zip on any computer, including a computer in a commercial
    organization. You don't need to register or pay for 7-Zip.


  GNU LGPL information
  --------------------

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You can receive a copy of the GNU Lesser General Public License from
    http://www.gnu.org/




  BSD 3-clause License
  --------------------

    The "BSD 3-clause License" is used for the code in 7z.dll that implements LZFSE data decompression.
    That code was derived from the code in the "LZFSE compression library" developed by Apple Inc,
    that also uses the "BSD 3-clause License":

    ----
    Copyright (c) 2015-2016, Apple Inc. All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

    2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer
        in the documentation and/or other materials provided with the distribution.

    3.  Neither the name of the copyright holder(s) nor the names of any contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ----




  unRAR license restriction
  -------------------------

    The decompression engine for RAR archives was developed using source
    code of unRAR program.
    All copyrights to original unRAR code are owned by Alexander Roshal.

    The license for original unRAR code has the following restriction:

      The unRAR sources cannot be used to re-create the RAR compression algorithm,
      which is proprietary. Distribution of modified unRAR sources in separate form
      or as a part of other software is permitted, provided that it is clearly
      stated in the documentation and source comments that the code may
      not be used to develop a RAR (WinRAR) compatible archiver.


  --
  Igor Pavlov
