<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.4.0. [English](../../../REVIEW.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.4.0.
>
> **1.4.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire. Setup conserve automatiquement les fichiers existants avant de les remplacer ou de les déplacer. Les autres fichiers restent inchangés.


> **1.4.0:** Choisir le dossier du jeu → Suivant → choisir l’apparence → Suivant → vérifier → Installer la mise à niveau → Terminer. Patch-Y HD ou Patch-Y Non-HD est fixé selon le client détecté. Les options supplémentaires commencent désactivées ; les cartes déjà installées sont conservées. La vérification affiche Patch-Y (version de Lau) et les options choisies, WoW.exe, Patch-Q, les fichiers de langue, le téléchargement et les sauvegardes. Suivant ne modifie aucun fichier du jeu. La langue de l’interface peut être choisie à chaque étape et est mémorisée ; Automatique suit à nouveau le système. La restauration reste disponible.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../REVIEW.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="installer-review"></a>

# Examen de l'installateur

Auteur : Neil Mitchell  
Créateur : Neil Mitchell  
Dernière modification par : Neil Mitchell

Examen de la nouvelle application par rapport à la liste de contrôle d'examen GStack, y compris un examen de sécurité indépendant en lecture seule. Tous les problèmes de mise en œuvre identifiés ont été résolus dans le cadre du travail de l'installateur agréé :

- Un exécutable manquant pourrait empêcher la sélection du client pour la récupération après incident. La sélection de dossiers découvre et valide désormais les enregistrements de récupération avant d'inspecter WoW.exe. Un test de régression GUI couvre le cas de l'exécutable manquant.
- Les téléchargements ont eu lieu avant le verrouillage des opérations. Un bail couvre désormais le cache de téléchargement via la validation ; la récupération en attente est vérifiée à l'intérieur de ce bail.
- Des temporaires prévisibles et inscriptibles pourraient suivre les liens physiques NTFS. Les temporaires de journaux et d’assemblys utilisent désormais les noms GUID avec CreateNew. Les fichiers partiels repris sont ouverts exclusivement et leur nombre de liens est vérifié avant toute troncature ou écriture. Un véritable test de régression de lien dur prouve que le fichier non lié reste inchangé.
- Un journal de restauration falsifié pourrait créer un verrou sous une autre racine avant validation. La taille, l'emplacement, la racine, les paramètres régionaux, les entrées et les chemins étendus sont désormais validés avant d'acquérir le verrou de restauration. Un test de régression prouve qu'aucun verrou étranger n'est créé.
- La restauration interrompue n'avait pas son propre état pouvant être repris. RESTORING est journalisé avant la mutation et reconnu tout au long de l'interface utilisateur et du chemin de récupération. Injection de fautes après chaque étape de restauration.
- Les options de carte installées/restaurées pourraient rester obsolètes dans l'interface utilisateur. La détection des clients est actualisée après chaque opération réussie. Le test GUI installe la sélection de carte, vérifie son état conservé, restaure et vérifie l'état précédent.

La migration GitHub épingle en outre le référentiel, la balise de version et le nom de fichier dans le catalogue intégré. Les redirections sont suivies manuellement afin que chaque destination HTTPS soit vérifiée avant une demande, y compris les informations d'identification et les vérifications de port. L'ancien analyseur de confirmation HTML de Google Drive a été supprimé. Les tests ajoutés couvrent la falsification de l'URL du catalogue, un transfert redirigé avec reprise et des destinations de redirection rejetées.

Un examen indépendant de la migration a révélé que l'optimisation de Python pouvait supprimer les contrôles de publication écrits sous forme d'assertions. Les contrôles de téléchargement, d’actualisation du catalogue et de publication génèrent désormais des exceptions explicites. Le téléchargeur résout également chaque source et exige qu'elle reste directement dans le répertoire de charge utile. Les tests de protection de publication réussissent sous `python -O` pour les chemins de fichiers, les tailles, les hachages et la falsification d'URL/de résumé à distance.

Dernière suite de régression complète : `reports/tests-20260911-200603/results.json` ; Les groupes de tests 38 ont réussi, y compris les combinaisons d'installation/restauration de luminaires réelles 108, tous les points d'interruption de validation/restauration, la protection des chemins/jonctions/liens physiques, les verrouillages de processus et de fichiers, la corruption/dérive, la gestion de la plage HTTP, l'annulation, l'assemblage hors ligne et l'installation/restauration de l'interface graphique à l'aide du véritable exécutable versionné.

La révision de l'interface utilisateur 1.0.1 couvre un texte de support plus clair, un texte de pied de page plus grand et une peinture de contrôle désactivée personnalisée. La sémantique Native Enabled reste en place ; seule l'apparence désactivée est dessinée manuellement. Les aperçus Windows initiaux, prêts et occupés, ont été inspectés visuellement. Core.cs, Downloader.cs et toutes les charges utiles du jeu restent identiques en octets à la v1.0.0. Ses preuves de jeu/réseau sont conservées ; la suite de régression Windows est réexécutée pour cette mise à jour. La sonde de faisabilité Wine n’a pas réussi la construction du formulaire et n’établit pas de support de plate-forme.

Les contrôles de publication et les métadonnées binaires finales sont des portes distinctes. Consultez la version VALIDATION.json pour connaître la portée des preuves, y compris les vérifications qui ont été conservées à partir de la ligne de base du jeu inchangée.

<a id="installer-110"></a>

## Installateur 1.1.0

La mise en œuvre du Wine fait suite à un Conseil de trois avis et à deux examens par les pairs.
Il conserve le moteur de transaction C# et nécessite un Linux authentifié en direct
assistant pour l'inspection du chemin Wine, les vérifications du processus hôte et le verrouillage des préfixes croisés.
L'assistant rejette les liens, la casse ambiguë, la visibilité restreinte du processus et
systèmes de fichiers non pris en charge. Les mappages de lecteurs Wine ne sont acceptés qu'après
inspection ciblée. La politique de processus exige de manière prudente que tous les WoW
instances à clôturer. Des contrôles répétés réduisent les courses ; ils ne verrouillent pas
programmes sans rapport ou éliminer les modifications concurrentes hostiles du système de fichiers.

L'examen ciblé de la mise en œuvre a révélé une couverture de montage et un déverrouillage imbriqués.
après une racine, renommer les lacunes. Les deux ont été corrigés : les chemins gérés et leurs plus proches
les ancêtres existants doivent rester sur le système de fichiers local du client et publier
utilise le chemin natif et le jeton enregistrés sans nécessiter que la racine existe toujours.
Les tests natifs correspondants réussissent.

Les vérifications d'espace libre interrogent désormais le cache Linux et les systèmes de fichiers clients,
au lieu de la racine du lecteur mappé de Wine. Tests de téléchargement et d'installation réels de Wine
avec zéro espace libre signalé, rejetez l’opération et conservez les fichiers originaux.

La validation inclut les groupes 38 sur Windows et 38 sur Wine, les tests d'assistance natifs 15,
8 Wine valises de sécurité comprenant deux préfixes et perte d'aide après un déplacement, un
nouvelle installation/restauration anonyme de GitHub sous Wine et un lanceur pour utilisateur normal
et transaction de montage. L'ICO W-and-shield est copié octet par octet à partir du
favicon du site de version existant. Les instantanés de l'interface utilisateur couvrent les tâches initiales, prêtes et occupées
États ; la branche prérequise Windows a été examinée et le runtime installé
chemin exercé. Aucune machine Windows dépourvue de .NET n’a été modifiée pour un test.
Le code final répète également l'installation principale et la restauration exacte avec le
octets de charge utile GitHub précédemment téléchargés et remaniés.

<a id="setup-117-review"></a>

## Configuration 1.1.7 avis

Examen de la différence actuelle pour la portée du chemin, la confiance de la source locale, la sélection de téléchargement, les vérifications de dérive en amont/validation, les sauvegardes de transactions et la compatibilité des restaurations. Aucune découverte non résolue. La réutilisation locale est limitée à la paire S racine/locale active correspondant au catalogue ; les fichiers désactivés sont déplacés dans le journal de sauvegarde vérifié existant. Les deux plates-formes ont réussi les groupes de régression 50 et l'activation/désactivation/désactivation du fichier de version réel avec une restauration empilée exacte. Aucun changement de charge utile du jeu.
