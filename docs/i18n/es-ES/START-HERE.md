<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.4.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.4.0. [English](../../../START-HERE.txt) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)
>
> **Descarga actual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.4.0.
>
> **1.4.0:** Los archivos adicionales de mejora reconocidos se guardan en una copia de seguridad y la instalación continúa. Restaurar los devuelve. No hay que moverlos manualmente. Setup conserva automáticamente los archivos existentes antes de reemplazarlos o moverlos. Los archivos ajenos a la actualización no se modifican.



> **1.4.0:** Elegir carpeta del juego → Siguiente → elegir aspecto → Siguiente → revisar → Instalar actualización → Finalizar. Patch-Y HD o Patch-Y Non-HD queda fijado según el cliente detectado. Las opciones extra empiezan desactivadas; se conservan los mapas ya instalados. La revisión muestra Patch-Y (versión de Lau) y los extras elegidos, WoW.exe, Patch-Q, archivos de idioma, descarga y copias de seguridad. Siguiente no modifica archivos del juego. Puedes elegir el idioma de la interfaz en cada paso; se guarda y Automático vuelve al idioma del sistema. Restaurar instalación anterior sigue disponible.

<!-- BEGINNER-140-STEPS -->
1. Cierre WoW por completo.
2. Descargue solo `LauSetup.zip`. En Windows: clic derecho, **Extraer todo**, abra `LauSetup` y haga doble clic en `LauSetup.exe`.

Elegir carpeta del juego → Siguiente → elegir aspecto → Siguiente → revisar → Instalar actualización → Finalizar. Patch-Y HD o Patch-Y Non-HD queda fijado según el cliente detectado. Las opciones extra empiezan desactivadas; se conservan los mapas ya instalados. La revisión muestra Patch-Y (versión de Lau) y los extras elegidos, WoW.exe, Patch-Q, archivos de idioma, descarga y copias de seguridad. Siguiente no modifica archivos del juego. Puedes elegir el idioma de la interfaz en cada paso; se guarda y Automático vuelve al idioma del sistema. Restaurar instalación anterior sigue disponible.

Linux/Wine: Wine 11.0, Wine Mono 10.4.1, Python 3.9+, 64-bit WINEPREFIX. `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`. [Guide](https://github.com/CRSD-Lau/Lau-Setup/blob/main/wine/README.txt).

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../START-HERE.txt). Si la redacción difiere, la fuente en inglés tiene autoridad.

CONFIGURACIÓN DE LAU: LANZAMIENTO 3.0.8

Windows y Linux/Wine: descargue `LauSetup.zip` y extraiga `LauSetup/`. En Windows abra `LauSetup/LauSetup.exe`; en Linux/Wine ejecute `LauSetup/LauSetup.sh`.
Para Wine use el iniciador Linux incluido. No ejecute directamente el EXE.

1. Cierre World of Warcraft.
2. Abra LauSetup.exe y elija su carpeta WoW.
3. Elija sus imágenes y haga clic en Instalar actualización.

¿Actualizando desde una versión anterior o prueba v2? Descargue primero el nuevo instalador; Las copias antiguas incorporan el catálogo antiguo.
Seleccione el mismo cliente y objetos visuales. Las comprobaciones de hash de archivos detectan los parches modificados.
Inicie WoW y escriba /pyversion; debería informar 3.0.8 Lau.

El instalador detecta el idioma de su cliente y la configuración del modelo HD.
La Consagración mejorada está seleccionada de forma predeterminada. Desmarcarlo para el stock.
apariencia; el hechizo en sí todavía funciona. Las nuevas imágenes de hechizos requieren una
cliente de modelo HD compatible existente. Los mapas/minimapas actualizados son opcionales.

Necesita un cliente WoW 3.3.5a existente, compilar 12340, en Windows 10 o 11.
Esta descarga es una actualización, no un cliente completo ni un paquete de idioma.
El archivo WoW.exe compatible requerido se instala automáticamente.

No es necesario copiar parches ni cambiar el nombre manualmente. No descargues todo
liberación de datos compartidos. La aplicación descarga solo los archivos necesarios para su selección.

Las copias de seguridad y las descargas reanudables permanecen en LauSetupBackups dentro de su WoW
carpeta, fuera de Datos. Para deshacer la actualización, cierre WoW, vuelva a abrir LauSetup.exe,
elija la misma carpeta y haga clic en Restaurar instalación anterior. Recuperación también
funciona si una actualización interrumpida dejó WoW.exe temporalmente perdido.

Sus complementos, SavedVariables, fuentes, ilustraciones de inicio de sesión, configuraciones de dominio y
Se conservan parches no relacionados. Sin marca Pizza Warriors, personal
Se incluyen la configuración de ElvUI, LoginUI, los datos de la cuenta o el cliente de juego completo.

Las descargas provienen de versiones GitHub; no se necesita ninguna cuenta GitHub.
Si se detiene una descarga, vuelva a intentarlo más tarde. Archivos verificados
se reutilizan y se reanudan las descargas parciales. Los archivos del juego se cambian sólo después
todas las descargas requeridas han pasado la verificación. Mantenga LauSetupBackups si
la aplicación informa que se necesita recuperación.

Este instalador no está firmado digitalmente, por lo que Windows puede mostrar un editor desconocido
advertencia. Utilice la suma de verificación proporcionada para verificar su descarga. no lo hace
requieren deshabilitar la seguridad Windows o instalar herramientas Python/PowerShell.
Se requiere el tiempo de ejecución de .NET Framework 4.8.

Una vez que este instalador ha agregado la actualización del mapa, mantiene esa actualización durante
cambios de edición. Utilice Restaurar instalación anterior para deshacer la instalación del mapa.

Créditos: Andre (líneas de base Patch-Y), Loriendal y Trimitor (base HD),
Colaboradores de Project Reforged (ilustraciones en HD), Blizzard (ilustraciones originales y
texto localizado), Lau (adaptación, compatibilidad, indicadores, pruebas).

Author / Creator / Last Modified By: Neil Mitchell

Configuración 1.1.7: Las nuevas imágenes de hechizo desactivadas mantienen a Patch-S como .mpq.disabled junto a
su camino original. Una copia deshabilitada diferente nunca se sobrescribe.
Para deshacer la instalación completa, utilice Restaurar instalación anterior. Para archivos
ya eliminados por versiones de instalación anteriores, recupérelos de esas copias de seguridad
usando Restaurar instalación anterior antes de reinstalar. Mantenga LauSetupBackups.

El archivo S actual siempre se convierte en .mpq.disabled. Si una persona mayor discapacitada
La copia existe, el programa de instalación primero la conserva como `.mpq.disabled.<12-character hash>`. Sin cambio de nombre manual
es necesario para cambiar las opciones. Volver a habilitar manualmente requiere eliminar
.disabled y cualquier hash siguiente, con WoW cerrado y sin ningún otro activo
archivo que se sobrescribe. Utilice Restaurar instalación anterior para una reversión administrada.

1.1.7 Revisión: habilitar nuevas imágenes de hechizos reutiliza un Patch-S deshabilitado coincidente sin descargarlo nuevamente. La copia simple deshabilitada se mueve a la copia de seguridad de la transacción verificada en LauSetupBackups, incluso cuando el Patch-S activo ya coincide. Las diferentes versiones siguen siendo recuperables con Restaurar instalación anterior. Al apagar todavía se usa .mpq.disabled. Los archivos existentes con sufijo hash se dejan intactos.
