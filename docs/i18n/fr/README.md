<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.3.0. [English](../../../README.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.3.0.
>
> **1.3.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire.


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

> Traduction automatique. [source anglaise](../../../README.md). Si la formulation diffère, la source anglaise fait autorité.

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="../../assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>Votre client. Votre langue. Votre Wrath.</strong><br />Le programme d'installation de Windows et Linux/Wine pour la mise à niveau visuelle de Lau.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">Dernière version</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">Site Web et galerie</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">Signaler un problème</a> ·
  <a href="https://github.com/users/CRSD-Lau/projects/2">Feuille de route communautaire</a>
</p>

---

Texte orthographique multilingue, illustration de chargement grand écran, indicateurs de sol personnalisés et cartes HD en option pour **WoW 3.3.5a, build 12340**. Choisissez votre client et vos visuels existants ; Lau Setup télécharge les fichiers requis, les vérifie, place les correctifs et sauvegarde les originaux.

**Installateur 1.1.7 · Version du jeu 3.0.8 Lau · Neuf langues client**

<a id="patch-s-stays-recoverable"></a>

## Patch-S reste récupérable

**Configuration du correctif 1.1.7 :** la réactivation des visuels du nouveau sort réutilise un Patch-S désactivé correspondant et déplace la copie désactivée simple dans `LauSetupBackups`, afin que les données ne conservent pas de doublon actif/désactivé. Différentes copies sont conservées dans la sauvegarde des transactions. La mise hors tension utilise toujours `.mpq.disabled`. Utilisez **Restaurer l'installation précédente** pour la récupération.

<a id="90-breath-and-slime-spray-warnings"></a>

## 90° avertissements concernant l'haleine et le Slime Spray

**3.0.8 Lau :** tous les indicateurs de respiration pris en charge et Rotface Slime Spray sont **90° au total**, suite à la confirmation du testeur Warmane. Couvre Halion dans les deux royaumes, Saviana Ragefire, Sartharion, ICC Rimefang et Sindragosa. La portée et le timing de l'animation sont préservés. Le plus grand rayon de tir de météore Halion approuvé et la Coldflame bleu clair sont inchangés.

**Déjà installé ?** Téléchargez **Configuration 1.1.7** d'abord, sélectionnez le même dossier et les mêmes visuels, puis installez. Le programme d'installation vérifie les hachages SHA-256 réels : même une modification d'un octet avec la même taille et le même horodatage est détectée. Seuls les nouveaux fichiers correspondants sont considérés comme déjà installés. `/pyversion` rapporte **3.0.8 Lau**. Les anciens installateurs conservent leur ancien catalogue intégré.

[Aperçus couleur animés et journal des modifications](https://wrath-multilingual-hd.vercel.app/#changelog)

<a id="download"></a>

## Télécharger

| Windows | Linux / Wine |
| :--- | :--- |
| **[Télécharger LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** | **[Télécharger LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** |
| Windows 10 / 11 · .NET Framework 4.8 | Wine 11.0 · Wine Mono 10.4.1 · 64-bit préfixe |
| À propos de **156 Ko** | À propos de **80 Ko** · Python 3.9+ |
| [Guide Windows](START-HERE.md) | [Guide et prérequis Wine](wine/README.md) |

Les fichiers du jeu sont téléchargés lors de l'installation. Une installation principale en anglais concerne **472 MB** avec des modèles HD et de nouveaux visuels de sorts, ou **259 MB** avec des modèles originaux. Les cartes facultatives ajoutent un téléchargement plus important ; l'installation affiche le total avant l'installation.

[Sommes de contrôle SHA-256](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [Notes de version](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [Rapport de validation](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **Apportez votre client existant.** Il s'agit d'une mise à niveau, pas d'un client de jeu complet, d'un module linguistique ou d'une base de modèle HD. L’interface de l’installateur suit automatiquement la langue du système parmi dix options ; un choix manuel est mémorisé. Les données de jeu du client prennent toujours en charge neuf paramètres régionaux et suivent les paramètres régionaux détectés du jeu.

<a id="one-setup-the-details-handled"></a>

## Une configuration. Les détails traités.

| Choisissez vos visuels | Gardez le contrôle de votre installation |
| :--- | :--- |
| Consécration améliorée ou en stock | Détection du langage client et du modèle |
| Nouveaux visuels de sorts pour les clients HD compatibles | Seuls les fichiers requis téléchargés |
| Cartes HD et textures de mini-carte en option | Vérification SHA-256 avant l'installation |
| Illustration de chargement sur écran large régional | Sauvegardes automatiques et téléchargements pouvant être repris |
| Noms de sorts localisés, rangs et info-bulles | Restauration et récupération après interruption d'opération |

<p align="center"><img src="../../assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

Vos modules complémentaires, SavedVariables, polices, illustrations de connexion, paramètres de domaine et correctifs non liés restent en place. Aucune interface utilisateur personnelle, informations d'identification ou analyses ne sont incluses.

<a id="get-started"></a>

## Commencer

1. **Fermez complètement WoW.** Sur Wine, fermez chaque instance de WoW sur tous les préfixes.
2. **Lancez l’installation et choisissez votre dossier client.** Extrayez `LauSetup.zip` dans le dossier `LauSetup/`. Sous Windows, ouvrez `LauSetup.exe`; sous Linux/Wine, lancez `LauSetup.sh`.
3. ** Choisissez vos visuels et installez. ** La consécration améliorée démarre cochée ; décochez-la pour l'apparence du stock. Les nouveaux visuels de sorts nécessitent une base de modèle HD compatible. Les cartes sont facultatives.
4. **Lancez WoW et exécutez `/pyversion`.** Confirmez l'édition installée avant de vous lancer dans le jeu.

Sur Linux, exécutez ceci à partir du dossier extrait avec votre préfixe existant :

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Utilisez le lanceur en tant qu'utilisateur normal. Il vérifie les chemins Linux, les jeux en cours d'exécution, l'espace libre et les verrous du programme d'installation sur les préfixes. Utilisez le stockage local Linux ; les dossiers liés, les partages réseau et les lecteurs montés sur Windows ne sont pas pris en charge. Le [guide Wine](wine/README.md) répertorie les polices et tous les prérequis.

Sur Windows, le programme d'installation propose la page de téléchargement officielle du .NET Framework 4.8 de Microsoft si le runtime est manquant. La configuration Wine testée utilise **Wine Mono**, et non le programme d'installation .NET Windows.

<a id="nine-client-languages"></a>

## Neuf langues clientes

English · Français · Deutsch · 한국어 · Русский · 简体中文 · 繁體中文 · Español (España) · Español (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

L'installation suit les paramètres régionaux actifs de votre client. Installez les fichiers de langue et les polices appropriés avant de modifier la configuration. La seule modification d’une valeur de configuration n’installe pas de module linguistique.

<a id="restore-with-your-backups"></a>

## Restaurer avec vos sauvegardes

Fermez WoW, rouvrez l'installation via le même lanceur, choisissez le même client et sélectionnez **Restaurer l'installation précédente**. Conservez `LauSetupBackups` dans le dossier client : il contient les originaux et les enregistrements de récupération.

Une installation ou une restauration interrompue peut être récupérée même si `WoW.exe` est temporairement manquant. Si une autre mise à jour a modifié les fichiers installés, la restauration s'arrête et conserve la sauvegarde pour la résolution. Une fois que ce programme d'installation ajoute la mise à niveau de la carte, il la conserve lors des modifications d'édition ; restaurez l'installation précédente pour annuler cette mise à niveau.

<a id="tested-with-clear-limits"></a>

## Testé, avec des limites claires

La version 1.1.7 a réussi les **groupes de régression 50 sur Windows et sur Wine**, y compris les plans de paramètres régionaux/éditions/cartes 108 par plate-forme. La version du jeu 3.0.8 a déjà passé avec succès les mises à niveau de six éditions et la détection d'un octet sur les deux plates-formes ; ses charges utiles sont inchangées. La configuration 1.1.7 couvre également la séquence d'activation de tous les drapeaux vers les nouveaux sorts désactivés avec des copies désactivées plus anciennes, des commutateurs répétés et une restauration exacte. Les charges utiles publiques ont été téléchargées de manière anonyme et vérifiées par hachage ; L'installation et la restauration réelles du noyau ont été testées.

Wine a été testé avec **Wine 11.0 / Wine Mono 10.4.1** sur le stockage local Linux, y compris le lanceur fourni en tant qu'utilisateur normal. La géométrie du feu de météore Halion correspond exactement à la v2 approuvée par les testeurs. Coldflame, les pistes d'animation, le feu natif et les tables de sorts restent identiques en octets à 3.0.7. Les animations du site Web sont des maquettes illustratives. Ces tests ne certifient pas chaque distribution Linux ou rencontre en jeu.

Les intégrations Lutris, Proton et macOS sont en dehors de cette version. Le fichier exécutable n'est pas signé numériquement.

<a id="known-limitations-and-feature-requests"></a>

## Limitations connues et demandes de fonctionnalités

Lire [Limites et hypothèses connues](KNOWN-LIMITATIONS.md) avant de suggérer une fonctionnalité : Warmane contrôle du serveur, portée des DLL/code natif, actions Lua protégées, précision et synchronisation des indicateurs, dépendances DBC et limites de plate-forme/récupération.

<a id="for-contributors"></a>

## Pour les contributeurs

- [Conception de construction, de placement d'archives et de récupération](docs/TECHNICAL.md)
- [Contribution et conseils pour signaler des bugs](CONTRIBUTING.md)
- [Examen de la mise en œuvre](REVIEW.md)
-[Portée et faisabilité de la plateforme](PLATFORM-FEASIBILITY.md)

Les charges utiles du jeu sont distribuées via les versions GitHub. Ce référentiel contient la source du programme d'installation, le catalogue, le lanceur et la documentation ; vous n'avez pas besoin de le cloner pour installer la mise à niveau.

<a id="built-on-community-work"></a>

## Construit sur le travail communautaire

**Andre** — Lignes de base de Patch-Y · **Loriendal et Trimitor** — Fondation client HD · **Contributeurs Project Reforged** — Illustration HD · **Blizzard** — Jeu original, illustration et texte localisé · **Lau** — indicateurs de masse, compatibilité, adaptations, outils de test et de version.

[Crédits complets](https://wrath-multilingual-hd.vercel.app/credits) · [Captures d'écran et aide à l'installation](https://wrath-multilingual-hd.vercel.app/)

<sub>Projet communautaire non officiel. Non affilié ou approuvé par Blizzard Entertainment. Le jeu original et les illustrations tierces restent la propriété de leurs propriétaires respectifs.</sub>

<a id="dbc-change-tracking"></a>

## Suivi des modifications DBC

Consultez le [Journal des modifications DBC](DBC-CHANGELOG.md) pour les modifications de tables/enregistrements/champs individuels et les preuves de comparaison. **3.0.7 → 3.0.8 n'a eu aucune modification DBC** : la mise à jour de l'indicateur 90° a modifié la géométrie du modèle. Les configurations 1.1.5 à 1.1.7 laissent également les données DBC inchangées.
