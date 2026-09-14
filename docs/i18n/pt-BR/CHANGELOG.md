<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **Versão atual: Setup 1.4.0 / jogo 3.0.9 Lau.** Feche o WoW, extraia todo o LauSetup.zip, abra LauSetup.exe no Windows e use Browse... para escolher a pasta que contém WoW.exe. Avançar → opções visuais → Avançar → revisar → instalar → concluir. Todos os extras começam desativados. WoW.exe e telas de carregamento são uma opção conjunta; os mapas são independentes e incluem arquivos WDM. Mapas já instalados são mantidos. Patches duplicados renomeados permanecem; apenas um Patch-V vazio é salvo automaticamente. Arquivos substituídos são salvos em LauSetupBackups. Nenhum DBC do Patch-Y foi alterado; os mapas opcionais adicionam tabelas originais documentadas. Mapas de cavernas continuam em beta. Linux/Wine usa LauSetup.sh com os requisitos documentados. O erro Google HTTP 429 impede atualizar a tradução completa. O texto antigo abaixo é apenas referência histórica; consulte a fonte em inglês para as instruções atuais.
>
> [English](../../../CHANGELOG.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../CHANGELOG.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 Hotfix - Alternar opções com Patch-S desabilitado existente

Corrige a mensagem 1.1.5 "Um Patch-S desabilitado diferente já existe" ao desativar os visuais do novo feitiço após uma instalação anterior.

A instalação mantém ambos os arquivos automaticamente. O arquivo S atual sempre se torna `.mpq.disabled`. Se já existir uma cópia desabilitada mais antiga, a Instalação primeiro preservará essa cópia mais antiga como `.mpq.disabled.<12-character hash>`. Uma cópia salva idêntica é reutilizada. Ambas as versões são mantidas. Uma cópia com nome de hash cujo conteúdo não corresponde ao arquivo mais antigo que está sendo preservado ainda interrompe a operação para inspeção.

Isso se aplica a arquivos S raiz e de localidade ativa, incluindo a sequência **todos os três sinalizadores ativados -> Novos visuais de feitiço desativados**, trocas repetidas e reversão. A escolha do mapa é mantida.

Baixe o novo EXE ou Wine ZIP e tente novamente sua seleção. Não é necessário excluir ou renomear a cópia desabilitada existente para resolver a colisão comum mostrada por 1.1.5.

Para desfazer a instalação completa, use **Restaurar instalação anterior**. Para reativar manualmente um arquivo S salvo, feche WoW e remova `.disabled` e qualquer hash seguinte, restaurando seu nome de arquivo `.mpq` original. Nunca substitua um arquivo ativo diferente. Alterações manuais podem interromper a reversão gerenciada em caso de desvio de arquivo; mantenha seus backups. Os arquivos removidos pelos instaladores antes de 1.1.5 ainda precisam de recuperação por meio de seus backups.

O lançamento do jogo permanece **3.0.8 Lau** e a carga útil de cada jogo permanece inalterada. Todos os cones de grau 90, raio de fogo de meteoro e Coldflame são preservados.

As verificações Windows e Wine incluem grupos de regressão 46, todos os nove locais, arquivos desativados existentes, interruptores liga/desliga repetidos, proteção contra cópia adulterada, recuperação de interrupção e reversão exata. Downloads públicos recentes são testados com arquivos de versão On/Off reais e uma cópia antiga desativada presente. Esta é a validação do instalador, não a validação de novos encontros no jogo.

[Patch-Y ZIP bruto de seis edições](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Ajuda de instalação e registro de alterações](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup 1.1.5 Hotfix - Manter arquivos Patch-S desativados

A desativação de **Novos recursos visuais de feitiço** agora preserva os arquivos raiz e de localidade ativa Patch-S ao lado de seus locais originais como `.mpq.disabled`, em vez de deixá-los apenas nos backups do instalador. Seus bytes são verificados antes e depois da alteração. WoW não carrega o nome de arquivo desativado.

- Uma cópia `.disabled` existente diferente bloqueia a instalação; nunca é sobrescrito.
- Uma cópia idêntica desativada é reutilizada e preservada.
- Ativar a opção instala os arquivos S ativos da versão selecionada e mantém cópias desativadas.
- Instalações repetidas, reversão e recuperação de interrupção cobrem caminhos ativos e desativados.

Para reativar manualmente um arquivo desativado, feche WoW e remova apenas o sufixo `.disabled`. Não substitua um arquivo ativo diferente. Para desfazer a instalação completa do Lau, use **Restaurar instalação anterior**; excluir apenas Patch-Y não desfaz Q/M/executável ou outras alterações. Alterações manuais de arquivos podem fazer com que a reversão gerenciada seja interrompida, portanto, mantenha os backups.

**Já foi afetado por um instalador mais antigo?** Esta atualização não extrai automaticamente backups antigos. Use Restaurar instalação anterior para recuperar esses arquivos, retrocedendo em todas as instalações empilhadas, antes de reinstalar com a nova configuração. Mantenha LauSetupBackups.

O lançamento do jogo permanece **3.0.8 Lau**. Todos os MPQs permanecem inalterados: respirações de grau 90/Slime Spray, aprovado +50% Raio de fogo de meteoro Halion e Coldflame são preservados. Baixe o novo EXE ou Wine ZIP para a correção do instalador.

A validação Windows e Wine está incluída em VALIDATION.json. Os testes cobrem todos os nove locais, colisões de cópia desabilitada, transições liga/desliga, instalação repetida, interrupção em cada etapa de movimentação/restauração, desvio de arquivo e reversão exata. A correção não exige validação de novos encontros no jogo.

[Patch-Y ZIP bruto de seis edições (3.0.8 inalterado)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Ajuda de instalação e registro de alterações](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · Lançamento do jogo 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## 1.1.7 Hotfix - Patch-S reativar a limpeza

- A reativação de novos visuais de feitiço reutiliza um Patch-S desativado quando seu SHA-256 e tamanho correspondem à versão selecionada, evitando esse download.
- A cópia simples desativada é movida para o backup da transação verificada fora dos Dados, mesmo que o Patch-S ativo já corresponda. Diferentes arquivos desativados permanecem recuperáveis ​​através da restauração da instalação anterior.
- Aplica-se à localidade raiz e ativa Patch-S. Off ainda usa o nome de arquivo simples `.mpq.disabled`. Os arquivos existentes com sufixo hash são deixados intactos.
- As cargas úteis do jogo permanecem 3.0.8 Lau. Windows e Wine passaram, cada um, por grupos de regressão 50, comutação liga/desliga/liga de arquivo real e reversão exata.

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## Todos os avisos de hálito e spray de limo agora são 90°

Após a confirmação do testador Warmane, Halion (ambos os reinos), Saviana Ragefire, Sartharion, ICC Rimefang e Rotface Slime Spray agora usam **90° cones totais**, correspondendo ao aviso 90° existente de Sindragosa. Isso se aplica a todas as seis edições e nove idiomas clientes, incluindo os mapeamentos de feitiços normais/heróicos existentes.

Apenas a largura do cone muda. Alcance, tempo de animação, efeitos de feitiços nativos e tabelas de feitiços são preservados. O maior raio de fogo de meteoro Halion aprovado do 50%, Coldflame azul claro, cores e Consagração permanecem inalterados. Estes são buffers de aviso visual; os danos e a mecânica do servidor permanecem inalterados. Terrenos irregulares ainda podem cortar cones planos.

<a id="updating"></a>

## Atualizando

Baixe **LauSetup.exe** ou **LauSetup-Wine.zip** desta versão primeiro. Feche WoW, selecione o mesmo cliente e recursos visuais e clique em **Instalar atualização**. Os instaladores antigos mantêm seus catálogos antigos. Verifique `/pyversion` para **3.0.8 Lau**.

A instalação verifica os hashes SHA-256 reais, portanto, versões anteriores e até mesmo alterações de um byte com tamanho e carimbo de data/hora inalterados são detectadas. Somente os arquivos atuais exatos contam como já instalados. Backups e restauração da instalação anterior permanecem disponíveis.

Windows requer .NET Framework 4.8. Os usuários Wine extraem todos os quatro arquivos e executam `LauSetup.sh` como um usuário normal com o prefixo Wine/Mono existente compatível. Os instaladores de tempo de execução não estão incluídos.

<a id="validation"></a>

## Validação

Consulte VALIDATION.json para regressão Windows e Wine, atualizações de seis edições de 3.0.7, detecção de repetição, verificações de um byte, reversão e verificações de download público. As verificações de geometria verificam cones 90°, intervalo preservado, limites válidos e enrolamento triangular em cada edição. Exatamente onze membros existentes do arquivo mudam: cinco modelos, suas cinco skins e a versão TOC. Todos os outros membros são idênticos em bytes a 3.0.7.

A decisão de largura segue o teste Warmane relatado. Esta versão não é uma certificação para todos os encontros ou para limites exatos de servidor.

[Registro de alterações do site e ajuda de instalação](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · Lançamento do jogo 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## Avisos maiores de incêndio de meteoros Halion

Promove o **teste v2** aprovado pelo testador: o raio do marcador de solo vermelho do Halion é **50% maior que o lançamento 3.0.6**, ao redor de trilhas e pousando fogo. O teste v3 não está incluído. Coldflame, cores, faixas de animação, chamas nativas, Consagração e os cones Sindragosa/Rotface permanecem inalterados. Todas as seis edições e nove idiomas clientes são suportados.

O testador confirmou a v2 após corrigir um patch não atualizado. Este é um buffer de aviso visual, não uma alteração nos danos do servidor ou uma certificação de cada posição ou encontro.

<a id="update-with-the-new-installer"></a>

## Atualize com o novo instalador

Baixe **LauSetup.exe** ou **LauSetup-Wine.zip** desta versão primeiro. Feche WoW, selecione o mesmo cliente e recursos visuais e clique em **Instalar atualização**. Instaladores antigos retêm catálogos antigos. `/pyversion` relata **3.0.7 Lau**.

Os usuários existentes do 3.0.6 e do teste v2 recebem a atualização. A instalação compara hashes de arquivos reais, incluindo alterações de um byte com tamanho e carimbo de data/hora inalterados; apenas os arquivos atuais exatos contam como já instalados. Backups e restauração da instalação anterior permanecem disponíveis.

Windows requer .NET Framework 4.8. Os usuários Wine extraem todos os quatro arquivos e executam `LauSetup.sh` como um usuário normal com o prefixo Wine/Mono existente compatível. Nenhum instalador de tempo de execução está incluído.

<a id="validation-1"></a>

## Validação

Regressão do instalador Windows e Wine, atualizações de seis edições, detecção de repetição, verificações de um byte, reversão e verificações de download público são registradas em VALIDATION.json. Os modelos e skins Halion são idênticos em bytes para testar v2. Apenas sua geometria/limites e a versão TOC diferem de 3.0.6; Coldflame e outros membros do arquivo permanecem inalterados.

[Registro de alterações do site e ajuda de instalação](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · Lançamento do jogo 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## Blue Coldflame, fogo de meteoro vermelho

- **Marrowgar Coldflame:** círculos azuis claros com o brilho interno existente e animação no sentido horário, incluindo heróico.
- **Fogo de meteoro Halion:** dispare círculos vermelhos ao redor das trilhas e atire com a animação existente no sentido horário.
- Todas as seis edições HD/Não HD e nove idiomas de cliente. Chamas nativas, durações, opções de consagração e os cones 90° Sindragosa / 60° Rotface permanecem inalterados.

[Prévias de cores animadas e changelog completo](https://wrath-multilingual-hd.vercel.app/#changelog). As prévias são maquetes ilustrativas, não gravações do jogo. Os danos e a mecânica do servidor permanecem inalterados; bordas de advertência permanecem buffers visuais.

<a id="already-installed-download-the-new-installer-first"></a>

## Já instalado? Baixe o novo instalador primeiro

Baixe **LauSetup.exe** ou **LauSetup-Wine.zip** desta versão. Feche WoW, escolha a mesma pasta e configurações visuais e clique em **Instalar atualização**. Os instaladores baixados antigos mantêm seu antigo catálogo incorporado.

A instalação faz hash dos arquivos reais. Arquivos 3.0.5 mais antigos foram substituídos; até mesmo uma alteração de um byte com tamanho de arquivo e carimbo de data/hora idênticos é detectada. Apenas os novos arquivos exatos são tratados como já instalados. `/pyversion` relata **3.0.6 Lau**. Backups e restauração da instalação anterior permanecem disponíveis.

Usuários Wine: extraiam todos os quatro arquivos juntos e execute `LauSetup.sh` como seu usuário normal com seu prefixo 64-bit Wine 11.0 / Mono 10.4.1 existente. São necessários armazenamento Python 3.9+ e Linux local. Windows precisa do .NET Framework 4.8. Os tempos de execução não são agrupados.

<a id="fresh-verification-on-windows-and-wine"></a>

## Nova verificação em Windows e Wine

- Grupos de regressão 38 por plataforma, incluindo planos de localidade/edição/mapa 108 cada.
- Todas as seis atualizações reais de 3.0.5 para 3.0.6, instalações não operacionais repetidas e reversão exata em ambas as plataformas.
- Alterações de um byte no mesmo tamanho/mesmo carimbo de data/hora detectadas e reparadas independentemente na raiz e na localidade Y em ambas as plataformas.
- Downloads anônimos de carga útil GitHub, instalações principais reais e reversão em Windows e Wine.
- Testes de segurança de host 15 Linux e o inicializador Wine exato de quatro arquivos para um usuário normal; Renderização do formulário Windows verificada.
- Três referências de textura do marcador M2 e o TOC da versão alterado a cada edição; duas texturas de cores adicionadas. Todos os outros membros preservaram byte por byte.

Essas verificações do instalador não certificam todas as distribuições Linux ou todos os encontros no jogo. O executável não possui assinatura digital. Evidências detalhadas, somas de verificação e fonte estão anexadas.

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · Lançamento do jogo 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## Avisos de ataque mais amplos

- Sindragosa Frost Breath: **75° → 90° total** (7.5° extra por lado).
- Rotface Slime Spray: **25° → 60° total** (17.5° extra por lado).
- Aplicado a todas as seis edições HD/Não HD e disponível em todas as nove localidades do cliente. Outros indicadores, configurações de consagração, tabelas localizadas e arte permanecem inalterados.

Esses são avisos visuais armazenados em buffer informados por imagens de ataque Warmane e registros de ataques de feitiço. Eles não alteram os danos ou a mecânica do servidor, nem reivindicam um limite exato de danos.

<a id="updating-an-existing-installation"></a>

## Atualizando uma instalação existente

Baixe o novo **LauSetup.exe** ou **LauSetup-Wine.zip** primeiro. Feche WoW, selecione a mesma pasta e opções visuais e clique em **Instalar atualização**. O instalador compara os hashes de arquivo reais: os patches 3.0.4 mais antigos são substituídos, enquanto uma instalação exata do 3.0.5 é relatada como já instalada. `/pyversion` relata **3.0.5 Lau** após a atualização. Os instaladores baixados antigos mantêm seu catálogo antigo.

Os downloads de Windows e Wine incluem o mesmo executável de configuração reconstruído. Para Wine, extraia todos os quatro arquivos juntos e use `LauSetup.sh` conforme descrito no README incluído. Os requisitos de tempo de execução existentes permanecem inalterados.

<a id="verification"></a>

## Verificação

Todos os grupos de regressão 38 Windows foram aprovados, incluindo planos de localidade/edição/mapa 108. Todas as seis edições passaram nas verificações reais de atualização 3.0.4 para 3.0.5, instalação repetida e reversão exata. Novas cargas passaram em verificações anônimas de download/hash; uma instalação principal isolada de GitHub e reversão aprovada. Cada edição preserva todos os membros, exceto quatro arquivos de modelo/geometria e a versão TOC.

O código do iniciador Wine permanece inalterado e o ZIP contém o EXE reconstruído exato. A evidência de tempo de execução anterior de Wine 11.0 / Mono 10.4.1 é retida; a nova execução de Wine não estava disponível porque o mecanismo Docker não foi iniciado. A nova geometria do cone é verificada estaticamente, e não recentemente certificada no jogo.

As somas de verificação de download, a fonte e o relatório de validação detalhado estão anexados. Mantenha `LauSetupBackups` para recuperação.

Author / Creator / Last Modified By: Neil Mitchell
