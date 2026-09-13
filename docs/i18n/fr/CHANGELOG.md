<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.3.0. [English](../../../CHANGELOG.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.3.0.
>
> **1.3.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../CHANGELOG.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 Hotfix - Options de commutation avec Patch-S désactivé existant

Corrige le message 1.1.5 « Un autre Patch-S désactivé existe déjà » lors de la désactivation des visuels du nouveau sort après une installation antérieure.

Le programme d'installation conserve automatiquement les deux fichiers. Le fichier S actuel devient toujours `.mpq.disabled`. Si une autre copie désactivée plus ancienne existe déjà, le programme d’installation conserve d’abord cette ancienne copie sous le nom `.mpq.disabled.<12-character hash>`. Une copie enregistrée à l'identique est réutilisée. Les deux versions sont conservées. Une copie nommée par hachage dont le contenu ne correspond pas à l'ancien fichier conservé arrête quand même l'opération pour inspection.

Cela s'applique aux fichiers S racine et aux paramètres régionaux actifs, y compris la séquence **les trois indicateurs activés -> Nouveaux visuels de sort désactivés**, les commutateurs répétés et la restauration. Le choix de la carte est conservé.

Téléchargez le nouveau ZIP EXE ou Wine et réessayez votre sélection. Vous n'avez pas besoin de supprimer ou de renommer la copie désactivée existante pour résoudre la collision ordinaire affichée par 1.1.5.

Pour annuler l'installation complète, utilisez **Restaurer l'installation précédente**. Pour réactiver manuellement un fichier S enregistré, fermez WoW et supprimez `.disabled` et tout hachage suivant, en restaurant son nom de fichier `.mpq` d'origine. N'écrasez jamais un autre fichier actif. Les modifications manuelles peuvent arrêter la restauration gérée en cas de dérive de fichiers ; conservez vos sauvegardes. Les fichiers supprimés par les installateurs avant 1.1.5 doivent encore être récupérés via leurs sauvegardes.

La version du jeu reste **3.0.8 Lau** et chaque charge utile du jeu est inchangée. Tous les cônes de degré 90, le rayon de tir de météore et Coldflame sont préservés.

Les contrôles Windows et Wine incluent les groupes de régression 46, les neuf paramètres régionaux, les fichiers désactivés existants, les interrupteurs marche/arrêt répétés, la protection contre la copie falsifiée, la récupération après interruption et la restauration exacte. Les nouveaux téléchargements publics sont testés avec de vrais fichiers de version On/Off et une ancienne copie désactivée présente. Il s'agit d'une validation de l'installateur, pas d'une validation d'une nouvelle rencontre dans le jeu.

[ZIP Patch-Y brut en six éditions](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Aide à l'installation et journal des modifications](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup Correctif 1.1.5 - Conserver les fichiers Patch-S désactivés

La désactivation des **Nouveaux visuels de sorts** préserve désormais les fichiers racine et locaux actifs Patch-S à côté de leurs emplacements d'origine sous le nom `.mpq.disabled`, plutôt que de les laisser uniquement dans les sauvegardes du programme d'installation. Leurs octets sont vérifiés avant et après le changement. WoW ne charge pas le nom de fichier désactivé.

- Une autre copie existante de `.disabled` bloque l'installation ; il n'est jamais écrasé.
- Une copie identique désactivée est réutilisée et conservée.
- L'activation de l'option installe les fichiers S actifs de la version sélectionnée et conserve les copies désactivées.
- Les installations répétées, la restauration et la récupération après interruption couvrent à la fois les chemins actifs et désactivés.

Pour réactiver manuellement un fichier désactivé, fermez WoW et supprimez uniquement le suffixe `.disabled`. N'écrasez pas un autre fichier actif. Pour annuler l'installation complète de Lau, utilisez **Restaurer l'installation précédente** ; la suppression uniquement de Patch-Y n'annule pas Q/M/exécutable ou d'autres modifications. Les modifications manuelles des fichiers peuvent entraîner l'arrêt de la restauration gérée en cas de dérive, alors conservez les sauvegardes.

**Déjà affecté par un ancien programme d'installation ?** Cette mise à jour n'extrait pas automatiquement les anciennes sauvegardes. Utilisez Restaurer l'installation précédente pour récupérer ces fichiers, en remontant dans toutes les installations empilées, avant de les réinstaller avec la nouvelle configuration. Conservez LauSetupBackups.

La version du jeu reste **3.0.8 Lau**. Tous les MPQ sont inchangés : les respirations à degrés 90/Spray Slime, approuvés +50%, le rayon de feu de météore Halion et la flamme froide sont préservés. Téléchargez le nouveau ZIP EXE ou Wine pour le correctif du programme d'installation.

La validation Windows et Wine est incluse dans VALIDATION.json. Les tests couvrent les neuf paramètres régionaux, les collisions de copie désactivée, les transitions marche/arrêt, les installations répétées, l'interruption à chaque étape de déplacement/restauration, la dérive des fichiers et la restauration exacte. Le correctif ne revendique pas la validation de nouvelles rencontres dans le jeu.

[ZIP Patch-Y brut en six éditions (3.0.8 inchangé)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Aide à l'installation et journal des modifications](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · Sortie du jeu 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## Correctif 1.1.7 - Patch-S réactive le nettoyage

- La réactivation des visuels du nouveau sort réutilise un Patch-S désactivé lorsque son SHA-256 et sa taille correspondent à la version sélectionnée, évitant ainsi ce téléchargement.
- La copie simplement désactivée est transférée dans la sauvegarde de transaction vérifiée en dehors des données, même si le Patch-S actif correspond déjà. Différents fichiers désactivés restent récupérables via la restauration de l'installation précédente.
- S'applique à la racine et aux paramètres régionaux actifs Patch-S. Off utilise toujours le nom de fichier simple `.mpq.disabled`. Les archives existantes avec suffixe de hachage restent intactes.
- Les charges utiles du jeu restent 3.0.8 Lau. Windows et Wine ont chacun réussi les groupes de régression 50, la commutation marche/arrêt/marche de fichier réel et la restauration exacte.

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## Tous les avertissements concernant l'haleine et le Slime Spray sont désormais 90°

Suite à la confirmation du testeur Warmane, Halion (les deux royaumes), Saviana Ragefire, Sartharion, ICC Rimefang et Rotface Slime Spray utilisent désormais **Cônes totaux 90°**, correspondant à l'avertissement 90° existant de Sindragosa. Cela s'applique aux six éditions et aux neuf langues clientes, y compris les mappages de sorts normaux/héroïques existants.

Seule la largeur du cône change. La portée, le timing de l'animation, les effets des sorts natifs et les tables de sorts sont préservés. Le rayon de feu de météore Halion plus grand approuvé 50%, la flamme froide bleu clair, les couleurs et la consécration sont inchangés. Ce sont des tampons d'avertissement visuels ; Les dégâts et la mécanique du serveur sont inchangés. Un terrain inégal peut encore couper des cônes plats.

<a id="updating"></a>

## Mise à jour

Téléchargez d'abord **LauSetup.exe** ou **LauSetup-Wine.zip** à partir de cette version. Fermez WoW, sélectionnez le même client et les mêmes visuels, puis cliquez sur **Installer la mise à niveau**. Les anciens installateurs conservent leurs anciens catalogues. Vérifiez `/pyversion` pour **3.0.8 Lau**.

Le programme d'installation vérifie les hachages SHA-256 réels, de sorte que les versions précédentes et même les modifications d'un octet avec une taille et un horodatage inchangés sont détectées. Seuls les fichiers actuels exacts sont considérés comme déjà installés. Les sauvegardes et la restauration de l'installation précédente restent disponibles.

Windows nécessite .NET Framework 4.8. Les utilisateurs de Wine extraient les quatre fichiers et exécutent `LauSetup.sh` en tant qu'utilisateur normal avec le préfixe Wine/Mono existant pris en charge. Les installateurs d'exécution ne sont pas regroupés.

<a id="validation"></a>

## Validation

Voir VALIDATION.json pour la régression Windows et Wine, les mises à niveau en six éditions de 3.0.7, la détection répétée, les vérifications d'un octet, les vérifications de restauration et de téléchargement public. Les contrôles géométriques vérifient les cônes 90°, la plage préservée, les limites valides et l'enroulement du triangle dans chaque édition. Exactement onze membres d'archives existants changent : cinq modèles, leurs cinq skins et la version TOC. Tous les autres membres sont identiques en octets à 3.0.7.

La décision en matière de largeur fait suite aux tests Warmane rapportés. Cette version ne constitue pas une certification à chaque rencontre ou une certification exacte des limites du serveur.

[Journal des modifications du site Web et aide à l'installation](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · Sortie du jeu 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## Avertissements de tirs de météores Halion plus importants

Favorise le **test v2** approuvé par les testeurs : le rayon du marqueur au sol rouge de Halion est **50% plus grand que la version 3.0.6**, autour des sentiers et des tirs d'atterrissage. Le test v3 n'est pas inclus. Coldflame, les couleurs, les pistes d'animation, les flammes natives, la Consécration et les cônes Sindragosa/Rotface sont inchangés. Les six éditions et les neuf langues client sont prises en charge.

Le testeur a confirmé la v2 après avoir corrigé un patch non mis à jour. Il s'agit d'un tampon d'avertissement visuel, et non d'une modification des dommages causés au serveur ou d'une certification de chaque position ou rencontre.

<a id="update-with-the-new-installer"></a>

## Mettre à jour avec le nouvel installateur

Téléchargez d'abord **LauSetup.exe** ou **LauSetup-Wine.zip** à partir de cette version. Fermez WoW, sélectionnez le même client et les mêmes visuels, puis cliquez sur **Installer la mise à niveau**. Les anciens installateurs conservent les anciens catalogues. `/pyversion` rapporte **3.0.7 Lau**.

Les utilisateurs existants de 3.0.6 et de test v2 reçoivent la mise à jour. Le programme d'installation compare les hachages de fichiers réels, y compris les modifications d'un octet avec une taille et un horodatage inchangés ; seuls les fichiers actuels exacts comptent comme déjà installés. Les sauvegardes et la restauration de l'installation précédente restent disponibles.

Windows nécessite .NET Framework 4.8. Les utilisateurs de Wine extraient les quatre fichiers et exécutent `LauSetup.sh` en tant qu'utilisateur normal avec le préfixe Wine/Mono existant pris en charge. Aucun programme d'installation d'exécution n'est fourni.

<a id="validation-1"></a>

## Validation

La régression du programme d'installation Windows et Wine, les mises à niveau en six éditions, la détection de répétition, les vérifications d'un octet, les vérifications de restauration et de téléchargement public sont enregistrées dans VALIDATION.json. Les modèles et skins Halion sont identiques en octets pour tester la v2. Seules leur géométrie/limites et la version TOC diffèrent de 3.0.6 ; Coldflame et les autres membres des archives restent inchangés.

[Journal des modifications du site Web et aide à l'installation](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · Sortie du jeu 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## Blue Coldflame, feu de météore rouge

- **Marrowgar Coldflame :** cercles bleu clair avec la lueur vers l'intérieur existante et l'animation dans le sens des aiguilles d'une montre, y compris héroïque.
- **Feu de météores Halion :** déclenche des cercles rouges autour des sentiers et un tir d'atterrissage avec l'animation existante dans le sens des aiguilles d'une montre.
- Les six éditions HD/Non-HD et neuf langues client. Les flammes natives, les durées, les choix de Consécration et les cônes 90° Sindragosa / 60° Rotface sont inchangés.

[Aperçus couleur animés et journal des modifications complet](https://wrath-multilingual-hd.vercel.app/#changelog). Les aperçus sont des maquettes illustratives et non des enregistrements du jeu. Les dégâts et la mécanique du serveur sont inchangés ; les bords d’avertissement restent des tampons visuels.

<a id="already-installed-download-the-new-installer-first"></a>

## Déjà installé ? Téléchargez d'abord le nouveau programme d'installation

Téléchargez **LauSetup.exe** ou **LauSetup-Wine.zip** à partir de cette version. Fermez WoW, choisissez le même dossier et les mêmes paramètres visuels, puis cliquez sur **Installer la mise à niveau**. Les anciens installateurs téléchargés conservent leur ancien catalogue intégré.

Le programme d'installation hache les fichiers réels. Les anciens fichiers 3.0.5 sont remplacés ; même une modification d'un octet avec une taille de fichier et un horodatage identiques est détectée. Seuls les nouveaux fichiers exacts sont traités comme déjà installés. `/pyversion` rapporte **3.0.6 Lau**. Les sauvegardes et la restauration de l'installation précédente restent disponibles.

Utilisateurs de Wine : extrayez les quatre fichiers ensemble et exécutez `LauSetup.sh` en tant qu'utilisateur normal avec votre préfixe 64-bit Wine 11.0 / Mono 10.4.1. Python 3.9+ et le stockage local Linux sont requis. Windows nécessite .NET Framework 4.8. Les runtimes ne sont pas regroupés.

<a id="fresh-verification-on-windows-and-wine"></a>

## Nouvelle vérification sur Windows et Wine

- Groupes de régression 38 par plate-forme, y compris les plans de localisation/édition/carte 108 chacun.
- Les six mises à niveau réelles de 3.0.5 à 3.0.6, répétition des installations sans opération et restauration exacte sur les deux plates-formes.
- Modifications d'un octet de même taille/même horodatage détectées et réparées indépendamment à la racine et aux paramètres régionaux Y sur les deux plates-formes.
- Téléchargements anonymes de la charge utile GitHub, installations de base réelles et restauration sur Windows et Wine.
- Tests de sécurité de l'hôte 15 Linux et lanceur Wine exact à quatre fichiers sous un utilisateur normal ; Rendu du formulaire Windows vérifié.
- Trois références de texture du marqueur M2 et la version TOC modifiée par édition ; deux textures de couleurs ajoutées. Tous les autres membres ont conservé octet par octet.

Ces vérifications d'installation ne certifient pas chaque distribution Linux ou chaque rencontre dans le jeu. Le fichier exécutable n'est pas signé numériquement. Des preuves détaillées, des sommes de contrôle et la source sont jointes.

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · Sortie du jeu 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## Avertissements de raid plus larges

- Sindragosa Frost Breath : **75° → 90° total** (7.5° supplémentaire par côté).
- Rotface Slime Spray : **25° → 60° total** (17.5° supplémentaire par côté).
- Appliqué aux six éditions HD/Non-HD et disponible avec les neuf paramètres régionaux client. Les autres indicateurs, paramètres de consécration, tableaux localisés et illustrations sont inchangés.

Il s'agit d'avertissements visuels mis en mémoire tampon informés par les images de raid Warmane et les journaux de sorts. Ils ne modifient pas les dégâts ou la mécanique du serveur, ni ne revendiquent une limite exacte des dégâts.

<a id="updating-an-existing-installation"></a>

## Mise à jour d'une installation existante

Téléchargez d'abord le nouveau **LauSetup.exe** ou **LauSetup-Wine.zip**. Fermez WoW, sélectionnez le même dossier et les mêmes choix visuels, puis cliquez sur **Installer la mise à niveau**. Le programme d'installation compare les hachages de fichiers réels : les anciens correctifs 3.0.4 sont remplacés, tandis qu'une installation exacte de 3.0.5 est signalée comme étant déjà installée. `/pyversion` rapporte **3.0.5 Lau** après la mise à jour. Les anciens installateurs téléchargés conservent leur ancien catalogue.

Les téléchargements Windows et Wine incluent le même exécutable d'installation reconstruit. Pour Wine, extrayez les quatre fichiers ensemble et utilisez `LauSetup.sh` comme décrit dans le fichier README inclus. Les exigences d’exécution existantes restent inchangées.

<a id="verification"></a>

## Vérification

Tous les groupes de régression 38 Windows ont réussi, y compris les plans de paramètres régionaux/éditions/cartes 108. Les six éditions ont passé avec succès les vérifications réelles de mise à niveau, de réinstallation et de restauration de 3.0.4 à 3.0.5. Les nouvelles charges utiles ont réussi les contrôles de téléchargement/hachage anonymes ; une installation principale isolée de GitHub et une restauration réussie. Chaque édition conserve chaque membre à l'exception de quatre fichiers de modèle/géométrie et de la version TOC.

Le code du lanceur Wine est inchangé et le ZIP contient l’EXE exactement reconstruit. Les preuves d'exécution antérieures de Wine 11.0 / Mono 10.4.1 sont conservées ; la nouvelle exécution de Wine n'était pas disponible car le moteur Docker n'a pas démarré. La nouvelle géométrie du cône est vérifiée statiquement et non nouvellement certifiée dans le jeu.

Les sommes de contrôle de téléchargement, la source et le rapport de validation détaillé sont joints. Conservez `LauSetupBackups` pour la récupération.

Author / Creator / Last Modified By: Neil Mitchell
