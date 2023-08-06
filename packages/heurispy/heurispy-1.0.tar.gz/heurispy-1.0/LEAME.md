HeurisPy
======

``HeurisPy`` es un framework orientado a objetos desarrollado en Python que busca 
auxiliar en la obtención de experiencia para el uso de heurísticas de búsqueda
local en problemas de optimización discreta.

Se ha diseñado con los siguientes principios en mente:

--``HeurisPy`` debe ser lo suficientemente general para permitir el planteamiento 
de varios problemas de optimización discreta.

--``HeurisPy`` debe ser accesible para usuarios con poca experiencia tanto en el
uso de heurísticas de búsqueda local como en programación.

--``HeurisPy`` debe contener varias heurísticas de búsqueda local listas para su
uso, así como una clase lo suficientemente general para permitir el agregado
de nuevas heurísticas.

--``HeurisPy`` debe permitir el trabajo en paralelo para facilitar el análisis
estadístico, y brindar herramientas que faciliten el trabajo.

Así, se espera que el usuario sólo deba preocuparse por la programación de su 
problema de optimización discreta y de experimentar con las heurísticas. ``HeurisPy``
se encargará de realizar las búsquedas y de brindar la información 
estadística para que el usuario pueda realizar una decisión informada.

``HeurisPy`` fue programado en Python 3.7 [(que se descarga aquí)](https://www.python.org/downloads/)
, y requiere de las siguientes bibliotecas para su funcionamiento:

--**numpy**: Biblioteca para el cómputo científico en Python. [Página](https://www.numpy.org/)

--**pathos**: Biblioteca para el procesamiento en paralelo. [Página](https://pypi.org/project/pathos/)

--**pandas**: Biblioteca para el análisis de datos. [Página](https://pandas.pydata.org/)

--**pyFPDF**: Biblioteca para la generación de archivos PDF. [Página](https://pyfpdf.readthedocs.io/en/latest/)

--**PyPDF2**: Un kit de herramientas para archivos PDF. [Página](https://pypi.org/project/PyPDF2/)

--**matplotlib**: Biblioteca para la generación de gráficas. [Página](https://matplotlib.org/)

--**tqdm**: Biblioteca para la muestra del progreso de la exploración heurística. [Página](https://tqdm.github.io/)

Instalación
======


``HeurisPy`` está disponible como una biblioteca en PyPi, y se puede instalar con el
siguiente comando:

    pip install heurispy
    
Para verificar la instalación, corre uno de los scripts de ejemplo, como "coloracion_grafo_recsim.py" en la ruta /heurispy/ejemplos/.

Licencia
======

 Copyright 2019, LANIA, A.C.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Cómo funciona
======

``HeurisPy`` tiene tres clases principales que necesitan del usuario para funcionar:
Problema, Heurística, y Framework.

--**Problema**: Se encarga de retener la información del problema de 
optimización definido por el usuario.

--**Heurística**: Recibe los atributos del problema para iniciar la búsqueda de
soluciones con parámetros que el usuario determina.

--**Framework**: Dirige todos los procesos internos, como el procesamiento en
paralelo, la recolección de los datos y el llamado de métodos para la generación
de archivos.

Planteando el p.o.d.
======

Antes que nada, se necesita definir el problema de optimización discreta en ``HeurisPy``. Para esto, se debe:

--Definir un método para la creación de nuevas soluciones.

--Crear un método encargado de variar una solución existente.

--Crear una función objetivo a minimizar.

Por ejemplo, en el problema de coloración de grafos, se asignan colores a los vértices de un grafo, tratando de minimizar la cantidad 
de colores utilizados para colorearlo sin tener colores adyacentes repetidos. El grafo está representado en ``HeurisPy`` con un diccionario.
Un diccionario es un conjunto de valores a los que se les asigna etiquetas llamadas "llaves". Entonces:

    adyacencias_en_grafo = {"0": [1, 4, 6],
               "1": [0, 2, 7],
               "2": [1, 3, 8],
               "3": [2, 4, 9],
               "4": [0, 3, 5],
               "5": [4, 7, 8],
               "6": [0, 8, 9],
               "7": [1, 5, 9],
               "8": [2, 5, 6],
               "9": [3, 6, 7]}
               
    cantidad_vertices = len(adyacencias_en_grafo)

Los elementos entre comillas representan los vértices, y las listas son sus vértices adyacentes. Además, la longitud del diccionario
determina la cantidad de vértices. 

Para crear una solución, se asigna a cada vértice un color aleatorio (representado por un número entero). Esto se puede definir como sigue:

    def crear_solucion():
        import random
        nueva_solucion = []
        for indice in range(cantidad_vertices):
            nueva_solucion.append(random.randint(0, cantidad_vertices-1))
        return nueva_solucion
        
Así, la solucion es una lista cuyos índces representan el vértice, y el valor del índice representa el color. Para variar una solución dada,
se elige un vértice al azar de la solución, se verifican los vértices adyacentes y los valores de su coloración, y se elige un color 
diferente a todos ellos. Los colores adyacentes se obtienen con: 

    def obtener_colores_adyacentes(solucion, indice):
        vertices = adyacencias[str(indice)]
        colores = []
        for indice in vertices:
            colores.append(solucion[indice])
        return colores
        
Y la solución variada se realiza con:

    def variar_solucion(solucion):
        import random
        nueva_solucion = solucion.copy()
        longitud_solucion = len(nueva_solucion)
        indice_a_cambiar = random.randint(0, longitud_solucion-1)
        colores = list(range(cantidad_vertices))
        colores_adyacentes = obtener_colores_adyacentes(nueva_solucion, indice_a_cambiar)
        colores_disponibles = [color for color in colores if color not in colores_adyacentes]
        nueva_solucion[indice_a_cambiar] = random.choice(colores_disponibles)
        return nueva_solucion

La función objetivo comprueba la cantidad de colores diferentes en una solución, y qué tantos vértices adyacentes tienen colores repetidos. 
Esto es de la siguiente manera:

    def costo_colores_diferentes(solucion):
        colores_distintos = set(solucion)
        return len(colores_distintos)

    def costo_colores_adyacentes(solucion):
        valor_final = 0
        longitud_solucion = len(solucion)
        #print("SOLUCION:", solucion)
        for indice in range(longitud_solucion):
            #print("VERTICE:", indice)
            #print("COLOR:", solucion[indice])
            color = solucion[indice]
            colores_adyacentes = obtener_colores_adyacentes(solucion, indice)
            repeticiones = colores_adyacentes.count(color)
            valor_final = valor_final + repeticiones
        return valor_final
        
Para permitir darle más peso al costo de los colores o al costo de los colores adyacentes, se agregan las variables c_1 y c_2, que 
multiplican las funciones correspondientes, y entonces se define la función objetivo:
        
    c_1 = 1
    c_2 = 1

    def funcion_objetivo(solucion):
        costo_colores = costo_colores_diferentes(solucion)
        costo_adyacencia = costo_colores_adyacentes(solucion)
        return c_1 * costo_colores + c_2 * costo_adyacencia

Para finalizar, se necesita generar una instancia de la clase Problema, que se logra de la siguiente manera:

    from heurispy.problema import Problema
    
    problema_coloracion = Problema(dominio=crear_solucion , funcion_objetivo=funcion_objetivo, funcion_variacion_soluciones)
    
Este ejemplo se encuentra implementado en el script problema_coloracion_grafo.py, que está en la ruta  "/heurispy/ejemplos/".
Se necesitan definir para que la implementación de ejemplo funcione.
    
Preparando una heurística para su uso
======

Toda heurística implementada en ``HeurisPy`` es una clase que hereda de Heuristica. Para utilizar alguna en particular, 
sólo se necesita importar
la clase correspondiente, asignarle una instancia de la clase Problema, y definir algunos parámetros generales. Por ejemplo, para utilizar
la búsqueda tabú, se escribe lo siguiente:

    from heurispy.heuristicas.busqueda_tabu import BusquedaTabu
    
    busqueda_tabu = BusquedaTabu(problema_coloracion, max_iteraciones = 100000)
    
Sin embargo, todavía faltan definir parámetros específicos de la heurística que se desea utilizar.

Definiendo parámetros de la heurística
======

Para definir los parámetros específicos de la heurística, se necesita generar un diccionario. Para la búsqueda tabú, le corresponde:

    parametros_busqueda_tabu = dict(espacio_memoria=[50, 100, 150], max_busquedas_sin_mejoras=[100])
    
Este diccionario es la base que HeurisPy necesita para realizar la exploración. En este caso, se tienen tres tipos de corridas:

--Espacio en memoria = 50, Máximo de búsquedas sin mejora=100

--Espaio en memoria= 100, Máximo de búsquedas sin mejora=100

--Espacio en memoria= 150, Máximo de búsquedas sin mejora=100

Se necesita que todo valor en el diccionario sea una lista con todos los valores esperados en cada parámetro. El siguiente paso es determinar
cuántas repeticiones se realizarán para cada tipo de corrida.

Determinando repeticiones
======

Para determinar las repeticiones en cada tipo de corrida, se necesita del siguiente método:

    from heurispy.framework import genera_bloque_parametros
    
    lista_corridas = genera_bloque_parametros(parametros_busqueda_tabu, repeticiones=10)
    
Con esto, se realizarán 30 ejecuciones en total. 10 para el espacio en memoria de 50, 10 para el espacio en memoria de 100, y 10 para
el espacio en memoria de 150, todas con un máximo de búsqueda sin mejora de 100. 

Teniendo la heurística a utilizar definida por el problema y el total de ejecuciones a realizar, ya se puede iniciar el funcionamiento
de ``HeurisPy``.

Iniciando la explorción heurística
======

Basta utiliar los siguientes comandos para iniciar la exploración:

    from heurispy.framework import inicia_exploracion_heuristica
    
    inicia_exploracion_heuristica(busqueda_tabu, lista_corridas)
    
Como ``HeurisPy`` utiliza el procesamiento en paralelo, se puede definir la cantidad de nucleos a ocupar con el parámetro nucleos_cpu.
Por defecto, se utilizan todos los nucleos del procesdor.

Al iniciar el proceso, ``HeurisPy`` manda una barra de progreso (generada por la biblioteca tqdm) que contabiliza las ejecuciones a realizar, y
va arrojando información sobre la información recopilada y los archivos generados como resultados. 

Examinando los archivos
======

Al terminar la exploración heurística, se crean dos carpetas: Resultados, que guarda los resultados estadísticos y gráficos creados por
exploración heurística, e Información, que 
contiene los datos e información avanzada sobre las exploraciones realizadas. En Resultados, se genera una carpeta con el nombre de la
heurística utilizada, y dentro de ella se encuentran las exploraciones realizadas, cuyo nombre es la fecha y la hora en la que se finalizó
la exploración. Por ejemplo, si el ejemplo antes descrito terminó su exploración el 4 de julio del 2019 a las 12:31 pm, entonces se guardan
en la carpeta "2019-07-04---12-31". Aquí se encuentra un archivo pdf, cuyo nombre contiene la heurístca utilizada, los parámetros que 
corresponden a la corrida evaluada, y la fecha y hora en la que se generó el archivo. Se destaca que la información que despliegan los 
archivos es dependiente de la heurística, por lo que los datos estadísticos y gráficos pueden variar.

Como el desempeño de la heurística es muy dependiente de sus parámetros y del problema de optimización discreta, no hay una regla que 
determine la combinación ideal entre heurística y parámetros, por lo que es conveniente poner a prueba el p.o.d. con varias heurísticas y 
varias configuraciones de parámetros, buscando diversificar las corridas para obtener la mayor cantidad de información posible, y buscar 
consistencia en los resultados.

    
