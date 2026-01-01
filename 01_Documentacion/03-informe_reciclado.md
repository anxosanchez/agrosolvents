## Simulación de uns planta de reciclado de fames y microemulsiones

La simulación de una planta de reciclaje de biodiésel (FAME - Fatty Acid Myl Esters) que ha sido utilizado como disolvente industrial es un proyecto de ingeniería química complejo. No obstante, en este proyecto se trata de analizar e intentar aprovechas las capacidades de la emprese hermana d DORVI, REGADI, posee en las instalaciones de DROVI y destinadas al reciclaje de disolventes convencioonales por combinaci´on de evaporación en un evpapofador de capa fina agitada y una columna de destilación. 

Los FAME poseen un alto punto de ebullición y propiedades termodinámicas específicas que hacen que su recuperación requiera cuidados para evitar la degradación térmica. Aquí hay una hoja de ruta estructurada paso a paso para comenzar su proyecto:

### Definición del problema y el caudal de entrada

Antes de abrir cualquier software, necesita datos concretos. El simulador devolverá basura si introducimos basura (basura que entra, basura que sale). 
 - Composición del biodiesel: Suele ser una mezcla de ésteres metílicos (C16, C18, etc.). Para la simulación, el oleato de metilo se utiliza a menudo como "pseudocomponente" representativo si no se dispone de la cromatografía exacta. 
 - Contaminantes: ¿Qué disolvió el biodiesel?
   - ¿Pinturas o resinas? (Sólidos o polímeros)
   - ¿Aceites minerales? (Hidrocarburos Pesados)
   - Agua?
- Especificaciones del Producto: 
  - ¿Qué pureza necesita para reutilizar como solvente? (ej. 99 % de pureza, <0,05 % de agua).

### Selección de operaciones unitarias

Dependiendo de los contaminantes, el proceso variará, pero el esquema clásico para recuperar solventes de alto punto de ebullición suele ser: 
- Filtración: si el biodiesel tiene partículas sólidas o lodos arrastrados. 
- Decantación (flash): si hay agua o solventes altamente volátiles mezclados, un tanque flash puede separarlos fácilmente. 
- Destilación al vacío: este es el punto crítico. El biodiesel se degrada (oxida o polimeriza) a altas temperaturas (generalmente por encima de $250^\circ\text{C}$).
  - Dado que su punto de ebullición a presión atmosférica es muy alto ($340-375^\circ\text{C}$), es obligatorio utilizar vacío para bajar la temperatura de ebullición y destilarlo sin "quemarlo"


### Elección de software de simulación

Hay varias opciones según el presupuesto y acceso: 
- Aspen Plus / Aspen HYSYS: El estándar de la industria. Tiene bases de datos muy completas para FAMEs.
- ChemCAD: Muy potente para procesos químicos y destilaciones.
- DWSIM (Recomendado por precio): Es Open Source y gratuito. Tiene una buena base de datos y permite simular destilaciones y reactores. Para un proyecto académico o de creación de prototipos, es la mejor opción.
- ProSim: Otra opción comercial con buenas capacidades de simulación.
- Simuladores específicos de destilación: Algunos simuladores están especializados en destilación y pueden ser útiles si la destilación es el foco principal.
  
En nuestro caso (UVIGO) poseemos software de simulación ASPEN - HYSYS que es el utilizado en muchos de nuestras simulaciones sobre todo en lo relacionado acon la viabilidad de la recuperación y la simulación del reciclado de los palmitatos y las microsemulsiones pero,desafortunadamente la empresa DROVI no posee licencia de este software y, dado que la licencia de la UVIGO es de educación, no podemos pasar los archivos de simulación a entidades privadas, por lo que se recomienda utilizar DWSIM que es gratuito y de código abierto en sus simulaciones. No obstante, en este apartado dejaremos las instrucciones necesarias para la simulación con ASPEN - HYSYS y DWSIM.

### Configuración de la simulación
 
#### Modelo Termodinámico (El "motor" de la simulación) Esta es una decisión técnica muy importante. El biodiesel es una molécula polar y orgánica or lo que:

- No se debe usar el modelo de gas ideal. 
- Utilizar modelos de coeficientes de actividad como NRTL o UNIQUAC. Funcionan muy bien para mezclas líquido-líquido y para predecir el equilibrio cuando hay agua o alcoholes presentes. 
- Si la mezcla consta solo de hidrocarburos (aceites), Peng-Robinson podría funcionar, pero NRTL es más seguro si no está seguro. 

### Pasos para configurar la simulación (Ejemplo en DWSIM/Aspen)

Una vez elegido el software, siga este orden: 
- Configuración de componentes: 
  - Agregar oleato de metilo (como componente base). 
  - Agregar agua (si hay humedad). 
  - Agregar el contaminante principal (por ejemplo, tolueno o un componente genérico pesado).
  - Selección do Paquete de Fluídos: Selecciona NRTL ou UNIQUAC.

