OpenPDF v2.0
============

Herramienta para generar estadísticas de encuestas en formato *PDF*.

Este proyecto continúa el trabajo un quatrimestre anterior para la asignatura *SLDS* (*FIB*, *UPC*). 

Índice
======
  * [OpenPDF v2.0](#OpenPDF-v2.0)
  * [FAQ](#FAQ)
  * [Instalación](#Instalación)
  * [Uso](#Uso)
  * [TODO](#TODO)
  * [Licencia](#Licencia)

FAQ
===
##### ¿Cuál es la idea?
Conseguir procesar un montón encuestas en formato *.pdf*, extraer datos acerca de las respuestas seleccionadas, y pintar las gráficas correspondientes.

##### ¿Qué distingue las respuestas seleccionadas?
Es posible resaltar texto (*highlight*) y guardar el *pdf* modificado utilizando un editor como [Acrobat Reader](https://acrobat.adobe.com/us/en/acrobat/pdf-reader.html).

##### ¿Cómo sabemos a qué pregunta corresponde cada respuesta?
Por la localización del *highlight* de la respuesta dentro de la página.

Para ello es necesario proporcionar una copia modificada de la encuesta *pdf* con todas las preguntas y respuestas seleccionadas. El color del resaltado se utilizará para distinguir preguntas de respuestas. 

##### PDFs de ejemplo
- Una [simple encuesta](https://github.com/Pacific01/openPDF/blob/development/Preguntas/SLDS_Project_Questions-raw.pdf), y la [plantilla con preguntas y respuestas marcadas](https://github.com/Pacific01/openPDF/blob/development/Preguntas/SLDS_Project_Questions.pdf).
- Puedes ver diferentes respuestas a la encuesta en la carpeta [Respuestas](https://github.com/Pacific01/openPDF/blob/development/Respuestas).

##### ¿Cómo proporciona *OpenPDF* los resultados?
Tras procesar las encuestas, el programa genera dos ficheros *.json*  -uno contiene datos acerca de las preguntas, y el otro de las respuestas. Su estructura general es la siguiente:

```javascript
// questions.json
{
  "questions": [
    {
      "text": "1. De qué color es el caballo blanco de Santiago?", 
      "numAnswers": 3, 
      "id": 1, 
      "answers": [
        {
          "text": "1) Rojo", 
          "id": 1
        }, 
        {
          "text": "2) Verde", 
          "id": 2
        }, 
        {
          "text": "3) Azul", 
          "id": 3
        }
      ]
    },
    ...
  ]
}
```
```javascript
// answers.json
{
  "numAnswers": 5, 
  "answers": [
    {
      "questionId": 1, 
      "answers": [
        3, 
        1, 
        1
      ]
    }, 
    ...
  ]
}
```
Además, *OpenPDF* genera una serie de plots que representan la distribución de respuestas para cada pregunta. Si ejecutas el programa sin más, podrás ver las gráficas resultantes de procesar las encuestas de los *pdf* de ejemplo en la carpeta `Plots`.

##### ¿Qué piensas del formato *pdf*?
Es **el mal** (ver [la especificación](http://www.adobe.com/devnet/pdf/pdf_reference.html)).

Instalación
===========
Es necesario instalar el siguiente software para ejecutar *OpenPDF v2.0*
- [python 2.7](https://www.python.org/)
    *OpenPDF v2.0* está escrito en python y requiere la versión 2.7
- [pdfquery](https://pypi.python.org/pypi/pdfquery)
    El parseo de los ficheros *.pdf* se realiza con *pdfquery*
- [gnuplot](http://www.gnuplot.info/)
    Los gráficos de las encuestas se generan con *gnuplot*

Una vez tengas todo instalado, sólo debes clonar este repo y ya puedes empezar!
```
git clone https://github.com/Pacific01/openPDF.git
```

Uso
===
Para probar rápidamente *OpenPDF*, basta con ejecutar los siguientes comandos desde la carpeta `openPDF`:
```
python main.py
python histo.py
```

Scripts
-------
**main.py**
*main.py* analiza todas las encuestas y genera los ficheros *.json* que contienen los resultados (*questions.json* y *answers.json*).

**histo.py**
*histo.py* genera una gráfica para cada pregunta: un histograma con las frecuencias de las diferentes respuestas.

Flujo de trabajo
----------------
Típicamente querrás analizar los resultados de tus propias encuestas. Para ello es conveniente seguir los siguientes pasos:

**Crear el *pdf* de la encuesta** 
Este paso es especialmente delicado ya que este *pdf* necesita tener una estructura muy concreta. En particular, el texto de cada pUtilizar Adobe Reader garantiza que la restriccion del highlight se cumpleregunta y cada respuesta debe encontrarse en un *PDFObject* de tipo *LTTextBoxHorizontal*. Crear el *pdf* con [latex](https://www.latex-project.org/) y una plantilla parecida a [esta](https://github.com/Pacific01/openPDF/blob/development/Samples/main.tex) garantiza que dicha restricción se cumplirá.

**Resaltar las preguntas y las respuestas**
Elige un color (por ejemplo, azul) y resalta, una por una, todas las preguntas del cuestionario. A continuación, selecciona un segundo color diferente al anterior (por ejemplo, verde), y resalta, una por una, todas las respuestas. Guarda el *pdf*, y ¡ya tienes la plantilla de preguntas-respuestas!

El *pdf* resultante debe cumplir la restricción del anterior apartado, y además para toda pregunta y respuesta ha de existir un *PDFObject* de tipo *Annot*, subtipo */Highlight*, y cuyo color es el de una pregunta o una respuesta. Utilizar [Adobe Reader](https://acrobat.adobe.com/us/en/acrobat/pdf-reader.html) garantiza que la restriccion del *highlight* se cumplirá.

Para comprobar que el *pdf* tiene el formato aceptado, imprime el árbol en *xml* utilizando [pdfminer](https://github.com/euske/pdfminer) (se te instala con *pdfquery*):
```python
import pdfquery

pdf = pdfquery.PDFQuery(QUESTIONS_FILE)
pdf.load()
pdf.tree.write("test.xml", pretty_print=True, encoding="utf-8")
```
Si el `test.xml` tiene una estructura similar a [esta](https://github.com/Pacific01/openPDF/blob/development/Samples/test.xml), es que tiene el formato aceptado.

**Configurar el script *main.py***
Para hacer su trabajo, *OpenPDF* sólo necesita saber cuál es la plantilla de preguntas-respuestas, y el directorio donde buscar los *pdf* con las respuestas. Abre el fichero *main.py* con un editor de texto cualquiera, y modifica las siguientes constantes para especificar tus propias encuestas:
```
QUESTIONS_FILE = 'Preguntas/SLDS_Project_Questions.pdf'
ANSWERS_FOLDER = 'Respuestas/'
```
Adicionalmente, puedes especificar el color del que estarán resaltadas las preguntas y las respuestas (por defecto deberían ser azul y verde, respectivamente):
```
QCOLOR, ACOLOR = '[0.0, 0.0, 1.0]', '[0.0, 1.0, 0.0]'
```

**Pasar las encuestas**
El siguiente paso es que los encuestados contesten enviando un *pdf* con sus propias respuestas seleccionadas. Es importante que no rompan las restricciones de formato, por lo que de nuevo se recomienda que utilizen *Adobe Reader* para añadir los *highlights*. Cabe notar que el color del *highlight* en este paso ya no importa. Añade todos estos *pdf* de respuestas a la carpeta anteriormente indicada.

**Ejecutar OpenPDF**
¡Teclea los siguientes comandos y tus encuestas serán procesadas! :)
```
python main.py
python histo.py
```
Encontrarás los ficheros *questions.json* y *answers.json*, y los histogramas quedarán guardados en la carpeta `Plots`.

TODO
====
- Pedir los parámetros de configuración (plantilla *pdf*, carpeta respuestas, etc...) de forma interactiva.
- Control de errores: *OpenPDF* asume que todos los *pdf* que va a tratar cumplen las restricciones anteriormente mencionadas. Si un usuario no contesta una pregunta, por ejemplo, la salida del programa será indeterminada.


Licencia
========
OpenPDF es software open-source bajo la licencia [MIT](https://opensource.org/licenses/MIT).
