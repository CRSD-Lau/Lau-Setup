<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **Version actuelle : Setup 1.4.0 / jeu 3.0.9 Lau.** Fermez WoW, extrayez tout LauSetup.zip, ouvrez LauSetup.exe sous Windows et choisissez avec Browse... le dossier contenant WoW.exe. Suivant → visuels → Suivant → vérification → installation → terminé. Toutes les options supplémentaires sont désactivées au départ. WoW.exe et les écrans de chargement forment une seule option ; les cartes sont indépendantes et incluent les fichiers WDM. Les cartes déjà installées sont conservées. Les doublons renommés restent en place ; seul un Patch-V vide est sauvegardé automatiquement. Les fichiers remplacés sont sauvegardés dans LauSetupBackups. Aucun DBC de Patch-Y ne change ; les cartes optionnelles ajoutent des tables amont documentées. Les cartes de grottes restent en bêta. Linux/Wine utilise LauSetup.sh avec les prérequis documentés. La traduction complète reste bloquée par Google HTTP 429. Le texte ancien ci-dessous sert uniquement de référence historique ; consultez la source anglaise pour les instructions actuelles.
>
> [English](../../../START-HERE.txt) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

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
