<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.3.0. [English](../../../CHANGELOG.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Descarga actual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.3.0.
>
> **1.3.0:** Los archivos adicionales de mejora reconocidos se guardan en una copia de seguridad y la instalación continúa. Restaurar los devuelve. No hay que moverlos manualmente.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../CHANGELOG.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="lau-setup-116-hotfix---switch-options-with-existing-disabled-patch-s"></a>

# Lau Setup 1.1.6 Revisión: cambiar opciones con Patch-S deshabilitado existente

Corrige el mensaje 1.1.5 "Ya existe otro Patch-S deshabilitado" cuando se desactivan los elementos visuales de Nuevo hechizo después de una instalación anterior.

El programa de instalación conserva ambos archivos automáticamente. El archivo S actual siempre se convierte en `.mpq.disabled`. Si ya existe una copia anterior deshabilitada, el programa de instalación primero conserva esa copia anterior como `.mpq.disabled.<12-character hash>`. Se reutiliza una copia guardada idéntica. Se mantienen ambas versiones. Una copia con nombre hash cuyo contenido no coincide con el archivo anterior que se conserva aún detiene la operación para su inspección.

Esto se aplica a archivos S raíz y de configuración regional activa, incluida la secuencia **las tres banderas activadas -> Nuevos efectos visuales de hechizo desactivados**, cambios repetidos y reversión. Se conserva la elección del mapa.

Descargue el nuevo EXE o ZIP Wine y vuelva a intentar su selección. No es necesario eliminar ni cambiar el nombre de la copia deshabilitada existente para resolver la colisión normal que se muestra en 1.1.5.

Para deshacer la instalación completa, use **Restaurar instalación anterior**. Para volver a habilitar manualmente un archivo S guardado, cierre WoW y elimine `.disabled` y cualquier hash siguiente, restaurando su nombre de archivo original `.mpq`. Nunca sobrescribas un archivo activo diferente. Los cambios manuales pueden detener la reversión administrada en caso de desvío de archivos; mantenga sus copias de seguridad. Los archivos eliminados por los instaladores antes de 1.1.5 aún necesitan recuperación a través de sus copias de seguridad.

El lanzamiento del juego sigue siendo **3.0.8 Lau** y la carga útil del juego no cambia. Se conservan todos los conos de grados 90, el radio de fuego de meteorito y Coldflame.

Las comprobaciones de Windows y Wine incluyen grupos de regresión 46, las nueve configuraciones regionales, archivos deshabilitados existentes, interruptores de encendido/apagado repetidos, protección contra copia manipulada, recuperación de interrupciones y reversión exacta. Las descargas públicas nuevas se prueban con archivos de lanzamiento reales activados o desactivados y una copia anterior deshabilitada presente. Esta es una validación del instalador, no una validación de nuevos encuentros en el juego.

[Patch-Y ZIP sin formato de seis ediciones](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Ayuda de instalación y registro de cambios](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-115-hotfix---keep-disabled-patch-s-files"></a>

# Lau Setup 1.1.5 Revisión: mantener deshabilitados los archivos Patch-S

Al desactivar **Nuevos elementos visuales de hechizo** ahora se conservan los archivos raíz y de configuración regional activa Patch-S junto a sus ubicaciones originales como `.mpq.disabled`, en lugar de dejarlos solo en las copias de seguridad del instalador. Sus bytes se verifican antes y después del cambio. WoW no carga el nombre de archivo deshabilitado.

- Una copia diferente de `.disabled` existente bloquea la instalación; nunca se sobrescribe.
- Se reutiliza y conserva una copia idéntica deshabilitada.
- Al activar la opción se instalan los archivos S activos de la versión seleccionada y se mantienen las copias deshabilitadas.
- Las instalaciones repetidas, la reversión y la recuperación de interrupciones cubren rutas activas y deshabilitadas.

Para volver a habilitar un archivo deshabilitado manualmente, cierre WoW y elimine solo el sufijo `.disabled`. No sobrescriba un archivo activo diferente. Para deshacer la instalación completa de Lau, utilice **Restaurar instalación anterior**; eliminar solo Patch-Y no deshace Q/M/ejecutable ni otros cambios. Los cambios manuales de archivos pueden hacer que la reversión administrada se detenga al desviarse, así que conserve las copias de seguridad.

**¿Ya te ha afectado un instalador anterior?** Esta actualización no extrae automáticamente las copias de seguridad antiguas. Utilice Restaurar instalación anterior para recuperar esos archivos, trabajando hacia atrás a través de cualquier instalación apilada, antes de reinstalar con la nueva configuración. Mantenga LauSetupBackups.

El lanzamiento del juego permanece **3.0.8 Lau**. Todos los MPQ no han cambiado: 90 Respiraciones de grados/Slime Spray, aprobado +50% Se conservan el radio de fuego de meteorito Halion y Coldflame. Descargue el nuevo EXE o ZIP Wine para corregir el instalador.

La validación de Windows y Wine se incluye en VALIDATION.json. Las pruebas cubren las nueve configuraciones regionales, colisiones de copia deshabilitada, transiciones de encendido/apagado, instalación repetida, interrupción en cada paso de movimiento/restauración, deriva de archivos y reversión exacta. La solución no reclama la validación de nuevos encuentros en el juego.

[Patch-Y ZIP sin formato de seis ediciones (sin cambios 3.0.8)](https://github.com/CRSD-Lau/Lau-Setup/releases/download/v1.1.4/Lau-Patch-Y-3.0.8-All-Editions.zip)

[Ayuda de instalación y registro de cambios](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-114--game-release-308-lau"></a>

# Lau Setup 1.1.4 · Lanzamiento del juego 3.0.8 Lau

<a id="117-hotfix---patch-s-re-enable-cleanup"></a>

## 1.1.7 Revisión: Patch-S vuelve a habilitar la limpieza

- Volver a habilitar las imágenes de nuevos hechizos reutiliza un Patch-S deshabilitado cuando su SHA-256 y su tamaño coinciden con la versión seleccionada, evitando esa descarga.
- La copia simple deshabilitada pasa a la copia de seguridad de la transacción verificada fuera de los Datos, incluso si el Patch-S activo ya coincide. Diferentes archivos deshabilitados permanecen recuperables mediante Restaurar instalación anterior.
- Se aplica a la raíz y a la configuración regional activa Patch-S. Off todavía usa el nombre de archivo simple `.mpq.disabled`. Los archivos existentes con sufijo hash se dejan intactos.
- Las cargas útiles del juego siguen siendo 3.0.8 Lau. Windows y Wine pasaron cada uno de ellos los grupos de regresión 50, el encendido/apagado/encendido de archivos reales y la reversión exacta.

<a id="all-breath-and-slime-spray-warnings-are-now-90"></a>

## Todas las advertencias de aliento y Slime Spray ahora son 90°

Tras la confirmación del probador Warmane, Halion (ambos reinos), Saviana Ragefire, Sartharion, ICC Rimefang y Rotface Slime Spray ahora usan **90° total de conos**, coincidiendo con la advertencia 90° existente de Sindragosa. Esto se aplica a las seis ediciones y los nueve idiomas del cliente, incluidas las asignaciones de hechizos normales/heroicos existentes.

Sólo cambia el ancho del cono. Se conservan el alcance, el tiempo de animación, los efectos de hechizos nativos y las tablas de hechizos. El radio de fuego de meteorito Halion más grande aprobado 50%, Coldflame azul claro, los colores y la Consagración no cambian. Estos son amortiguadores de advertencia visual; Los daños y la mecánica del servidor no cambian. El terreno irregular aún puede cortar los conos planos.

<a id="updating"></a>

## Actualizando

Descargue primero **LauSetup.exe** o **LauSetup-Wine.zip** de esta versión. Cierre WoW, seleccione el mismo cliente y elementos visuales, luego haga clic en **Instalar actualización**. Los instaladores antiguos conservan sus catálogos antiguos. Verifique `/pyversion` para **3.0.8 Lau**.

La configuración verifica los hashes SHA-256 reales, por lo que se detectan versiones anteriores e incluso cambios de un byte con tamaño y marca de tiempo sin cambios. Sólo los archivos actuales exactos cuentan como ya instalados. Las copias de seguridad y la restauración de la instalación anterior permanecen disponibles.

Windows requiere .NET Framework 4.8. Los usuarios de Wine extraen los cuatro archivos y ejecutan `LauSetup.sh` como un usuario normal con el prefijo Wine/Mono existente compatible. Los instaladores de tiempo de ejecución no están incluidos.

<a id="validation"></a>

## Validación

Consulte VALIDATION.json para conocer la regresión Windows y Wine, actualizaciones de seis ediciones de 3.0.7, detección de repetición, comprobaciones de un byte, reversión y comprobaciones de descarga pública. Las comprobaciones de geometría verifican los conos 90°, el rango conservado, los límites válidos y el devanado triangular en cada edición. Cambian exactamente once miembros del archivo existente: cinco modelos, sus cinco máscaras y la versión TOC. Todos los demás miembros tienen bytes idénticos a 3.0.7.

La decisión sobre el ancho sigue las pruebas informadas Warmane. Esta versión no es una certificación para todos los encuentros ni una certificación exacta de los límites del servidor.

[Registro de cambios del sitio web y ayuda para la instalación](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-113--game-release-307-lau"></a>

# Lau Setup 1.1.3 · Lanzamiento del juego 3.0.7 Lau

<a id="larger-halion-meteor-fire-warnings"></a>

## Advertencias de incendio de meteoritos Halion más grandes

Promueve la **prueba v2** aprobada por los probadores: el radio del marcador de suelo rojo de Halion es **50% mayor que el de la versión 3.0.6**, alrededor de los senderos y el fuego de aterrizaje. La prueba v3 no está incluida. Coldflame, los colores, las pistas de animación, las llamas nativas, la Consagración y los conos de Sindragosa/Rotface no cambian. Se admiten las seis ediciones y los nueve idiomas del cliente.

El evaluador confirmó la versión 2 después de corregir un parche no actualizado. Este es un buffer de advertencia visual, no un cambio en el daño del servidor o una certificación de cada posición o encuentro.

<a id="update-with-the-new-installer"></a>

## Actualizar con el nuevo instalador

Descargue primero **LauSetup.exe** o **LauSetup-Wine.zip** de esta versión. Cierre WoW, seleccione el mismo cliente y elementos visuales, luego haga clic en **Instalar actualización**. Los instaladores antiguos conservan los catálogos antiguos. `/pyversion` informa **3.0.7 Lau**.

Los usuarios existentes de 3.0.6 y de prueba v2 reciben la actualización. El programa de instalación compara los hashes de archivos reales, incluidos los cambios de un byte con tamaño y marca de tiempo sin cambios; sólo los archivos actuales exactos cuentan como ya instalados. Las copias de seguridad y la restauración de la instalación anterior permanecen disponibles.

Windows requiere .NET Framework 4.8. Los usuarios de Wine extraen los cuatro archivos y ejecutan `LauSetup.sh` como un usuario normal con el prefijo Wine/Mono existente compatible. No se incluyen instaladores de tiempo de ejecución.

<a id="validation-1"></a>

## Validación

La regresión del instalador Windows y Wine, las actualizaciones de seis ediciones, la detección de repetición, las comprobaciones de un byte, la reversión y las comprobaciones de descarga pública se registran en VALIDATION.json. Los modelos y máscaras de Halion son idénticos en bytes a los de la prueba v2. Sólo su geometría/límites y la versión TOC difieren de 3.0.6; Coldflame y otros miembros del archivo no han cambiado.

[Registro de cambios del sitio web y ayuda para la instalación](https://wrath-multilingual-hd.vercel.app/#changelog)

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-112--game-release-306-lau"></a>

# Lau Setup 1.1.2 · Lanzamiento del juego 3.0.6 Lau

<a id="blue-coldflame-red-meteor-fire"></a>

## Blue Coldflame, fuego de meteorito rojo

- **Marrowgar Coldflame:** círculos de color azul claro con el brillo interior existente y animación en el sentido de las agujas del reloj, incluido heroico.
- **Fuego de meteorito Halion:** dispara círculos rojos alrededor de los senderos y aterriza con la animación existente en el sentido de las agujas del reloj.
- Las seis ediciones HD/No HD y nueve idiomas de cliente. Las llamas nativas, las duraciones, las opciones de Consagración y los conos 90° Sindragosa / 60° Rotface no cambian.

[Vistas previas de colores animados y registro de cambios completo](https://wrath-multilingual-hd.vercel.app/#changelog). Las vistas previas son maquetas ilustrativas, no grabaciones del juego. Los daños y la mecánica del servidor no cambian; Los bordes de advertencia siguen siendo amortiguadores visuales.

<a id="already-installed-download-the-new-installer-first"></a>

## ¿Ya está instalado? Descargue primero el nuevo instalador

Descargue **LauSetup.exe** o **LauSetup-Wine.zip** de esta versión. Cierre WoW, elija la misma carpeta y configuración visual, luego haga clic en **Instalar actualización**. Los instaladores descargados antiguos conservan su antiguo catálogo integrado.

El programa de instalación aplica hash a los archivos reales. Se reemplazan los archivos 3.0.5 más antiguos; incluso se detecta un cambio de un byte con tamaño de archivo y marca de tiempo idénticos. Sólo los archivos nuevos exactos se tratan como ya instalados. `/pyversion` informa **3.0.6 Lau**. Las copias de seguridad y la restauración de la instalación anterior permanecen disponibles.

Usuarios de Wine: extraiga los cuatro archivos juntos y ejecute `LauSetup.sh` como su usuario normal con su prefijo 64-bit Wine 11.0 / Mono 10.4.1 existente. Se requieren Python 3.9+ y almacenamiento local Linux. Windows necesita .NET Framework 4.8. Los tiempos de ejecución no están incluidos.

<a id="fresh-verification-on-windows-and-wine"></a>

## Verificación nueva en Windows y Wine

- Grupos de regresión 38 por plataforma, incluidos los planes locales/edición/mapa 108 de cada uno.
- Las seis actualizaciones reales de 3.0.5 a 3.0.6, instalaciones repetidas sin operación y reversión exacta en ambas plataformas.
- Cambios de un byte del mismo tamaño/misma marca de tiempo detectados y reparados de forma independiente en la raíz y la configuración regional Y en ambas plataformas.
- Descargas anónimas de carga útil GitHub, instalaciones principales reales y reversión en Windows y Wine.
- Pruebas de seguridad del host 15 Linux y el iniciador exacto de cuatro archivos Wine bajo un usuario normal; Representación del formulario Windows marcada.
- Tres referencias de textura del marcador M2 y la versión TOC cambiadas por edición; Se agregaron dos texturas de color. Todos los demás miembros se conservan byte por byte.

Estas comprobaciones del instalador no certifican todas las distribuciones de Linux ni todos los encuentros en el juego. El ejecutable no está firmado digitalmente. Se adjuntan pruebas detalladas, sumas de verificación y fuente.

Author / Creator / Last Modified By: Neil Mitchell

---

<a id="lau-setup-111--game-release-305-lau"></a>

# Lau Setup 1.1.1 · Lanzamiento del juego 3.0.5 Lau

<a id="wider-raid-warnings"></a>

## Advertencias de incursiones más amplias

- Sindragosa Frost Breath: **75° → 90° total** (7.5° extra por lado).
- Rotface Slime Spray: **25° → 60° en total** (17.5° extra por lado).
- Aplicado a las seis ediciones HD/No HD y disponible en las nueve configuraciones regionales del cliente. Otros indicadores, entornos de consagración, tablas localizadas y obras de arte no cambian.

Estas son advertencias visuales almacenadas informadas por imágenes de incursiones Warmane y registros de hechizos. No cambian los daños o la mecánica del servidor, ni reclaman un límite de daño exacto.

<a id="updating-an-existing-installation"></a>

## Actualizar una instalación existente

Descargue primero el nuevo **LauSetup.exe** o **LauSetup-Wine.zip**. Cierre WoW, seleccione la misma carpeta y opciones visuales, luego haga clic en **Instalar actualización**. El instalador compara los hashes de archivos reales: los parches 3.0.4 más antiguos se reemplazan, mientras que una instalación exacta de 3.0.5 se informa como ya instalada. `/pyversion` informa **3.0.5 Lau** después de la actualización. Los instaladores descargados antiguos conservan su catálogo antiguo.

Las descargas de Windows y Wine incluyen el mismo ejecutable de configuración reconstruido. Para Wine, extraiga los cuatro archivos juntos y use `LauSetup.sh` como se describe en el archivo README incluido. Los requisitos de tiempo de ejecución existentes no cambian.

<a id="verification"></a>

## Verificación

Se aprobaron todos los grupos de regresión 38 Windows, incluidos los planes locales/edición/mapa de 108. Las seis ediciones pasaron las verificaciones reales de actualización, instalación repetida y reversión exacta de 3.0.4 a 3.0.5. Las nuevas cargas útiles pasaron verificaciones de hash/descarga anónimas; una instalación de núcleo aislado de GitHub y se aprobó la reversión. Cada edición conserva todos los miembros excepto cuatro archivos de modelo/geometría y la versión TOC.

El código del iniciador Wine no ha cambiado y el ZIP contiene el EXE reconstruido exacto. Se conserva la evidencia de tiempo de ejecución anterior Wine 11.0 / Mono 10.4.1; La nueva ejecución de Wine no estaba disponible porque el motor Docker no se inició. La nueva geometría del cono se verifica estáticamente, no se certifica recientemente en el juego.

Se adjuntan las sumas de verificación de descarga, la fuente y el informe de validación detallado. Conserve `LauSetupBackups` para la recuperación.

Author / Creator / Last Modified By: Neil Mitchell
