<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.3.0. [English](../../../TRANSLATION.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.3.0.
>
> **1.3.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire. Setup conserve automatiquement les fichiers existants avant de les remplacer ou de les déplacer. Les autres fichiers restent inchangés.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../TRANSLATION.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="repository-translations"></a>

# Traductions du référentiel

L'action **Traduire la documentation** GitHub utilise le **site Web gratuit de Google Translate** pour que la documentation du référentiel soit disponible dans toutes les langues de jeu prises en charge, ainsi qu'en **portugais brésilien**. Aucune clé API, compte Cloud Translation payant, aucun abonnement ou téléchargement de modèle n'est requis.

Utilisez les liens linguistiques en haut du README. GitHub affiche le fichier README racine par défaut ; les visiteurs choisissent leur langue à l'aide de ces liens. Ce flux de travail traduit la documentation, y compris les guides d'installation et les références techniques. Il ne traduit pas l'interface, les problèmes, les descriptions de versions, le site Web séparé ou l'interface du programme d'installation de GitHub, et n'ajoute pas de paramètres régionaux de jeu portugais.

<a id="languages"></a>

## Langues

La couverture est vérifiée par rapport à `build/catalog.json`, avec `ptBR` ajouté à des fins de documentation. Les options de lecture sont l'anglais, l'allemand, l'espagnol pour l'Espagne et le Mexique, le français, le coréen, le russe, le chinois simplifié, le chinois traditionnel et le portugais brésilien.

Le sélecteur de langue Web de Google identifie `pt` comme étant le portugais (Brésil) ; Le portugais (Portugal) est une cible différente. Google fournit une cible `es`, de sorte que les pages Espagne et Mexique utilisent la même traduction générale en espagnol. Les cibles chinoises sont distinctes. Les codes cibles Google et les noms de langue maternelle se trouvent dans `tools/translation-locales.json`. L'ajout d'un paramètre régional de jeu nécessite l'ajout de son mappage de documentation ; la couverture manquante échoue à la validation.

<a id="automatic-updates"></a>

## Mises à jour automatiques

Les poussées de modification de la documentation anglaise, du catalogue ou des outils de traduction déclenchent l'Action. Les responsables peuvent également sélectionner **Actions → Traduire la documentation → Exécuter le workflow → principal**. Il découvre les fichiers Markdown et texte suivis dans la racine du référentiel et `docs/`, ainsi que `wine/README.txt`. Les traductions générées et `AGENTS.md` sont exclues. Les guides textuels sont rendus Markdown sous `docs/i18n/<language>/`.

Seuls les documents modifiés nécessitent une traduction. Les hachages source et sortie et un cache de segments évitent les requêtes répétées. Bump `TRANSLATION_REVISION` lors de la modification des conventions de traduction. Au maximum trois tâches linguistiques s'exécutent en même temps, avec une pause entre les requêtes dans chaque tâche. Une limite de débit arrête la tâche affectée ; réessayez plus tard. L'interface Web gratuite n'est pas officielle pour l'automatisation et peut modifier ou bloquer les demandes. Il n’y a pas de solution de rechange payante. Les pages publiées existantes restent disponibles en cas d'échec de la génération.

L’exécution standard du coureur hébergé par GitHub est gratuite pour ce référentiel public. Les tâches sont désactivées si le référentiel devient privé. Les petits artefacts intermédiaires expirent après un jour ; aucun modèle ou dépendance importante n'est stocké.

<a id="integrity-and-publication"></a>

## Intégrité et publication

Le code, les commandes, les URL, les numéros de version, les noms de produits, les crédits et les déclarations de statut de signature sont protégés. Les liens relatifs aux documents pointent vers la même langue, tandis que les liens vers les images et les codes pointent vers les originaux. Les ancres de titre en anglais stables préservent les liens de section. Chaque page s'identifie comme une traduction automatique, renvoie à sa source anglaise et conserve les métadonnées Auteur, Créateur et Dernière modification par pour **Neil Mitchell**.

Les neuf options de lecture traduites doivent réussir les contrôles d'intégrité source/sortie avant leur publication sur `main`. La publication refuse une révision de source modifiée et ne force jamais. Les demandes d'extraction exécutent des vérifications unitaires et une véritable traduction de fumée README en portugais brésilien avec un accès en lecture seule. Si la protection de la succursale empêche ultérieurement de s'engager, adaptez la publication au processus de relations publiques approuvé.

La traduction automatique nécessite encore une révision fluide par un lecteur. L'anglais fait toujours autorité. Pour des corrections durables, mettez à jour la source anglaise ou les outils de traduction ; les modifications directes des fichiers générés seront régénérées. Les lots échoués ou partiels ne remplacent pas les documents existants.

<a id="local-use"></a>

## Utilisation locale

Python 3.11 ou une version plus récente est suffisant ; aucun forfait supplémentaire n’est requis. Vérifier la structure sans accès au réseau :

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

Traduisez la documentation publique à l'aide du site Web gratuit de Google :

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

Références : [Google Translate](https://translate.google.com/), [GitHub Facturation des actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions). L'[API Google Cloud Translation](https://cloud.google.com/translate/pricing) distincte est un service facturé et n'est pas utilisé ici.