#### Diseño del Diagrama de Flujo (PFD):

- Creara unha Corrente de Alimentación (Feed) coa temperatura e presión atmosférica.
- Colocar una Columna de Destilación Rigurosa.
- Configuración de la columna: 
  - Presión del condensador: Establecer una presión de vacío (por ejemplo, $0,1 \text{ bar}$ o $10 \text{ kPa}$). 
  - Relación de reflujo: comenzar con algo conservador, como 1,5 o 2. 
  - Especificaciones: definir lo que desea obtener del fondo (el biodiesel limpio generalmente sale por el fondo si los contaminantes son volátiles, o por la parte superior si los contaminantes son lodos pesados). 

#### Resumen de los desafíos clave

- **Nota importante**: a diferencia de la recuperación de acetona o etanol, el biodiesel no se evapora fácilmente. Si sus residuos son más pesados ​​que el biodiesel (por ejemplo, resinas), tendrá que evaporar el biodiesel (mucha energía). Si los residuos son más ligeros (por ejemplo, agua, disolventes ligeros), basta con decapar o evaporar los ligeros y dejar el biodiesel líquido (mucho más eficiente).

## Evaporador de Película Agitada (ATFE - Agitated Thin Film Evaporator)

La emppresa REGADI utiliza un evaporador de película agitada (ATFE) para la recuperación de disolventes. Este tipo de evaporador es especialmente adecuado para líquidos viscosos y sensibles al calor, como el biodiésel. El ATFE funciona creando una película delgada de líquido sobre una superficie calentada, mientras una cuchilla agita el líquido para mejorar la transferencia de calor y masa. Esto permite una rápida evaporación del disolvente volátil a temperaturas más bajas, minimizando el riesgo de degradación térmica del biodiésel. El diseño del ATFE incluye un rotor que gira a alta velocidad, creando una fuerza centrífuga que distribuye el líquido en una capa delgada. La agitación mecánica mejora la transferencia de calor al reducir la resistencia térmica en la película líquida y facilita la liberación del vapor formado. De hecho, es el equipo ideal para biodiesel sucio porque minimiza el tiempo de residencia y evita la degradación térmica ("quemar" el biodiesel), además de manejar bien la viscosidad. 

No existe una biblioteca Python específica llamada "modelo ATFE" o similar. A diferencia de las redes neuronales o la simulación de datos (donde tiene scikit-learn), en la ingeniería de procesos en Python generalmente se debe construir el modelo de operación unitaria por uno mismo o usar libros genéricos de termodinámica para respaldar sus cálculos. 

Para simular esto en Python, necesitará crear un modelo discreto (paso a paso) o resolver un sistema de ecuaciones diferenciales ordinarias (EDO) a lo largo del evaporador. Nosotros lo hemos abordado de la siguiente forma:

### La Física del ATFE

El ATFE no es un tanque mixto; es un tubo largo. Se debes modelizar dividiendo el tubo en pequeñas “rodajas” o nodos (volumen de control). En cada rebanada ($dz$), suceden tres cosas principales: 
1. Transferencia de calor: desde la pared caliente ($T_{wall}$) a la película líquida ($T_{liq}$).
2. Evaporación: Parte del disolvente volátil se convierte en vapor debido al calor recibido. 
3. Cambio de Composición: El líquido que pasa a la siguiente rebanada es más rico en biodiesel y más viscoso. 

Las variables clave son: 
- $U$ (Coeficiente general de transferencia de calor): en el ATFE, este valor es alto debido a la agitación mecánica.
- $\lambda$ (Calor latente de vaporización): energía requerida para evaporar el solvente.

### Bibliotecas Python necesarias

Para hacer esto, necesitaremos: 
- **NumPy**: para manejar vectores y matrices. 
- **SciPy** (integrar): para resolver ecuaciones diferenciales (odeint o solve_ivp) si quiere ser riguroso, o simplemente un bucle for si hace un modelo de diferencias finitas. 
- **Thermo** (opcional pero recomendado): una biblioteca Python de código abierto para obtener propiedades químicas ($Cp$, puntos de ebullición, densidad) sin tener que escribirlas a mano. (pipa instalación termo).

## Códigos de simulaciónen python

A partir de esta premisa hemos creado códigos específicos para simular el comportamiento de cada componente que forma parte de este proyecto de reciclado de ésteres y microemulsiones en las instalaciones de DROVI y REGADI. Los códigos están disponibles en el repositorio de GitHub asociado a este proyecto y se entrega copia digital con esta memoria.

La siumulación `atfe_1.py` simula el comportamiento del evaporador de película agitada (ATFE) para la recuperación de biodiésel a partir de una mezcla contaminada. Este código utiliza un modelo de diferencias finitas para dividir el evaporador en segmentos y calcular la transferencia de calor, la evaporación y el cambio de composición a lo largo del equipo.

