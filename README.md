# NucoroCurrency

Proyecto para entrevista laboral.

### Instrucciones instalación:
Al tratarse de una prueba, la he realizado usando sqlite para compartir la base de datos con datos ya introducidos de manera más simple, puesto que al no ser para algo que va a usarse en producción, las limitaciones que tiene sqlite no van a afectar. De esta forma las instrucciones para montar el proyecto van a ir igualmente dadas para el objetivo de usarlo utilizando el servidor de desarrollo que Django incorpora:

- Creamos carpeta donde queremos poner el proyecto y accedemos a ella.
- Clonamos el repositorio dentro de esa carpeta: git clone https://github.com/lskyr3l/Nucoro.git
- Accedemos a la carpeta Nucoro.
- Generamos el entorno virtual y le instalamos las dependencias django, requests y djangorestframework. En mi caso utilizo pipenv, por lo tanto lo hago de la siguiente forma:
    - pipenv install
    - pipenv install requests
    - pipenv install django
    - pipenv install djangorestframework
    - pipenv shell (para acceder al venv)
- Entramos en la carpeta NucoroCurrencyDjango.
- Activamos el servidor de desarrollo: python manage.py runserver
- El mismo terminal nos proporcionará donde podemos consultar la aplicación.


### Listado de urls:
- 1 admin/        Administrador de Django -- User: admin -- Pass: istrador
- 2 mockdata/<int:year>-<int:month>-<int:day>     Api que proporciona datos aleatorios.
- 3 timeseries/       Primera API a desarrollar en el test.
- 4 timeseries2/      Primera API a desarrollar en el test, versión realizada usando vistas genéricas y serializers. No recoge datos en caso de que no los haya, por lo que solo muestra datos guardados en la base de datos. El resultado obtenido pese a ser parecido, no es el óptimo a obtener, aunque ya que lo estuve haciendo, consideré interesante incluirlo debido a que hay que entender bastante bien como funcionan las clases y django restframework para obtener un resultado similar.
- 5 calculator/       Segunda API a desarrollar en el test.
- 6 time_weighted_rate/       Tercera API a desarrollar en el test.
- 7 backoffice/       Backoffice demandado en el test.


### Instrucciones BackOffice
Los archivos para los que he diseñado el BackOffice son los JSON que devuelve exchangeratesapi.io en su endpoint history. De esta forma, y pese a que he incluido dentro de currencyApp en la carpeta test_files un fichero para probar, se puede realizar la prueba descargando cualquier JSON de la API que he especificado y cargándolo en formulario correspondiente en el BackOffice.


### Mejoras propuestas sobre lo desarrollado
- Podría haber realizado una subclase de APIView e introducir allí la verificación de parámetros, por ejemplo, y despues usar esta subclase para desarrollar las APIs en vez de incluir la verificación de parámetros cada vez para de esta forma ahorrar y reutilizar código.
- Debería haber incluido verificación del formato en el que se introducen las fechas que van en los parámetros get.


### Mejoras propuestas para la aplicación
- En el modelo Currency, al ser el code único se podría usar como pk y así tendríamos el code también como un index.
- En el get_exchange_rate_data, no he incluido el exchanged_currency, ya que he considerado que lo óptimo sería hacer la consulta a la API de fixer obteniendo los datos de todas las Currency que tenemos guardadas, ya que con algunos cálculos de esta forma rellenamos la tabla realizando menos llamadas a la API.
- El endpoint historical que es la que he entendido que hay que usar en el test de entre las 2 gratuitas disponibles, tiene la limitación de consultar una fecha por llamada, lo cual hace que tengamos que realizar muchas llamadas a la misma.
- En el caso de los Provider, lo he realizado basándome en lo que he visto dentro del ejercicio, es decir, tanto fixer.io como exchangeratesapi.io devuelven más o menos los mismos datos, de forma que he considerado solo un endpoint a usar puesto que para la realización del mismo no he visto la necesidad de usar otros (el de latest, aunque presenta valores actualizados al momento, no he visto la necesidad de usarlo, puesto que con el historical y usando la fecha, ya me devolvía un valor aunque no estuviera 100% actualizado). De esta forma, en el caso de realizar esto para producción y estudiando otros proveedores probablemente hubiera escogido otra opción, como incluir un JsonField en el Provider donde especificara un diccionario que parseándolo nos proporcionara acceso a los diferentes endpoints, los parámetros que aceptaría cada uno y demás. De esta forma, podríamos configurar completamente los diferentes proveedores con sus diferentes endpoints y la forma en que devuelven los datos directamente desde el administrador de Django por ejemplo.