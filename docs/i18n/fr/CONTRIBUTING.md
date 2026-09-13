<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Correctif 1.1.8** — Setup vérifie les MPQ de Data et du dossier de langue actif pour repérer les fichiers Patch-Y renommés connus et les copies exactes du catalogue. En cas de conflit possible ou d’archive illisible ou non prise en charge, il s’arrête et indique le fichier sans le supprimer automatiquement. Renommer un fichier ne change pas le hachage de son contenu. Les fichiers du jeu restent en version 3.0.8.
>
> La traduction complète n’a pas encore été actualisée, car Google limite les requêtes. Le texte existant ci-dessous correspond à un état antérieur. Les informations anglaises actuelles font référence. [English](../../../CONTRIBUTING.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

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