A este modelo le falta mejorar dos puntos en el código, aunque en la actualidad no se emplean en el reciclaje de disolventes actual por parte de REGADI, pero que muy probablemente se pueda usar en el futuro es la destilación de los FAMES recuperados para su purificación final. Ello imlica tener en cuanta también ell equilibbrio vappor-líquido y la variación del coeficiente de transferencia de calor $U$ a lo largo del evaporador. Estos dos puntos son:

- VLE (Equilibrio vapor-líquido): hemos supuesto que la temperatura de ebullición es constante ($45^\circ\text{C}$). De hecho, a medida que el disolvente se evapora y aumenta la concentración de biodiesel, aumenta la temperatura de ebullición de la mezcla (Elevación del punto de ebullición). Debe llamar a termo en cada paso para recalcular la temperatura de equilibrio (punto de burbuja). 
- Viscosidad y U variable: a medida que el biodiesel se concentra, la viscosidad se dispara. Esto hace que el coeficiente $U$ disminuya al final de la tubería. Un buen modelo ATFE tiene una fórmula que recalcula $U$ en función de la viscosidad local.

También hay que tenr en cuenta que:
- A medida que el disolvente se evapora, la mezcla se vuelve "más pesada" y la temperatura de ebulición sube (esto es crítico para no degradar el biodiesel).
- La energía necesaria para evaporar ($\Delta H_{vap}$) cambia según la composición.

En caso de necesitar incorporar el uso de la destilación en la simulación del reciclado de los ésteres y las microemulsiones, se recomienda utilizar el código `destilacion_fames.py` como base para la simulación de la columna de destilación, adaptándolo según las necesidades específicas del proceso y las características de la mezcla a tratar.

La simulación `destilacion_fames.py` modela una columna de destilación para purificar el biodiésel recuperado. Utiliza un enfoque de equilibrio de fases y balances de masa para determinar la composición del destilado y del fondo en función de las condiciones operativas de la columna. Ambos códigos están diseñados para ser flexibles y adaptarse a diferentes condiciones de operación y composiciones de alimentación, permitiendo a los usuarios optimizar el proceso de reciclaje de biodiésel.

En el mundo real, a medida que el disolvente (metanol/hexano) se evapora, el líquido restante se vuelve "más espeso" (más viscoso). En un ATFE, las palas del rotor giran para mantener el líquido pegado a la pared en una fina capa:
- Si la viscosidad es baja (agua/metanol): el flujo es muy turbulento, la transferencia de calor ($U$) es muy alta. 
- Si la viscosidad es alta (fames/resinas): el líquido se congela, la turbulencia es baja y cuesta mucho más calentar el interior. El valor de $U$ se desploma.


#### Física: cómo modelar la variable $U$

En ingeniería química, para equipos de superficie rayada (como ATFE), se suele utilizar la teoría de la penetración o las correlaciones empíricas. Un enfoque estándar simplificado es escalar la base $U$ en función de la viscosidad:
  
$$
U_{local} = U_{base} \cdot \left( \frac{\mu_{base}}{\mu_{local}} \right)^n
$$
  
Donde $n$ suele estar entre $0,25$ y $0,33$. Esto significa que si la viscosidad sube mucho, el $U$ baja, pero no de forma lineal (las comillas ayudan a mitigar la caída). Código Python actualizado (con viscosidad dinámica) Agregamos la lógica para leer la viscosidad (mix.mul) en cada paso y recalcular la eficiencia térmica y creamos una nueva simulación `afte_2.py` que tiene en cuenta la varción de viscosidad.

Cuando se ejecute este código se revela en el gráfico:
- La "curva de agotamiento" de $U$: al principio, $U$ es alto (~1500). Pero hacia el final, cuando el biodiesel es casi puro (90%+), la línea roja (viscosidad) se dispara y la línea azul ($U$) cae.
- Consecuencia práctica: Los últimos 0,5 metros del evaporador son muy ineficientes. Es mucho más difícil sacar el último 1% del disolvente que el primer 50%. 

Lo siguiente fue preparar una simulación a nivel "industrial" contando con el Tiempo de Residencia. El biodiesel se degrada si pasa mucho tiempo caliente. Pero ante tendremos en cuenta algunas consideraciones teóricas.

## Simulaciones de recuperación de FAMES y microemulsiones en ASPEN - HYSYS y DWSIM

### El Biodiésel como Biosolvente Industrial

El biodiésel (FAME - Ésteres Metílicos de Ácidos Grasos) se conoce principalmente como combustible, pero en la industria química moderna está ganando terreno como "Biodisolvente Verde". Se utiliza para sustituir disolventes derivados del petróleo (como el tolueno o xileno) en la limpieza de resinas, tintas y formulación de agroquímicos debido a:
- Alto punto de inflamación: Es más seguro de manipular.
- Biodegradabilidad: Menor impacto en caso de vertido.
- Poder disolvente (Índice Kauri-Butanol): Muy eficaz para disolver compuestos orgánicos no polares.

