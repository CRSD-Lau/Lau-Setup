<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **Versão atual: Setup 1.4.0 / jogo 3.0.9 Lau.** Feche o WoW, extraia todo o LauSetup.zip, abra LauSetup.exe no Windows e use Browse... para escolher a pasta que contém WoW.exe. Avançar → opções visuais → Avançar → revisar → instalar → concluir. Todos os extras começam desativados. WoW.exe e telas de carregamento são uma opção conjunta; os mapas são independentes e incluem arquivos WDM. Mapas já instalados são mantidos. Patches duplicados renomeados permanecem; apenas um Patch-V vazio é salvo automaticamente. Arquivos substituídos são salvos em LauSetupBackups. Nenhum DBC do Patch-Y foi alterado; os mapas opcionais adicionam tabelas originais documentadas. Mapas de cavernas continuam em beta. Linux/Wine usa LauSetup.sh com os requisitos documentados. O erro Google HTTP 429 impede atualizar a tradução completa. O texto antigo abaixo é apenas referência histórica; consulte a fonte em inglês para as instruções atuais.
>
> [English](../../../../wine/README.txt) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../../wine/README.txt). Se o texto for diferente, a fonte em inglês é oficial.

Lau Setup para Wine em Linux
Author / Creator / Last Modified By: Neil Mitchell

1. Use um cliente WoW 3.3.5a 12340 existente em um sistema de arquivos Linux local.
2. Feche todas as instâncias WoW, incluindo jogos em outros prefixos Wine.
3. Extraia `LauSetup.zip`. Mantenha juntos os cinco arquivos de `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` e `README.txt`.
4. Abra um terminal na pasta extraída e execute:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5. Escolha a pasta do jogo existente e instale. Os backups automáticos habituais
   e o botão Restaurar instalação anterior estão disponíveis.

Requisitos para esta versão:
- Wine 11.0, um prefixo 64-bit, e Wine Mono 10.4.1 já instalado lá.
- Python 3.9 ou mais recente para o auxiliar de segurança do host (somente biblioteca padrão).
- Fontes Liberation Sans ou DejaVu Sans; o pacote completo de fontes Wine deve
  também ser instalado para que os próprios controles padrão do Wine Mono possam ser renderizados.
- Armazenamento local Linux. Compartilhamentos de rede e unidades montadas em Windows são excluídos.
- Visibilidade normal do processo host. Não execute este iniciador em uma sandbox
  que oculta outros processos Wine. Execute como seu usuário normal, nunca sudo/root.

O prefixo 64-bit pode conter o cliente 32-bit WoW. Este instalador não
crie, converta ou atualize seu prefixo Wine, instale Wine/Mono, configure
DXVK ou altere o inicializador do jogo. Use a configuração Wine da sua distribuição
instruções primeiro se seu tempo de execução estiver faltando.

Pacote oficial Wine Mono para este tempo de execução testado:
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

Use o tempo de execução Wine Mono com Wine. O instalador do .NET Framework Windows é
não é empacotado e não é exigido por esta configuração Wine Mono testada.

Sempre inicie por meio de LauSetup.sh. Executando LauSetup.exe diretamente em Wine
recusará operações do cliente sem o auxiliar Linux. Ele verifica caminhos de host
e processa e mantém um bloqueio de host compartilhado entre prefixos Wine. Se parar,
reabra o inicializador e restaure a instalação pendente antes de tentar novamente.

Mantenha WoW fechado até a configuração terminar. As verificações de processo reduzem corridas; eles não podem
impedir que outro programa inicie o jogo ou altere arquivos posteriormente.
Caminhos com links simbólicos, hardlinks e maiúsculas e minúsculas de nomes de arquivos ambíguos são rejeitados. Dados
e os diretórios de backup devem permanecer no mesmo sistema de arquivos que o cliente.

Escopo de validação: isolado Wine 11.0 / Wine Mono 10.4.1 clientes, equipamentos e
testes de instalação/restauração de carga útil real, testes de segurança de dois prefixos e amostra de GUI
verificações. Esta não é uma certificação de todos Linux distribuição, sistema de arquivos,
escala de exibição, Wine versão ou encontro de jogo. Sem Lutris, Proton ou macOS
a integração está incluída nesta versão.

A interface do instalador segue automaticamente o idioma do sistema entre dez opções; a escolha manual é salva. Os dados do jogo do cliente continuam a oferecer suporte a nove localidades e seguem a localidade detectada do jogo.

Configuração 1.1.7: Novo visual de feitiço desativado mantém Patch-S como .mpq.disabled próximo a
seu caminho original. Uma cópia desativada diferente nunca é substituída.
Para desfazer a instalação completa, use Restaurar instalação anterior. Para arquivos
já removidos por versões de configuração mais antigas, recupere-os desses backups
usando Restaurar instalação anterior antes de reinstalar. Mantenha LauSetupBackups.

O arquivo S atual sempre se torna .mpq.disabled. Se um idoso deficiente
cópia existir, a Instalação primeiro a preservará como `.mpq.disabled.<12-character hash>`. Sem renomeação manual
é necessário para mudar as opções. A reativação manual requer a remoção
.disabled e qualquer hash seguinte, com WoW fechado e nenhum ativo diferente
arquivo sendo sobrescrito. Use Restaurar instalação anterior para reversão gerenciada.

1.1.7 reativar limpeza: correspondência desativada Patch-S é reutilizada localmente. A cópia simples desativada é movida para o backup da transação verificada em LauSetupBackups, deixando um S ativo. Cópias diferentes permanecem recuperáveis ​​por meio da Restauração da instalação anterior. Os arquivos existentes com sufixo hash não são varridos.
