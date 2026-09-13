<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.2.0. [English](../../../CONTRIBUTING.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../CONTRIBUTING.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="contributing-to-lau-setup"></a>

# Contribuyendo a Lau Setup



Gracias por ayudar a mejorar la instalación y recuperación para la comunidad Wrath.

<a id="community-roadmap"></a>

## Hoja de ruta comunitaria

Siga la [hoja de ruta de la comunidad](https://github.com/users/CRSD-Lau/projects/2) para ver el trabajo como problemas y las solicitudes de extracción alimentan automáticamente el tablero a través de **Registro**, **Listo**, **En progreso**, **Probando** y **Listo**. Las tarjetas de **prueba** incluyen listas de verificación de aceptación y recopilan la evidencia necesaria para finalizar la validación; utilice [Ideas](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) para discutir propuestas antes de presentar un problema. [Notas de la versión](https://github.com/CRSD-Lau/Lau-Setup/releases) siguen siendo la autoridad sobre lo que se envía en cada versión.

<a id="report-a-problem"></a>

## Informar un problema

Utilice el [formulario de informe de errores](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose). Incluya la versión del instalador, la plataforma, la configuración regional del cliente, los elementos visuales seleccionados, el comportamiento esperado y los pasos para reproducir. Para problemas dentro del juego, incluye `/pyversion`, el jefe o habilidad, la dificultad y una captura de pantalla. Los informes Wine deben incluir las versiones Wine y Wine Mono.

Elimine nombres de cuentas, contraseñas, tokens y rutas personales de capturas de pantalla o extractos. No cargue su cliente, carpeta WTF, SavedVariables ni registros completos. Mantenga copias de seguridad locales si la recuperación está pendiente.

<a id="propose-a-change"></a>

## Proponer un cambio

Comience con [Limitaciones y suposiciones conocidas](KNOWN-LIMITATIONS.md). Utilice [Ideas](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas) para obtener recomendaciones; identifique cualquier dependencia de servidor, código nativo o acción protegida antes de proponer una implementación.

Mantenga las solicitudes de extracción enfocadas. Explique el problema visible para el usuario, el cambio y las comprobaciones que realizó. Pruebe las operaciones de archivos solo en dispositivos aislados, nunca en un cliente de juego personal activo.

Conserve la lista de archivos permitidos, las comprobaciones de hash, los diarios de copia de seguridad, las comprobaciones de procesos y el bloqueo de prefijos cruzados. No cambie los registros de carga útil del juego como parte de una actualización de documentación o interfaz.

La [referencia técnica](docs/TECHNICAL.md) explica la construcción pública y las pruebas que requieren instalaciones locales privadas. Separe claramente una construcción exitosa, una prueba de dispositivos y una validación real en el juego en su PR.

<a id="artwork-and-attribution"></a>

## Ilustraciones y atribución

Mantenga intactos la marca W-and-shield establecida y los créditos ascendentes. Incluya la fuente y los permisos aplicables para la obra de arte propuesta. No introducir el estado de cliente personal en los bienes públicos.

<a id="dbc-release-records"></a>

## Registros de publicación de DBC

Cada versión de juego o instalador debe actualizar [DBC-CHANGELOG.md](DBC-CHANGELOG.md) e incluir una sección **cambios DBC** en sus notas de versión GitHub. Para ediciones reales de DBC, tabla de lista, ID de registro, campo con nombre e índice de base cero, valores antiguos/nuevos, ediciones/configuraciones regionales afectadas y motivo, con hashes antes/después y evidencia de comparación. Para DBC sin cambios, registre explícitamente **Sin ediciones de DBC**. Separe las ediciones de geometría, textura e instalador de los cambios de DBC. Consulte el registro de cambios para conocer el formato requerido y los límites de validación.
