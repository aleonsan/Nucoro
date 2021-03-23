# NecoroCurrency

Proyecto para entrevista laboral.

### Instrucciones instalación:
Al tratarse de una prueba, la he realizado usando sqlite para compartir la base de datos con datos ya introducidos de manera más simple, puesto que al no ser para algo que va a usarse en producción, las limitaciones que tiene sqlite no van a afectar. De esta forma las instrucciones para montar el proyecto van a ir igualmente dadas para el objetivo de usarlo utilizando el servidor de desarrollo que Django incorpora:

https://github.com/lskyr3l/Nucoro.git


### Listado de urls:
1 admin/        Administrador de Django -- User: admin -- Pass: istrador
2 mockdata/<int:year>-<int:month>-<int:day>     Api que proporciona datos aleatorios.
3 timeseries/       Primera API a desarrollar en el test.
4 timeseries2/      Primera API a desarrollar en el test, versión realizada usando vistas genéricas y serializers. No recoge datos en caso de que no los haya. El resultado obtenido pese a ser parecido, no es el óptimo a obtener.
5 calculator/       Segunda API a desarrollar en el test.
6 time_weighted_rate/       Tercera API a desarrollar en el test.
7 backoffice/       Backoffice demandado en el test.


### Mejoras propuestas sobre lo desarrollado
- Podría haber realizado una subclase de APIView e introducir allí la verificación de parámetros, por ejemplo, y despues usar esta subclase para desarrollar las APIs en vez de incluir la verificación de parámetros cada vez para de esta forma ahorrar y reutilizar código.
- Debería haber incluido verificación del formato en el que se introducen las fechas que van en los parámetros get.


### Mejoras propuestas para la aplicación
- En el modelo Currency, al ser el code único se podría usar como pk y así tendríamos el code también como un index.
- En el get_exchange_rate_data, no he incluido el exchanged_currency, ya que he considerado que lo óptimo sería hacer consultar la API de fixer obteniendo los datos de todas las Currency que tenemos guardadas, ya que con algunos cálculos de esta forma rellenamos la tabla realizando menos llamadas a la API.
- El endpoint historical que es la que he entendido que hay que usar en el test de entre las 2 gratuitas disponibles, tiene la limitación de consultar una fecha por llamada, lo cual hace que tengamos que realizar muchas llamadas a la misma. 