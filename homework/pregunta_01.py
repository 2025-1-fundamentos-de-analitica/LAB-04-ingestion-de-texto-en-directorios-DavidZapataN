# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    import os
    import shutil
    import zipfile
    import pandas as pd
    from glob import glob

    # Extracción y preparación del archivo comprimido
    ubicacion_archivo_zip = "files/input.zip"
    directorio_extraccion = "input"

    # Eliminar directorio previo si existe
    if os.path.exists(directorio_extraccion):
        shutil.rmtree(directorio_extraccion)

    # Extraer contenido del ZIP
    with zipfile.ZipFile(ubicacion_archivo_zip, "r") as extractor_zip:
        extractor_zip.extractall(".")

    # Preparación del espacio de trabajo
    os.makedirs("files/output", exist_ok=True)

    # Motor de procesamiento de textos y sentimientos
    def construir_dataset_desde_directorio(modalidad_entrenamiento):
        """Genera DataFrame a partir de archivos de texto organizados por sentimiento"""
        ruta_conjunto_datos = os.path.join(directorio_extraccion, modalidad_entrenamiento)
        coleccion_registros = []
        
        # Procesar cada categoría emocional
        for categoria_emocional in ["positive", "negative", "neutral"]:
            directorio_categoria = os.path.join(ruta_conjunto_datos, categoria_emocional)
            
            # Leer archivos ordenados alfabéticamente
            for nombre_documento in sorted(os.listdir(directorio_categoria)):
                ruta_completa_archivo = os.path.join(directorio_categoria, nombre_documento)
                
                # Extraer contenido textual
                with open(ruta_completa_archivo, encoding="utf-8") as manipulador_archivo:
                    contenido_textual = manipulador_archivo.read().strip()
                    
                    # Agregar registro estructurado
                    coleccion_registros.append({
                        "phrase": contenido_textual,
                        "target": categoria_emocional
                    })
        
        return pd.DataFrame(coleccion_registros)

    # Generación y almacenamiento de datasets finales
    dataframe_entrenamiento = construir_dataset_desde_directorio("train")
    dataframe_evaluacion = construir_dataset_desde_directorio("test")

    # Exportar datasets como archivos CSV
    dataframe_entrenamiento.to_csv(os.path.join("files/output", "train_dataset.csv"), index=False)
    dataframe_evaluacion.to_csv(os.path.join("files/output", "test_dataset.csv"), index=False)

# Punto de entrada principal del laboratorio
if __name__ == "__main__":
    pregunta_01()
