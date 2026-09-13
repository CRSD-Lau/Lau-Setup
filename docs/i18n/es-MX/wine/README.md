<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../../es-ES/README.md) · [Español (México)](../README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Un solo ZIP incluye ahora el instalador de Windows y el iniciador para Linux/Wine. La interfaz sigue automáticamente el idioma del sistema operativo entre diez opciones; la elección manual se guarda. La versión 3.0.8 y los archivos del juego no cambian. No hay cambios en DBC.
>
> La actualización completa de las guías sigue pendiente por un HTTP 429 de Google. El texto anterior puede estar desactualizado; consulta la fuente inglesa actual y las notas 1.3.0. [English](../../../../wine/README.txt) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Descarga actual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows y Linux/Wine. Extrae la carpeta `LauSetup/` con cinco archivos: en Windows abre `LauSetup.exe`; en Linux/Wine ejecuta `LauSetup.sh`. Las instrucciones antiguas de abajo sobre ZIP Wine o EXE separados no se aplican a 1.3.0.
>
> **1.3.0:** Los archivos adicionales de mejora reconocidos se respaldan y la instalación continúa. Restaurar los devuelve. No hay que moverlos manualmente.


<!-- BEGINNER-120-STEPS -->
## Primeros pasos

1. Cierre WoW por completo.
2. Descargue solo `LauSetup.zip`. En Windows: clic derecho, **Extraer todo**, abra `LauSetup` y haga doble clic en `LauSetup.exe`.
3. Extraiga `LauSetup.zip`. Mantenga juntos los cinco archivos de `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` y `README.txt`.
4. **Idioma de la interfaz** solo cambia el texto de Setup: Automático sigue el sistema y guarda la elección; no cambia los nueve idiomas del juego.
5. **Consagración mejorada** está activada por defecto. Los nuevos efectos requieren modelos HD compatibles detectados; mapas/minimapa son opcionales.
6. Elija **Instalar actualización**, espere sin cerrar Setup, inicie WoW y escriba `/pyversion`. Para restaurar, cierre WoW, use la misma carpeta y elija **Restaurar instalación anterior**.

### Linux/Wine

Use el mismo ZIP solo con un prefijo Wine 64-bit existente, Wine 11.0, Wine Mono 10.4.1, Python 3.9+, fuentes documentadas y almacenamiento Linux local. Extraiga y ejecute `WINEPREFIX="/path/to/prefix" sh LauSetup.sh`; nunca ejecute el EXE directamente en Wine.
<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../../wine/README.txt). Si la redacción difiere, la fuente en inglés tiene autoridad.

Lau Setup para Wine en Linux
Author / Creator / Last Modified By: Neil Mitchell

1. Utilice un cliente WoW 3.3.5a existente de compilación 12340 en un sistema de archivos Linux local.
2. Cierre todas las instancias de WoW, incluidos los juegos con otros prefijos Wine.
3. Extraiga `LauSetup.zip`. Mantenga juntos los cinco archivos de `LauSetup/`: `LauSetup.exe`, `LauSetup.sh`, `lau_wine.py`, `lau-languages.json` y `README.txt`.
4. Abra una terminal en la carpeta extraída y ejecute:

```sh
WINEPREFIX="/absolute/path/to/your/existing/prefix" sh LauSetup.sh
```

5. Elija la carpeta de su juego existente e instálela. Las habituales copias de seguridad automáticas
   y el botón Restaurar instalación anterior están disponibles.

Requisitos para esta versión:
- Wine 11.0, un prefijo 64-bit y Wine Mono 10.4.1 ya instalado allí.
- Python 3.9 o posterior para el asistente de seguridad del host (solo biblioteca estándar).
- Fuentes Liberation Sans o DejaVu Sans; el paquete de fuentes completo Wine debe
  También se puede instalar para que los propios controles predeterminados de Wine Mono puedan renderizarse.
- Almacenamiento local Linux. Se excluyen los recursos compartidos de red y las unidades montadas en Windows.
- Visibilidad normal del proceso del host. No ejecute este lanzador a través de una zona de pruebas
  que oculta otros procesos Wine. Ejecute como su usuario normal, nunca sudo/root.

El prefijo 64-bit puede contener el cliente 32-bit WoW. Este instalador no
cree, convierta o actualice su prefijo Wine, instale Wine/Mono, configure
DXVK, o cambia el iniciador de tu juego. Utilice la configuración Wine de su distribución
instrucciones primero si falta su tiempo de ejecución.

Paquete oficial Wine Mono para este tiempo de ejecución probado:
https://github.com/wine-mono/wine-mono/releases/tag/wine-mono-10.4.1

Utilice el tiempo de ejecución Wine Mono con Wine. El instalador de .NET Framework Windows es
no incluido y no es requerido por esta configuración Wine Mono probada.

Inicie siempre a través de LauSetup.sh. Ejecutando LauSetup.exe directamente debajo de Wine
rechazará las operaciones del cliente sin el ayudante Linux. Comprueba las rutas del host
y procesa y mantiene un bloqueo de host compartido entre los prefijos Wine. Si se detiene,
Vuelva a abrir el iniciador y restaure la instalación pendiente antes de volver a intentarlo.

Mantenga WoW cerrado hasta que finalice la instalación. Los controles de proceso reducen las carreras; no pueden
Evite que otro programa inicie el juego o cambie archivos después.
Se rechazan las rutas con enlaces simbólicos, los enlaces duros y las mayúsculas y minúsculas de nombres de archivos. Datos
y los directorios de respaldo deben permanecer en el mismo sistema de archivos que el cliente.

Alcance de validación: clientes aislados Wine 11.0 / Wine Mono 10.4.1, accesorios y
pruebas de instalación/restauración de carga útil real, pruebas de seguridad de dos prefijos y GUI de muestra
cheques. Esta no es una certificación de cada distribución, sistema de archivos, Linux.
escala de visualización, versión Wine o encuentro de juego. Sin Lutris, Proton o macOS
La integración está incluida en esta versión.

La interfaz del instalador sigue automáticamente el idioma del sistema entre diez opciones; la elección manual se guarda. Los datos del juego del cliente siguen admitiendo nueve configuraciones regionales y siguen la configuración regional detectada del juego.

Configuración 1.1.7: Las nuevas imágenes de hechizos desactivadas mantienen a Patch-S como .mpq.disabled junto a
su camino original. Una copia deshabilitada diferente nunca se sobrescribe.
Para deshacer la instalación completa, utilice Restaurar instalación anterior. Para archivos
ya eliminados por versiones de instalación anteriores, recupérelos de esas copias de seguridad
usando Restaurar instalación anterior antes de reinstalar. Mantenga LauSetupBackups.

El archivo S actual siempre pasa a ser .mpq.disabled. Si una persona mayor discapacitada
La copia existe, el programa de instalación primero la conserva como `.mpq.disabled.<12-character hash>`. Sin cambio de nombre manual
es necesario para cambiar las opciones. Volver a habilitar manualmente requiere eliminar
.disabled y cualquier hash siguiente, con WoW cerrado y sin ningún otro activo
archivo que se sobrescribe. Utilice Restaurar instalación anterior para una reversión administrada.

1.1.7 volver a habilitar la limpieza: la coincidencia deshabilitada Patch-S se reutiliza localmente. La copia simple deshabilitada se mueve a la copia de seguridad de la transacción verificada en LauSetupBackups, dejando una S activa. Diferentes copias permanecen recuperables a través de Restaurar instalación anterior. Los archivos existentes con sufijo hash no se barren.
