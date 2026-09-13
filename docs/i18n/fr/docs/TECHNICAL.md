<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../../es-MX/README.md) · [Français](../README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — Une seule archive ZIP contient désormais l’installateur Windows et le lanceur Linux/Wine. L’interface suit automatiquement la langue du système d’exploitation parmi dix options ; un choix manuel est mémorisé. La version 3.0.8 et les fichiers du jeu restent inchangés. Aucune modification DBC.
>
> La mise à jour complète des guides reste en attente à cause d’une erreur Google HTTP 429. Le texte ci-dessous peut être ancien ; consultez la source anglaise actuelle et les notes 1.4.0. [English](../../../TECHNICAL.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **Téléchargement actuel :** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) pour Windows et Linux/Wine. Extrayez le dossier `LauSetup/` avec cinq fichiers : Windows ouvre `LauSetup.exe` ; Linux/Wine lance `LauSetup.sh`. Les anciennes instructions ci-dessous sur des ZIP Wine ou EXE séparés ne s’appliquent pas à 1.4.0.
>
> **1.4.0:** Les fichiers de mise à niveau supplémentaires reconnus sont sauvegardés et l’installation continue. La restauration les remet en place. Aucun déplacement manuel nécessaire. Setup conserve automatiquement les fichiers existants avant de les remplacer ou de les déplacer. Les autres fichiers restent inchangés.


> **1.4.0:** Choisir le dossier du jeu → Suivant → choisir l’apparence → Suivant → vérifier → Installer la mise à niveau → Terminer. Patch-Y HD ou Patch-Y Non-HD est fixé selon le client détecté. Les options supplémentaires commencent désactivées ; les cartes déjà installées sont conservées. La vérification affiche Patch-Y (version de Lau) et les options choisies, WoW.exe, Patch-Q, les fichiers de langue, le téléchargement et les sauvegardes. Suivant ne modifie aucun fichier du jeu. La langue de l’interface peut être choisie à chaque étape et est mémorisée ; Automatique suit à nouveau le système. La restauration reste disponible.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../TECHNICAL.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="technical-reference"></a>

# Référence technique



[Retour à Lau Setup](../README.md)

<a id="build-and-verification"></a>

## Construction et vérification

Exécutez `tools/build.ps1` sur Windows avec le compilateur .NET Framework installé. Le bundle source public contient l'application, le catalogue intégré, le script de build et la documentation. La caisse de développement complète contient en outre `tools/test.ps1` pour les tests de transaction, de téléchargement, de chemin, de processus, de récupération et de régression de l'interface graphique ; ces tests utilisent des appareils isolés et un exécutable de référence local. `tools/build.ps1 -Release` refuse un catalogue qui n'a pas franchi la porte de publication. Le faisceau de tests, la génération de charge utile et les tests de jeu natifs dépendent de chemins de source locaux privés et ne font pas partie du bundle de sources publiques.

`build/catalog.json` nomme chaque actif et segment de téléchargement par taille et SHA-256, ainsi que les URL de version GitHub observées. Le catalogue épingle le référentiel, la balise de version et le fichier nommé par hachage. Le programme d'installation télécharge de manière anonyme et vérifie chaque redirection avant de la suivre. Aucun compte GitHub, navigateur connecté ou identifiant API n'est requis par le programme d'installation. Lors de la vérification du développement complet, `tools/refresh_github_catalog.py` associe les actifs téléchargés sans modifier les hachages, et `tools/verify-public.ps1` vérifie chaque segment et actif reconstruit via le même téléchargeur utilisé par l'application.

<a id="file-placement"></a>

## Placement de fichier

| Composant | Destination |
|---|---|
| Exécutable compatible | `WoW.exe` |
| Q régional sélectionné | Copies identiques dans la racine `Data/patch-q.mpq` et les paramètres régionaux actifs `Data/<locale>/patch-<locale>-Q.MPQ` |
| Édition sélectionnée Y | Copies identiques dans la racine `Data/patch-y.mpq` et les paramètres régionaux actifs `Data/<locale>/patch-<locale>-Y.MPQ` |
| Nouveaux actifs de sorts, lorsqu'ils sont sélectionnés | Racine `Data/patch-s.mpq` |
| Tables de sorts localisées correspondantes, lorsque sélectionnées | Paramètres régionaux actifs `Data/<locale>/patch-<locale>-S.MPQ` |
| Cartes/minicarte facultatives | Racine `Data/patch-m.mpq` ; le paramètre local actif remplacé M est sauvegardé |

Core Q conserve le LoadingScreens.dbc de la version, le Map.dbc localisé et charge les images octet par octet. Il omet les définitions de carte du monde et les illustrations de carte du monde ajoutées. Le mode carte complète utilise le Q régional d'origine et le M partagé sans les reconditionner. Les deux emplacements S contiennent des archives différentes. La désactivation des nouveaux sorts préserve la paire racine/locale S étendue sous la forme .mpq.disabled ; la réactivation déplace les copies désactivées vers des sauvegardes de transactions vérifiées, comme décrit dans la section Configuration 1.1.7 ci-dessous. La détection HD nécessite les correctifs F racine et régionaux existants correspondants.

<a id="recovery-design"></a>

## Conception de récupération

Un verrou client couvre le téléchargement, la préparation et l’installation. Les fichiers sont vérifiés avant la préparation et à nouveau après le placement. Les fichiers existants sont déplacés vers `LauSetupBackups/transactions/<id>/before/`, en préservant leurs octets et leurs horodatages ; le journal est rédigé de manière durable avant de s'engager. Un commit échoué restaure les originaux lorsqu’ils sont sûrs. Les validations interrompues et les restaurations interrompues restent détectables à la réouverture de l'application, même sans WoW.exe.

La restauration refuse les fichiers modifiés par une autre mise à jour et conserve la sauvegarde pour une résolution manuelle. Seuls les chemins Q/M/S/Y racine/locale active exacts et WoW.exe sont acceptés. Les traversées, les flux alternatifs et les points d'analyse sont rejetés ; les fichiers repris en écriture doivent avoir un lien physique. Les temporaires de journaux et d’assemblages utilisent des noms uniques et des créations exclusives. L'application n'énumère jamais une archive dans le système de fichiers client.

<a id="release-boundaries"></a>

## Limites de publication

Cet installateur n'est pas signé numériquement. Les tests d'installation Windows et Wine, les vérifications échantillonnées de l'interface graphique et la base de données de jeu conservée sont enregistrés séparément dans VALIDATION.json. Les contrôles Wine 1.1.0 utilisent Wine 11.0 / Wine Mono 10.4.1 et le stockage de superposition Docker local ; le test de montage imbriqué se moque de l'identité du périphérique car ce conteneur ne peut pas créer de montages. Ces vérifications ne certifient pas chaque distribution/système de fichiers Linux, échelle d'affichage, rencontre ou modification de client tiers. Les ZIP bruts de l'édition Patch-Y sont disponibles sur les versions GitHub. Voir [limitations connues](../KNOWN-LIMITATIONS.md) pour connaître la portée et les hypothèses actuelles.


<a id="306-color-update--setup-112"></a>

## 3.0.6 mise à jour des couleurs/configuration 1.1.2

Chacune des six archives Y modifie trois membres M2 et la table des matières !PYAndre, et ajoute deux textures BLP. `Spells/PW_Coldflame_Ground.m2` fait désormais référence à `Spells/PW_Coldflame_Blue.blp` ; `Spells/PW_HalionMeteor_Ground.m2` et `Spells/PW_HalionMeteor_Ring.m2` référence `Spells/PW_Halion_Red.blp`. Seule la longueur/décalage du nom de fichier du descripteur de texture 4 change dans chaque modèle d'origine ; le nouveau chemin est ajouté. Les textures de particules natives (indices 0 – 3), les skins, la géométrie, les pistes d'animation globales, les limites et les octets DBC sont inchangés. La texture blanche partagée reste inchangée pour les autres indicateurs.

Les nouvelles textures préservent le format opaque 8×8 DXT1 BLP2 existant et les quatre niveaux MIP. Seul le point final RGB565 change : le bleu clair décode comme (120,216,248,255), le rouge comme (248,68,40,255). La quantification est inhérente au format de texture existant. Les deux modèles Halion utilisent la même texture rouge. Les choix de consécration et d’édition du modèle restent indépendants.

Les décisions de mise à jour comparent le SHA-256 réel et sa taille, et non les étiquettes de version ou les horodatages. Les tests de régression modifient un octet sans changer la taille du fichier ni l'horodatage à chaque emplacement Y, nécessitent exactement une opération de réparation, vérifient le hachage réparé, puis restaurent la version précédente. Un ancien EXE intègre l'ancien catalogue, donc la mise à niveau nécessite d'abord de télécharger le nouveau EXE/ZIP.

<a id="307-halion-radius--setup-113"></a>

## 3.0.7 Rayon Halion / Configuration 1.1.3

Favorise les octets test-v2 exacts pour `Spells/PW_HalionMeteor_Ground.m2`, `Spells/PW_HalionMeteor_Ring.m2` et leurs fichiers `00.skin`. Les coordonnées X/Y du maillage sont 1.5 fois 3.0.6. Les Z/UV/normales et les pistes d'animation/particules sont préservées. Les limites du modèle (décalage 160), les limites de séquence (séquence +32) et les limites du sous-maillage de peau (sous-maillage +20) reflètent la géométrie agrandie. La version de la table des matières passe de 3.0.6 à 3.0.7. Exactement cinq membres existants changent par édition ; aucun membre ajouté ou supprimé. La géométrie du test v3 est exclue. Coldflame et tous les autres membres correspondent à 3.0.6. L'utilisateur a relayé l'acceptation de la v2 par le testeur ; la certification de rencontre large n’est pas revendiquée.

<a id="308-all-cones--setup-114"></a>

## 3.0.8 tous les cônes / Configuration 1.1.4

Les six éditions utilisent la géométrie totale du ventilateur en degrés 90. Les noms de fichiers des modèles hérités et toutes les lignes DBC restent inchangés pour préserver le routage des sorts. Modifications : PW_White_Fan60_60yd_Glowing (Halion dans les deux royaumes), PW_White_Fan60_30yd_Glowing (Saviana), PW_White_Fan60_100y_Glowing (ICC Rimefang) et PW_Rotface_SlimeSpray_Fan25_Room (Rotface) s'élargissent à partir de 60. à 90 ; PW_White_Fan82_60yd_Glowing (Sartharion) s'élargit de 82 à 90. PW_White_Fan75_60yd_Glowing (Sindragosa) est déjà 90 et est identique en octets.

Pour chaque modèle modifié, seuls le sommet XY (foulée de sommet en octets 48) et les limites changent. Angle sur les échelles +X par 90/old-angle ; le rayon de chaque sommet et Z sont conservés. Les limites du modèle au décalage 160, les limites de séquence à séquence+32 et les limites de sous-maillage de peau à sous-maillage+20 sont mises à jour. Les UV, les normales, les animations et les traces de particules restent inchangées. Dix membres de modèle/habillage et deux chaînes de version dans la table des matières changent par édition ; aucun membre n’est ajouté ou supprimé. Tous les autres membres, y compris la géométrie Halion meteor-fire test-v2 et Coldflame, correspondent à 3.0.7 octet par octet.

<a id="setup-115-disabled-patch-s-preservation"></a>

## Configuration 1.1.5 désactivée Préservation Patch-S

Seuls les chemins S racine et actifs-locales obtiennent le suffixe .disabled. Chaque désactivation crée une copie intermédiaire locale épinglée par hachage avant de désactiver S ; les deux chemins sont journalisés, avec au plus onze destinations. La restauration restaure les fichiers actifs d'origine et supprime uniquement les copies désactivées nouvellement créées. Les copies désactivées identiques préexistantes restent en dehors de la transaction et sont préservées. Des fichiers ou répertoires en conflit bloquent la planification. La réactivation installe les actifs du catalogue S et ne consomme pas les copies désactivées. Les revues existantes restent lisibles. Aucun chemin source local arbitraire n'est accepté : chaque copie locale doit correspondre à son opération de désactivation S appariée.

<a id="setup-116-disabled-copy-collisions"></a>

## Configuration des collisions de copie désactivées 1.1.6

Le fichier S actif actuel prend toujours le nom simple .mpq.disabled. Avant de remplacer un autre fichier désactivé existant, le programme d'installation transforme ses octets en un frère se terminant par les premiers caractères 12 de son SHA-256 ; le SHA-256 complet et la longueur sont vérifiés avant toute réutilisation. Cela maintient les noms dans les limites de chemin Windows existantes. Les contenus d'archives en conflit échouent lors de la fermeture. Le S actif, le fichier désactivé et la copie d'archives nouvellement créée sont journalisés indépendamment, avec au plus treize entrées ; la restauration restaure tous les originaux. Les sources locales sont limitées aux opérations de désactivation S couplées ou de remplacement de fichiers désactivés. Les anciens journaux restent lisibles.

<a id="setup-117-re-enable-cleanup"></a>

## Configuration 1.1.7 réactiver le nettoyage

L'activation des nouveaux journaux de sorts supprime la racine simple et les fichiers S désactivés en paramètres régionaux actifs. La transaction déplace leurs octets d'origine vérifiés avant la sauvegarde en dehors des données. Si un fichier désactivé correspond au catalogue SHA-256 et à sa taille, il est transféré localement pour la destination S correspondante et exclu des téléchargements. Les sources locales doivent être associées à la suppression exacte du fichier désactivé et à l’actif du catalogue. Active S déjà correspondant produit toujours une transaction de nettoyage. Les archives existantes avec suffixe de hachage ne sont pas balayées. Les revues précédentes restent lisibles. On/off/on, dérive des sources, interruptions à chaque nouvelle étape de validation/restauration, tous les paramètres régionaux et restaurations empilées sont couverts.
