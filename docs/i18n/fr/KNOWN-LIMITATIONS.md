<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traduction automatique. [source anglaise](../../../KNOWN-LIMITATIONS.md). Si la formulation diffère, la source anglaise fait autorité.

<a id="known-limitations-and-assumptions"></a>

# Limites et hypothèses connues



[Retour à Lau Setup](README.md) · [Recommandations et demandes de fonctionnalités](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [Historique des modifications DBC](DBC-CHANGELOG.md)

Lisez ceci avant de proposer une fonctionnalité. Lau Setup installe une mise à niveau visuelle côté client pour **WoW 3.3.5a build 12340**. Ce n'est pas un framework de modification de serveur. Les limites ci-dessous décrivent le projet actuel ; hors du champ d’application ne signifie pas nécessairement techniquement impossible.

<a id="what-we-can-and-cannot-change"></a>

## Ce que nous pouvons et ne pouvons pas changer

| Demande | Limite actuelle |
| --- | --- |
| Améliorez les indicateurs de sol, les textures, les modèles ou les tables client localisées pris en charge | Dans la portée, sous réserve des dépendances des fichiers et des tests. Une amélioration visuelle ne doit pas être décrite comme une modification des dommages ou de la mécanique du serveur. |
| Améliorer l'installation, les sauvegardes, l'accessibilité ou la documentation | Dans le cadre. Conservez les fichiers non liés et vérifiez l’installation et la récupération. |
| Modifier les dégâts Warmane, la détection des coups, la durée des capacités, les scripts de ciblage ou de rencontre | Hors de notre contrôle. Warmane exécute son propre code serveur ; ce projet n'a pas accès pour modifier ou déployer ce code. Un MPQ ou un addon ne peut pas obliger le serveur à adopter des mécanismes différents. |
| Ajoutez du code C++ personnalisé au noyau de Warmane | Ce n’est pas quelque chose que cette version peut offrir. Les modifications apportées à un serveur de test contrôlé séparément ne modifient pas Warmane. |
| Injectez une DLL, hookez le client ou ajoutez un nouveau comportement de moteur natif | En dehors du flux de travail de correctifs/compléments pris en charge. Cela nécessite une enquête d'ingénierie et de compatibilité distincte, pas seulement une modification DBC. Aucun cadre d'injection de DLL ni prise en charge générale du crochet client n'est fourni. |
| Débloquez des actions Lua protégées ou des API de jeu manquantes | Ce n'est pas une fonctionnalité prise en charge. Le module complémentaire modifiable Lua et les actions client protégées sont des choses différentes. La réécriture de Lua n'accorde pas elle-même d'autorisations ni ne crée une API que le client n'expose pas. Signalez l'action/l'API exacte avant de supposer qu'une solution de contournement existe. |
| Fournir un client complet, un autre pack linguistique ou une base de modèle HD | Non inclus. Apportez un client compatible existant avec les fichiers de langue, les polices et la configuration du modèle requis. |

Le `WoW.exe` compatible fourni par l'installation a un rôle spécifique dans le moteur de rendu de chargement approuvé, la capacité d'archivage et la prise en charge des grandes adresses. Son inclusion n'est **pas** une promesse de modifications arbitraires d'exécutables ou de DLL. De même, tous les fichiers Lua ne sont pas protégés ou non modifiables : des modifications ordinaires des modules complémentaires et de l'interface utilisateur peuvent être réalisables dans le cadre du comportement pris en charge par le client.

<a id="indicators-are-visual-guidance"></a>

## Les indicateurs sont des conseils visuels

- **Warmane est la référence d'exécution pour les rapports Warmane.** AzerothCore et les clients isolés aident à vérifier l'intégrité et le comportement des fichiers dans ces environnements. Ils ne peuvent pas prouver le comportement personnalisé de détection, de synchronisation ou de rencontre de Warmane.
- **Un bord tiré ne constitue pas une limite de sécurité garantie.** Les respirations prises en charge et le Slime Spray utilisent des cônes totaux 90° suite aux commentaires du testeur. Halion meteor-fire utilise l'agrandissement test-v2 accepté. Il s'agit d'avertissements visuels basés sur des observations et non sur des mesures provenant de la source du serveur Warmane.
- **Le terrain peut couper les indicateurs plats.** Un maillage de sol plat peut croiser des pentes, des marches et des surfaces inégales. L’agrandir ou l’élever ne garantit pas partout une projection suivant le terrain.
- **La durée de vie de l'effet nécessite des preuves.** Les retours de poursuite/fantôme incluent des effets disparaissant après une ou deux secondes. Changer une texture, une forme ou une animation en boucle ne prouve pas à lui seul que le client conservera l'instance d'effet en vie pendant toute la durée de sa poursuite. Un correctif de timing nécessite des images et des preuves d'événements pour cette capacité spécifique ; ne traitez pas une maquette ou une version expérimentale comme un correctif confirmé.
- **Les maquettes sont illustratives.** Les animations de sites Web/chat démontrent l'apparence. Il ne s’agit pas d’enregistrements ni de preuves du rendu, de la durée ou de la couverture du jeu.

Pour les rapports de limites ou de timing, incluez la rencontre, la capacité, la difficulté, l'édition client, `/pyversion` et un clip montrant la préparation et la fin des dommages ou des effets. Les captures d'écran sont utiles, mais les effets de perspective et de chevauchement limitent les mesures exactes du rayon.

<a id="dbc-and-patch-compatibility"></a>

## DBC et compatibilité des correctifs

Les tables DBC sont des données connectées et non des commutateurs indépendants. L’ajout d’un visuel peut nécessiter des références de sort, de visuel, de kit, d’effet et de modèle correspondantes. Le remplacement d'un tableau complet peut également remplacer son texte localisé et entrer en conflit avec un autre correctif fournissant le même tableau.

La dépendance à la localisation a été un réel problème lors du développement de ce projet. Andre et Lau avons travaillé dessus ensemble. Le [audit historique DBC](DBC-CHANGELOG.md) sépare le calendrier de développement rapporté des preuves d'archives conservées : Andrela ligne de base de est omise `Spell.dbc`, pas tous les DBC. Ne présumez pas que la copie d’un tableau anglais dans une autre langue est sûre.

- Utilisez l'édition correspondant à votre configuration actuelle de HD/modèle original. Les nouveaux visuels de sorts nécessitent les dépendances HD compatibles ; la détection ne certifie pas tous les packs de modèles tiers.
- Si vous supprimez ou désactivez les correctifs du modèle HD après l'installation, réexécutez la dernière installation pour la configuration résultante. Une édition HD installée ne se convertit pas dynamiquement. Des actifs incompatibles peuvent produire des visuels manquants ou incorrects et nécessiter une enquête sur les plantages ; ni un crash ni un comportement sans crash ne sont garantis.
- Les emplacements racine et actifs ont des rôles distincts. En particulier, les deux archives S sont différentes. Suivez le [guide de placement](docs/TECHNICAL.md#file-placement), pas une instruction générique pour dupliquer chaque MPQ.
- Les correctifs non liés sont conservés, mais la préservation ne constitue pas une garantie de compatibilité. Une autre archive remplaçant les mêmes données peut modifier le résultat.
- Le contenu du jeu prend en charge neuf paramètres régionaux ; l'interface de l'installateur est actuellement en anglais. Changement `Config.wtf` seul, n'installe pas les fichiers ou les polices d'une autre langue.

<a id="installer-and-recovery-assumptions"></a>

## Hypothèses d'installation et de récupération

Fermez complètement WoW avant l’installation ou la restauration. Utilisez le dossier client exact prévu et conservez `LauSetupBackups` intact.

Le programme d'installation compare les hachages de fichiers réels avec son **catalogue intégré**. Une modification d'un octet peut être détectée même lorsque la taille et l'horodatage correspondent, mais un ancien programme d'installation ne connaît toujours que son ancien catalogue. Téléchargez le dernier programme d'installation lors de la mise à niveau. Le programme d'installation ne surveille pas en permanence un client après sa fermeture ni ne concilie automatiquement les modifications manuelles ultérieures des correctifs.

La désactivation des visuels du nouveau sort préserve les fichiers S étendus tels que `.mpq.disabled`. La réactivation utilise les octets désactivés correspondants lorsqu'ils sont disponibles et déplace la copie simplement désactivée dans la sauvegarde de transaction vérifiée. Les anciennes copies avec suffixe de hachage sont conservées. Voir le [mise en œuvre actuelle du rétablissement](docs/TECHNICAL.md#setup-117-re-enable-cleanup).

La restauration dépend des sauvegardes et des enregistrements de récupération. Il s'arrête lorsque des modifications ultérieures rendent la restauration automatique dangereuse. Il ne peut pas promettre la récupération des fichiers dont la seule sauvegarde a été supprimée. La suppression de Patch-Y à elle seule ne constitue pas une restauration complète de l'exécutable et des autres correctifs installés par le programme d'installation. Utilisez **Restaurer l'installation précédente** pour la transaction gérée.

<a id="platform-and-validation-limits"></a>

## Limites de la plateforme et de la validation

La cible Windows documentée est Windows 10/11 avec .NET Framework 4.8. La configuration Linux testée utilise Wine 11.0, Wine Mono 10.4.1, un préfixe 64-bit existant et Python 3.9+. Les installateurs d'exécution ne sont pas regroupés. Suivez les [prérequis Wine](wine/README.md) ; utilisez le stockage local Linux. Les dossiers liés, les partages réseau et les lecteurs montés sur Windows se trouvent en dehors de la configuration du chemin Wine prise en charge.

Lutris, Proton, l'intégration spécifique à Steam Deck et macOS ne sont pas des cibles d'intégration prises en charge dans cette version. Cela ne veut pas dire que tout autre environnement est impossible ; cela signifie que nous n’avons pas établi de support pour cela. Les paquets Windows ne sont pas signés numériquement.

Les builds, les vérifications de hachage, les tests de régression de l'installateur, les tests Wine et les tests en jeu répondent à différentes questions. En adopter un ne remplace pas les autres. Les contrôles visuels sont échantillonnés, et non la certification de chaque zone, rencontre, échelle d'affichage, distribution Linux ou modification client tiers. Consultez le rapport de validation de chaque version pour savoir ce qui a été réellement vérifié.

<a id="before-requesting-a-feature"></a>

## Avant de demander une fonctionnalité

Décrivez le problème visible par le joueur, votre configuration et les preuves. Les propositions dans le cadre du champ d'application soutenu sont les bienvenues [Idées](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas); les défauts reproductibles appartiennent à [Problèmes](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

Pour les propositions de DLL, de code natif, d’action protégée ou dépendantes du serveur, identifiez explicitement la dépendance. Ils nécessitent des travaux de faisabilité et un contrôle approprié du système concerné avant que la mise en œuvre puisse être promise. Veuillez ne pas les classer comme de simples options DBC manquantes.
