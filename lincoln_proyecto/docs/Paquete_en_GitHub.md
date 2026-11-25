# Generación del paquete de revisión

El workflow Lincoln - validación sin secretos incluye un job empaquetar, condicionado a validar. Instala ReportLab4.4.10, genera el informe y comprueba que tenga nueve páginas. El ZIP contiene archivos leídos directamente del commit mediante git show, el PDF y un manifiesto con hashes. No incorpora respaldos privados, credenciales ni resultados locales ajenos al commit.

En la ejecución de GitHub Actions, abrir Artifacts y descargar Lincoln-Proyecto-Revision. El artefacto conserva el PDF y el ZIP durante30días; el código permite regenerarlos después. Su existencia se acredita solo tras completar el job satisfactoriamente. El paquete sigue marcado REVISION por los controles y pruebas operativos pendientes.

El archivo previamente compartido en ChatGPT no se actualiza al generar un artefacto en GitHub. No confundir ambas versiones. El manifiesto identifica el commit exacto.
