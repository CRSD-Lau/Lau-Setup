<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../CONTRIBUTING.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="contributing-to-lau-setup"></a>

# Contribuindo para Lau Setup



Obrigado por ajudar a melhorar a instalação e recuperação da comunidade Wrath.

<a id="report-a-problem"></a>

## Relate um problema

Use o [formulário de relatório de bug](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Inclua a versão do instalador, plataforma, localidade do cliente, recursos visuais selecionados, comportamento esperado e etapas de reprodução. Para problemas no jogo, inclua `/pyversion`, o chefe ou habilidade, dificuldade e uma captura de tela. Os relatórios Wine devem incluir as versões Wine e Wine Mono.

Remova nomes de contas, senhas, tokens e caminhos pessoais de capturas de tela ou trechos. Não carregue seu cliente, pasta WTF, SavedVariables ou logs inteiros. Mantenha backups locais se a recuperação estiver pendente.

<a id="propose-a-change"></a>

## Proponha uma mudança

Comece com [Limitações e suposições conhecidas](KNOWN-LIMITATIONS.md). Use [Ideias](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) para recomendações; identifique qualquer dependência de servidor, código nativo ou ação protegida antes de propor uma implementação.

Mantenha as solicitações pull focadas. Explique o problema visível ao usuário, a alteração e as verificações que você executou. Teste as operações dos arquivos apenas em jogos isolados, nunca em um cliente de jogo pessoal ativo.

Preserve a lista de permissões de arquivo, verificações de hash, diários de backup, verificações de processos e bloqueio de prefixo cruzado. Não altere os registros de carga útil do jogo como parte de uma documentação ou atualização de interface.

A [referência técnica](docs/TECHNICAL.md) explica a construção pública e os testes que requerem equipamentos locais privados. Separe claramente uma construção bem-sucedida, testes de acessórios e validação real no jogo em seu PR.

<a id="artwork-and-attribution"></a>

## Arte e atribuição

Mantenha intactas a marca W-and-shield e os créditos upstream estabelecidos. Inclua a fonte e as permissões aplicáveis ​​à arte proposta. Não introduza o estado do cliente pessoal nos bens públicos.

<a id="dbc-release-records"></a>

## Registros de lançamento do DBC

Cada versão de jogo ou instalador deve ser atualizada [DBC-CHANGELOG.md](DBC-CHANGELOG.md) e incluir uma seção **Alterações de DBC** em suas notas de versão GitHub. Para edições reais do DBC, tabela de lista, ID de registro, campo nomeado e índice baseado em zero, valores antigos/novos, edições/localidades afetadas e motivo, com hashes antes/depois e evidências de comparação. Para DBCs inalterados, registre explicitamente **Nenhuma edição de DBC**. Separe as edições de geometria, textura e instalador das alterações do DBC. Consulte o changelog para obter o formato necessário e os limites de validação.
