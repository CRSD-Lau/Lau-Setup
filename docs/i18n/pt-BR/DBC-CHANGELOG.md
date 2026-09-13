<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.2.0** — Um único ZIP agora contém o instalador do Windows e o iniciador para Linux/Wine. A interface segue automaticamente o idioma do sistema operacional entre dez opções; a escolha manual é salva. A versão 3.0.8 e os arquivos do jogo não mudam. Não há alterações de DBC.
>
> A atualização completa dos guias continua pendente devido a um HTTP 429 do Google. O texto abaixo pode estar desatualizado; consulte a fonte atual em inglês e as notas da versão 1.2.0. [English](../../../DBC-CHANGELOG.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)
>
> **Download atual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows e Linux/Wine. Extraia a pasta `LauSetup/` com cinco arquivos: no Windows, abra `LauSetup.exe`; no Linux/Wine, execute `LauSetup.sh`. As instruções antigas abaixo sobre EXE ou ZIP Wine separados não se aplicam à versão 1.2.0.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../DBC-CHANGELOG.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="dbc-changelog"></a>

# Registro de alterações do DBC



Acompanhe as edições do DBC do cliente separadamente das alterações de modelo, textura e instalador. As versões do jogo e as versões do instalador são separadas: `/pyversion` informa a edição do jogo.

<a id="handoff-history-andre-303-onward"></a>

## Histórico de transferência: Andre 3.0.3 em diante

[Edições individuais do DBC e histórico de desenvolvimento](docs/dbc/history/INDIVIDUAL-EDITS.md) · [Comparação de seis edições e hashes de linha de base](../../dbc/history/andre-to-3.0.4.json)

Andre omitiu intencionalmente **Spell.dbc** para evitar conflitos de localização. A substituição inicial do Lau expôs essa dependência; **Lau e Andre depuraram juntos** e a reconstrução multilíngue resolveu o problema de compatibilidade de texto ortográfico. Os arquivos Andre retidos contêm seis outros DBCs visuais/modelos, portanto, isso não deve ser descrito como uma ausência de cada DBC.

Lau descreve os marcos como **3.0.4: adição inicial de tabela**, **3.0.5: resolução multilíngue** e **3.0.6–3.0.8: hotfixes com alterações de versão**. Sobreposição de rótulos de versões anteriores: a compilação publicada arquivada denominada 3.0.4 já contém a correção multilíngue. As comparações de artefatos abaixo usam hashes exatos e não apagam o histórico de desenvolvimento.

A comparação inicial do Patch-Y inclui quinze edições de links visuais do Spell por edição, novos registros visuais/kit/anexos de indicadores, diferenças de consagração e edições de localização decodificadas. A adição da tabela é comparada com seu estoque subjacente ou com base no HD Spell, de forma que os registros herdados não sejam apresentados como novos trabalhos de autoria. [Verificação do estágio de localização](../../dbc/history/localization-stage.json) confirma a reconstrução do texto dos dados numéricos preservados nas quatro edições HD/Não HD de pré-localização retidas.

<a id="archived-releases-304--308"></a>

## Versões arquivadas 3.0.4 → 3.0.8

| Transição arquivada | Resultado DBC | Outras alterações |
| --- | --- | --- |
| 3.0.4 → 3.0.5 | Sem edições DBC; 42 tabelas idênticas | Geometria do cone Sindragosa e Rotface, etiqueta de versão |
| 3.0.5 → 3.0.6 | Sem edições DBC; 42 tabelas idênticas | Ativos e referências de cores do marcador Coldflame/Halion, rótulo de versão |
| 3.0.6 → 3.0.7 | Sem edições DBC; 42 tabelas idênticas | Geometria aprovada de fogo de meteoro Halion, etiqueta de versão |
| 3.0.7 → 3.0.8 | Sem edições DBC; 42 tabelas idênticas | Geometria do cone do hálito restante/Slime Spray, etiqueta da versão |

[Todas as comparações de tabelas 168 e hashes de arquivo](../../dbc/history/3.0.4-through-3.0.8.json). Estas são comparações de artefatos de liberação retidos, e não uma afirmação de que o incidente de localização anterior não aconteceu.

<a id="307--308--no-dbc-edits"></a>

## 3.0.7 → 3.0.8 — sem edições DBC

Lançado com [Configuração 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4). Todas as comparações DBC **42 passaram byte por byte**: sete tabelas em cada uma das seis edições Patch-Y. Não há tabelas adicionadas/excluídas, registros alterados, campos alterados ou blocos de string alterados.

