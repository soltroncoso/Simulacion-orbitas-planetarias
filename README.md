# Simulacion-orbitas-planetarias
Este script en Python simula el movimiento de los cuerpos celestes en el sistema solar, implementando y comparando dos métodos de integración numérica: Leapfrog y Euler-Cromer. La simulación está diseñada para ilustrar las diferencias en precisión y rendimiento entre estos métodos en el contexto del ramo física computacional.
### Installation
```
git clone [https://github.com/soltroncoso/Simulacion-orbitas-planetarias.git]
```

```
pip install numpy matplotlib
```


# Ejemplo de Uso

### Este fragmento muestra cómo se crean objetos `CuerpoCeleste` y cómo se configura y ejecuta la simulación del sistema solar utilizando los métodos Leapfrog o Euler-Cromer:

```
python
import numpy as np
from FisicaComputacional import CuerpoCeleste, simular_sistema_solar, visualizar_orbitas

# Datos de los planetas
# Definición de las características de la Tierra y el Sol para la simulación.
# Estos incluyen masa, eje semi-mayor (distancia promedio al Sol), y velocidad orbital.
datos_tierra = {"masa": 5.972 * (10**24),  # Masa de la Tierra en kilogramos
                "eje_semi_mayor": 1.000 * 1.496e11,  # Distancia promedio al Sol en metros
                "velocidad_orbital": 29.8 * 1000}  # Velocidad orbital en metros/segundo
datos_sol = {"masa": 1.989 * (10**30),  # Masa del Sol en kilogramos
             "eje_semi_mayor": 0,  # El Sol se considera en el origen
             "velocidad_orbital": 0}  # El Sol está estacionario en este modelo

# Crear instancias de CuerpoCeleste
# Inicializa objetos de CuerpoCeleste para la Tierra y el Sol con los datos definidos.
tierra = CuerpoCeleste("Tierra", datos_tierra["masa"], datos_tierra["eje_semi_mayor"], datos_tierra["velocidad_orbital"]) 
sol = CuerpoCeleste("Sol", datos_sol["masa"], datos_sol["eje_semi_mayor"], datos_sol["velocidad_orbital"])

# Lista de cuerpos celestes
# Agrupa los cuerpos celestes en una lista para la simulación.
# Se pueden añadir más cuerpos celestes a esta lista según sea necesario.
cuerpos_celestes = [sol, tierra]  # Aquí se pueden añadir más cuerpos celestes

# Parámetros de la simulación
dt = 86400  # Define un paso de tiempo de un día (en segundos) para la simulación.
num_pasos = 365 * 10  # Duración de la simulación: 10 años (en días).

# Realizar la simulación
# Ejecuta la simulación del movimiento de los cuerpos celestes durante el periodo definido.
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas de los cuerpos celestes
# Genera un gráfico de las órbitas de los cuerpos celestes basado en los datos de la simulación.
visualizar_orbitas(cuerpos_celestes)
```