El reto económico y ambiental es que, tras su uso, el biodiésel queda contaminado. Tirarlo es caro y contaminante; reciclarlo es obligatorio.

### Tecnología Clave: Evaporador de Película Agitada (ATFE)

Para reciclar el biodiésel, debemos separarlo de los contaminantes (pinturas, polímeros, aceites sucios). La destilación convencional (en tanque o columna) es peligrosa para el biodiésel porque requiere mantenerlo caliente mucho tiempo, lo que provoca su degradación. Aquí entra el ATFE (Agitated Thin Film Evaporator). ¿Qué es y cómo funciona?:

El ATFE es un intercambiador de calor de carcasa y tubos modificado. Dentro del tubo hay un rotor con aspas que gira a alta velocidad. 
- El líquido entra y las aspas lo "esparcen" contra la pared caliente formando una película finísima (0.5 - 2 mm). 
- Al ser una capa tan fina, la transmisión de calor es instantánea. Los componentes volátiles se evaporan en segundos. 
- El residuo pesado (o el producto purificado, dependiendo del proceso) cae por gravedad en espiral hacia el fondo.

#### Ventajas Críticas para el Biodiésel:
- Tiempo de Residencia Corto: El líquido solo está dentro del equipo unos segundos (10-60 s). Esto evita que el biodiésel se "queme" u oxide.
- Manejo de Viscosidad: Como viste en la simulación, cuando el disolvente se evapora, la viscosidad sube. Las aspas del ATFE rompen esa viscosidad, manteniendo el flujo.
- Operación a Alto Vacío: Permite bajar drásticamente la temperatura de ebullición.

#### Tipos de ATFE:
- Vertical (Más común): Usa la gravedad para bajar el producto. Ideal para destilar el solvente limpio.
- Horizontal: Se usa cuando se quiere secar completamente un sólido (formar polvo o pasta muy seca).
- Rotores Rígidos vs. Pendulares:
  - Rígidos: Mantienen una distancia fija con la pared (gap fijo).
  - Pendulares: La fuerza centrífuga pega las aspas a la pared (scrape surface), ideal si el residuo es muy pegajoso (fouling).

### Comparativa: Girasol vs. Palma

No todos los biodiéseles son iguales. Su comportamiento en el reciclado y su impacto ambiental dependen de su Perfil de Ácidos Grasos.

Diferencias Químicas y Operativas en el ATFE

| Característica         | Biodiésel de Girasol  | Biodiésel de Palma |  
| :--------------------- | :-------------------- | :----------------- |  
| Composición Principal  | Rico en Linoleico (C18:2). Es poliinsaturado (muchos dobles enlaces) | Rico en Palmítico (C16:0) y Oleico. Es saturado (cadenas estables) |  
| Estado Físico (20°C)   | Líquido fluido | Semisólido o pasta (se congela fácilmente)|  
| Punto de Niebla (CFPP) | Bajo (-5°C a 0°C). Fluye bien en frío | Alto (+13°C a +15°C). Necesita calefacción |  
| Estabilidad Térmica    | BAJA. Los dobles enlaces reaccionan con el oxígeno y el calor. Tiende a polimerizar (formar gomas) dentro del ATFE si se pasa de temperatura | ALTA. Resiste muy bien el calor sin degradarse. Es más robusto para reciclar |  
| Reto en el Reciclado   | Evitar la oxidación. Requiere vacío más profundo y temperaturas más bajas en el ATFE | Evitar que se solidifique. Requiere eléctrico (calefacción) en todas las tuberías y bombas |  

### Diagrama de Bloques del Proceso de Reciclado

![](../03_Recursos_Graficos/diagrama_bloques_reciclado_biodiesel.png)


### Implicaciones Ambientales (LCA - Análisis de Ciclo de Vida)

El origen de la materia prima define la "mochila ecológica" del disolvente reciclado.

### Biodiésel de Girasol

- Impacto de Uso de Suelo: Se cultiva extensivamente en Europa (España, Francia, Ucrania). Su huella de transporte es baja si la planta de reciclado está en Europa.
- Huella de Carbono: Generalmente menor debido al transporte reducido.
- Crítica: Menor rendimiento por hectárea que la palma, requiere más tierra para producir la misma cantidad de aceite.

### Biodiésel de Palma
Es un aceite que podríamos denominar eficiente pero polémico.- Rendimiento: Es el cultivo oleaginoso más eficiente del mundo (produce 5-10 veces más aceite por hectárea que el girasol).
Impacto Ambiental: Históricamente asociado a la deforestación de selvas tropicales (Indonesia, Malasia) y pérdida de biodiversidad (orangutanes).
Certificación: Si se usa palma, industrialmente se exige certificado RSPO (Roundtable on Sustainable Palm Oil) para asegurar que no proviene de deforestación reciente.
Transporte: Alta huella de carbono logística para traerlo a plantas de reciclaje en Occidente.

