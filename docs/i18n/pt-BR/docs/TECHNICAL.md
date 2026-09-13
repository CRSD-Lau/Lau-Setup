<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Correção 1.1.8** — O Setup verifica os MPQs de Data e da pasta do idioma ativo para detectar arquivos Patch-Y renomeados conhecidos e cópias exatas do catálogo. Se houver um possível conflito ou um arquivo ilegível ou incompatível, ele para e identifica o arquivo sem excluí-lo automaticamente. Renomear um arquivo não altera o hash do conteúdo. Os arquivos do jogo continuam na versão 3.0.8.
>
> A tradução completa ainda não foi atualizada devido ao limite de solicitações do Google. O texto existente abaixo corresponde a uma versão anterior. Consulte as informações atuais em inglês. [English](../../../TECHNICAL.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../TECHNICAL.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="technical-reference"></a>

# Referência técnica



[Voltar para Lau Setup](../README.md)

<a id="build-and-verification"></a>

## Construção e verificação

Execute `tools/build.ps1` em Windows com o compilador .NET Framework instalado. O pacote de origem pública contém o aplicativo, o catálogo incorporado, o script de construção e a documentação. A verificação de desenvolvimento completa contém adicionalmente `tools/test.ps1` para testes de transação, download, caminho, processo, recuperação e regressão de GUI; esses testes usam equipamentos isolados e um executável de referência local. `tools/build.ps1 -Release` recusa um catálogo que não passou pelo portão de publicação. O equipamento de teste, a geração de carga útil e os testes de jogos nativos dependem de caminhos de origem locais privados e não fazem parte do pacote de origem pública.

`build/catalog.json` nomeia cada ativo e segmento de download por tamanho e SHA-256, juntamente com URLs de lançamento GitHub observados. O catálogo fixa o repositório, a tag de lançamento e o arquivo com nome de hash. O instalador baixa anonimamente e verifica cada redirecionamento antes de segui-lo. Nenhuma conta GitHub, navegador conectado ou credencial de API é exigida pelo instalador. Na verificação completa do desenvolvimento, `tools/refresh_github_catalog.py` associa ativos carregados sem alterar hashes, e `tools/verify-public.ps1` verifica cada segmento e ativo reconstruído por meio do mesmo downloader usado pelo aplicativo.

<a id="file-placement"></a>

## Colocação de arquivo

| Componente | Destino |
|---|---|
| Executável compatível | `WoW.exe` |
| Q regional selecionado | Cópias idênticas na raiz `Data/patch-q.mpq` e localidade ativa `Data/<locale>/patch-<locale>-Q.MPQ` |
| Edição selecionada Y | Cópias idênticas na raiz `Data/patch-y.mpq` e localidade ativa `Data/<locale>/patch-<locale>-Y.MPQ` |
| Novos recursos de feitiço, quando selecionados | Raiz `Data/patch-s.mpq` |
| Correspondência de tabelas de feitiços localizadas, quando selecionadas | Local ativo `Data/<locale>/patch-<locale>-S.MPQ` |
| Mapas/minimapa opcionais | Raiz `Data/patch-m.mpq`; o backup do local ativo M substituído |

Core Q mantém o LoadingScreens.dbc do lançamento, Map.dbc localizado e carregando imagens byte por byte. Ele omite as definições adicionadas do mapa-múndi e a arte do mapa-múndi. O modo de mapa completo usa o Q regional original e o M compartilhado sem reempacotá-los. As duas colocações S contêm arquivos diferentes. A desativação de novos feitiços preserva o par raiz/localidade S com escopo definido como .mpq.disabled; a reativação move as cópias simples desativadas para backups de transações verificadas, conforme descrito na seção Configuração 1.1.7 abaixo. A detecção de HD requer os patches F de raiz e localidade existentes correspondentes.

<a id="recovery-design"></a>

## Projeto de recuperação

Um bloqueio de cliente cobre download, teste e instalação. Os arquivos são verificados antes da preparação e novamente após a colocação. Os arquivos existentes são movidos para `LauSetupBackups/transactions/<id>/before/`, preservando seus bytes e carimbos de data/hora; o diário é escrito de forma durável antes do commit. Uma confirmação com falha restaura os originais quando seguro. As confirmações e restaurações interrompidas permanecem detectáveis ​​quando o aplicativo é reaberto, mesmo sem WoW.exe.

A restauração recusa arquivos alterados por outra atualização e mantém o backup para resolução manual. Somente caminhos Q/M/S/Y exatos de raiz/localidade ativa e WoW.exe são aceitos. Traversal, fluxos alternativos e pontos de nova análise são rejeitados; arquivos retomados graváveis ​​devem ter um hardlink. Os temporários de diário e montagem usam nomes exclusivos e criação exclusiva. O aplicativo nunca enumera um arquivo no sistema de arquivos do cliente.

<a id="release-boundaries"></a>

## Liberar limites

Este instalador não possui assinatura digital. Os testes do instalador Windows e Wine, amostras de verificações da GUI e a linha de base dos dados do jogo retidos são registrados separadamente em VALIDATION.json. As verificações Wine 1.1.0 usam Wine 11.0 / Wine Mono 10.4.1 e armazenamento de sobreposição local do Docker; o teste de montagem aninhada simula a identidade do dispositivo porque esse contêiner não pode criar montagens. Essas verificações não certificam cada distribuição/sistema de arquivos Linux, escala de exibição, encontro ou modificação de cliente de terceiros. Os ZIPs da edição Patch-Y bruta estão disponíveis nas versões GitHub. Consulte [limitações conhecidas](../KNOWN-LIMITATIONS.md) para obter o escopo e as premissas atuais.


<a id="306-color-update--setup-112"></a>

## 3.0.6 atualização de cores / configuração 1.1.2

Cada um dos seis arquivos Y altera três membros M2 e o !PYAndre TOC, e adiciona duas texturas BLP. `Spells/PW_Coldflame_Ground.m2` agora faz referência a `Spells/PW_Coldflame_Blue.blp`; `Spells/PW_HalionMeteor_Ground.m2` e `Spells/PW_HalionMeteor_Ring.m2` fazem referência a `Spells/PW_Halion_Red.blp`. Somente o comprimento/deslocamento do nome do arquivo do descritor de textura 4 muda em cada modelo original; o novo caminho é anexado. Texturas de partículas nativas (índices 0 – 3), skins, geometria, trilhas de animação global, limites e bytes DBC permanecem inalterados. A textura branca compartilhada permanece inalterada para outros indicadores.

As novas texturas preservam o formato opaco 8×8 DXT1 BLP2 existente e todos os quatro níveis mip. Apenas o endpoint RGB565 muda: azul claro é decodificado como (120,216,248,255), vermelho como (248,68,40,255). A quantização é inerente ao formato de textura existente. Ambos os modelos Halion usam a mesma textura vermelha. As escolhas de consagração e edição do modelo permanecem independentes.

As decisões de atualização comparam SHA-256 e tamanho reais, não liberam rótulos ou carimbos de data/hora. Os testes de regressão modificam um byte sem alterar o tamanho do arquivo ou o carimbo de data/hora em cada posicionamento Y, exigem exatamente uma operação de reparo, verificam o hash reparado e, em seguida, restauram a versão anterior. Um EXE antigo incorpora o catálogo antigo, portanto, a atualização requer primeiro o download do novo EXE/ZIP.

<a id="307-halion-radius--setup-113"></a>

## 3.0.7 Raio Halion / Configuração 1.1.3

Promove bytes test-v2 exatos para `Spells/PW_HalionMeteor_Ground.m2`, `Spells/PW_HalionMeteor_Ring.m2` e seus arquivos `00.skin`. As coordenadas X/Y da malha são 1.5 vezes 3.0.6. Z/UVs/normais e trilhas de animação/partículas são preservadas. Os limites do modelo (deslocamento 160), limites de sequência (sequência +32) e limites de submalha de skin (submalha +20) refletem a geometria ampliada. A versão do TOC muda de 3.0.6 para 3.0.7. Exatamente cinco membros existentes mudam por edição; nenhum membro adicionado ou removido. A geometria do teste v3 foi excluída. Coldflame e todos os outros membros correspondem a 3.0.6. Aceitação do testador retransmitido pelo usuário da v2; a certificação de encontro amplo não é reivindicada.

<a id="308-all-cones--setup-114"></a>

## 3.0.8 todos os cones / Configuração 1.1.4

Todas as seis edições usam geometria total do ventilador em graus 90. Os nomes de arquivos do modelo legado e todas as linhas do DBC permanecem inalterados para preservar o roteamento ortográfico. Mudanças: PW_White_Fan60_60yd_Glowing (Halion ambos os reinos), PW_White_Fan60_30yd_Glowing (Saviana), PW_White_Fan60_100y_Glowing (ICC Rimefang) e PW_Rotface_SlimeSpray_Fan25_Room (Rotface) ampliam de 60 a 90; PW_White_Fan82_60yd_Glowing (Sartharion) amplia de 82 para 90. PW_White_Fan75_60yd_Glowing (Sindragosa) já é 90 e é idêntico em bytes.

Para cada modelo modificado, apenas o vértice XY (passo do vértice 48-byte) e os limites mudam. Ângulo sobre escalas +X por 90/ângulo antigo; cada raio de vértice e Z são preservados. Os limites do modelo no deslocamento 160, os limites da sequência na sequência+32 e os limites da submalha de skin na submalha+20 são atualizados. UVs, normais, animações e trilhas de partículas permanecem inalteradas. Dez membros de modelo/skin e duas strings de versão na alteração do TOC por edição; nenhum membro é adicionado ou removido. Todos os outros membros, incluindo a geometria Halion meteor-fire test-v2 e Coldflame, correspondem a 3.0.7 byte por byte.

<a id="setup-115-disabled-patch-s-preservation"></a>

## Configuração 1.1.5 desativada preservação Patch-S

Somente os caminhos S raiz e de localidade ativa ganham o sufixo .disabled. Cada desativação cria uma cópia preparada local fixada em hash antes de desativar S; ambos os caminhos são registrados em diário, com no máximo onze destinos. A reversão restaura os arquivos ativos originais e remove apenas as cópias desabilitadas recém-criadas. Cópias idênticas desativadas pré-existentes permanecem fora da transação e são preservadas. Arquivos ou diretórios conflitantes bloqueiam o planejamento. A reativação instala os ativos do catálogo S e não consome as cópias desativadas. Os periódicos existentes permanecem legíveis. Nenhum caminho de origem local arbitrário é aceito: cada cópia local deve corresponder à sua operação de desativação S emparelhada.

<a id="setup-116-disabled-copy-collisions"></a>

## Configurar colisões de cópia desabilitada 1.1.6

O arquivo S ativo atual sempre leva o nome simples .mpq.disabled. Antes de substituir um arquivo desabilitado existente diferente, a Instalação organiza seus bytes em um irmão que termina nos primeiros caracteres 12 de seu SHA-256; SHA-256 completo e comprimento são verificados antes de qualquer reutilização. Isso mantém os nomes dentro dos limites de caminho Windows existentes. O conteúdo conflitante do arquivo falha ao fechar. O S ativo, o arquivo simples desabilitado e a cópia de arquivo recém-criada são registrados em diário de forma independente, com no máximo treze entradas; a reversão restaura todos os originais. As fontes locais são restritas à desativação de S emparelhado ou às operações de substituição de arquivos desativados. Diários antigos permanecem legíveis.

<a id="setup-117-re-enable-cleanup"></a>

## Setup 1.1.7 reativa a limpeza

Habilitando a remoção de novos diários de feitiços da raiz simples e dos arquivos S desativados de localidade ativa. A transação move seus bytes originais verificados para o backup anterior aos dados. Se um arquivo desativado corresponder ao catálogo SHA-256 e ao tamanho, ele será preparado localmente para o destino S correspondente e excluído dos downloads. As fontes locais devem ser combinadas com a remoção exata de arquivos desativados e o ativo de catálogo. O Active S já correspondente ainda produz uma transação de limpeza. Os arquivos existentes com sufixo hash não são varridos. Os periódicos anteriores permanecem legíveis. Ligado/desligado/ligado, desvio de origem, interrupções a cada nova etapa de confirmação/restauração, todos os locais e restauração empilhada são cobertos.
