<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Corrección 1.1.8** — Setup revisa los MPQ de Data y de la carpeta del idioma activo para detectar Patch-Y renombrados conocidos y copias exactas del catálogo. Si hay un posible conflicto o un archivo ilegible o no compatible, se detiene e indica el archivo sin borrarlo automáticamente. Cambiar el nombre de un archivo no cambia el hash de su contenido. Los archivos del juego siguen en 3.0.8.
>
> La traducción completa aún no se ha actualizado debido al límite de solicitudes de Google. El texto anterior que aparece debajo corresponde a una versión previa. Consulta la información actual en inglés. [English](../../../KNOWN-LIMITATIONS.md) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../KNOWN-LIMITATIONS.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="known-limitations-and-assumptions"></a>

# Limitaciones y suposiciones conocidas



[Volver a Lau Setup](README.md) · [Recomendaciones y solicitudes de funciones](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [Historial de cambios de DBC](DBC-CHANGELOG.md)

Lea esto antes de proponer una función. Lau Setup instala una actualización visual del lado del cliente para **WoW 3.3.5a compilación 12340**. No es un marco de modificación del servidor. Los límites a continuación describen el proyecto actual; fuera del alcance no significa necesariamente que sea técnicamente imposible.

<a id="what-we-can-and-cannot-change"></a>

## Lo que podemos y no podemos cambiar

| Solicitar | Límite actual |
| --- | --- |
| Mejorar indicadores de terreno soportados, texturas, modelos o tablas de clientes localizadas | Dentro del alcance, sujeto a dependencias de archivos y pruebas. Una mejora visual no debe describirse como un cambio en el daño o la mecánica del servidor. |
| Mejorar la instalación, las copias de seguridad, la accesibilidad o la documentación | Dentro del alcance. Conserve archivos no relacionados y verifique la instalación y recuperación. |
| Cambiar Warmane scripts de daño, detección de golpes, duración de habilidades, orientación o encuentros | Fuera de nuestro control. Warmane ejecuta su propio código de servidor; este proyecto no tiene acceso para cambiar o implementar ese código. Un MPQ o complemento no puede hacer que el servidor adopte mecánicas diferentes. |
| Agregue código C++ personalizado al núcleo de Warmane | No es algo que esta versión pueda ofrecer. Los cambios en un servidor de prueba controlado por separado no cambian Warmane. |
| Inyecte una DLL, conecte el cliente o agregue un nuevo comportamiento de motor nativo | Fuera del flujo de trabajo de parches/complementos admitidos. Esto requiere una investigación de ingeniería y compatibilidad por separado, no solo una edición de DBC. No se proporciona ningún marco de inyección de DLL ni soporte general para el enlace del cliente. |
| Desbloquear acciones Lua protegidas o API de juegos faltantes | No es una característica compatible. El complemento editable Lua y las acciones protegidas del cliente son cosas diferentes. Reescribir Lua no otorga permisos ni crea una API que el cliente no expone. Informe la acción/API exacta antes de asumir que existe una solución alternativa. |
| Proporcionar un cliente completo, otro paquete de idiomas o una base de modelo HD | No incluido. Traiga un cliente compatible existente con los archivos de idioma, las fuentes y la configuración del modelo necesarios. |

El `WoW.exe` compatible proporcionado por la instalación tiene una función específica en el renderizador de carga aprobado, capacidad de archivo y soporte para direcciones grandes. Su inclusión **no** es una promesa de modificaciones arbitrarias de ejecutables o DLL. Del mismo modo, no todos los archivos Lua están protegidos o no son editables: los cambios ordinarios en los complementos y en la interfaz de usuario pueden ser factibles dentro del comportamiento admitido del cliente.

<a id="indicators-are-visual-guidance"></a>

## Los indicadores son una guía visual

- **Warmane es la referencia en tiempo de ejecución para los informes Warmane.** AzerothCore y los clientes aislados ayudan a verificar la integridad y el comportamiento de los archivos en esos entornos. No pueden probar la detección de impactos personalizada, el momento o el comportamiento de encuentro de Warmane.
- **Un borde dibujado no es un límite seguro garantizado.** Las respiraciones admitidas y Slime Spray utilizan conos totales 90° siguiendo los comentarios del evaluador. Halion meteor-fire utiliza la ampliación test-v2 aceptada. Estas son advertencias visuales basadas en observaciones, no en mediciones de la fuente del servidor de Warmane.
- **El terreno puede recortar indicadores planos.** Una malla de suelo plana puede cruzar pendientes, escalones y superficies irregulares. Ampliarlo o elevarlo no garantiza una proyección que siga el terreno en todas partes.
- **La duración del efecto necesita evidencia de encuentro.** La retroalimentación de persecución/fantasma ha incluido efectos que desaparecen después de uno o dos segundos. Cambiar una textura, forma o animación en bucle por sí solo no prueba que el cliente mantendrá viva la instancia del efecto durante toda la búsqueda. Una solución de tiempo necesita imágenes y evidencia de eventos para esa habilidad específica; No trate una maqueta o una compilación experimental como una solución confirmada.
- **Las maquetas son ilustrativas.** Las animaciones del sitio web/chat demuestran la apariencia. No son grabaciones ni prueba de representación, duración o cobertura del juego.

Para informes de límites o tiempos, incluya el encuentro, la habilidad, la dificultad, la edición del cliente, `/pyversion` y un clip que muestre el inicio y el final del daño o efecto. Las capturas de pantalla son útiles, pero los efectos de perspectiva y superposición limitan las mediciones exactas del radio.

<a id="dbc-and-patch-compatibility"></a>

## Compatibilidad con DBC y parches

Las tablas DBC son datos conectados, no conmutadores independientes. Agregar un elemento visual puede requerir referencias coincidentes de hechizos, elementos visuales, kits, efectos y modelos. Reemplazar una tabla completa también puede reemplazar su texto localizado y entrar en conflicto con otro parche que proporciona la misma tabla.

La dependencia de la localización fue un problema real durante el desarrollo de este proyecto. Andre y Lau trabajaron juntos. La [auditoría histórica de DBC](DBC-CHANGELOG.md) separa el cronograma de desarrollo informado de la evidencia de archivo retenida: la línea de base de Andre omitió `Spell.dbc`, no todos los DBC. No asuma que copiar una tabla en inglés a otra configuración regional es seguro.

- Utilice la edición que coincida con su configuración actual HD/modelo original. Las nuevas imágenes de hechizos requieren dependencias HD compatibles; La detección no certifica todos los paquetes de modelos de terceros.
- Si elimina o desactiva los parches del modelo HD después de la instalación, vuelva a ejecutar la instalación más reciente para la configuración resultante. Una edición HD instalada no se convierte dinámicamente. Los activos no coincidentes pueden producir imágenes faltantes o incorrectas y pueden requerir una investigación de los accidentes; No se garantiza ni un fallo ni un comportamiento libre de fallos.
- Las ubicaciones raíz y local activa tienen funciones distintas. En particular, los dos archivos S son diferentes. Siga la [guía de colocación](docs/TECHNICAL.md#file-placement), no una instrucción genérica para duplicar cada MPQ.
- Se conservan los parches no relacionados, pero la conservación no es una garantía de compatibilidad. Otro archivo que anule los mismos datos puede cambiar el resultado.
- El contenido del juego admite nueve configuraciones regionales; La interfaz del instalador está actualmente en inglés. Cambiar `Config.wtf` por sí solo no instala los archivos o fuentes de otro idioma.

<a id="installer-and-recovery-assumptions"></a>

## Supuestos del instalador y de la recuperación

Cierre WoW completamente antes de la instalación o restauración. Utilice exactamente la carpeta de cliente deseada y mantenga intacto `LauSetupBackups`.

El programa de instalación compara los hashes de archivos reales con su **catálogo integrado**. Se puede detectar un cambio de un byte incluso cuando el tamaño y la marca de tiempo coinciden, pero un instalador antiguo todavía conoce sólo su catálogo antiguo. Descargue el instalador más reciente al actualizar. El programa de instalación no monitorea continuamente un cliente después de que sale ni concilia automáticamente cambios de parches manuales posteriores.

Al desactivar las imágenes visuales de nuevos hechizos se conservan los archivos S con alcance como `.mpq.disabled`. La reactivación utiliza bytes deshabilitados coincidentes cuando están disponibles y mueve la copia simple deshabilitada a la copia de seguridad de la transacción verificada. Se conservan las copias más antiguas con el sufijo hash. Consulte la [implementación de recuperación actual](docs/TECHNICAL.md#setup-117-re-enable-cleanup).

La restauración depende de las copias de seguridad y los registros de recuperación. Se detiene cuando cambios posteriores hacen que la restauración automática sea insegura. No puede prometer la recuperación de archivos cuya única copia de seguridad fue eliminada. La eliminación de Patch-Y por sí sola no supone una reversión completa del ejecutable y de otros parches instalados mediante el programa de instalación. Utilice **Restaurar instalación anterior** para la transacción administrada.

<a id="platform-and-validation-limits"></a>

## Plataforma y límites de validación

El destino Windows documentado es Windows 10/11 con .NET Framework 4.8. La configuración Linux probada utiliza Wine 11.0, Wine Mono 10.4.1, un prefijo 64-bit existente y Python 3.9+. Los instaladores de tiempo de ejecución no están incluidos. Siga los [requisitos previos de Wine](wine/README.md); utilice el almacenamiento local Linux. Las carpetas vinculadas, los recursos compartidos de red y las unidades montadas en Windows están fuera de la configuración de ruta compatible con Wine.

Lutris, Proton, la integración específica de Steam Deck y macOS no son objetivos de integración compatibles en esta versión. Esto no afirma que cualquier otro entorno sea imposible; significa que no hemos establecido soporte para ello. Los paquetes para Windows no están firmados digitalmente.

Las compilaciones, las comprobaciones de hash, las pruebas de regresión del instalador, las pruebas Wine y las pruebas en el juego responden a diferentes preguntas. Pasar uno no reemplaza a los demás. Las comprobaciones visuales son muestras, no la certificación de cada zona, encuentro, escala de visualización, distribución Linux o modificación de cliente de terceros. Consulte el informe de validación de cada versión para conocer lo que realmente se verificó.

<a id="before-requesting-a-feature"></a>

## Antes de solicitar una función

Describe el problema visible para el jugador, tu configuración y la evidencia. Las propuestas dentro del alcance admitido son bienvenidas en [Ideas](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas); Los defectos reproducibles pertenecen a [Problemas](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

Para propuestas DLL, código nativo, acción protegida o dependientes del servidor, identifique la dependencia explícitamente. Necesitan un trabajo de viabilidad y un control adecuado del sistema afectado antes de que se pueda prometer su implementación. No los archive como simples opciones DBC faltantes.