### Resumen del Proceso de Reciclado

El diagrama de bloques del proceso completo sería:
- Recepción: Biodiésel sucio (con tintas/resinas)
- Filtración Previa: Eliminar virutas metálicas o sólidos grandes (>100 micras) para no dañar el rotor del ATFE.
- Evaporación Flash (Opcional): Si trae agua o disolventes muy ligeros (acetona), se quitan aquí.
- Unidad ATFE (Corazón del proceso):
  - Entrada: Biodiésel Sucio.Condiciones: Vacío (10-50 mbar) y Tª (160-180°C).
  - Salida Vapor: Biodiésel puro (se condensa y recupera).
  - Salida Fondos: Lodos concentrados (residuos de resina/pintura) para gestión de residuos externos.
- Control de Calidad: Comprobar acidez y contenido de agua para validar su reutilización.

#### ¿Cómo te contempla esto en una simulación Python?

Hemos refinado el código Python:
- Si simulamos Girasol: Debemos vigilar que la temperatura de pared ($T_{wall}$) no sea excesiva, o añadir una función de "pérdida por degradación".
- Si simulamoss Palma: No hay que preocuparse tanto por la degradación, pero se debe vigilar la Viscosidad a temperaturas bajas (si el líquido se enfría, la viscosidad se dispara exponencialmente y bloquea el equipo).

## Reciclado de ésteres dibásicos

### ¿Qué son los Ésteres Dibásicos (DBE)?

Los DBE (Dibasic Esters) son una familia de disolventes oxigenados derivados de ácidos dicarboxílicos. Industrialmente, rara vez se usan puros; suelen ser una mezcla de tres ésteres metílicos purificados (la fracción "AGS"):
- Dimetil Adipato (C6)
- Dimetil Glutarato (C5)
- Dimetil Succinato (C4)

¿Por qué son "Disolventes Verdes"?:
- Baja Presión de Vapor: Se evaporan muy lentamente (bajos COV - Compuestos Orgánicos Volátiles), lo que reduce la inhalación por parte de los trabajadores.
- Biodegradabilidad: Se degradan fácilmente en el medio ambiente.
- No son inflamables (generalmente): Tienen puntos de inflamación altos ($>100^\circ\text{C}$), similares al biodiésel.
- Sustitución: Se usan para reemplazar disolventes tóxicos o clorados (como el Cloruro de Metileno o la NMP) en decapado de pinturas, limpieza de resinas y limpieza de moldes de poliuretano.

### El Reciclado de DBEs

Recuperar DBE es muy rentable porque es un disolvente caro (más que el biodiésel).
#### Proceso en ATFE

El comportamiento en un evaporador de película agitada es excelente, pero con una diferencia clave respecto al biodiésel:
- Punto de Ebullición:Los DBE hierven entre 196°C y 225°C (a presión atmosférica). Esto es más bajo que el biodiésel ($>300^\circ\text{C}$), pero mucho más alto que el agua o el acetona.
- Hidrólisis (El enemigo oculto): Si el residuo sucio contiene agua y el pH es ácido o básico, al calentar en el ATFE, el éster se rompe (hidrólisis), volviendo a formarse ácido adípico/glutárico (que son corrosivos) y metanol.
  - Solución: Es obligatorio neutralizar el pH y eliminar el agua (Flash previo) antes de meterlo al ATFE caliente.

### La Mezcla DBE + FAME: Retos de Interacción

En la industria es común encontrar mezclas (blends) de DBE + FAME. Se mezclan a propósito para obtener un disolvente con "doble acción": el DBE ataca la resina y el Biodiésel aporta lubricidad y mantiene la suciedad en suspensión.

Al intentar reciclar esta mezcla, surgen complicaciones termodinámicas:

#### Diferencia de Volatilidad (Separación)

Termodinámicamente, no son difíciles de separar entre sí si tienes una buena columna, pero en un ATFE (que tiene solo una etapa teórica de equilibrio) es complejo obtener cortes puros.DBE: 
  - Hierve a $\approx 200^\circ\text{C}$.
  - FAME: Hierve a $\approx 350^\circ\text{C}$.
 
En un solo paso de ATFE:
- Si se ajusta la temperatura para evaporar el DBE, el biodiésel se quedará en el fondo con los residuos (se pierde biodiésel).
- Si se sube la temperatura para evaporar también el biodiésel, ambos saldrán mezclados por el tope (recuperas el disolvente mezcla, pero no los separas).
- Nota: A menudo, recuperar la mezcla "Sucia pero destilada" es aceptable para volver a usarla en limpieza industrial.

