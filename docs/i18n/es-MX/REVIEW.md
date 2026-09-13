<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../REVIEW.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="installer-review"></a>

# Revisión del instalador

Autor: Neil Mitchell  
Creador: Neil Mitchell  
Última modificación por: Neil Mitchell

Revisó la nueva aplicación con la lista de verificación de revisión de GStack, incluida una revisión de seguridad independiente de solo lectura. Todos los problemas de implementación identificados se abordaron dentro del trabajo del instalador autorizado:

- Un ejecutable faltante podría impedir la selección del cliente para la recuperación de fallos. La selección de carpetas ahora descubre y valida los registros de recuperación antes de inspeccionar WoW.exe. Una prueba de regresión GUI cubre el caso de falta de ejecutable.
- Las descargas se produjeron antes del bloqueo de la operación. Un contrato de arrendamiento ahora cubre el caché de descarga mediante confirmación; La recuperación pendiente se verifica dentro de ese contrato de arrendamiento.
- Los temporales de escritura predecibles podrían seguir enlaces duros NTFS. Los temporales de diario y ensamblado ahora usan nombres GUID con CreateNew. Los archivos parciales reanudados se abren exclusivamente y se verifica su recuento de enlaces antes de truncarlos o escribirlos. Una prueba de regresión de vínculo físico real demuestra que el archivo no relacionado permanece sin cambios.
- Un diario de restauración manipulado podría crear un bloqueo en otra raíz antes de la validación. El tamaño, la ubicación, la raíz, la configuración regional, las entradas y las rutas de alcance ahora se validan antes de adquirir el bloqueo de restauración. Una prueba de regresión demuestra que no se crea ningún bloqueo externo.
- La restauración interrumpida no tenía estado reanudable propio. RESTORING se registra antes de la mutación y se reconoce a lo largo de la interfaz de usuario y la ruta de recuperación. Inyección de fallas después de cada paso de restauración.
- Las opciones de mapas instaladas/restauradas podrían permanecer obsoletas en la interfaz de usuario. La detección de clientes se actualiza después de cada operación exitosa. La prueba de GUI instala la selección del mapa, verifica su estado retenido, restaura y verifica el estado anterior.

La migración GitHub además fija el repositorio, la etiqueta de versión y el nombre del archivo en el catálogo integrado. Los redireccionamientos se siguen manualmente para que cada destino HTTPS se verifique antes de una solicitud, incluidas las credenciales y las verificaciones de puertos. Se eliminó el antiguo analizador de confirmación HTML de Google Drive. Las pruebas agregadas cubren la manipulación de URL del catálogo, una transferencia reanudable redirigida y destinos de redireccionamiento rechazados.

Una revisión independiente de la migración encontró que la optimización de Python podría eliminar los controles de publicación escritos como afirmaciones. Las comprobaciones de carga, actualización del catálogo y puerta de lanzamiento ahora generan excepciones explícitas. El cargador también resuelve cada fuente y requiere que permanezca directamente dentro del directorio de carga útil. Las pruebas de protección de publicación pasan bajo `python -O` para rutas de archivos, tamaños, hashes y manipulación remota de URL/resúmenes.

Última suite de regresión completa: `reports/tests-20260911-200603/results.json`; Se aprobaron los grupos de prueba 38, incluidas las combinaciones de instalación/restauración de dispositivos reales 108, todos los puntos de interrupción de confirmación/restauración, protección de rutas/uniones/vínculos duros, bloqueos de procesos y archivos, corrupción/desviación, manejo de rango HTTP, cancelación, ensamblaje fuera de línea e instalación/restauración de GUI utilizando el ejecutable con versión real.

La revisión de la interfaz de usuario 1.0.1 cubre texto de apoyo más brillante, texto de pie de página más grande y pintura personalizada de control deshabilitado. La semántica habilitada de forma nativa permanece vigente; Sólo la apariencia deshabilitada se dibuja manualmente. Se inspeccionaron visualmente las vistas previas iniciales, listas y ocupadas de Windows. Core.cs, Downloader.cs y todas las cargas útiles del juego permanecen idénticas en bytes a v1.0.0. Se conserva la evidencia del juego/red; El conjunto de regresión Windows se vuelve a ejecutar para esta actualización. La sonda de viabilidad Wine no pasó la construcción y no establece soporte de plataforma.

Las comprobaciones de publicación y los metadatos binarios finales son puertas independientes. Consulte el comunicado VALIDATION.json para conocer el alcance de la evidencia, incluidas las comprobaciones que se conservaron de la línea base del juego sin cambios.

<a id="installer-110"></a>

## Instalador 1.1.0

La implementación de Wine siguió a un Consejo de tres opiniones y dos revisiones por pares.
Mantiene el motor de transacciones de C# y requiere un Linux autenticado en vivo
ayuda para la inspección de rutas Wine, comprobaciones de procesos de host y bloqueo de prefijos cruzados.
El asistente rechaza enlaces, carcasas ambiguas, visibilidad restringida del proceso y
sistemas de archivos no compatibles. Las asignaciones de unidades Wine se aceptan solo después de la configuración nativa.
inspección de objetivos. La política de proceso requiere de manera conservadora todo WoW
instancias a cerrar. Los controles repetidos reducen las carreras; no se bloquean
programas no relacionados o eliminar cambios hostiles simultáneos en el sistema de archivos.

La revisión de implementación enfocada encontró cobertura de montaje anidado y liberación de bloqueo.
después de una raíz, cambie el nombre de los espacios. Ambos eran fijos: rutas gestionadas y sus más cercanas.
Los ancestros existentes deben permanecer en el sistema de archivos local del cliente y liberarse.
utiliza la ruta nativa guardada y el token sin necesidad de que la raíz aún exista.
Pasan las pruebas nativas correspondientes.

Las comprobaciones de espacio libre ahora consultan el caché Linux real y los sistemas de archivos del cliente.
en lugar de la raíz de la unidad asignada de Wine. Pruebas reales de descarga e instalación de Wine
con cero espacio libre reportado, rechace la operación y conserve los archivos originales.

La validación incluye grupos 38 en Windows y 38 en Wine, pruebas auxiliares nativas 15.
8 Wine casos de seguridad que incluyen dos prefijos y pérdida de ayuda después de un movimiento, un
Nueva instalación/reversión anónima de GitHub en Wine y un iniciador de usuario normal
y transacción de accesorios. El ICO W-and-shield se copia byte por byte del
favicon del sitio de lanzamiento existente. Las instantáneas de la interfaz de usuario cubren inicial, listo y ocupado
estados; Se revisó la rama de requisitos previos Windows y se actualizó el tiempo de ejecución instalado.
camino ejercido. No se modificó ninguna máquina Windows que careciera de .NET para una prueba.
El código final también repite la instalación central y la reversión exacta con el
bytes de carga útil GitHub previamente descargados y repetidos.

<a id="setup-117-review"></a>

## Configuración de revisión de 1.1.7

Se revisó la diferencia actual para el alcance de la ruta, la confianza en la fuente local, la selección de descargas, las comprobaciones previas/de deriva de confirmación, las copias de seguridad de las transacciones y la compatibilidad con la reversión. No hay hallazgos no resueltos. La reutilización local se limita al par S raíz/localización activa que coincide con el catálogo; Los archivos deshabilitados se mueven a través del diario de respaldo verificado existente. Ambas plataformas pasaron los grupos de regresión 50 y el archivo de lanzamiento real activado/desactivado con reversión apilada exacta. No hay cambios en la carga útil del juego.
