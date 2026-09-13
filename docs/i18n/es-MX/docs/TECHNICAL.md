<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.4.0. [English](../../../TECHNICAL.md) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **Descarga actual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.4.0.
>
> **1.4.0:** Los archivos adicionales de mejora reconocidos se respaldan y la instalación continúa. Restaurar los devuelve. No hay que moverlos manualmente. Setup conserva automáticamente los archivos existentes antes de reemplazarlos o moverlos. Los archivos ajenos a la actualización no se modifican.


> **1.4.0:** Elegir carpeta del juego → Siguiente → elegir aspecto → Siguiente → revisar → Instalar actualización → Finalizar. Patch-Y HD o Patch-Y Non-HD queda fijado según el cliente detectado. Las opciones extra empiezan desactivadas; se conservan los mapas ya instalados. La revisión muestra Patch-Y (versión de Lau) y los extras elegidos, WoW.exe, Patch-Q, archivos de idioma, descarga y copias de seguridad. Siguiente no modifica archivos del juego. Puedes elegir el idioma de la interfaz en cada paso; se guarda y Automático vuelve al idioma del sistema. Restaurar instalación anterior sigue disponible.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../TECHNICAL.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="technical-reference"></a>

# Referencia técnica



[Volver a Lau Setup](../README.md)

<a id="build-and-verification"></a>

## Construcción y verificación

Ejecute `tools/build.ps1` en Windows con el compilador .NET Framework instalado. El paquete de código fuente público contiene la aplicación, el catálogo integrado, el script de compilación y la documentación. La caja de desarrollo completa contiene además `tools/test.ps1` para pruebas de transacción, descarga, ruta, proceso, recuperación y regresión de GUI; esas pruebas utilizan accesorios aislados y un ejecutable de referencia local. `tools/build.ps1 -Release` rechaza un catálogo que no ha pasado la puerta de publicación. El arnés de prueba, la generación de carga útil y las pruebas del juego nativo dependen de rutas de origen locales privadas y no forman parte del paquete de código fuente público.

`build/catalog.json` nombra cada recurso y segmento de descarga por tamaño y SHA-256, junto con las URL de publicación de GitHub observadas. El catálogo fija el repositorio, la etiqueta de lanzamiento y el archivo con nombre hash. El instalador se descarga de forma anónima y comprueba cada redireccionamiento antes de seguirlo. El instalador no requiere ninguna cuenta GitHub, navegador registrado ni credencial API. En la verificación de desarrollo completo, los asociados de `tools/refresh_github_catalog.py` cargaron activos sin cambiar los hashes, y `tools/verify-public.ps1` verifica cada segmento y activo reconstruido a través del mismo descargador utilizado por la aplicación.

<a id="file-placement"></a>

## Colocación de archivos

| Componente | Destino |
|---|---|
| Ejecutable compatible | `WoW.exe` |
| Q regional seleccionada | Copias idénticas en raíz `Data/patch-q.mpq` y configuración regional activa `Data/<locale>/patch-<locale>-Q.MPQ` |
| Edición seleccionada Y | Copias idénticas en raíz `Data/patch-y.mpq` y configuración regional activa `Data/<locale>/patch-<locale>-Y.MPQ` |
| Nuevos recursos de hechizo, cuando se seleccionan | Raíz `Data/patch-s.mpq` |
| Coincidencia de tablas de hechizos localizadas, cuando se seleccionan | Configuración regional activa `Data/<locale>/patch-<locale>-S.MPQ` |
| Mapas/minimapa opcionales | Raíz `Data/patch-m.mpq`; se realiza una copia de seguridad de la configuración regional activa M reemplazada |

Core Q conserva el LoadingScreens.dbc de la versión, el Map.dbc localizado y la carga de imágenes byte por byte. Omite las definiciones de mapas mundiales y las ilustraciones del mapa mundial agregadas. El modo de mapa completo utiliza la Q regional original y la M compartida sin volver a empaquetarlas. Las dos ubicaciones S contienen archivos diferentes. Desactivar nuevos hechizos conserva el par raíz/localización S con ámbito como .mpq.disabled; La reactivación mueve las copias simples deshabilitadas a copias de seguridad de transacciones verificadas, como se describe en la sección Configuración 1.1.7 a continuación. La detección de HD requiere los parches F raíz y local existentes que coincidan.

<a id="recovery-design"></a>

## Diseño de recuperación

