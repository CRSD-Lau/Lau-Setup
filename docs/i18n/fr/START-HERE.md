<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.3.0. [English](../../../START-HERE.txt) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.3.0.
>
> **1.3.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire. Setup conserve automatiquement les fichiers existants avant de les remplacer ou de les déplacer. Les autres fichiers restent inchangés.


<!-- BEGINNER-120-STEPS -->
## Premiers pas

1. Fermez complètement WoW.
2. Téléchargez seulement `LauSetup.zip`. Sous Windows : clic droit, **Extraire tout**, ouvrez `LauSetup` puis double-cliquez `LauSetup.exe`.
3. Choisissez **Choisir le dossier…** puis le dossier contenant directement `WoW.exe`, pas `Data` ni un dossier de lanceur.
4. **Langue de l’interface** ne change que le texte de Setup : Automatique suit le système et le choix est mémorisé ; les neuf langues du jeu ne changent pas.
5. **Consécration améliorée** est activée par défaut. Les nouveaux effets exigent des modèles HD compatibles détectés ; cartes/minicarte sont facultatives.
6. Choisissez **Installer la mise à niveau**, attendez la fin sans fermer Setup, puis lancez WoW et tapez `/pyversion`. Pour annuler : fermez WoW, reprenez le même dossier et choisissez **Restaurer l’installation précédente**.

### Linux/Wine

Utilisez la même ZIP seulement avec un préfixe Wine 64-bit existant, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, les polices documentées et un stockage Linux local. Extrayez-la puis lancez `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`; ne lancez jamais l’EXE directement sous Wine.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../START-HERE.txt). Si la formulation diffère, la source anglaise fait autorité.

CONFIGURATION LAU — VERSION 3.0.8

Windows et Linux/Wine : téléchargez `LauSetup.zip` et extrayez `LauSetup/`. Sous Windows, ouvrez `LauSetup/LauSetup.exe`; sous Linux/Wine, lancez `LauSetup/LauSetup.sh`.
Pour Wine, utilisez le lanceur Linux inclus. N’exécutez pas directement l’EXE.

1. Fermez World of Warcraft.
2. Ouvrez LauSetup.exe et choisissez votre dossier WoW.
3. Choisissez vos visuels et cliquez sur Installer la mise à niveau.

Vous effectuez une mise à jour à partir d'une ancienne version ou testez la v2 ? Téléchargez d'abord le nouveau programme d'installation ; les anciennes copies intègrent l'ancien catalogue.
Sélectionnez le même client et les mêmes visuels. Les vérifications de hachage de fichier détectent les correctifs modifiés.
Démarrez WoW et tapez /pyversion ; il doit indiquer 3.0.8 Lau.

Le programme d'installation détecte la langue de votre client et la configuration du modèle HD.
La consécration améliorée est sélectionnée par défaut. Décochez-le pour le stock
apparence; le sort lui-même fonctionne toujours. Les nouveaux visuels de sorts nécessitent un
Client modèle HD compatible existant. Les cartes/mini-cartes mises à niveau sont facultatives.

Vous avez besoin d'un client WoW 3.3.5a existant, build 12340, sur Windows 10 ou 11.
Ce téléchargement est une mise à niveau et non un client ou un module linguistique complet.
Le WoW.exe compatible requis est installé automatiquement.

Aucune copie ou renommage manuel des correctifs n’est nécessaire. Ne téléchargez pas l'intégralité
diffusion de données partagées. L'application télécharge uniquement les fichiers nécessaires à votre sélection.

Les sauvegardes et les téléchargements pouvant être repris restent dans LauSetupBackups à l'intérieur de votre WoW.
dossier, en dehors de Data. Pour annuler la mise à jour, fermez WoW, rouvrez LauSetup.exe,
choisissez le même dossier et cliquez sur Restaurer l'installation précédente. La récupération aussi
fonctionne si une mise à jour interrompue a laissé WoW.exe temporairement manquant.

Vos modules complémentaires, SavedVariables, polices, illustrations de connexion, paramètres de domaine et
les correctifs non liés sont conservés. Pas de marque Pizza Warriors, personnel
La configuration ElvUI, LoginUI, les données de compte ou le client de jeu complet sont fournis.

Les téléchargements proviennent des versions GitHub ; aucun compte GitHub n’est nécessaire.
Si un téléchargement s'arrête, réessayez plus tard. Fichiers vérifiés
sont réutilisés et les téléchargements partiels reprennent. Les fichiers du jeu ne sont modifiés qu'après
tous les téléchargements requis ont réussi la vérification. Conservez LauSetupBackups si
l'application signale qu'une récupération est nécessaire.

Cet installateur n'est pas signé numériquement, donc Windows peut afficher un éditeur inconnu
avertissement. Utilisez la somme de contrôle fournie pour vérifier votre téléchargement. Ce n'est pas le cas
nécessitent la désactivation de la sécurité Windows ou l’installation des outils Python/PowerShell.
Le runtime .NET Framework 4.8 est requis.

Une fois que ce programme d'installation a ajouté la mise à niveau de la carte, il conserve cette mise à niveau pendant
changements d'édition. Utilisez Restaurer l’installation précédente pour annuler l’installation de la carte.

Crédits : Andre (lignes de base Patch-Y), Loriendal et Trimitor (fondation HD),
Contributeurs de Project Reforged (illustration HD), Blizzard (illustration originale et
texte localisé), Lau (adaptation, compatibilité, indicateurs, tests).

Author / Creator / Last Modified By: Neil Mitchell

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

Correctif 1.1.7 : l'activation des visuels de nouveaux sorts réutilise un Patch-S désactivé correspondant sans le télécharger à nouveau. La copie simplement désactivée est déplacée vers la sauvegarde de transaction vérifiée dans LauSetupBackups, même si Patch-S active correspond déjà. Différentes versions restent récupérables avec Restaurer l'installation précédente. La désactivation utilise toujours .mpq.disabled. Les archives existantes avec suffixe de hachage restent intactes.
