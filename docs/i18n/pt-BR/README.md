<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Um único ZIP agora contém o instalador do Windows e o iniciador para Linux/Wine. A interface segue automaticamente o idioma do sistema operacional entre dez opções; a escolha manual é salva. A versão 3.0.8 e os arquivos do jogo não mudam. Não há alterações de DBC.
>
> A atualização completa dos guias continua pendente devido a um HTTP 429 do Google. O texto abaixo pode estar desatualizado; consulte a fonte atual em inglês e as notas da versão 1.3.0. [English](../../../README.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
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

> Tradução automática. [Fonte em inglês](../../../README.md). Se o texto for diferente, a fonte em inglês é oficial.

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="../../assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>Seu cliente. Sua língua. Seu Wrath.</strong><br />O instalador Windows e Linux/Wine para a atualização visual Lau.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">Último lançamento</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">Site e galeria</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">Informar um problema</a> ·
  <a href="https://github.com/users/CRSD-Lau/projects/2">Roteiro comunitário</a>
</p>

---

Texto mágico multilíngue, arte de carregamento em tela ampla, indicadores de solo personalizados e mapas HD opcionais para **WoW 3.3.5a, construção 12340**. Escolha seu cliente e recursos visuais existentes; Lau Setup baixa os arquivos necessários, verifica-os, coloca os patches e faz backup dos originais.

**Instalador 1.1.7 · Lançamento do jogo 3.0.8 Lau · Nove idiomas de cliente**

<a id="patch-s-stays-recoverable"></a>

## Patch-S permanece recuperável

**Configuração do hotfix 1.1.7:** a reativação de novos visuais de feitiço reutiliza um Patch-S desativado correspondente e move a cópia simples desativada para `LauSetupBackups`, de modo que os dados não retém uma duplicata ativa/desativada. Cópias diferentes são preservadas no backup da transação. Desligar ainda usa `.mpq.disabled`. Use **Restaurar instalação anterior** para recuperação.

<a id="90-breath-and-slime-spray-warnings"></a>

## 90° avisos de respiração e spray de limo

**3.0.8 Lau:** todos os indicadores de respiração suportados e Rotface Slime Spray são **90° no total**, após a confirmação do testador Warmane. Abrange Halion em ambos os reinos, Saviana Ragefire, Sartharion, ICC Rimefang e Sindragosa. O intervalo e o tempo da animação são preservados. O maior raio de disparo do meteoro Halion aprovado e o Coldflame azul claro permanecem inalterados.

**Já instalado?** Baixe **Configuração 1.1.7** primeiro, selecione a mesma pasta e recursos visuais e, em seguida, instale. A instalação verifica os hashes SHA-256 reais: até mesmo uma alteração de um byte com o mesmo tamanho e carimbo de data/hora é detectada. Apenas os novos arquivos correspondentes contam como já instalados. `/pyversion` relata **3.0.8 Lau**. Instaladores antigos mantêm seu antigo catálogo incorporado.

[Prévias de cores animadas e changelog](https://wrath-multilingual-hd.vercel.app/#changelog)

<a id="download"></a>

## Baixar

| Windows | Linux / Wine |
| :--- | :--- |
| **[Baixar LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** | **[Baixar LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** |
| Windows 10 / 11 · .NET Framework 4.8 | Wine 11.0 · Wine Mono 10.4.1 · 64-bit prefixo |
| Sobre **156 KB** | Sobre **80 KB** · Python 3.9+ |
| [Guia Windows](START-HERE.md) | [Guia e pré-requisitos Wine](wine/README.md) |

Download de arquivos do jogo durante a configuração. Uma instalação básica em inglês custa cerca de **472 MB** com modelos HD e novos visuais de feitiços, ou **259 MB** com modelos originais. Mapas opcionais adicionam um download maior; a configuração mostra o total antes de você instalar.

[Somas de verificação SHA-256](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [Notas de versão](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [Relatório de validação](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **Traga seu cliente existente.** Esta é uma atualização, não um cliente de jogo completo, pacote de idiomas ou modelo HD base. A interface do instalador segue automaticamente o idioma do sistema entre dez opções; a escolha manual é salva. Os dados do jogo do cliente continuam a oferecer suporte a nove localidades e seguem a localidade detectada do jogo.

<a id="one-setup-the-details-handled"></a>

## Uma configuração. Os detalhes tratados.

| Escolha seu visual | Mantenha o controle da sua instalação |
| :--- | :--- |
| Consagração aprimorada ou em estoque | Linguagem do cliente e detecção de modelo |
| Novos visuais de feitiços para clientes HD compatíveis | Apenas os arquivos necessários baixados |
| Mapas HD opcionais e texturas de minimapa | Verificação SHA-256 antes da instalação |
| Arte de carregamento regional widescreen | Backups automáticos e downloads recuperáveis ​​|
| Nomes de feitiços, classificações e dicas de ferramentas localizadas | Restauração e recuperação de operação interrompida |

<p align="center"><img src="../../assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

Seus complementos, SavedVariables, fontes, arte de login, configurações de domínio e patches não relacionados permanecem no lugar. Nenhuma UI pessoal, credenciais ou análises estão incluídas.

<a id="get-started"></a>

## Comece

1. **Feche WoW completamente.** Em Wine, feche cada instância WoW em todos os prefixos.
2. **Inicie a configuração e escolha sua pasta de cliente.** Extraia `LauSetup.zip` na pasta `LauSetup/`. No Windows, abra `LauSetup.exe`; no Linux/Wine, execute `LauSetup.sh`.
3. **Escolha seu visual e instale.** Consagração Aprimorada começa marcada; desmarque para a aparência do estoque. Novos visuais de feitiços exigem uma base de modelo HD compatível. Os mapas são opcionais.
4. **Inicie WoW e execute `/pyversion`.** Confirme a edição instalada antes de entrar no jogo.

Em Linux, execute isto da pasta extraída com seu prefixo existente:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Use o inicializador como seu usuário normal. Ele verifica caminhos Linux, jogos em execução, espaço livre e bloqueios do instalador entre prefixos. Use armazenamento Linux local; pastas vinculadas, compartilhamentos de rede e unidades montadas em Windows não são suportadas. O [guia Wine](wine/README.md) lista as fontes e todos os pré-requisitos.

Em Windows, a instalação oferece a página de download oficial do .NET Framework 4.8 da Microsoft se o tempo de execução estiver faltando. A configuração Wine testada usa **Wine Mono**, não o instalador .NET Windows.

<a id="nine-client-languages"></a>

## Nove idiomas clientes

Inglês · Français · Deutsch · 한국어 · Русский · 简体中文 · 繁體中文 · Español (Espanha) · Español (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

A configuração segue a localidade ativa do seu cliente. Instale os arquivos de idioma e fontes apropriados antes de alterar a configuração. A alteração de um valor de configuração por si só não instala um pacote de idiomas.

<a id="restore-with-your-backups"></a>

## Restaure com seus backups

Feche WoW, reabra a configuração através do mesmo inicializador, escolha o mesmo cliente e selecione **Restaurar instalação anterior**. Mantenha `LauSetupBackups` dentro da pasta do cliente: ela contém os originais e os registros de recuperação.

Uma instalação ou restauração interrompida pode ser recuperada mesmo se `WoW.exe` estiver temporariamente ausente. Se outra atualização alterar os arquivos instalados, a restauração será interrompida e preservará o backup para resolução. Depois que este instalador adiciona a atualização do mapa, ele a mantém durante as alterações de edição; restaure a instalação anterior para desfazer essa atualização.

<a id="tested-with-clear-limits"></a>

## Testado, com limites claros

A versão 1.1.7 passou **grupos de regressão 50 em Windows e em Wine**, incluindo planos de localidade/edição/mapa de 108 por plataforma. O lançamento do jogo 3.0.8 passou anteriormente por atualizações de seis edições e detecção de um byte em ambas as plataformas; suas cargas úteis permanecem inalteradas. A configuração 1.1.7 também cobre a sequência de todos os sinalizadores ativados para novos feitiços desativados com cópias desabilitadas mais antigas, trocas repetidas e reversão exata. Cargas públicas foram baixadas anonimamente e verificadas por hash; a instalação real do núcleo e a reversão foram testadas.

Wine foi testado com **Wine 11.0 / Wine Mono 10.4.1** no armazenamento Linux local, incluindo o inicializador fornecido como um usuário normal. A geometria do fogo de meteoro Halion corresponde exatamente à versão 2 aprovada pelo testador. Coldflame, trilhas de animação, fogo nativo e tabelas de feitiços permanecem idênticos em bytes a 3.0.7. As animações do site são maquetes ilustrativas. Esses testes não certificam todas as distribuições Linux ou encontros no jogo.

As integrações Lutris, Proton e macOS estão fora desta versão. O executável não possui assinatura digital.

<a id="known-limitations-and-feature-requests"></a>

## Limitações conhecidas e solicitações de recursos

Leia [Limitações e suposições conhecidas](KNOWN-LIMITATIONS.md) antes de sugerir um recurso: controle de servidor Warmane, escopo de DLL/código nativo, ações Lua protegidas, precisão e tempo do indicador, dependências de DBC e limites de plataforma/recuperação.

<a id="for-contributors"></a>

## Para contribuidores

- [Construir, colocar arquivo e projetar recuperação](docs/TECHNICAL.md)
- [Contribuição e orientação para relatórios de bugs](CONTRIBUTING.md)
- [Revisão da implementação](REVIEW.md)
- [Escopo e viabilidade da plataforma](PLATFORM-FEASIBILITY.md)

As cargas úteis do jogo são distribuídas por meio das versões GitHub. Este repositório contém a fonte do instalador, catálogo, inicializador e documentação; você não precisa cloná-lo para instalar a atualização.

<a id="built-on-community-work"></a>

## Baseado no trabalho comunitário

**Andre** — Linhas de base Patch-Y · **Loriendal e Trimitor** — Base do cliente HD · **Contribuidores de Project Reforged** — arte em HD · **Blizzard** — jogo original, arte e texto localizado · **Lau** — indicadores de solo, compatibilidade, adaptações, ferramentas de teste e liberação.

[Créditos completos](https://wrath-multilingual-hd.vercel.app/credits) · [Capturas de tela e ajuda de instalação](https://wrath-multilingual-hd.vercel.app/)

<sub>Projeto comunitário não oficial. Não afiliado ou endossado por Blizzard Entertainment. O jogo original e a arte de terceiros permanecem propriedade de seus respectivos proprietários.</sub>

<a id="dbc-change-tracking"></a>

## Rastreamento de alterações do DBC

Consulte o [registro de alterações do DBC](DBC-CHANGELOG.md) para edições individuais de tabelas/registros/campos e evidências de comparação. **3.0.7 → 3.0.8 não teve edições DBC**: a atualização do indicador 90° alterou a geometria do modelo. A configuração 1.1.5 – 1.1.7 também deixa os dados DBC inalterados.