Un bloqueo de cliente cubre la descarga, la preparación y la instalación. Los archivos se verifican antes de la preparación y nuevamente después de su colocación. Los archivos existentes se trasladan a `LauSetupBackups/transactions/<id>/before/`, conservando sus bytes y marcas de tiempo; el diario se escribe de forma duradera antes de comprometerse. Una confirmación fallida restaura los originales cuando es seguro. Las confirmaciones y restauraciones interrumpidas permanecen visibles cuando se vuelve a abrir la aplicación, incluso sin WoW.exe.

Restaurar rechaza archivos modificados por otra actualización y mantiene la copia de seguridad para resolución manual. Sólo se aceptan rutas Q/M/S/Y exactas de raíz/localización activa y WoW.exe. Se rechazan los puntos transversales, alternativos y de análisis; Los archivos reanudados grabables deben tener un enlace físico. Los temporales de revistas y asambleas utilizan nombres únicos y de creación exclusiva. La aplicación nunca enumera un archivo en el sistema de archivos del cliente.

<a id="release-boundaries"></a>

## Liberar límites

Este instalador no está firmado digitalmente. Las pruebas del instalador Windows y Wine, las comprobaciones de la GUI de muestra y la línea base de datos del juego retenida se registran por separado en VALIDATION.json. Las comprobaciones Wine 1.1.0 utilizan Wine 11.0 / Wine Mono 10.4.1 y el almacenamiento local de superposición de Docker; la prueba de montaje anidado se burla de la identidad del dispositivo porque ese contenedor no puede crear montajes. Estas comprobaciones no certifican cada distribución/sistema de archivos de Linux, escala de visualización, encuentro o modificación de cliente de terceros. Los archivos ZIP sin formato de la edición Patch-Y están disponibles en las versiones GitHub. Consulte [limitaciones conocidas](../KNOWN-LIMITATIONS.md) para conocer el alcance y los supuestos actuales.


<a id="306-color-update--setup-112"></a>

## 3.0.6 actualización de color/Configuración 1.1.2

Cada uno de los seis archivos Y cambia tres miembros de M2 ​​y el TOC de !PYAndre, y agrega dos texturas BLP. `Spells/PW_Coldflame_Ground.m2` ahora hace referencia a `Spells/PW_Coldflame_Blue.blp`; Referencia `Spells/PW_HalionMeteor_Ground.m2` y `Spells/PW_HalionMeteor_Ring.m2` `Spells/PW_Halion_Red.blp`. Sólo la longitud/desplazamiento del nombre de archivo del descriptor de textura 4 cambia en cada modelo original; se adjunta la nueva ruta. Las texturas de partículas nativas (índices 0–3), máscaras, geometría, pistas de animación global, límites y bytes DBC no cambian. La textura blanca compartida permanece sin cambios para otros indicadores.

Las nuevas texturas conservan el formato opaco 8×8 DXT1 BLP2 existente y los cuatro niveles de mip. Solo cambia el punto final RGB565: el azul claro se decodifica como (120,216,248,255), el rojo como (248,68,40,255). La cuantización es inherente al formato de textura existente. Ambos modelos Halion utilizan la misma textura roja. Las opciones de consagración y edición del modelo siguen siendo independientes.

Las decisiones de actualización comparan el SHA-256 y el tamaño reales, no las etiquetas de lanzamiento ni las marcas de tiempo. Las pruebas de regresión modifican un byte sin cambiar el tamaño del archivo o la marca de tiempo en cada ubicación Y, requieren exactamente una operación de reparación, verifican el hash reparado y luego restauran la versión anterior. Un EXE antiguo incorpora el catálogo anterior, por lo que la actualización requiere descargar primero el nuevo EXE/ZIP.

<a id="307-halion-radius--setup-113"></a>

## 3.0.7 Radio de halión / Configuración 1.1.3

Promueve bytes de prueba v2 exactos para `Spells/PW_HalionMeteor_Ground.m2`, `Spells/PW_HalionMeteor_Ring.m2` y sus archivos `00.skin`. Las coordenadas X/Y de la malla son 1.5 multiplicadas por 3.0.6. Se conservan Z/UV/normales y animaciones/pistas de partículas. Los límites del modelo (desplazamiento 160), los límites de la secuencia (secuencia +32) y los límites de la submalla de revestimiento (submalla +20) reflejan la geometría ampliada. La versión TOC cambia de 3.0.6 a 3.0.7. Exactamente cinco miembros existentes cambian por edición; no se agregan ni eliminan miembros. Se excluye la geometría de prueba v3. Coldflame y todos los demás miembros coinciden con 3.0.6. Aceptación del probador transmitida por el usuario de v2; No se reclama la certificación de encuentro amplio.

