<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.2.0. [English](../../../PLATFORM-FEASIBILITY.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../PLATFORM-FEASIBILITY.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="lau-setup-platform-feasibility"></a>

# Faisabilité de la plateforme Lau Setup

Auteur : Neil Mitchell  
Créateur : Neil Mitchell  
Dernière modification par : Neil Mitchell  
Date d'évaluation : 2026-09-11

Mise à jour : l'utilisateur sélectionné Wine seulement. Installateur 1.1.0 fournit maintenant le testé
Wine 11 / Wine Mono 10.4.1 lanceur décrit dans [le Wine guide](wine/README.md).
Le Wine 8 l’enquête et les recommandations ci-dessous sont conservées à titre d’évaluation historique.
L'intégration de Lutris, Proton et macOS reste hors de portée.

Lau Setup 1.0.1 reste un programme d'installation de Windows. Linux à Wine est la prochaine cible de compatibilité recommandée. Cette évaluation ne certifie pas l'installation sur Linux ou macOS. Les cas précédents 63 Docker/Wine utilisaient les données du jeu, pas ce programme d'installation.

| Options | Recommandation | Ce que cela signifie pour Lau Setup |
| --- | --- | --- |
| Wine sur Linux | Première cible ; réalisable en principe, actuellement non vérifié | Réutilisez le programme d'installation de Windows dans un préfixe Wine explicitement sélectionné. Prouvez son exécution, la sélection des dossiers, les téléchargements, la sécurité des fichiers et la récupération avant de publier le support. |
| Lutris | Ensuite, après le passage direct de Wine | Une petite recette d'intégration peut lancer l'installation dans le préfixe du jeu existant. Aucun format de charge utile distinct n’est nécessaire. |
| Vapeur / Proton | Plus tard, conditionnel | Utilisez le préfixe correct du jeu existant. L'ajout d'une configuration en tant qu'autre jeu non Steam peut lui donner un environnement différent. La convivialité de Steam Deck nécessite des vérifications séparées de l’écran et du contrôleur. |
| CrossOver sur macOS | Piste d'essai plausible et séparée | Courez à l’intérieur de la bouteille du jeu. Validez sur le matériel macOS réel et les versions CrossOver prises en charge ; Les tests Linux ne peuvent pas l’établir. |
| Wine + DXVK | Configuration du jeu en option | DXVK traduit Direct3D pour le jeu. Cela ne résout pas les exigences du programme d'installation en matière de .NET, de police ou de sécurité des fichiers. |
| Whisky | Ne pas adopter comme nouvelle cible de support | Son projet en amont n'est plus activement maintenu. |

La classification ci-dessus suit les rôles décrits par [Wine Mono](https://github.com/wine-mono/wine-mono), [Lutris](https://lutris.net/about/), [Proton](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [Mac de CrossOver guide](https://support.codeweavers.com/en_US/crossover-mac-user-guide) et [Whisky](https://github.com/Whisky-App/Whisky). Les recommandations sont notre évaluation et non une certification en amont de Lau Setup. CrossOver peut exécuter des applications 32-bit Windows dans des bouteilles 64-bit ; la perte de la prise en charge native de macOS 32-bit ne l’exclut pas à elle seule.

<a id="bounded-probe-results"></a>

## Résultats de la sonde délimitée

La sonde locale utilisait Wine 8.0 (Debian 8.0~repack-4), un préfixe win32 isolé et Xvfb. Cet ancien runtime disponible localement n'est pas un test des versions actuelles de Wine. Aucun client de jeu personnel n'a été monté ou modifié.

1. L'image de test de jeu héritée a désactivé mscoree. L'activer a révélé que Wine Mono manquait. Il s'agissait d'un problème d'environnement de test.
2. Installé le fonctionnaire Wine Mono 7.4.0 MSI dans le préfixe jetable après vérification SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`, épinglé par [Wine 8.0la source](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3. Un faisceau de diagnostic initialisé WinForms et chargé le catalogue intégré, puis échoué à construire le formulaire avec `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`. La copie des polices Liberation disponibles dans ce préfixe n'a pas résolu le problème. Aucune capture d'écran ou installation réussie du programme d'installation n'a abouti.
4. Les preuves locales sont conservées sous `reports/wine-feasibility/`. Le conteneur de sonde est arrêté. Le faisceau de diagnostic n'est pas inclus dans le programme d'installation distribué ou dans le bundle de sources publiques.

Cela identifie le travail d'exécution/de provisionnement des polices, et non la preuve que Wine est impossible. Aucune transaction d'installation/restauration n'a été tentée sous Wine dans cette sonde.

<a id="acceptance-work-before-wine-support"></a>

## Travaux d'acceptation avant le support Wine

1. Établissez une combinaison Wine/runtime/police actuelle reproductible sur un bureau Linux. Afficher les états initiaux, prêts, de téléchargement, de récupération et d'erreur à des échelles d'affichage communes ; vérifiez l’accès au clavier et la sélection des dossiers.
2. Vérifiez le mappage exact du dossier hôte et la gestion de la casse sur un système de fichiers sensible à la casse, y compris les noms en double qui diffèrent uniquement selon la casse. Conservez les correctifs et les paramètres personnels non liés.
3. Prouvez le comportement de lien, de verrouillage exclusif, d'espace libre, de journal et de remplacement atomique. Le programme d'installation appelle actuellement les API d'informations sur les fichiers Windows ; leur sémantique doit être testée sous Wine plutôt que supposée.
4. Prouvez le gardien du jeu en cours d'exécution à travers les préfixes. Le code actuel énumère les processus Windows et compare les répertoires exécutables. La visibilité du préfixe Wine peut laisser un autre préfixe exécutant le même client non détecté. Résolvez ce problème avant de proposer une assistance pour une installation sécurisée ; un test réussi avec le même préfixe seul ne suffit pas.
5. Exécutez la matrice d'installation/restauration et de récupération interrompue de l'appareil, puis un téléchargement/installation/restauration anonyme et propre de GitHub en utilisant les ressources de version exactes. Testez TLS, redirections, reprise, annulation et récupération hors ligne.
6. Suivez avec une vérification en jeu dans ce même environnement pris en charge. Ensuite seulement, publiez les instructions Wine et une intégration Lutris. Gardez Proton et macOS explicitement non vérifiés jusqu'à ce que leurs propres vérifications soient réussies.

Conservez un ensemble d'actifs de jeu immuables sur les versions GitHub. N'ajoutez pas de clients complets, d'interface utilisateur personnelle ou de copies de chaque charge utile au référentiel Git pour activer un autre lanceur. Si Wine ne peut pas satisfaire les contrôles de sécurité de manière fiable, évaluez un programme d'installation natif de Linux autour des mêmes règles de manifeste et de transaction en tant qu'implémentation distincte.
