<!-- LANGUAGES:START -->
[English](../../../../README.md) · [Deutsch](../../de/README.md) · [Español (España)](../README.md) · [Español (México)](../../es-MX/README.md) · [Français](../../fr/README.md) · [한국어](../../ko/README.md) · [Русский](../../ru/README.md) · [简体中文](../../zh-CN/README.md) · [繁體中文](../../zh-TW/README.md) · [Português (Brasil)](../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- HOTFIX-118-NOTICE -->
> **Corrección 1.1.8** — Setup revisa los MPQ de Data y de la carpeta del idioma activo para detectar Patch-Y renombrados conocidos y copias exactas del catálogo. Si hay un posible conflicto o un archivo ilegible o no compatible, se detiene e indica el archivo sin borrarlo automáticamente. Cambiar el nombre de un archivo no cambia el hash de su contenido. Los archivos del juego siguen en 3.0.8.
>
> La traducción completa aún no se ha actualizado debido al límite de solicitudes de Google. El texto anterior que aparece debajo corresponde a una versión previa. Consulta la información actual en inglés. [English](../../../../wine/README.txt) · [1.1.8](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.1.8)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../../wine/README.txt). Si la redacción difiere, la fuente en inglés tiene autoridad.

Lau Setup para Wine en Linux
Author / Creator / Last Modified By: Neil Mitchell

1. Utilice un cliente WoW 3.3.5a existente de compilación 12340 en un sistema de archivos Linux local.
2. Cierre todas las instancias de WoW, incluidos los juegos con otros prefijos Wine.
3. Extraiga este ZIP. Mantenga los cuatro archivos juntos.
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

La interfaz del instalador es en inglés. Los datos del juego del cliente son compatibles con los nueve
configuraciones regionales existentes y se selecciona de la configuración regional del juego detectada.

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
