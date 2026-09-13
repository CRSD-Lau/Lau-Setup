<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../../de/README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../../es-MX/README.md) · [Français](../../../README.md) · [한국어](../../../../ko/README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../../zh-CN/README.md) · [繁體中文](../../../../zh-TW/README.md) · [Português (Brasil)](../../../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.2.0. [English](../../../../../dbc/history/INDIVIDUAL-EDITS.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../../../dbc/history/INDIVIDUAL-EDITS.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# Modifications individuelles du DBC Patch-Y : ligne de base Andre pour conserver la version multilingue Lau



<a id="read-the-chronology-first"></a>

## Lisez d'abord la chronologie

Andre a intentionnellement omis **Spell.dbc** en raison de conflits de localisation, selon Lau. Les archives Andre 3.0.3 conservées contiennent six DBC visuels/modèles ; ils ne contiennent pas de Spell.dbc. L'ajout initial de Lau a introduit la dépendance linguistique. Lau et Andre ont débogué le problème ensemble et la reconstruction multilingue l'a résolu.

Lau identifie ces étapes de développement comme 3.0.4 (ajout initial) et 3.0.5 (correctif multilingue), 3.0.6 – 3.0.8 étant des correctifs dont les numéros de version ont été modifiés. Les artefacts conservés ne correspondent pas clairement à ce souvenir : la ligne de base publiée intitulée 3.0.4 contient déjà le correctif multilingue. Ce rapport nomme explicitement les artefacts et les hachages plutôt que d’attribuer silencieusement une première version cassée à cette étiquette publiée.

[Preuve au stade de la localisation](../../../../../dbc/history/localization-stage.json) compare quatre archives v35 de pré-localisation retenues avec les versions multilingues : uniquement Spell.dbc changements, tous les champs numériques restent identiques et les liens visuels existants sont préservés. HD New Spells Off a été assemblé séparément à l’aide de données numériques d’origine.

<a id="format-and-scope"></a>

## Format et portée

Il s'agit de la comparaison de transfert Patch-Y, et non d'un audit de chaque pipeline de localisation Q/S/carte distinct. Les CSV de six éditions répertorient les modifications individuelles des tables/enregistrements/champs et toutes les valeurs d'enregistrement ajoutées. Deux fichiers gzip JSON partagés contiennent les modifications du texte des sorts décodés sans dupliquer le texte pour les variantes de Consécration. Chaque cellule de texte est `[record_id, zero_based_field, old_string_index, new_string_index]` ; résolvez les deux derniers via le tableau `strings` de ce fichier.

Les valeurs numériques sont des mots 32-bit bruts non signés, y compris les modèles de bits flottants ; les noms de schéma inconnus ne sont pas devinés. Champ Spell.dbc 131 est le lien visuel utilisé par les scripts de build. Les décalages de chaîne sont décodés avant comparaison. Le Spell.dbc ajouté utilise les données HD Patch-S conservées pour les nouveaux sorts HD activés et les données extraites du serveur de stock pour les nouveaux sorts HD désactivés et non HD. Les lignes héritées ne sont pas créditées en tant qu’enregistrements nouvellement créés.

<a id="what-the-edit-groups-mean"></a>

### Que signifient les groupes d'édition

- Champ de sort 131 : quinze liens visuels d'indicateur de raid acceptés dans chaque édition.
- Cellules de texte orthographique : population d'emplacements multilingues/de repli ; ces décomptes ne sont pas des décomptes de traductions nouvellement rédigées.
- SpellVisual, SpellVisualKit et rangées d'accessoires : routage des indicateurs, kits et configuration des accessoires du modèle.
- SpellVisualEffectName : ajout de références de modèles et de différences d'apparence de Consécration.
- CreatureDisplayInfo et CreatureModelData : inchangé par rapport à la ligne de base Andre correspondante.
- HD New Spells Off : le kit privé Rimefang utilise 90059 pour préserver le kit 90046 en amont.

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-Off-Consecration-On

| Tableau | Enregistrements modifiés/ajoutés | Différences de valeur de champ | ID ajoutés | ID supprimés |
| --- | --- : | --- : | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Aucun | Aucun |
| creaturemodeldata.dbc | 0 | 0 | Aucun | Aucun |
| spell.dbc | 49839 | 824619 | Aucun | Aucun |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Aucun |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Aucun |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Aucun |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Aucun |

| Tableau | Identifiant de l'enregistrement | Champ [0-basé] | Vieux | Nouveau |
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
| spellvisualeffectname.dbc | 2542 | 2 | sorts\consecration_impact_base.mdx | sorts\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Toutes les modifications d'enregistrement/champ et enregistrements ajoutés](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [Modifications de texte décodées](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-Off-Consécration-Off

| Tableau | Enregistrements modifiés/ajoutés | Différences de valeur de champ | ID ajoutés | ID supprimés |
| --- | --- : | --- : | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Aucun | Aucun |
| creaturemodeldata.dbc | 0 | 0 | Aucun | Aucun |
| spell.dbc | 49839 | 824619 | Aucun | Aucun |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Aucun |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Aucun |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Aucun |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Aucun |

| Tableau | Identifiant de l'enregistrement | Champ [0-basé] | Vieux | Nouveau |
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

[Toutes les modifications d'enregistrement/champ et enregistrements ajoutés](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [Modifications de texte décodées](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-On-Consecration-On

| Tableau | Enregistrements modifiés/ajoutés | Différences de valeur de champ | ID ajoutés | ID supprimés |
| --- | --- : | --- : | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Aucun | Aucun |
| creaturemodeldata.dbc | 0 | 0 | Aucun | Aucun |
| spell.dbc | 33950 | 227113 | Aucun | Aucun |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Aucun |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Aucun |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Aucun |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Aucun |

| Tableau | Identifiant de l'enregistrement | Champ [0-basé] | Vieux | Nouveau |
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
| spellvisualeffectname.dbc | 2542 | 2 | sorts\consecration_impact_base.mdx | sorts\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Toutes les modifications d'enregistrement/champ et enregistrements ajoutés](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [Modifications de texte décodées](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-On-Consecration-Off

| Tableau | Enregistrements modifiés/ajoutés | Différences de valeur de champ | ID ajoutés | ID supprimés |
| --- | --- : | --- : | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Aucun | Aucun |
| creaturemodeldata.dbc | 0 | 0 | Aucun | Aucun |
| spell.dbc | 33950 | 227113 | Aucun | Aucun |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Aucun |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Aucun |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Aucun |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Aucun |

| Tableau | Identifiant de l'enregistrement | Champ [0-basé] | Vieux | Nouveau |
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

[Toutes les modifications d'enregistrement/champ et enregistrements ajoutés](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [Modifications de texte décodées](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-Non-HD-Consécration-On

| Tableau | Enregistrements modifiés/ajoutés | Différences de valeur de champ | ID ajoutés | ID supprimés |
| --- | --- : | --- : | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Aucun | Aucun |
| creaturemodeldata.dbc | 0 | 0 | Aucun | Aucun |
| spell.dbc | 49839 | 824619 | Aucun | Aucun |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Aucun |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Aucun |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Aucun |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Aucun |

| Tableau | Identifiant de l'enregistrement | Champ [0-basé] | Vieux | Nouveau |
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
| spellvisualeffectname.dbc | 2542 | 2 | sorts\consecration_impact_base.mdx | sorts\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Toutes les modifications d'enregistrement/champ et enregistrements ajoutés](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [Modifications de texte décodées](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-Non-HD-Consécration-Off

| Tableau | Enregistrements modifiés/ajoutés | Différences de valeur de champ | ID ajoutés | ID supprimés |
| --- | --- : | --- : | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Aucun | Aucun |
| creaturemodeldata.dbc | 0 | 0 | Aucun | Aucun |
| spell.dbc | 49839 | 824619 | Aucun | Aucun |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Aucun |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Aucun |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Aucun |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Aucun |

| Tableau | Identifiant de l'enregistrement | Champ [0-basé] | Vieux | Nouveau |
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

[Toutes les modifications d'enregistrement/champ et enregistrements ajoutés](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [Modifications de texte décodées](../../../../../dbc/history/spell-text-nonhd.json.gz)
