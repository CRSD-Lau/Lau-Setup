<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.2.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.2.0. [English](../../../../wine/README.txt) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.2.0.


<!-- BEGINNER-120-STEPS -->
## Premiers pas

1. Fermez complètement WoW.
2. Téléchargez seulement `LauSetup.zip`. Sous Windows : clic droit, **Extraire tout**, ouvrez `LauSetup` puis double-cliquez `LauSetup.exe`.
3. Extrayez `LauSetup.zip`. Conservez les cinq fichiers de `LauSetup/` ensemble : `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` et `README.txt`.
4. **Langue de l’interface** ne change que le texte de Setup : Automatique suit le système et le choix est mémorisé ; les neuf langues du jeu ne changent pas.
5. **Consécration améliorée** est activée par défaut. Les nouveaux effets exigent des modèles HD compatibles détectés ; cartes/minicarte sont facultatives.
6. Choisissez **Installer la mise à niveau**, attendez la fin sans fermer Setup, puis lancez WoW et tapez `/pyversion`. Pour annuler : fermez WoW, reprenez le même dossier et choisissez **Restaurer l’installation précédente**.

### Linux/Wine

Utilisez la même ZIP seulement avec un préfixe Wine 64-bit existant, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, les polices documentées et un stockage Linux local. Extrayez-la puis lancez `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`; ne lancez jamais l’EXE directement sous Wine.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../../wine/README.txt). Si la formulation diffère, la source anglaise fait autorité.

Lau Setup pour Wine sur Linux
Author / Creator / Last Modified By: Neil Mitchell

1. Utilisez un client WoW 3.3.5a build 12340 existant sur un système de fichiers Linux local.
2. Fermez chaque instance WoW, y compris les jeux dans d'autres préfixes Wine.
3. Extrayez `LauSetup.zip`. Conservez les cinq fichiers de `LauSetup/` ensemble : `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` et `README.txt`.
4. Ouvrez un terminal dans le dossier extrait et exécutez :

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5. Choisissez votre dossier de jeu existant et installez-le. Les sauvegardes automatiques habituelles
   et le bouton Restaurer l’installation précédente sont disponibles.

Conditions requises pour cette version :
- Wine 11.0, un préfixe 64-bit et Wine Mono 10.4.1 déjà installés.
- Python 3.9 ou version ultérieure pour l'assistant de sécurité hôte (bibliothèque standard uniquement).
- Polices Liberation Sans ou DejaVu Sans ; le package de polices Wine complet doit
  également être installé pour que les contrôles par défaut de Wine Mono puissent être rendus.
- Stockage local Linux. Les partages réseau et les lecteurs montés sur Windows sont exclus.
- Visibilité normale du processus hôte. N'exécutez pas ce lanceur via un bac à sable
  qui cache d'autres processus Wine. Exécutez en tant qu'utilisateur normal, jamais sudo/root.

Le préfixe 64-bit peut contenir le client 32-bit WoW. Ce programme d'installation ne
créez, convertissez ou mettez à niveau votre préfixe Wine, installez Wine/Mono, configurez
DXVK, ou changez votre lanceur de jeu. Utilisez la configuration Wine de votre distribution
instructions en premier si son runtime est manquant.

Package officiel Wine Mono pour ce runtime testé :
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

Utilisez le runtime Wine Mono avec Wine. Le programme d'installation de Windows .NET Framework est
n'est pas fourni et n'est pas requis par cette configuration Wine Mono testée.

Lancez toujours via LauSetup.sh. Exécution de LauSetup.exe directement sous Wine
refusera les opérations du client sans l'assistant Linux. Il vérifie les chemins des hôtes
et traite et détient un verrou d'hôte partagé entre les préfixes Wine. Si ça s'arrête,
rouvrez le lanceur et restaurez l'installation en attente avant de réessayer.

Gardez WoW fermé jusqu'à la fin de l'installation. Les contrôles de processus réduisent les courses ; ils ne peuvent pas
empêcher un autre programme de lancer le jeu ou de modifier des fichiers par la suite.
Les chemins symboliques, les liens physiques et la casse des noms de fichiers ambigus sont rejetés. Données
et les répertoires de sauvegarde doivent rester sur le même système de fichiers que le client.

Périmètre de validation : clients Wine 11.0 / Wine Mono 10.4.1 isolés, luminaires et
tests d'installation/restauration de charge utile réelle, tests de sécurité à deux préfixes et interface graphique échantillonnée
chèques. Il ne s'agit pas d'une certification de chaque distribution, système de fichiers, Linux.
échelle d'affichage, version Wine ou rencontre de jeu. Pas de Lutris, Proton ou macOS
l'intégration est incluse dans cette version.

L’interface de l’installateur suit automatiquement la langue du système parmi dix options ; un choix manuel est mémorisé. Les données de jeu du client prennent toujours en charge neuf paramètres régionaux et suivent les paramètres régionaux détectés du jeu.

Configuration 1.1.7 : Les nouveaux visuels de sorts désactivés conservent Patch-S sous la forme .mpq.disabled à côté de
son chemin originel. Une autre copie désactivée n’est jamais écrasée.
Pour annuler l'installation complète, utilisez Restaurer l'installation précédente. Pour les fichiers
déjà supprimés par les anciennes versions d'installation, récupérez-les à partir de ces sauvegardes
en utilisant Restaurer l’installation précédente avant de réinstaller. Conservez LauSetupBackups.

Le fichier S actuel devient toujours .mpq.disabled. Si une personne âgée handicapée
copie existe, le programme d'installation la conserve d'abord sous le nom `.mpq.disabled.<12-character hash>`. Pas de changement de nom manuel
est nécessaire pour changer d’option. La réactivation manuelle nécessite la suppression
.disabled et tout hachage suivant, avec WoW fermé et aucun autre actif
fichier en cours d'écrasement. Utilisez Restaurer l’installation précédente pour une restauration gérée.

1.1.7 réactive le nettoyage : la correspondance désactivée Patch-S est réutilisée localement. La copie simplement désactivée est déplacée vers la sauvegarde de transaction vérifiée dans LauSetupBackups, laissant un S actif. Différentes copies restent récupérables via la restauration de l'installation précédente. Les archives existantes avec suffixe de hachage ne sont pas balayées.
