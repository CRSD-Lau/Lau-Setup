<!-- LANGUAGES:START -->
[English](../../../../../../README.md) · [Deutsch](../../../../de/README.md) · [Español (España)](../../../../es-ES/README.md) · [Español (México)](../../../README.md) · [Français](../../../../fr/README.md) · [한국어](../../../../ko/README.md) · [Русский](../../../../ru/README.md) · [简体中文](../../../../zh-CN/README.md) · [繁體中文](../../../../zh-TW/README.md) · [Português (Brasil)](../../../../pt-BR/README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

<!-- STABLE-140-CURRENT-GUIDE -->
> **Versión actual: Setup 1.4.0 / juego 3.0.9 Lau.** Cierra WoW, extrae todo LauSetup.zip, abre LauSetup.exe en Windows y usa Browse... para elegir la carpeta que contiene WoW.exe. Siguiente → opciones visuales → Siguiente → revisar → instalar → finalizar. Todos los extras empiezan desactivados. WoW.exe y las pantallas de carga son una sola opción; los mapas son independientes e incluyen archivos WDM. Se conservan los mapas ya instalados. Los parches duplicados renombrados permanecen; solo un Patch-V vacío se guarda automáticamente. Los archivos reemplazados se guardan en LauSetupBackups. No hay cambios DBC en Patch-Y; los mapas opcionales añaden tablas originales documentadas. Los mapas de cuevas siguen en beta. Linux/Wine usa LauSetup.sh con los requisitos documentados. Google HTTP 429 impide actualizar la traducción completa. El texto anterior que aparece abajo es solo una referencia histórica; las instrucciones actuales están en la fuente inglesa.
>
> [English](../../../../../dbc/history/INDIVIDUAL-EDITS.md) · [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) · [1.4.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.4.0)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Traducción automática. [Fuente en inglés](../../../../../dbc/history/INDIVIDUAL-EDITS.md). Si la redacción difiere, la fuente en inglés tiene autoridad.

<a id="individual-patch-y-dbc-edits-andre-baseline-to-retained-multilingual-lau-build"></a>

# Ediciones individuales de Patch-Y DBC: línea base de Andre para la compilación multilingüe Lau retenida



<a id="read-the-chronology-first"></a>

## Lea primero la cronología

Andre omitió intencionalmente **Spell.dbc** debido a conflictos de localización, según Lau. Los archivos Andre 3.0.3 retenidos contienen seis DBC visuales/modelos; no contienen Spell.dbc. La adición inicial Lau introdujo la dependencia del idioma. Lau y Andre depuraron el problema juntos y la reconstrucción multilingüe lo resolvió.

Lau identifica estos hitos de desarrollo como 3.0.4 (adición inicial) y 3.0.5 (solución multilingüe), siendo 3.0.6–3.0.8 las revisiones cuyos números de versión se modificaron. Los artefactos retenidos no se asignan claramente a esa colección: la línea base publicada etiquetada como 3.0.4 ya contiene la solución multilingüe. Este informe nombra artefactos y hashes explícitamente en lugar de asignar silenciosamente una compilación temprana rota a esa etiqueta publicada.

[Prueba en etapa de localización](../../../../../dbc/history/localization-stage.json) compara cuatro archivos v35 previos a la localización retenidos con las versiones multilingües: solo cambia Spell.dbc, todos los campos numéricos permanecen idénticos y se conservan los enlaces visuales existentes. HD New Spells Off se compiló por separado utilizando datos numéricos de stock.

<a id="format-and-scope"></a>

## Formato y alcance

Esta es la comparación de transferencia Patch-Y, no una auditoría de cada canal de localización de mapas/Q/S por separado. Los CSV de seis ediciones enumeran las ediciones de tablas, registros o campos individuales y todos los valores de registros agregados. Dos archivos JSON gzip compartidos contienen cambios de texto de hechizo decodificados sin duplicar el texto para las variantes de Consagración. Cada celda de texto es `[record_id, zero_based_field, old_string_index, new_string_index]`; resuelva los dos últimos a través de la matriz `strings` de ese archivo.

Los valores numéricos son palabras 32-bit sin firmar, incluidos patrones de bits flotantes; Los nombres de esquemas desconocidos no se adivinan. El campo Spell.dbc 131 es el enlace visual utilizado por los scripts de compilación. Los desplazamientos de cadenas se decodifican antes de la comparación. El Spell.dbc agregado utiliza datos HD Patch-S retenidos para HD New Spells On y datos extraídos del servidor para HD New Spells Off y Non-HD. Las filas heredadas no se acreditan como registros recién creados.

<a id="what-the-edit-groups-mean"></a>

### Qué significan los grupos de edición

- Campo de hechizo 131: quince enlaces visuales de indicadores de incursión aceptados en cada edición.
- Deletrear celdas de texto: ocupación de espacios multilingües/de reserva; Estos recuentos no son recuentos de traducciones de nueva creación.
- SpellVisual, SpellVisualKit y filas de accesorios: enrutamiento de indicadores, kits y configuración de accesorios del modelo.
- SpellVisualEffectName: referencias de modelos agregadas y diferencias de apariencia de Consagración.
- CreatureDisplayInfo y CreatureModelData: sin cambios desde la línea base Andre correspondiente.
- HD New Spells Off: el kit privado Rimefang utiliza 90059 para preservar el kit 90046 anterior.

<a id="y-hd-newspells-off-consecration-on"></a>

## Y-HD-NewSpells-Off-Consagración-On

| Mesa | Registros modificados/añadidos | Diferencias de valores de campo | ID agregadas | Identificaciones eliminadas |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Ninguno | Ninguno |
| creaturemodeldata.dbc | 0 | 0 | Ninguno | Ninguno |
| spell.dbc | 49839 | 824619 | Ninguno | Ninguno |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Ninguno |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Ninguno |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Ninguno |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Ninguno |

| Mesa | ID de registro | Campo [0-basado] | Viejo | Nuevo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | hechizos\consecration_impact_base.mdx | hechizos\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas las ediciones de registros/campos y registros agregados](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-On.csv) · [Cambios de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-off-consecration-off"></a>

## Y-HD-NewSpells-Off-Consagración-Off

| Mesa | Registros modificados/añadidos | Diferencias de valores de campo | ID agregadas | Identificaciones eliminadas |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Ninguno | Ninguno |
| creaturemodeldata.dbc | 0 | 0 | Ninguno | Ninguno |
| spell.dbc | 49839 | 824619 | Ninguno | Ninguno |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Ninguno |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Ninguno |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | Ninguno |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Ninguno |

| Mesa | ID de registro | Campo [0-basado] | Viejo | Nuevo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas las ediciones de registros/campos y registros agregados](../../../../../dbc/history/Y-HD-NewSpells-Off-Consecration-Off.csv) · [Cambios de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-hd-newspells-on-consecration-on"></a>

## Y-HD-NewSpells-On-Consagración-On

| Mesa | Registros modificados/añadidos | Diferencias de valores de campo | ID agregadas | Identificaciones eliminadas |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Ninguno | Ninguno |
| creaturemodeldata.dbc | 0 | 0 | Ninguno | Ninguno |
| spell.dbc | 33950 | 227113 | Ninguno | Ninguno |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Ninguno |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Ninguno |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Ninguno |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Ninguno |

| Mesa | ID de registro | Campo [0-basado] | Viejo | Nuevo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | hechizos\consecration_impact_base.mdx | hechizos\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas las ediciones de registros/campos y registros agregados](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-On.csv) · [Cambios de texto decodificado](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-hd-newspells-on-consecration-off"></a>

## Y-HD-NewSpells-On-Consagración-Off

| Mesa | Registros modificados/añadidos | Diferencias de valores de campo | ID agregadas | Identificaciones eliminadas |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Ninguno | Ninguno |
| creaturemodeldata.dbc | 0 | 0 | Ninguno | Ninguno |
| spell.dbc | 33950 | 227113 | Ninguno | Ninguno |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Ninguno |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Ninguno |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Ninguno |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Ninguno |

| Mesa | ID de registro | Campo [0-basado] | Viejo | Nuevo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas las ediciones de registros/campos y registros agregados](../../../../../dbc/history/Y-HD-NewSpells-On-Consecration-Off.csv) · [Cambios de texto decodificado](../../../../../dbc/history/spell-text-hd.json.gz)

