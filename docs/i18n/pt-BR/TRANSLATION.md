<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../TRANSLATION.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="repository-translations"></a>

# Traduções de repositório

A ação **Traduzir documentação** GitHub usa o **site gratuito do Google Tradutor** para manter a documentação do repositório disponível em todos os idiomas do jogo suportados, além do **Português do Brasil**. Não é necessária nenhuma chave de API, conta paga do Cloud Translation, assinatura ou download de modelo.

Use os links de idiomas na parte superior do README. GitHub exibe o README raiz por padrão; os visitantes escolhem seu idioma usando esses links. Este fluxo de trabalho traduz documentação, incluindo guias de instalação e referências técnicas. Ele não traduz a interface, problemas, descrições de lançamento, o site separado ou a interface do instalador do GitHub e não adiciona uma localidade do jogo em português.

<a id="languages"></a>

## Idiomas

A cobertura é verificada em relação a `build/catalog.json`, com `ptBR` adicionado para documentação. As opções de leitura são inglês, alemão, espanhol para Espanha e México, francês, coreano, russo, chinês simplificado, chinês tradicional e português brasileiro.

O seletor de idioma da web do Google identifica `pt` como português (Brasil); Português (Portugal) é um alvo diferente. O Google fornece um destino `es`, portanto, as páginas da Espanha e do México usam a mesma tradução geral para o espanhol. Os alvos chineses são separados. Os códigos de destino do Google e os nomes dos idiomas nativos residem em `tools/translation-locales.json`. Adicionar uma localidade de jogo requer adicionar seu mapeamento de documentação; a cobertura ausente falha na validação.

<a id="automatic-updates"></a>

## Atualizações automáticas

Empurra a alteração da documentação em inglês, o catálogo ou as ferramentas de tradução acionam a ação. Os mantenedores também podem selecionar **Ações → Traduzir documentação → Executar fluxo de trabalho → principal**. Ele descobre Markdown rastreado e arquivos de texto na raiz do repositório e `docs/`, além de `wine/README.txt`. As traduções geradas e `AGENTS.md` são excluídas. Os guias de texto são renderizados em Markdown em `docs/i18n/<language>/`.

Apenas os documentos alterados necessitam de tradução. Hashes de origem e saída e um cache de segmento evitam solicitações repetidas. Bump `TRANSLATION_REVISION` ao alterar as convenções de tradução. No máximo três trabalhos de linguagem são executados ao mesmo tempo, com uma pausa entre as solicitações em cada trabalho. Um limite de taxa interrompe o trabalho afetado; tente novamente mais tarde. A interface web gratuita não é oficial para automação e pode alterar ou bloquear solicitações. Não há substituto pago. As páginas publicadas existentes permanecem disponíveis quando a geração falha.

A execução padrão do executor hospedado em GitHub é gratuita para este repositório público. Os trabalhos serão desativados se o repositório se tornar privado. Pequenos artefatos intermediários expiram após um dia; nenhum modelo ou grande dependência é armazenado.

<a id="integrity-and-publication"></a>

## Integridade e publicação

Código, comandos, URLs, números de versão, nomes de produtos, créditos e declarações de status de assinatura são protegidos. Os links de documentos relativos apontam para o mesmo idioma, enquanto os links de imagens e códigos apontam para os originais. As âncoras de título estáveis ​​em inglês preservam os links das seções. Cada página se identifica como uma tradução automática, vincula-se à sua fonte em inglês e retém os metadados Autor, Criador e Última modificação por para **Neil Mitchell**.

Todas as nove opções de leitura traduzidas devem passar nas verificações de integridade de origem/saída antes da publicação em `main`. A publicação recusa uma revisão da fonte alterada e nunca força o push. As solicitações pull executam verificações de unidade e uma verdadeira tradução README do português brasileiro com acesso somente leitura. Se a proteção da filial impedir posteriormente a confirmação, adapte a publicação ao processo de PR aprovado.

A tradução automática ainda precisa da revisão do leitor fluente. O inglês permanece oficial. Para correções duradouras, atualize a fonte em inglês ou as ferramentas de tradução; edições diretas nos arquivos gerados serão regeneradas. Lotes reprovados ou parciais não substituem os documentos existentes.

<a id="local-use"></a>

## Uso local

Python 3.11 ou mais recente é suficiente; nenhum pacote adicional é necessário. Verifique a estrutura sem acesso à rede:

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

Traduza documentação pública usando o site gratuito do Google:

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

Referências: [Google Translate](https://translate.google.com/), [GitHub Faturamento de ações](https://docs.github.com/en/billing/concepts/product-billing/github-actions). A [API Google Cloud Translation](https://cloud.google.com/translate/pricing) separada é um serviço cobrado e não é usado aqui.
