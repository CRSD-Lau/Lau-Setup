<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../TRANSLATION.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="repository-translations"></a>

# Traducciones del repositorio

La acción **Traducir documentación** GitHub utiliza el **sitio web gratuito de Google Translate** para mantener la documentación del repositorio disponible en todos los idiomas admitidos del juego, además del **portugués brasileño**. No se requiere clave API, cuenta paga de Cloud Translation, suscripción ni descarga de modelo.

Utilice los enlaces de idiomas en la parte superior del archivo README. GitHub muestra el archivo README raíz de forma predeterminada; Los visitantes eligen su idioma utilizando estos enlaces. Este flujo de trabajo traduce documentación, incluidas guías de instalación y referencias técnicas. No traduce la interfaz de GitHub, los problemas, las descripciones de las versiones, el sitio web independiente o la interfaz del instalador, y no agrega una configuración regional del juego en portugués.

<a id="languages"></a>

## Idiomas

La cobertura se compara con `build/catalog.json`, y se agrega `ptBR` para documentación. Las opciones de lectura son inglés, alemán, español para España y México, francés, coreano, ruso, chino simplificado, chino tradicional y portugués brasileño.

El selector de idioma web de Google identifica `pt` como portugués (Brasil); El portugués (Portugal) es un objetivo diferente. Google proporciona un destino `es`, por lo que las páginas de España y México utilizan la misma traducción general al español. Los objetivos chinos están separados. Los códigos de destino de Google y los nombres de idiomas nativos se encuentran en `tools/translation-locales.json`. Agregar una configuración regional del juego requiere agregar su mapeo de documentación; La cobertura faltante no supera la validación.

<a id="automatic-updates"></a>

## Actualizaciones automáticas

Los impulsos que cambian la documentación en inglés, el catálogo o las herramientas de traducción activan la acción. Los mantenedores también pueden seleccionar **Acciones → Traducir documentación → Ejecutar flujo de trabajo → principal**. Descubre archivos de texto y Markdown rastreados en la raíz del repositorio y `docs/`, además de `wine/README.txt`. Se excluyen las traducciones generadas y `AGENTS.md`. Las guías de texto se representan como Markdown en `docs/i18n/<language>/`.

Sólo los documentos modificados necesitan traducción. Los hashes de origen y salida y un caché de segmento evitan solicitudes repetidas. Toque `TRANSLATION_REVISION` al cambiar las convenciones de traducción. Como máximo se ejecutan tres trabajos de idiomas a la vez, con una pausa entre las solicitudes de cada trabajo. Un límite de tarifa detiene el trabajo afectado; Vuelva a intentarlo más tarde. La interfaz web gratuita no es oficial para la automatización y puede cambiar o bloquear solicitudes. No hay ningún respaldo pagado. Las páginas publicadas existentes permanecen disponibles cuando falla la generación.

La ejecución estándar del ejecutor alojado en GitHub es gratuita para este repositorio público. Los trabajos se deshabilitan si el repositorio se vuelve privado. Los pequeños artefactos intermedios caducan al cabo de un día; no se almacena ningún modelo o dependencia grande.

<a id="integrity-and-publication"></a>

## Integridad y publicación

El código, los comandos, las URL, los números de versión, los nombres de productos, los créditos y las declaraciones de estado de las firmas están protegidos. Los enlaces de documentos relativos apuntan al mismo idioma, mientras que los enlaces de imágenes y códigos apuntan a los originales. Los anclajes de encabezado estables en inglés conservan los enlaces de las secciones. Cada página se identifica como una traducción automática, enlaza a su fuente en inglés y conserva los metadatos de Autor, Creador y Última modificación por para **Neil Mitchell**.

Las nueve opciones de lectura traducidas deben pasar comprobaciones de integridad de fuente/salida antes de su publicación en `main`. La publicación rechaza una revisión de la fuente modificada y nunca la fuerza. Las solicitudes de extracción ejecutan verificaciones de unidades y una verdadera traducción de humo README al portugués brasileño con acceso de solo lectura. Si la protección de la sucursal impide posteriormente el compromiso, adapte la publicación al proceso de relaciones públicas aprobado.

La traducción automática todavía necesita una revisión fluida del lector. El inglés sigue siendo autoritario. Para correcciones duraderas, actualice la fuente en inglés o las herramientas de traducción; Se regenerarán las ediciones directas de los archivos generados. Los lotes fallidos o parciales no reemplazan los documentos existentes.

<a id="local-use"></a>

## Uso local

Python 3.11 o más reciente es suficiente; no se requieren paquetes adicionales. Verificar estructura sin acceso a la red:

```sh
python -m unittest discover -s tests -p test_translate_docs.py -v
python tools/translate_docs.py --check
```

Traduzca documentación pública utilizando el sitio web gratuito de Google:

```sh
python tools/translate_docs.py --locale ptBR
python tools/translate_docs.py --navigation
```

Referencias: [Google Translate](https://translate.google.com/), [GitHub Facturación de acciones](https://docs.github.com/en/billing/concepts/product-billing/github-actions). La [API de Google Cloud Translation](https://cloud.google.com/translate/pricing) independiente es un servicio facturado y no se utiliza aquí.
