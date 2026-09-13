<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../START-HERE.txt). Se o texto for diferente, a fonte em inglês é oficial.

CONFIGURAÇÃO LAU - LIBERAÇÃO 3.0.8

Windows: baixe LauSetup.exe.
Linux/Wine: baixe LauSetup-Wine.zip e siga seu README.txt.
Wine requer o iniciador Linux fornecido; não execute o EXE diretamente.

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