#### Azeótropos y No-Idealidad

En este caso es donde la simulación (UNIQUAC/NRTL) es vital.
- Azeótropos con Agua: Tanto los DBE como el Biodiésel forman azeótropos con el agua. Esto significa que es difícil secarlos completamente solo con evaporación; siempre arrastran humedad, lo que fomenta la corrosión ácida.
- Interacción DBE-Biodiésel:
  - Químicamente son muy similares (polares, ésteres). Generalmente forman una mezcla zeotrópica (no azeotrópica), lo cual es bueno. Siguen la Ley de Raoult con desviaciones moderadas.
- El riesgo de la Transesterificación Cruzada:
  - Si la mezcla caliente contiene trazas de catalizador (ej. sosa cáustica de una limpieza anterior o metóxido), los grupos metilo pueden "saltar" de una molécula a otra. Aunque termodinámicamente no cambia mucho la mezcla (ambos son metil-ésteres), químicamente estás creando moléculas híbridas impredecibles.
#### Polimerización Cruzada

Si el residuo contiene pinturas o resinas de poliuretano:
- Los DBE son excelentes disolventes de poliuretano.
- Al concentrar el residuo en el fondo del ATFE, la concentración de resina sube.
- A altas temperaturas, el biodiésel (especialmente el de girasol) puede actuar como agente de curado o polimerizar con los residuos disueltos por el DBE, creando un gel sólido que puede bloquear el rotor del ATFE.

### Implementación en la Simulación Python

La incorporación de los ésteres dibásicos (DBE) a la simulación es un paso importante porque pasamos de una mezcla binaria (Disolvente/FAME) a una Mezcla Ternaria (o Multicomponente). El comportamiento cambia drásticamente:
- El Ligero (ej. Metanol/Agua): Se evapora casi instantáneamente al entrar.
- El Medio (DBE - Dimetil Adipato): Es el "componente difícil". Tiene un punto de ebullición alto (~227°C). Si nos pasamos de calor, lo evaporamos (se pierde por arriba); si nos quedam os cortos, se queda en el biodiésel.
- El Pesado (Biodiésel - Oleato): Debería quedarse líquido.

Para simular esto, se debe añadir un componente representativo de los DBE. El Dimetil Adipato es el mejor candidato estándar. Podríiamos crear un nuevo archivo `atfe_dbe_fame.py` que incluya:
- Componentes: FAME (oleato de metilo) + Dimetil Adipato + Agua + Contaminante (tolueno o resina).
- Modelo Termodinámico: NRTL o UNIQUAC para capturar las interacciones.
- Lógica de Hidrólisis: Si el pH < 6 o > 8 y hay agua, añadir una "pérdida" de DBE proporcional a la temperatura y tiempo de residencia.
- Control de Viscosidad: Similar al código anterior, pero considerando la mezcla DBE-FAME.  
- Salida: Composición del vapor (recuperado) y del fondo (residuo).

#### El Reto Matemático: Composición del Vapor ($y_i$)

En el código anterior asumíamos que solo evaporaba el disolvente. Ahora, todo puede evaporarse según su presión de vapor.Usaremos el cálculo de equilibrio de fases ($y_i$ vs $x_i$) de `thermo` para determinar qué composición exacta tiene el vapor que estamos retirando en cada centímetro del tubo.

Hemos creado otro simulador `atfe_dbe_fame_vle.py` que incluye este cálculo de equilibrio. En cada paso:
- Calculamos la composición líquida actual ($x_i$).
- Usamos `thermo` para obtener las presiones de vapor parciales y calcular la composición del vapor ($y_i$).
- Ajustamos las tasas de evaporación de cada componente según su fracción en el vapor.      

Con estas consideraciones, el código permitirá simular y optimizar el proceso de reciclado de mezclas DBE-FAME en un ATFE, ayudando a maximizar la recuperación de disolventes y minimizar los riesgos operativos.

#### Interpretación de los Resultados

Cuando se ejecuta este código, en la Gráfica 1 (Composición) se verás la "guerra" de volatilidades relativas:
- Metanol (Línea Roja punteada): 
  - Caerá a cero muy rápido (en los primeros 0.5 o 1 metro). 
  - Es tan volátil que el vacío se lo lleva enseguida.
- DBE (Línea Azul):
  - Al principio, su concentración sube. ¿Por qué? Porque estamos quitando metanol, así que porcentualmente el DBE y el Biodiésel aumentan.
  - Una vez que el metanol desaparece, la temperatura sube. Si la $T_{pared}$ es suficientemente alta, empezarás a ver cómo la línea azul empieza a bajar. Eso significa que estás evaporando el DBE (recuperándolo por arriba).
- Biodiésel (Línea Verde): Debería subir constantemente hasta acercarse al 100% (o al valor que desees) en el fondo.

#### Experimentación: ¿Cómo "jugar" con el código?

