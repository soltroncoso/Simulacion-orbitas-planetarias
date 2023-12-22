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
datos_tierra = {"masa": 5.972 * (10**24), "eje_semi_mayor": 1.000 * 1.496e11, "velocidad_orbital": 29.8 * 1000}
datos_sol = {"masa": 1.989 * (10**30), "eje_semi_mayor": 0, "velocidad_orbital": 0}

# Crear instancias de CuerpoCeleste
tierra = CuerpoCeleste("Tierra", datos_tierra["masa"], datos_tierra["eje_semi_mayor"], datos_tierra["velocidad_orbital"])
sol = CuerpoCeleste("Sol", datos_sol["masa"], datos_sol["eje_semi_mayor"], datos_sol["velocidad_orbital"])

# Lista de cuerpos celestes
cuerpos_celestes = [sol, tierra]  # Aquí se pueden añadir más cuerpos celestes

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # Simulación para 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas de los cuerpos celestes
visualizar_orbitas(cuerpos_celestes)
```