<a id="308-all-cones--setup-114"></a>

## 3.0.8 todos los conos / Configuración 1.1.4

Las seis ediciones utilizan una geometría de ventilador total en grados 90. Los nombres de archivos de los modelos heredados y todas las filas DBC permanecen sin cambios para preservar el enrutamiento de hechizos. Cambios: PW_White_Fan60_60yd_Glowing (Halion ambos reinos), PW_White_Fan60_30yd_Glowing (Saviana), PW_White_Fan60_100y_Glowing (ICC Rimefang) y PW_Rotface_SlimeSpray_Fan25_Room (Rotface) se amplían desde 60 a 90; PW_White_Fan82_60yd_Glowing (Sartharion) se amplía de 82 a 90. PW_White_Fan75_60yd_Glowing (Sindragosa) ya es 90 y tiene bytes idénticos.

Para cada modelo modificado, solo cambian el vértice XY (zancada de vértice 48-byte) y los límites. Ángulo sobre +X escalas por 90/old-angle; se conservan el radio de cada vértice y Z. Se actualizan los límites del modelo en el desplazamiento 160, los límites de secuencia en la secuencia+32 y los límites de la submalla de piel en la submalla+20. Los rayos UV, las normales, la animación y las pistas de partículas permanecen sin cambios. Diez miembros de modelo/apariencia y dos cadenas de versión en el TOC cambian por edición; no se agregan ni eliminan miembros. Todos los demás miembros, incluida la geometría Halion meteor-fire test-v2 y Coldflame, coinciden con 3.0.7 byte por byte.

<a id="setup-115-disabled-patch-s-preservation"></a>

## Configuración 1.1.5 deshabilitada preservación de Patch-S

Sólo las rutas S raíz y de configuración regional activa obtienen el sufijo .disabled. Cada desactivación crea una copia preparada local con hash antes de desactivar S; Ambos caminos están marcados con un diario, con un máximo de once destinos. La reversión restaura los archivos activos originales y elimina solo las copias deshabilitadas recién creadas. Las copias deshabilitadas idénticas preexistentes permanecen fuera de la transacción y se conservan. Los archivos o directorios en conflicto bloquean la planificación. Al volver a habilitar se instalan los recursos del catálogo S y no se consumen las copias deshabilitadas. Las revistas existentes siguen siendo legibles. No se aceptan rutas de origen locales arbitrarias: cada copia local debe coincidir con su operación de desactivación S emparejada.

<a id="setup-116-disabled-copy-collisions"></a>

## Configurar 1.1.6 colisiones de copia deshabilitadas

El archivo S activo actual siempre toma el nombre simple .mpq.disabled. Antes de reemplazar un archivo deshabilitado existente diferente, el programa de instalación coloca sus bytes en un hermano que termina en los primeros caracteres 12 de su SHA-256; SHA-256 completo y la longitud se verifican antes de cualquier reutilización. Esto mantiene los nombres dentro de los límites de ruta existentes Windows. Los contenidos de archivo conflictivos no se cierran. El S activo, el archivo simple deshabilitado y la copia de archivo recién creada se registran de forma independiente, con un máximo de trece entradas; la reversión restaura todos los originales. Las fuentes locales están restringidas a la desactivación de S emparejado o a operaciones de reemplazo de archivos deshabilitados. Las revistas antiguas siguen siendo legibles.

<a id="setup-117-re-enable-cleanup"></a>

## Configurar 1.1.7 volver a habilitar la limpieza

Habilitar la eliminación de nuevos diarios de hechizos de los archivos S deshabilitados de raíz simple y configuración regional activa. La transacción mueve sus bytes originales verificados a su copia de seguridad anterior fuera de Datos. Si un archivo deshabilitado coincide con el catálogo SHA-256 y el tamaño, se almacena localmente para el destino S coincidente y se excluye de las descargas. Las fuentes locales deben combinarse con el activo de catálogo y eliminación de archivos deshabilitados exacto. Active S que ya coincide todavía produce una transacción de limpieza. Los archivos existentes con sufijo hash no se barren. Las revistas anteriores siguen siendo legibles. Se cubren encendido/apagado/encendido, deriva de fuente, interrupciones en cada nuevo paso de confirmación/restauración, todas las configuraciones regionales y restauración apilada.