Si se quiere separar el DBE del Biodiésel:
- Subir T_wall_C a 190°C o 200°C. y la línea azul (DBE) caerá al final del tubo (se va al vapor).
- Si quieres limpiar el disolvente (DBE+Biodiésel) de impurezas ligeras:Baja T_wall_C a 140°C. El Metanol desaparecerá, pero el DBE se mantendrá líquido junto con el Biodiésel (la línea azul se mantendrá alta).

##### Nota sobre Azeótropos
El código actual usa thermo, que tiene modelos de coeficientes de actividad (como UNIFAC o NRTL modificados internamente si están disponibles). Si existen azeótropos conocidos en la base de datos entre estos componentes, el cálculo mix.flash ya los está teniendo en cuenta implícitamente.Ejemplo: Si hubiera un azeótropo Metanol-DBE, verías que no puedes bajar la concentración de uno de ellos a cero sin arrastrar el otro.

La simulación se mejoró también par acalcular la potencia consumida en el proceso. El cálculo de la potencia del rotor es fundamental. En plantas reales de reciclado de biodiésel, este es a menudo el "cuello de botella".

Si el residuo se vuelve demasiado viscoso (como una goma o pegamento) al final del tubo, el motor eléctrico sufrirá. Si no está bien dimensionado, saltarán las protecciones térmicas y la planta se parará.

### La Física: ¿Cuánta energía cuesta mover las aspas?
El consumo de potencia en un ATFE se debe principalmente al Cizallamiento Viscoso (arrastrar las palas a través del líquido).La fórmula de ingeniería simplificada para cada sección del tubo es:
  
$$
P_{corte} = \mu \cdot A \cdot \frac{v^2}{\delta}
$$
  
Donde:$\mu$: Viscosidad dinámica local (Pa·s) [Calculada por thermo].$A$: Área de la sección ($m^2$).$v$: Velocidad periférica de la pala ($m/s$).$\delta$: Espesor de la película o "gap" entre pala y pared (m).


El código `atfe_dbe_fame_poterncia.py` incluye el cálculo del consumo energético del ATFE basado en la transferencia de calor necesaria para evaporar los componentes volátiles. Este cálculo es crucial para evaluar la viabilidad económica del proceso de reciclado.

### Interpretación de la simulación

#### La correlación Viscosidad-Potencia

La línea roja (Potencia) debiera ser casi idéntica en forma a la azul (Viscosidad). Esto confirma que el consumo eléctrico es un "sensor" indirecto de cuán espeso está el producto.

#### El peligro del fondo

Si la línea roja se dispara exponencialmente en los últimos 0.5 metros, tienes un problema de diseño,lo que significa que el residuo se está volviendo demasiado viscoso., o sea que se está secando demasiado el residuo, lo cual es un riesgo ya que los FAMEs polimerizados puede bloquear el rotor (stall) o quemar el motor. La solución podría ser dejar un poco más de DBE o Biodiésel en el fondo (no intentar llegar al 100% de pureza) para que actúe como lubricante.

#### Tabla Comparativa Técnica 

Los resultados que obtendrías en la simulación (usando methyl linoleate vs methyl palmitate) con la realidad operativa en planta permiten elaborar la siguiente tabla comparativa.


| Variable de Ingeniería             | Biodiésel de Girasol                                                                | Biodiésel de Palma                                                                     |
|------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Componente Clave (Simulación)      | Metil Linoleato (C18:2)                                                             | Metil Palmitato (C16:0)                                                                |
| Estructura Molecular               | Cadena larga con 2 dobles enlaces ("kinks"). Molécula "doblada".                    | Cadena saturada lineal. Molécula "recta" y empaquetada.                                |
| Viscosidad (100∘C)                 | Baja. Fluye muy bien incluso concentrado.                                           | Media/Alta. Al ser saturado, es más espeso.                                            |
| Punto de Fusión / Fluidez          | −5∘C (Líquido siempre).                                                             | +30∘C (Tiende a solidificar en líneas frías).                                          |
| Sensibilidad Térmica (Degradación) | Muy Alta. Los dobles enlaces reaccionan con el calor.                               | Baja. Muy estable y robusto.                                                           |
| Riesgo Principal en ATFE           | Fouling por Polimerización. Si Tpared​>180∘C, se forman gomas (barniz) en la pared. | Bloqueo por Enfriamiento. Si el residuo se enfría al salir, se hace una "vela" sólida. |
| Potencia del Rotor (Simulada)      | Menor consumo (el líquido lubrica bien).                                            | Mayor consumo (+15-20%) debido a la mayor viscosidad.                                  |
| Estrategia de Operación            | Maximizar Vacío (<10 mbar) para bajar la Tª de ebullición.                          | Mantener traceado eléctrico en la descarga de fondo.                                   |

### Simulación con aceite de palma en vez de girasol

