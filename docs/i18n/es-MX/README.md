<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.3.0. [English](../../../README.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Descarga actual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.3.0.
>
> **1.3.0:** Los archivos adicionales de mejora reconocidos se respaldan y la instalación continúa. Restaurar los devuelve. No hay que moverlos manualmente. Setup conserva automáticamente los archivos existentes antes de reemplazarlos o moverlos. Los archivos ajenos a la actualización no se modifican.


<!-- BEGINNER-120-STEPS -->
## Primeros pasos

1. Cierre WoW por completo.
2. Descargue solo `LauSetup.zip`. En Windows: clic derecho, **Extraer todo**, abra `LauSetup` y haga doble clic en `LauSetup.exe`.
3. Elija **Elegir carpeta…** y la carpeta que contiene directamente `WoW.exe`, no `Data` ni una carpeta de lanzador.
4. **Idioma de la interfaz** solo cambia el texto de Setup: Automático sigue el sistema y guarda la elección; no cambia los nueve idiomas del juego.
5. **Consagración mejorada** está activada por defecto. Los nuevos efectos requieren modelos HD compatibles detectados; mapas/minimapa son opcionales.
6. Elija **Instalar actualización**, espere sin cerrar Setup, inicie WoW y escriba `/pyversion`. Para restaurar, cierre WoW, use la misma carpeta y elija **Restaurar instalación anterior**.

### Linux/Wine

Use el mismo ZIP solo con un prefijo Wine 64-bit existente, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, fuentes documentadas y almacenamiento Linux local. Extraiga y ejecute `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`; nunca ejecute el EXE directamente en Wine.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../README.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<p align="center">
  <a href="https://wrath-multilingual-hd.vercel.app/"><img src="../../assets/social-preview.png" alt="Wrath HD — gold W shield on an icy blue background" width="100%" /></a>
</p>

<h1 align="center">Lau Setup</h1>
<p align="center"><strong>Tu cliente. Tu idioma. Su Wrath.</strong><br />El instalador Windows y Linux/Wine para la actualización visual Lau.</p>
<p align="center">
  <a href="https://github.com/CRSD-Lau/Lau-Setup/releases/latest">Última versión</a> ·
  <a href="https://wrath-multilingual-hd.vercel.app/">Sitio web y galería</a> ·
  <a href="https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose">Informar un problema</a> ·
  <a href="https://github.com/users/CRSD-Lau/projects/2">Hoja de ruta comunitaria</a>
</p>

---

Texto ortográfico multilingüe, ilustraciones de carga en pantalla ancha, indicadores de terreno personalizados y mapas HD opcionales para **WoW 3.3.5a, compilación 12340**. Elija su cliente y sus imágenes existentes; Lau Setup descarga los archivos necesarios, los verifica, coloca los parches y realiza una copia de seguridad de los originales.

**Instalador 1.1.7 · Lanzamiento del juego 3.0.8 Lau · Nueve idiomas del cliente**

<a id="patch-s-stays-recoverable"></a>

## Patch-S sigue siendo recuperable

**Configuración de 1.1.7 Hotfix:** volver a habilitar nuevos elementos visuales de hechizo reutiliza un Patch-S coincidente deshabilitado y mueve la copia simple deshabilitada a `LauSetupBackups`, por lo que los datos no retienen un duplicado activo/deshabilitado. Se conservan diferentes copias en la copia de seguridad de la transacción. El apagado todavía utiliza `.mpq.disabled`. Utilice **Restaurar instalación anterior** para la recuperación.

<a id="90-breath-and-slime-spray-warnings"></a>

## 90° Advertencias sobre aliento y Slime Spray

**3.0.8 Lau:** todos los indicadores de aliento admitidos y Rotface Slime Spray son **90° en total**, después de la confirmación del probador Warmane. Cubre a Halion en ambos reinos, Saviana Ragefire, Sartharion, ICC Rimefang y Sindragosa. Se conservan el alcance y el tiempo de la animación. El radio de fuego de meteorito Halion más grande aprobado y Coldflame azul claro no cambian.

**¿Ya está instalado?** Primero descargue **Setup 1.1.7**, seleccione la misma carpeta y los mismos elementos visuales, luego instálelo. La configuración verifica los hashes SHA-256 reales: incluso se detecta un cambio de un byte con el mismo tamaño y marca de tiempo. Sólo los archivos nuevos coincidentes cuentan como ya instalados. `/pyversion` informa **3.0.8 Lau**. Los instaladores antiguos conservan su antiguo catálogo integrado.

[Vistas previas de colores animados y registro de cambios](https://wrath-multilingual-hd.vercel.app/#changelog)

<a id="download"></a>

## Descargar

| Windows | Linux / Wine |
| :--- | :--- |
| **[Descargar LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** | **[Descargar LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip)** |
| Windows 10 / 11 · .NET Framework 4.8 | Wine 11.0 · Wine Mono 10.4.1 · Prefijo 64-bit |
| Acerca de **156 KB** | Acerca de **80 KB** · Python 3.9+ |
| [Guía Windows](START-HERE.md) | [Guía y requisitos previos Wine](wine/README.md) |

Descarga de archivos del juego durante la instalación. Una instalación principal en inglés cuesta aproximadamente **472 MB** con modelos HD y nuevos efectos visuales de hechizos, o **259 MB** con modelos originales. Los mapas opcionales agregan una descarga más grande; La configuración muestra el total antes de instalar.

[Sumas de comprobación SHA-256](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/SHA256SUMS.txt) · [Notas de la versión](https://github.com/CRSD-Lau/Lau-Setup/releases/latest) · [Informe de validación](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/VALIDATION.json)

> **Traiga su cliente existente.** Esta es una actualización, no un cliente de juego completo, un paquete de idioma o un modelo base HD. La interfaz del instalador sigue automáticamente el idioma del sistema entre diez opciones; la elección manual se guarda. Los datos del juego del cliente siguen admitiendo nueve configuraciones regionales y siguen la configuración regional detectada del juego.

<a id="one-setup-the-details-handled"></a>

## Una configuración. Los detalles manejados.

| Elige tus imágenes | Mantenga el control de su instalación |
| :--- | :--- |
| Consagración mejorada o stock | Idioma del cliente y detección de modelos |
| Nuevas imágenes de hechizos para clientes HD compatibles | Solo se descargaron los archivos requeridos |
| Mapas HD opcionales y texturas de minimapas | Verificación SHA-256 antes de la instalación |
| Cargando obras de arte en pantalla ancha regional | Copias de seguridad automáticas y descargas reanudables |
| Nombres de hechizos localizados, rangos e información sobre herramientas | Restauración y recuperación de operación interrumpida |

<p align="center"><img src="../../assets/installer-windows.png" alt="Lau Setup on Windows: choose a WoW folder, select visuals, install or restore" width="836" /></p>

Sus complementos, SavedVariables, fuentes, ilustraciones de inicio de sesión, configuraciones de dominio y parches no relacionados permanecen en su lugar. No se incluyen UI personales, credenciales ni análisis.

<a id="get-started"></a>

## Empezar

1. **Cierre WoW por completo.** En Wine, cierre todas las instancias de WoW en todos los prefijos.
2. **Inicie la configuración y elija su carpeta de cliente.** Extraiga `LauSetup.zip` en la carpeta `LauSetup/`. En Windows abra `LauSetup.exe`; en Linux/Wine ejecute `LauSetup.sh`.
3. **Elija sus elementos visuales e instálelos.** La Consagración mejorada comienza marcada; desmárquelo para ver la apariencia original. Las nuevas imágenes de hechizos requieren una base de modelo HD compatible. Los mapas son opcionales.
4. **Inicie WoW y ejecute `/pyversion`.** Confirme la edición instalada antes de ingresar al juego.

En Linux, ejecute esto desde la carpeta extraída con su prefijo existente:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

Utilice el iniciador como su usuario normal. Comprueba las rutas Linux, los juegos en ejecución, el espacio libre y los bloqueos del instalador entre prefijos. Utilice el almacenamiento local Linux; Las carpetas vinculadas, los recursos compartidos de red y las unidades montadas en Windows no son compatibles. La [guía Wine](wine/README.md) enumera las fuentes y todos los requisitos previos.

En Windows, la instalación ofrece la página de descarga oficial de .NET Framework 4.8 de Microsoft si falta el tiempo de ejecución. La configuración probada de Wine utiliza **Wine Mono**, no el instalador Windows .NET.

<a id="nine-client-languages"></a>

## Nueve idiomas del cliente

English · Français · Deutsch · 한국어 · Русский · 简体中文 · 繁體中文 · Español (España) · Español (México)

`enUS` · `frFR` · `deDE` · `koKR` · `ruRU` · `zhCN` · `zhTW` · `esES` · `esMX`

La configuración sigue la configuración regional activa de su cliente. Instale los archivos de idioma y fuentes apropiados antes de cambiar la configuración. Cambiar un valor de configuración por sí solo no instala un paquete de idioma.

<a id="restore-with-your-backups"></a>

## Restaurar con tus copias de seguridad

Cierre WoW, vuelva a abrir la instalación a través del mismo iniciador, elija el mismo cliente y seleccione **Restaurar instalación anterior**. Mantenga `LauSetupBackups` dentro de la carpeta del cliente: contiene los originales y los registros de recuperación.

Una instalación o restauración interrumpida se puede recuperar incluso si `WoW.exe` falta temporalmente. Si otra actualización cambió los archivos instalados, la restauración se detiene y conserva la copia de seguridad para su resolución. Una vez que este instalador agrega la actualización del mapa, la conserva durante los cambios de edición; restaure la instalación anterior para deshacer esa actualización.

<a id="tested-with-clear-limits"></a>

## Probado, con límites claros

La versión 1.1.7 aprobó **grupos de regresión 50 en Windows y en Wine**, incluidos los planes de configuración regional/edición/mapa de 108 por plataforma. El lanzamiento del juego 3.0.8 pasó previamente por actualizaciones de seis ediciones y detección de un byte en ambas plataformas; sus cargas útiles no cambian. La configuración 1.1.7 también cubre la secuencia de banderas encendidas a nuevos hechizos desactivados con copias más antiguas deshabilitadas, cambios repetidos y reversión exacta. Las cargas útiles públicas se descargaron de forma anónima y se verificaron mediante hash; Se probaron la instalación y la reversión del núcleo real.

Wine se probó con **Wine 11.0 / Wine Mono 10.4.1** en el almacenamiento local Linux, incluido el iniciador suministrado como usuario normal. La geometría del fuego de meteorito Halion coincide exactamente con la v2 aprobada por el probador. Coldflame, pistas de animación, fuego nativo y tablas de hechizos siguen siendo idénticos en bytes a 3.0.7. Las animaciones del sitio web son maquetas ilustrativas. Estas pruebas no certifican cada distribución de Linux o encuentro en el juego.

Las integraciones de Lutris, Proton y macOS están fuera de esta versión. El ejecutable no está firmado digitalmente.

<a id="known-limitations-and-feature-requests"></a>

## Limitaciones conocidas y solicitudes de funciones

Leer [Limitaciones y suposiciones conocidas.](KNOWN-LIMITATIONS.md) antes de sugerir una característica: Warmane control del servidor, alcance de DLL/código nativo, acciones protegidas de Lua, precisión y sincronización del indicador, dependencias de DBC y límites de plataforma/recuperación.

<a id="for-contributors"></a>

## Para contribuyentes

- [Diseño de compilación, ubicación de archivo y recuperación](docs/TECHNICAL.md)
- [Guía de contribución y informe de errores](CONTRIBUTING.md)
- [Revisión de implementación](REVIEW.md)
- [Alcance y viabilidad de la plataforma](PLATFORM-FEASIBILITY.md)

Las cargas útiles del juego se distribuyen a través de las versiones GitHub. Este repositorio contiene la fuente, el catálogo, el iniciador y la documentación del instalador; no es necesario clonarlo para instalar la actualización.

<a id="built-on-community-work"></a>

## Construido sobre el trabajo comunitario

**Andre** — Líneas base de Patch-Y · **Loriendal & Trimitor** — Base del cliente HD · **Contribuyentes de Project Reforged** — Arte HD · **Blizzard** — Juego original, arte y texto localizado · **Lau**: indicadores de tierra, compatibilidad, adaptaciones, herramientas de prueba y liberación.

[Créditos completos](https://wrath-multilingual-hd.vercel.app/credits) · [Capturas de pantalla y ayuda para la instalación](https://wrath-multilingual-hd.vercel.app/)

<sub>Proyecto comunitario no oficial. No afiliado ni respaldado por Blizzard Entertainment. El juego original y las ilustraciones de terceros siguen siendo propiedad de sus respectivos dueños.</sub>

<a id="dbc-change-tracking"></a>

## Seguimiento de cambios de DBC

Consulte el [registro de cambios de DBC](DBC-CHANGELOG.md) para ver ediciones de tablas, registros o campos individuales y pruebas comparativas. **3.0.7 → 3.0.8 no tuvo ediciones de DBC**: la actualización del indicador 90° cambió la geometría del modelo. La configuración 1.1.5–1.1.7 también deja los datos DBC sin cambios.
