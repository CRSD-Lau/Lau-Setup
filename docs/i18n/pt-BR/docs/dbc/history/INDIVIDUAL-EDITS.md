<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../../de/README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../../es-MX/README.md) · [Français](../../../../fr/README.md) · [한국어](../../../../ko/README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../../zh-CN/README.md) · [繁體中文](../../../../zh-TW/README.md) · [Português (Brasil)](../../../README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Um único ZIP agora contém o instalador do Windows e o iniciador para Linux/Wine. A interface segue automaticamente o idioma do sistema operacional entre dez opções; a escolha manual é salva. A versão 3.0.8 e os arquivos do jogo não mudam. Não há alterações de DBC.
>
> A atualização completa dos guias continua pendente devido a um HTTP 429 do Google. O texto abaixo pode estar desatualizado; consulte a fonte atual em inglês e as notas da versão 1.2.0. [English](../../../../../dbc/history/INDIVIDUAL-EDITS.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../../../dbc/history/INDIVIDUAL-EDITS.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# Edições individuais do DBC Patch-Y: linha de base Andre para compilação Lau multilíngue retida



<a id="read-the-chronology-first"></a>

## Leia a cronologia primeiro

Andre omitiu intencionalmente **Spell.dbc** devido a conflitos de localização, de acordo com Lau. Os arquivos Andre 3.0.3 retidos contêm seis DBCs visuais/de modelo; eles não contêm Spell.dbc. A adição inicial do Lau introduziu a dependência do idioma. Lau e Andre depuraram o problema juntos e a reconstrução multilíngue o resolveu.

Lau identifica esses marcos de desenvolvimento como 3.0.4 (adição inicial) e 3.0.5 (correção multilíngue), com 3.0.6–3.0.8 sendo hotfixes cujos números de versão foram alterados. Os artefatos retidos não são mapeados corretamente para essa lembrança: a linha de base publicada denominada 3.0.4 já contém a correção multilíngue. Este relatório nomeia artefatos e hashes explicitamente, em vez de atribuir silenciosamente uma construção quebrada anteriormente a esse rótulo publicado.

[Prova do estágio de localização](../../../../../dbc/history/localization-stage.json) compara quatro arquivos v35 de pré-localização retidos com as versões multilíngues: apenas Spell.dbc muda, todos os campos numéricos permanecem idênticos e os links visuais existentes são preservados. HD New Spells Off foi montado separadamente usando dados numéricos de estoque.

<a id="format-and-scope"></a>

## Formato e escopo

Esta é a comparação de transferência Patch-Y, não uma auditoria de cada pipeline de localização Q/S/mapa separado. Seis CSVs de edição listam edições individuais de tabela/registro/campo e todos os valores de registro adicionados. Dois arquivos JSON gzip compartilhados contêm alterações de texto ortográfico decodificadas sem duplicar o texto para variantes de Consagração. Cada célula de texto é `[record_id, zero_based_field, old_string_index, new_string_index]`; resolva os dois últimos por meio da matriz `strings` desse arquivo.

Os valores numéricos são palavras 32-bit brutas e não assinadas, incluindo padrões de bits flutuantes; nomes de esquemas desconhecidos não são adivinhados. Campo Spell.dbc 131 é o link visual usado pelos scripts de construção. Os deslocamentos de string são decodificados antes da comparação. O Spell.dbc adicionado usa dados HD Patch-S retidos para HD New Spells On e dados extraídos do servidor de estoque para HD New Spells Off e Non-HD. As linhas herdadas não são creditadas como registros recém-criados.

<a id="what-the-edit-groups-mean"></a>

### O que significam os grupos de edição

- Campo de feitiço 131: quinze links visuais de indicadores de ataque aceitos em cada edição.
- Soletrar células de texto: preenchimento de slot multilíngue/substituto; essas contagens não são contagens de traduções de autoria recente.
- SpellVisual, SpellVisualKit e linhas de acessórios: roteamento de indicadores, kits e configuração de acessórios de modelo.
- SpellVisualEffectName: adicionadas referências de modelo e diferenças de aparência de Consagração.
- CreatureDisplayInfo e CreatureModelData: inalterados em relação à linha de base Andre correspondente.
- HD New Spells Off: o kit privado Rimefang usa 90059 para preservar o kit upstream 90046.

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-Off-Consagração-On

| Tabela | Registros alterados/adicionados | Diferenças de valores de campo | IDs adicionados | IDs removidos |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Nenhum | Nenhum |
| creaturemodeldata.dbc | 0 | 0 | Nenhum | Nenhum |
| spell.dbc | 49839 | 824619 | Nenhum | Nenhum |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Nenhum |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Nenhum |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Nenhum |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Nenhum |

| Mesa | ID do registro | Campo [0-baseado] | Velho | Novo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | feitiços\consecration_impact_base.mdx | feitiços\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas as edições de registros/campos e registros adicionados](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [Alterações de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-Off-Consagração-Desligado

| Tabela | Registros alterados/adicionados | Diferenças de valores de campo | IDs adicionados | IDs removidos |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Nenhum | Nenhum |
| creaturemodeldata.dbc | 0 | 0 | Nenhum | Nenhum |
| spell.dbc | 49839 | 824619 | Nenhum | Nenhum |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Nenhum |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Nenhum |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Nenhum |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Nenhum |

| Mesa | ID do registro | Campo [0-baseado] | Velho | Novo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas as edições de registros/campos e registros adicionados](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [Alterações de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-On-Consagração-On

| Tabela | Registros alterados/adicionados | Diferenças de valores de campo | IDs adicionados | IDs removidos |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Nenhum | Nenhum |
| creaturemodeldata.dbc | 0 | 0 | Nenhum | Nenhum |
| spell.dbc | 33950 | 227113 | Nenhum | Nenhum |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Nenhum |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Nenhum |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Nenhum |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Nenhum |

| Mesa | ID do registro | Campo [0-baseado] | Velho | Novo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | feitiços\consecration_impact_base.mdx | feitiços\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas as edições de registros/campos e registros adicionados](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [Alterações de texto decodificado](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-On-Consagração-Desligado

| Tabela | Registros alterados/adicionados | Diferenças de valores de campo | IDs adicionados | IDs removidos |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Nenhum | Nenhum |
| creaturemodeldata.dbc | 0 | 0 | Nenhum | Nenhum |
| spell.dbc | 33950 | 227113 | Nenhum | Nenhum |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Nenhum |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Nenhum |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Nenhum |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Nenhum |

| Mesa | ID do registro | Campo [0-baseado] | Velho | Novo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas as edições de registros/campos e registros adicionados](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [Alterações de texto decodificado](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-Não-HD-Consagração-On

| Tabela | Registros alterados/adicionados | Diferenças de valores de campo | IDs adicionados | IDs removidos |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Nenhum | Nenhum |
| creaturemodeldata.dbc | 0 | 0 | Nenhum | Nenhum |
| spell.dbc | 49839 | 824619 | Nenhum | Nenhum |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Nenhum |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Nenhum |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Nenhum |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Nenhum |

| Mesa | ID do registro | Campo [0-baseado] | Velho | Novo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | feitiços\consecration_impact_base.mdx | feitiços\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas as edições de registros/campos e registros adicionados](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [Alterações de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-Não-HD-Consagração-Desligada

| Tabela | Registros alterados/adicionados | Diferenças de valores de campo | IDs adicionados | IDs removidos |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Nenhum | Nenhum |
| creaturemodeldata.dbc | 0 | 0 | Nenhum | Nenhum |
| spell.dbc | 49839 | 824619 | Nenhum | Nenhum |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Nenhum |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Nenhum |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Nenhum |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Nenhum |

| Mesa | ID do registro | Campo [0-baseado] | Velho | Novo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas as edições de registros/campos e registros adicionados](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [Alterações de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)
