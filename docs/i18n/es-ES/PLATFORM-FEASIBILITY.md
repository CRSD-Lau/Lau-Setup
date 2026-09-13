<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- RELEASE-120-NOTICE -->
> **Setup 1.2.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.2.0. [English](../../../PLATFORM-FEASIBILITY.md) · [1.2.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.2.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../PLATFORM-FEASIBILITY.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="lau-setup-platform-feasibility"></a>

# Lau Setup viabilidad de la plataforma

Autor: Neil Mitchell  
Creador: Neil Mitchell  
Última modificación por: Neil Mitchell  
Fecha de evaluación: 2026-09-11

Actualización: el usuario seleccionó Wine únicamente. El instalador 1.1.0 ahora proporciona la versión probada
Lanzador Wine 11 / Wine Mono 10.4.1 descrito en [la guía Wine](wine/README.md).
La sonda Wine 8 y las recomendaciones siguientes se conservan como evaluación histórica.
La integración de Lutris, Proton y macOS sigue fuera de alcance.

Lau Setup 1.0.1 sigue siendo un instalador de Windows. Linux a Wine es el siguiente objetivo de compatibilidad recomendado. Esta evaluación no certifica la instalación en Linux o macOS. Los casos anteriores de 63 Docker/Wine ejercieron los datos del juego, no este instalador.

| Opción | Recomendación | Qué significa para Lau Setup |
| --- | --- | --- |
| Wine en Linux | Primer objetivo; factible en principio, actualmente no verificado | Reutilice el instalador Windows dentro de un prefijo Wine seleccionado explícitamente. Pruebe su tiempo de ejecución, selección de carpetas, descargas, seguridad de archivos y recuperación antes de publicar el soporte. |
| Lutris | A continuación, después de pases directos Wine | Una pequeña receta de integración puede iniciar la configuración en el prefijo del juego existente. No se necesita ningún formato de carga útil independiente. |
| Vapor / Protón | Más tarde, condicional | Utilice el prefijo correcto del juego existente. Agregar la configuración como otro juego que no sea de Steam puede darle un entorno diferente. La usabilidad de Steam Deck necesita comprobaciones separadas de la pantalla y el controlador. |
| CrossOver en macOS | Posible pista de pruebas separada | Corre dentro de la botella del juego. Validar en hardware macOS real y versiones compatibles de CrossOver; Las pruebas Linux no pueden establecer esto. |
| Wine + DXVK | Configuración de juego opcional | DXVK traduce Direct3D para el juego. No resuelve los requisitos de seguridad de archivos, fuentes o .NET del instalador. |
| whisky | No adoptar como nuevo objetivo de apoyo | Su proyecto upstream ya no se mantiene activamente. |

La clasificación anterior sigue los roles descritos por [Wine Mono](https://github.com/wine-mono/wine-mono), [Lutris](https://lutris.net/about/), [Proton](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [CrossOver's Mac guía](https://support.codeweavers.com/en_US/crossover-mac-user-guide) y [Whisky](https://github.com/Whisky-App/Whisky). Las recomendaciones son nuestra evaluación, no la certificación inicial de Lau Setup. CrossOver puede ejecutar aplicaciones 32-bit Windows en botellas 64-bit; La pérdida de compatibilidad nativa con macOS 32-bit por sí sola no lo descarta.

<a id="bounded-probe-results"></a>

## Resultados de la sonda acotados

La sonda local utilizó Wine 8.0 (Debian 8.0~repack-4), un prefijo win32 aislado y Xvfb. Este tiempo de ejecución más antiguo disponible localmente no es una prueba de las versiones actuales de Wine. No se montó ni modificó ningún cliente de juego personal.

1. La imagen de prueba del juego heredada deshabilitó mscoree. Habilitarlo expuso que Wine Mono faltaba. Este fue un problema del entorno de prueba.
2. Instalado el oficial Wine Mono 7.4.0 MSI en el prefijo desechable después de verificar SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`, fijado por [Wine 8.0la fuente](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3. Un arnés de diagnóstico inicializado WinForms y cargó el catálogo incrustado, luego falló al construir el formulario con `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`. Copiar las fuentes Liberation disponibles en ese prefijo no resolvió el problema. No se produjo ninguna captura de pantalla o instalación exitosa del instalador.
4. La evidencia local se conserva bajo `reports/wine-feasibility/`. El contenedor de la sonda está detenido. El arnés de diagnóstico no está incluido en el instalador distribuido ni en el paquete de fuente pública.

Esto identifica el trabajo de aprovisionamiento de fuentes/tiempo de ejecución, no prueba de que Wine sea imposible. No se intentó ninguna transacción de instalación/restauración bajo Wine en esta sonda.

<a id="acceptance-work-before-wine-support"></a>

## Trabajo de aceptación antes del soporte Wine

1. Establezca una combinación actual reproducible de Wine/tiempo de ejecución/fuente en un escritorio Linux. Muestre los estados inicial, listo, de descarga, de recuperación y de error en escalas de visualización comunes; verificar el acceso al teclado y la selección de carpetas.
2. Verifique la asignación exacta de carpetas de host y el manejo de casos en un sistema de archivos que distinga entre mayúsculas y minúsculas, incluidos los nombres duplicados que difieren solo por mayúsculas y minúsculas. Conserva parches no relacionados y configuraciones personales.
3. Demuestre el comportamiento de enlace, bloqueo exclusivo, espacio libre, diario y reemplazo atómico. Actualmente, el instalador llama a las API de información de archivos Windows; su semántica debe probarse según Wine en lugar de asumirse.
4. Demuestre la guardia del juego terrestre a través de prefijos. El código actual enumera los procesos Windows y compara directorios ejecutables. La visibilidad del prefijo Wine puede dejar sin detectar otro prefijo que ejecuta el mismo cliente. Resuelva esto antes de ofrecer soporte de instalación segura; una prueba exitosa del mismo prefijo por sí sola no es suficiente.
5. Ejecute la instalación/restauración del dispositivo y la matriz de recuperación interrumpida, luego una descarga/instalación/reversión limpia y anónima de GitHub utilizando los recursos de versión exactos. Pruebe TLS, redirecciones, reanudación, cancelación y recuperación fuera de línea.
6. Continúe con una verificación dentro del juego en el mismo entorno compatible. Solo entonces publique las instrucciones Wine y una integración de Lutris. Mantenga Proton y macOS explícitamente sin verificar hasta que pasen sus propias comprobaciones.

Mantenga un conjunto de recursos de juego inmutables en las versiones GitHub. No agregue clientes completos, IU personal ni copias de cada carga útil al repositorio de Git para habilitar otro iniciador. Si Wine no puede satisfacer las comprobaciones de seguridad de manera confiable, evalúe un instalador nativo Linux con las mismas reglas de manifiesto y transacción como una implementación separada.
