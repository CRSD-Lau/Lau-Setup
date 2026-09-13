<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.4.0. [English](../../../CONTRIBUTING.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.4.0.
>
> **1.4.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire. Setup conserve automatiquement les fichiers existants avant de les remplacer ou de les déplacer. Les autres fichiers restent inchangés.


> **1.4.0:** Choisir le dossier du jeu → Suivant → choisir l’apparence → Suivant → vérifier → Installer la mise à niveau → Terminer. Patch-Y HD ou Patch-Y Non-HD est fixé selon le client détecté. Les options supplémentaires commencent désactivées ; les cartes déjà installées sont conservées. La vérification affiche Patch-Y (version de Lau) et les options choisies, WoW.exe, Patch-Q, les fichiers de langue, le téléchargement et les sauvegardes. Suivant ne modifie aucun fichier du jeu. La langue de l’interface peut être choisie à chaque étape et est mémorisée ; Automatique suit à nouveau le système. La restauration reste disponible.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../CONTRIBUTING.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="contributing-to-lau-setup"></a>

# Contribuer à Lau Setup



Merci d'avoir aidé à améliorer l'installation et la récupération de la communauté Wrath.

<a id="community-roadmap"></a>

## Feuille de route de la communauté

Suivez le [Feuille de route communautaire](https://github.com/users/CRSD-Lau/projects/2) pour voir le travail sous forme de problèmes et les demandes d'extraction alimentent automatiquement le tableau **Arriéré**, **Prêt**, **En cours**, **Essai** et **Fait**. **Essai** les cartes incluent des listes de contrôle d'acceptation et collectent les preuves nécessaires pour terminer la validation ; utiliser [Idées](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) pour discuter des propositions avant de déposer un problème. [Notes de version](https://github.com/CRSD-Lau/Lau-Setup/releases) restent l'autorité sur ce qui est livré dans chaque version.

<a id="report-a-problem"></a>

## Signaler un problème

Utilisez le [formulaire de rapport de bug](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Incluez la version du programme d'installation, la plate-forme, les paramètres régionaux du client, les visuels sélectionnés, le comportement attendu et les étapes à reproduire. Pour les problèmes en jeu, incluez `/pyversion`, le boss ou la capacité, la difficulté et une capture d'écran. Les rapports Wine doivent inclure les versions Wine et Wine Mono.

Supprimez les noms de compte, les mots de passe, les jetons et les chemins personnels des captures d'écran ou des extraits. Ne téléchargez pas votre client, le dossier WTF, SavedVariables ou des journaux entiers. Conservez des sauvegardes locales si la récupération est en attente.

<a id="propose-a-change"></a>

## Proposer un changement

Commencez par [Limites et hypothèses connues](KNOWN-LIMITATIONS.md). Utiliser [Idées](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) pour des recommandations ; identifiez toute dépendance de serveur, de code natif ou d’action protégée avant de proposer une implémentation.

Gardez les demandes de tirage ciblées. Expliquez le problème visible par l'utilisateur, le changement et les vérifications que vous avez effectuées. Testez les opérations sur les fichiers uniquement dans des appareils isolés, jamais dans un client de jeu personnel actif.

Conservez la liste blanche des archives, les contrôles de hachage, les journaux de sauvegarde, les contrôles de processus et le verrouillage entre préfixes croisés. Ne modifiez pas les enregistrements de charge utile du jeu dans le cadre d'une mise à jour de la documentation ou de l'interface.

Le [référence technique](docs/TECHNICAL.md) explique la construction publique et les tests qui nécessitent des aménagements locaux privés. Séparez clairement une construction réussie, des tests de montage et une validation réelle dans le jeu dans votre PR.

<a id="artwork-and-attribution"></a>

## Illustration et attribution

Conservez intacts la marque W-and-shield établie et les crédits en amont. Incluez la source et les autorisations applicables pour l’œuvre d’art proposée. N’introduisez pas d’état client personnel dans les actifs publics.

<a id="dbc-release-records"></a>

## Records de sortie de DBC

Chaque version de jeu ou d'installation doit mettre à jour [DBC-CHANGELOG.md](DBC-CHANGELOG.md) et inclure une section **Modifications DBC** dans ses notes de version GitHub. Pour les modifications DBC réelles, la table de liste, l'ID d'enregistrement, le champ nommé et l'index de base zéro, les anciennes/nouvelles valeurs, les éditions/locales concernées et la raison, avec des hachages avant/après et des preuves de comparaison. Pour les DBC inchangés, enregistrez explicitement **Aucune modification DBC**. Séparez les modifications de géométrie, de texture et d’installation des modifications DBC. Consultez le journal des modifications pour connaître le format requis et les limites de validation.
