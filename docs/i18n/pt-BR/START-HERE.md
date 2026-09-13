<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Um único ZIP agora contém o instalador do Windows e o iniciador para Linux/Wine. A interface segue automaticamente o idioma do sistema operacional entre dez opções; a escolha manual é salva. A versão 3.0.8 e os arquivos do jogo não mudam. Não há alterações de DBC.
>
> A atualização completa dos guias continua pendente devido a um HTTP 429 do Google. O texto abaixo pode estar desatualizado; consulte a fonte atual em inglês e as notas da versão 1.3.0. [English](../../../START-HERE.txt) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Download atual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows e Linux/Wine. Extraia a pasta `LauSetup/` com cinco arquivos: no Windows, abra `LauSetup.exe`; no Linux/Wine, execute `LauSetup.sh`. As instruções antigas abaixo sobre EXE ou ZIP Wine separados não se aplicam à versão 1.3.0.
>
> **1.3.0:** Os arquivos extras de melhoria reconhecidos são salvos em backup e a instalação continua. A restauração os devolve. Não é preciso movê-los manualmente. O Setup preserva automaticamente os arquivos existentes antes de substituí-los ou movê-los. Os arquivos não relacionados permanecem intactos.


<!-- BEGINNER-120-STEPS -->
## Primeiros passos

1. Feche o WoW completamente.
2. Baixe apenas `LauSetup.zip`; no Windows, clique com o botão direito, **Extrair tudo**, abra `LauSetup` e clique duas vezes em `LauSetup.exe`.
3. Use **Escolher pasta…** e escolha a pasta que contém `WoW.exe`, não `Data`.
4. **Idioma da interface** muda apenas o texto do Setup; Automático segue o sistema e não muda os nove idiomas do jogo.
5. **Consagração aprimorada** vem ativada; efeitos exigem modelos HD compatíveis e mapas são opcionais.
6. Use **Instalar atualização**, espere sem fechar o Setup; abra WoW e digite `/pyversion`. Para restaurar, feche WoW, escolha a mesma pasta e use **Restaurar instalação anterior**.

### Linux/Wine

Use o mesmo ZIP somente com prefixo Wine 64-bit existente, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, fontes documentadas e armazenamento Linux local. Extraia e execute `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`; nunca execute o EXE diretamente no Wine.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../START-HERE.txt). Se o texto for diferente, a fonte em inglês é oficial.

CONFIGURAÇÃO LAU - LIBERAÇÃO 3.0.8

Windows e Linux/Wine: baixe `LauSetup.zip` e extraia `LauSetup/`. No Windows, abra `LauSetup/LauSetup.exe`; no Linux/Wine, execute `LauSetup/LauSetup.sh`.
Para Wine, use o inicializador Linux incluído. Não execute o EXE diretamente.

1. Feche World of Warcraft.
2. Abra LauSetup.exe e escolha sua pasta WoW.
3. Escolha seus recursos visuais e clique em Instalar atualização.

Atualizando de uma versão mais antiga ou de teste v2? Baixe primeiro o novo instalador; cópias antigas incorporam o catálogo antigo.
Selecione o mesmo cliente e recursos visuais. As verificações de hash de arquivo detectam os patches alterados.
Inicie WoW e digite /pyversion; deve relatar 3.0.8 Lau.

O instalador detecta o idioma do cliente e a configuração do modelo HD.
Consagração Aprimorada é selecionada por padrão. Desmarque para o estoque
aparência; o feitiço em si ainda funciona. Novos visuais de feitiços exigem um
cliente de modelo HD compatível existente. Mapas/minimapas atualizados são opcionais.

Você precisa de um cliente WoW 3.3.5a existente, build 12340, em Windows 10 ou 11.
Este download é uma atualização, não um cliente completo ou pacote de idiomas.
O WoW.exe compatível necessário é instalado automaticamente.

Nenhuma cópia ou renomeação manual de patches é necessária. Não baixe o inteiro
liberação de dados compartilhada. O aplicativo baixa apenas os arquivos necessários para sua seleção.

Backups e downloads recuperáveis permanecem em LauSetupBackups dentro de seu WoW
pasta, fora de Data. Para desfazer a atualização, feche WoW, reabra LauSetup.exe,
escolha a mesma pasta e clique em Restaurar instalação anterior. Recuperação também
funciona se uma atualização interrompida deixou WoW.exe temporariamente ausente.

Seus complementos, SavedVariables, fontes, arte de login, configurações de domínio e
patches não relacionados são preservados. Sem marca Pizza Warriors, pessoal
Configuração ElvUI, LoginUI, dados da conta ou cliente de jogo completo estão incluídos.

Os downloads vêm das versões GitHub; nenhuma conta GitHub é necessária.
Se um download for interrompido, tente novamente mais tarde. Arquivos verificados
são reutilizados e os downloads parciais são retomados. Os arquivos do jogo são alterados somente após
todos os downloads necessários passaram na verificação. Mantenha LauSetupBackups se
o aplicativo informa que a recuperação é necessária.

Este instalador não possui assinatura digital, então Windows pode exibir um editor desconhecido
aviso. Use a soma de verificação fornecida para verificar seu download. Não
requer a desativação da segurança Windows ou a instalação de ferramentas Python/PowerShell.
O tempo de execução do .NET Framework 4.8 é necessário.

Depois que este instalador tiver adicionado a atualização do mapa, ele manterá essa atualização durante
alterações de edição. Use Restaurar instalação anterior para desfazer a instalação do mapa.

Créditos: Andre (linhas de base Patch-Y), Loriendal e Trimitor (base HD),
Contribuidores Project Reforged (arte HD), Blizzard (arte original e
texto localizado), Lau (adaptação, compatibilidade, indicadores, testes).

Author / Creator / Last Modified By: Neil Mitchell

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

1.1.7 Hotfix: ativar novos recursos visuais de feitiço reutiliza um Patch-S desabilitado correspondente sem baixá-lo novamente. A cópia simples desativada é movida para o backup da transação verificada em LauSetupBackups, mesmo quando Patch-S ativo já corresponde. Versões diferentes permanecem recuperáveis ​​com Restaurar instalação anterior. Desligar ainda usa .mpq.disabled. Os arquivos existentes com sufixo hash são deixados intactos.