| Tabela | Edições de registros | Edições de campo | Resultado |
| --- | ---: | ---: | --- |
| CreatureDisplayInfo.dbc | 0 | 0 | Idêntico |
| CreatureModelData.dbc | 0 | 0 | Idêntico |
| Spell.dbc | 0 | 0 | Idêntico |
| SpellVisual.dbc | 0 | 0 | Idêntico |
| SpellVisualEffectName.dbc | 0 | 0 | Idêntico |
| SpellVisualKit.dbc | 0 | 0 | Idêntico |
| SpellVisualKitModelAttach.dbc | 0 | 0 | Idêntico |

[Evidência de comparação completa](../../dbc/3.0.7-to-3.0.8.json) registra o MPQ de origem/destino de cada edição SHA-256, cada DBC antes/depois de SHA-256, tamanho, contagem de linhas e contagem de campos. Os hashes MPQ foram verificados nos catálogos de lançamento. Os outros ativos do catálogo 22, incluindo recursos de localidade Q e ativos S compartilhados, permanecem inalterados.

<a id="what-actually-changed-in-308"></a>

### O que realmente mudou em 3.0.8

Cinco modelos de cone existentes foram ampliados para **90° total** editando sua geometria `.m2` e os limites `00.skin` correspondentes. As ligações DBC existentes foram mantidas.

| Haste modelo | Ângulo anterior | Novo ângulo |
| --- | ---: | ---: |
| PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_Glowing | 60° | 90° |
| PW_White_Fan60_30yd_Glowing | 60° | 90° |
| PW_White_Fan60_100y_Glowing | 60° | 90° |
| PW_White_Fan82_60yd_Glowing | 82° | 90° |

Os nomes dos arquivos mantêm rótulos de ângulos históricos; a geometria determina o ângulo exibido. Sindragosa já era 90° e não sofreu alterações nesta transição. Isso trouxe todos os indicadores de respiração suportada e Slime Spray para 90°. O alcance e o tempo de animação permaneceram inalterados. O raio do fogo do meteoro Halion, as cores da Chama Fria e a Consagração permaneceram inalterados.

Cada edição mudou exatamente **membros do arquivo 11**: cinco arquivos `.m2`, cinco arquivos `.skin` e o rótulo da versão do jogo `!pyandre.toc` de 3.0.7 para 3.0.8. Todos os outros membros de conteúdo listados são idênticos. A contabilidade do contêiner MPQ está fora da comparação entre membros do conteúdo.

Isso verifica as alterações no arquivo do cliente, não a mecânica do servidor Warmane ou um limite exato de danos.

<a id="setup-115-116-and-117--no-dbc-edits"></a>

## Configure 1.1.5, 1.1.6 e 1.1.7 — sem edições DBC

Estes são os hotfixes do instalador. Suas cargas de jogo permanecem 3.0.8, com dados DBC inalterados. O hotfix mais recente altera a instalação, preservação e reutilização do Patch-S, não seu conteúdo interno do DBC.

<a id="required-entry-for-future-releases"></a>

## Entrada obrigatória para lançamentos futuros

Cada versão deve adicionar uma entrada aqui e uma seção **Alterações de DBC** às notas de versão GitHub, incluindo versões somente para instalador. Indique explicitamente **Sem edições DBC** quando aplicável. Compare com a versão estável anterior do jogo, não com uma versão de teste não publicada. Não descreva uma edição de modelo/textura como uma edição DBC.

Para cada edição real do DBC, registre uma linha por campo (ou uma diferença vinculada em nível de linha legível por máquina para grandes alterações de localização):

| Transição de jogo | Tabela | ID do registro | Nome do campo/índice baseado em zero | Valor antigo | Novo valor | Edições/localidades | Razão |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VERSÃO → VERSÃO | TABLE.dbc | ID | Campo nomeado [índice] | Valor anterior | Novo valor | Variantes afetadas | Finalidade |

Registre também registros e tabelas adicionados/excluídos, alterações de esquema e edições de valores de string. Decodifique valores de string em vez de relatar a variação de deslocamento de bloco de string à medida que o conteúdo muda. Especifique a convenção de índice de campo e a origem do esquema; rotular campos desconhecidos em vez de adivinhar. Anexe hashes de arquivo e tabela antes/depois, o método de comparação e limites de validação. Nunca reivindique uma comparação aprovada sem evidências.

A auditoria de transferência abrange Patch-Y a partir das linhas de base retidas de Andre 3.0.3 em diante. Pipelines separados de localização de Q/S/mapa e construções experimentais não relacionadas estão fora desta retrospectiva inicial. Nenhum artefato quebrado anteriormente recebe um número de lançamento sem proveniência correspondente.
