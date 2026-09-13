<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.2.0. [English](../../../DBC-CHANGELOG.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../DBC-CHANGELOG.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="dbc-changelog"></a>

# Journal des modifications DBC



Suivez les modifications DBC du client séparément des modifications de modèle, de texture et d’installation. Les versions du jeu et les versions du programme d'installation sont distinctes : `/pyversion` indique l'édition du jeu.

<a id="handoff-history-andre-303-onward"></a>

## Historique de transfert : Andre 3.0.3 et suivants

[Modifications individuelles de DBC et historique de développement](docs/dbc/history/INDIVIDUAL-EDITS.md) · [Comparaison de six éditions et hachages de base](../../dbc/history/andre-to-3.0.4.json)

Andre a intentionnellement omis **Spell.dbc** pour éviter les conflits de localisation. Le remplacement initial de Lau a exposé cette dépendance ; **Lau et Andre l'ont débogué ensemble**, et la reconstruction multilingue a résolu le problème de compatibilité orthographe-texte. Les archives Andre conservées contiennent six autres DBC visuels/modèles, cela ne doit donc pas être décrit comme une absence de chaque DBC.

Lau décrit les jalons comme **3.0.4 : ajout initial de la table**, **3.0.5 : résolution multilingue** et **3.0.6–3.0.8 : correctifs avec changements de version**. Les étiquettes des premières versions se chevauchent : la version publiée archivée intitulée 3.0.4 contient déjà le correctif multilingue. Les comparaisons d'artefacts ci-dessous utilisent des hachages exacts et n'effacent pas cet historique de développement.

L'initiale Patch-Y la comparaison comprend quinze modifications de liens visuels Spell par édition, de nouveaux enregistrements d'indicateurs visuels/kits/pièces jointes, les différences de consécration et les modifications de localisation décodées. L'ajout de table est comparé à son stock sous-jacent ou à sa base HD Spell afin que les enregistrements hérités ne soient pas présentés comme un nouveau travail d'auteur. [Vérification au stade de la localisation](../../dbc/history/localization-stage.json) confirme que la reconstruction du texte a conservé les données numériques dans les quatre éditions HD/Non-HD de pré-localisation retenues.

<a id="archived-releases-304--308"></a>

## Versions archivées 3.0.4 → 3.0.8

| Transition archivée | Résultat DBC | Autres changements |
| --- | --- | --- |
| 3.0.4 → 3.0.5 | Aucune modification DBC ; 42 tableaux identiques | Géométrie du cône Sindragosa et Rotface, étiquette de version |
| 3.0.5 → 3.0.6 | Aucune modification DBC ; 42 tableaux identiques | Actifs et références des couleurs des marqueurs Coldflame/Halion, étiquette de version |
| 3.0.6 → 3.0.7 | Aucune modification DBC ; 42 tableaux identiques | Géométrie de feu de météore Halion approuvée, étiquette de version |
| 3.0.7 → 3.0.8 | Aucune modification DBC ; 42 tableaux identiques | Géométrie du cône souffle restant/Slime Spray, étiquette de version |

[Toutes les comparaisons de tables 168 et les hachages d'archives](../../dbc/history/3.0.4-through-3.0.8.json). Il s’agit de comparaisons d’artefacts de version conservés, et non d’une affirmation selon laquelle l’incident de localisation précédent ne s’est pas produit.

<a id="307--308--no-dbc-edits"></a>

## 3.0.7 → 3.0.8 — aucune modification DBC

Publié avec [Setup 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4). Toutes les **comparaisons DBC 42 ont été transmises octet par octet** : sept tables dans chacune des six éditions Patch-Y. Il n'y a pas de tables ajoutées/supprimées, d'enregistrements modifiés, de champs modifiés ou de blocs de chaînes modifiés.

| Tableau | Modifications d'enregistrement | Modifications de champ | Résultat |
| --- | --- : | --- : | --- |
| CreatureDisplayInfo.dbc | 0 | 0 | Identique |
| CreatureModelData.dbc | 0 | 0 | Identique |
| Spell.dbc | 0 | 0 | Identique |
| SpellVisual.dbc | 0 | 0 | Identique |
| SpellVisualEffectName.dbc | 0 | 0 | Identique |
| SpellVisualKit.dbc | 0 | 0 | Identique |
| SpellVisualKitModelAttach.dbc | 0 | 0 | Identique |

[Preuve de comparaison complète](../../dbc/3.0.7-to-3.0.8.json) enregistre la source/destination MPQ de chaque édition SHA-256, chaque DBC avant/après SHA-256, taille, nombre de lignes et nombre de champs. Les hachages MPQ ont été vérifiés par rapport aux catalogues de versions. L'autre 22 Les ressources du catalogue, y compris les ressources locales Q et S partagées, restent inchangées.

<a id="what-actually-changed-in-308"></a>

### Ce qui a réellement changé dans 3.0.8

Cinq modèles de cônes existants ont été élargis au **total 90°** en modifiant leur géométrie `.m2` et les limites `00.skin` correspondantes. Les liaisons DBC existantes ont été conservées.

| Tige modèle | Angle précédent | Nouvel angle |
| --- | --- : | --- : |
| PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_Glowing | 60° | 90° |
| PW_White_Fan60_30yd_Glowing | 60° | 90° |
| PW_White_Fan60_100y_Glowing | 60° | 90° |
| PW_White_Fan82_60yd_Glowing | 82° | 90° |

Les noms de fichiers conservent les étiquettes d'angle historiques ; la géométrie détermine l'angle affiché. Sindragosa était déjà 90° et n'a pas changé lors de cette transition. Cela a amené tous les indicateurs de respiration et de Slime Spray pris en charge à 90°. La portée et le timing de l'animation sont restés inchangés. Le rayon de tir du météore Halion, les couleurs de Coldflame et la consécration étaient inchangés.

Chaque édition a modifié exactement les **membres de l'archive 11** : cinq fichiers `.m2`, cinq fichiers `.skin` et l'étiquette de version du jeu `!pyandre.toc` de 3.0.7 à 3.0.8. Tous les autres membres de contenu répertoriés sont identiques. La comptabilité des conteneurs MPQ est en dehors de la comparaison des membres de contenu.

Cela vérifie les modifications du fichier client, et non la mécanique du serveur de Warmane ou une limite exacte des dommages.

<a id="setup-115-116-and-117--no-dbc-edits"></a>

## Configuration 1.1.5, 1.1.6 et 1.1.7 — aucune modification DBC

Il s'agit de correctifs d'installation. Leurs charges utiles de jeu restent 3.0.8, avec des données DBC inchangées. Le dernier correctif modifie l'installation, la préservation et la réutilisation de Patch-S, et non son contenu DBC interne.

<a id="required-entry-for-future-releases"></a>

## Entrée obligatoire pour les versions futures

Chaque version doit ajouter une entrée ici et une section **Modifications DBC** à ses notes de version GitHub, y compris les versions réservées au programme d'installation. Indiquez explicitement **Aucune modification DBC** le cas échéant. Comparez avec la version stable précédente du jeu, et non avec une version de test non publiée. Ne décrivez pas une modification de modèle/texture comme une modification DBC.

Pour chaque modification DBC réelle, enregistrez une ligne par champ (ou une différence au niveau de la ligne lisible par machine pour les changements de localisation importants) :

| Transition de jeu | Tableau | ID d'enregistrement | Nom du champ / index de base zéro | Ancienne valeur | Nouvelle valeur | Éditions / locales | Raison |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VERSION → VERSION | TABLE.dbc | ID | Champ nommé [index] | Valeur précédente | Nouvelle valeur | Variantes concernées | Objectif |

Enregistrez également les enregistrements et les tables ajoutés/supprimés, les modifications de schéma et les modifications de valeurs de chaîne. Décodez les valeurs de chaîne plutôt que de signaler l’évolution du décalage de bloc de chaîne à mesure que le contenu change. Spécifiez la convention d'index de champ et la source du schéma ; étiquetez les champs inconnus plutôt que de deviner. Joignez les hachages d'archive et de table avant/après, la méthode de comparaison et les limites de validation. Ne prétendez jamais qu’une comparaison a été faite sans preuve.

L’audit de transfert couvre Patch-Y à partir des lignes de base Andre 3.0.3 retenues. Les pipelines de localisation Q/S/carte séparés et les versions expérimentales non liées sont en dehors de cette rétrospective initiale. Aucun artefact brisé antérieur ne se voit attribuer un numéro de version sans provenance correspondante.