<a id="y-non-hd-consecration-on"></a>

## Y-No-HD-Consagración-On

| Mesa | Registros modificados/añadidos | Diferencias de valores de campo | ID agregadas | Identificaciones eliminadas |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Ninguno | Ninguno |
| creaturemodeldata.dbc | 0 | 0 | Ninguno | Ninguno |
| spell.dbc | 49839 | 824619 | Ninguno | Ninguno |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Ninguno |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Ninguno |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Ninguno |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Ninguno |

| Mesa | ID de registro | Campo [0-basado] | Viejo | Nuevo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | hechizos\consecration_impact_base.mdx | hechizos\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas las ediciones de registros/campos y registros agregados](../../../../../dbc/history/Y-Non-HD-Consecration-On.csv) · [Cambios de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)

<a id="y-non-hd-consecration-off"></a>

## Y-No-HD-Consagración-Off

| Mesa | Registros modificados/añadidos | Diferencias de valores de campo | ID agregadas | Identificaciones eliminadas |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | Ninguno | Ninguno |
| creaturemodeldata.dbc | 0 | 0 | Ninguno | Ninguno |
| spell.dbc | 49839 | 824619 | Ninguno | Ninguno |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | Ninguno |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | Ninguno |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | Ninguno |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | Ninguno |

| Mesa | ID de registro | Campo [0-basado] | Viejo | Nuevo |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[Todas las ediciones de registros/campos y registros agregados](../../../../../dbc/history/Y-Non-HD-Consecration-Off.csv) · [Cambios de texto decodificado](../../../../../dbc/history/spell-text-nonhd.json.gz)