La palma es rica en ácidos saturados. Usaremos el Metil Palmitato.

Simplemente habría que cambiar el el código python lo siguiente:

```
# Escenario PALMA
# Sustituimos 'methyl oleate' por 'methyl palmitate'
comps = ['methanol', 'dimethyl adipate', 'methyl palmitate']

# Nota para la simulación:
# Verás que la viscosidad (mu_liq) calculada por 'thermo' será mayor.
# Esto hará que el cálculo de 'Power_segment_Watts' suba.
``` 

#### Interpretación de Resultados

Si se ejecutan ambos escenarios y se comparan las gráficas de Potencia, se puede concluir lo siguiente:
- Eficiencia Energética: El reciclado de biodiésel de girasol consume menos electricidad en el motor del ATFE porque el fluido ofrece menos resistencia al cizallamiento.
- Ventana Operativa: 
  - El Girasol tiene una ventana estrecha por arriba (límite de temperatura).
  - La Palma tiene una ventana estrecha por abajo (límite de solidificación).
- Calidad del Destilado: Debido a la estabilidad, es más probable obtener un disolvente reciclado de Palma con menos acidez (menos degradación) que uno de Girasol, a menos que el equipo de vacío funcione perfectamente.

## Conclusiones

### Conclusiones del Estudio

El presente informe evalúa la viabilidad técnica de la recuperación biosolventes (Biodiésel y Ésteres Dibásicos) mediante evaporación en película agitada (ATFE). A través del modelado computacional en Python, integrando termodinámica de equilibrio de fases y mecánica de fluidos, se han alcanzado las siguientes conclusiones:
- Idoneidad de la Tecnología ATFE:La simulación confirma que el ATFE es el equipo crítico e insustituible para este proceso. La combinación de alto vacío (<50 mbar) y tiempos de residencia cortos es la única vía para separar los contaminantes sin provocar la degradación térmica (oxidación) del biodiésel ni la hidrólisis de los ésteres dibásicos (DBE).
- Influencia Crítica de la Materia Prima (Girasol vs. Palma):El perfil de ácidos grasos determina la estrategia operativa:
  - El Biodiésel de Girasol (Linoleico) presenta ventajas mecánicas (menor viscosidad y consumo de potencia en el rotor), pero impone un límite térmico estricto ($T_{pared} < 170^\circ\text{C}$) debido a su alta tendencia a la polimerización en caliente.
  - El Biodiésel de Palma (Palmítico) ofrece una gran estabilidad térmica, permitiendo operaciones más agresivas, pero requiere un mayor consumo energético en el motor (+15-20%) y sistemas de calentamiento auxiliar (traceado) para evitar la solidificación del residuo en la descarga.
- Dinámica de la Recuperación de DBEs:La recuperación de Ésteres Dibásicos en mezcla con biodiésel es termodinámicamente viable pero compleja. La simulación demuestra que existe una "ventana operativa" estrecha: se requiere una temperatura de pared suficiente para evaporar el DBE (P.eb. $\approx 200^\circ\text{C}$), pero el aumento de viscosidad resultante al secar el fondo reduce drásticamente el coeficiente de transferencia de calor ($U$), limitando la eficiencia en los últimos tramos del evaporador.
- Consumo Energético:El modelo electromecánico desarrollado revela que el consumo de potencia del rotor no es lineal. Se dispara exponencialmente en el último tercio del equipo a medida que aumenta la concentración de sólidos y la viscosidad. Esto subraya la importancia de no intentar secar el residuo al 100%, dejando un remanente de disolvente como lubricante para proteger el equipo.5.2. 

### Recomendaciones para Trabajos Futuros

Para avanzar desde esta simulación teórica hacia una implementación industrial, se sugieren las siguientes líneas de acción:
- Validación Experimental en Planta Piloto: Se recomienda realizar ensayos con muestras reales de disolvente sucio en un ATFE a escala laboratorio ($0.05 - 0.1 m^2$) para validar los coeficientes de transferencia de calor ($U$) calculados y ajustar el exponente de viscosidad ($n$) del modelo.
- Análisis de Ciclo de Vida (LCA): Realizar un estudio comparativo de la huella de carbono entre el proceso de reciclado propuesto y la incineración del residuo. El estudio debe cuantificar si el ahorro de emisiones por no producir disolvente virgen compensa el consumo eléctrico de las bombas de vacío y el calentamiento del ATFE.
- Diseño del Sistema de Vacío: Dado que se evaporan compuestos orgánicos volátiles (VOCs), se recomienda estudiar la implementación de bombas de vacío de tornillo seco en lugar de anillo líquido, para evitar la generación de agua residual contaminada.
- Integración Energética: Evaluar la posibilidad de utilizar el calor latente de los vapores de disolvente recuperados (que salen a $>100^\circ\text{C}$) para precalentar la alimentación, mejorando la eficiencia global de la planta.
