<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.3.0. [English](../../../DBC-CHANGELOG.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Descarga actual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.3.0.
>
> **1.3.0:** Los archivos adicionales de mejora reconocidos se guardan en una copia de seguridad y la instalación continúa. Restaurar los devuelve. No hay que moverlos manualmente. Setup conserva automáticamente los archivos existentes antes de reemplazarlos o moverlos. Los archivos ajenos a la actualización no se modifican.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../DBC-CHANGELOG.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="dbc-changelog"></a>

# Registro de cambios de DBC



Realice un seguimiento de las ediciones de DBC del cliente por separado de los cambios de modelo, textura e instalador. Las versiones del juego y las versiones del instalador están separadas: `/pyversion` informa la edición del juego.

<a id="handoff-history-andre-303-onward"></a>

## Historial de traspasos: Andre 3.0.3 en adelante

[Ediciones de DBC individuales e historial de desarrollo](docs/dbc/history/INDIVIDUAL-EDITS.md) · [Comparación de seis ediciones y hashes de referencia](../../dbc/history/andre-to-3.0.4.json)

Andre omitió intencionalmente **Spell.dbc** para evitar conflictos de localización. La anulación inicial de Lau expuso esa dependencia; **Lau y Andre lo depuraron juntos** y la reconstrucción multilingüe resolvió el problema de compatibilidad del texto ortográfico. Los archivos Andre retenidos contienen otros seis DBC visuales/modelos, por lo que esto no debe describirse como una ausencia de todos los DBC.

Lau describe los hitos como **3.0.4: adición de tabla inicial**, **3.0.5: resolución multilingüe** y **3.0.6–3.0.8: revisiones con mejoras de versión**. Las etiquetas de las primeras versiones se superponen: la compilación publicada archivada con la etiqueta 3.0.4 ya contiene la solución multilingüe. Las comparaciones de artefactos a continuación utilizan hashes exactos y no borran ese historial de desarrollo.

La comparación inicial Patch-Y incluye quince ediciones de enlaces visuales de hechizos por edición, nuevos indicadores visuales/kits/registros adjuntos, diferencias de consagración y ediciones de localización decodificadas. La adición de la tabla se compara con su stock subyacente o con la base HD Spell, por lo que los registros heredados no se presentan como trabajos de nuevo autor. [Verificación de la etapa de localización](../../dbc/history/localization-stage.json) confirma la reconstrucción del texto de los datos numéricos conservados en las cuatro ediciones HD/no HD de prelocalización retenidas.

<a id="archived-releases-304--308"></a>

## Lanzamientos archivados 3.0.4 → 3.0.8

| Transición archivada | Resultado DBC | Otros cambios |
| --- | --- | --- |
| 3.0.4 → 3.0.5 | Sin ediciones de DBC; 42 tablas idénticas | Geometría del cono de Sindragosa y Rotface, etiqueta de versión |
| 3.0.5 → 3.0.6 | Sin ediciones de DBC; 42 tablas idénticas | Recursos y referencias de color del marcador Coldflame/Halion, etiqueta de versión |
| 3.0.6 → 3.0.7 | Sin ediciones de DBC; 42 tablas idénticas | Geometría de fuego de meteorito Halion aprobada, etiqueta de versión |
| 3.0.7 → 3.0.8 | Sin ediciones de DBC; 42 tablas idénticas | Geometría del cono de aliento restante/Slime Spray, etiqueta de versión |

[Todas las comparaciones de tablas 168 y hashes de archivos](../../dbc/history/3.0.4-through-3.0.8.json). Estas son comparaciones de artefactos de liberación retenidos, no una afirmación de que el incidente de localización anterior no ocurrió.

<a id="307--308--no-dbc-edits"></a>

## 3.0.7 → 3.0.8 — sin ediciones DBC

Publicado con [Configuración 1.1.4](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.4). Todas las **comparaciones de DBC 42 se realizaron byte por byte**: siete tablas en cada una de las seis ediciones de Patch-Y. No hay tablas agregadas/eliminadas, registros modificados, campos modificados o bloques de cadenas modificados.

| Mesa | Ediciones de registros | Ediciones de campo | Resultado |
| --- | ---: | ---: | --- |
| CreatureDisplayInfo.dbc | 0 | 0 | Idéntico |
| CreatureModelData.dbc | 0 | 0 | Idéntico |
| Spell.dbc | 0 | 0 | Idéntico |
| SpellVisual.dbc | 0 | 0 | Idéntico |
| SpellVisualEffectName.dbc | 0 | 0 | Idéntico |
| SpellVisualKit.dbc | 0 | 0 | Idéntico |
| SpellVisualKitModelAttach.dbc | 0 | 0 | Idéntico |

[Evidencia de comparación completa](../../dbc/3.0.7-to-3.0.8.json) registra el MPQ de origen/destino de cada edición SHA-256, cada DBC antes/después de SHA-256, el tamaño, el recuento de filas y el recuento de campos. Los hash MPQ se compararon con los catálogos de versiones. Los demás recursos del catálogo 22, incluidos los recursos locales Q y S compartidos, no se modifican.

<a id="what-actually-changed-in-308"></a>

### Lo que realmente cambió en 3.0.8

Cinco modelos de cono existentes se ampliaron a **90° en total** editando su geometría `.m2` y sus límites `00.skin` correspondientes. Se conservaron las uniones de DBC existentes.

| Tallo modelo | Ángulo anterior | Nuevo ángulo |
| --- | ---: | ---: |
| PW_Rotface_SlimeSpray_Fan25_Room | 60° | 90° |
| PW_White_Fan60_60yd_Glowing | 60° | 90° |
| PW_White_Fan60_30yd_Glowing | 60° | 90° |
| PW_White_Fan60_100y_Glowing | 60° | 90° |
| PW_White_Fan82_60yd_Glowing | 82° | 90° |

Los nombres de archivos conservan etiquetas de ángulos históricos; la geometría determina el ángulo mostrado. Sindragosa ya era 90° y no cambió en esta transición. Esto llevó todos los indicadores de aliento y spray de limo admitidos a 90°. El alcance y el tiempo de animación se mantuvieron sin cambios. El radio del fuego del meteorito Halion, los colores de Coldflame y la Consagración se mantuvieron sin cambios.

Cada edición cambió exactamente **miembros del archivo 11**: cinco archivos `.m2`, cinco archivos `.skin` y la etiqueta de versión del juego `!pyandre.toc` de 3.0.7 a 3.0.8. Todos los demás miembros del contenido enumerados son idénticos. La contabilidad del contenedor MPQ está fuera de la comparación de contenido-miembro.

Esto verifica los cambios en los archivos del cliente, no la mecánica del servidor de Warmane ni un límite de daño exacto.

<a id="setup-115-116-and-117--no-dbc-edits"></a>

## Configuración 1.1.5, 1.1.6 y 1.1.7: sin ediciones DBC

Estas son revisiones del instalador. Las cargas útiles de su juego siguen siendo 3.0.8, con datos DBC sin cambios. La última revisión cambia la instalación, preservación y reutilización de Patch-S, no su contenido interno de DBC.

<a id="required-entry-for-future-releases"></a>

## Entrada obligatoria para futuras versiones

Cada versión debe agregar una entrada aquí y una sección **Cambios DBC** a sus notas de la versión GitHub, incluidas las versiones exclusivas para el instalador. Indique explícitamente **Sin ediciones de DBC** cuando corresponda. Compárelo con la versión estable anterior del juego, no con una versión de prueba no publicada. No describa una edición de modelo/textura como una edición DBC.

Para cada edición de DBC real, registre una fila por campo (o una diferencia de nivel de fila vinculada y legible por máquina para cambios de localización grandes):

| Transición del juego | Mesa | ID de registro | Nombre de campo/índice de base cero | Valor antiguo | Nuevo valor | Ediciones/locales | Razón |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VERSIÓN → VERSIÓN | TABLE.dbc | identificación | Campo con nombre [índice] | Valor anterior | Nuevo valor | Variantes afectadas | Propósito |

También registre registros y tablas agregados/eliminados, cambios de esquema y ediciones de valores de cadena. Decodifique los valores de las cadenas en lugar de informar la rotación del desplazamiento del bloque de cadenas a medida que cambia el contenido. Especifique la convención de índice de campos y el origen del esquema; etiquetar campos desconocidos en lugar de adivinar. Adjunte hash de tabla y archivo antes/después, el método de comparación y los límites de validación. Nunca reclames una comparación realizada sin evidencia.

La auditoría de transferencia cubre Patch-Y desde las líneas base retenidas Andre 3.0.3 en adelante. Los canales separados de localización de mapas, Q/S/y las compilaciones experimentales no relacionadas están fuera de esta retrospectiva inicial. A ningún artefacto roto anterior se le asigna un número de versión sin coincidir con su procedencia.
