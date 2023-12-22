#!/usr/bin/env python
# coding: utf-8

# ### simulación del sistema solar con leapfrog 10 años

# In[17]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, eje_semi_mayor, velocidad_orbital):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array([eje_semi_mayor, 0.0, 0.0], dtype=float)  # Posición inicial
        self.velocidad = np.array([0.0, velocidad_orbital, 0.0], dtype=float)  # Velocidad orbital
        self.velocidad_media = None  # Velocidad media para el método Leapfrog
        self.posiciones = []  # Lista para almacenar todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicialmente en cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Calcular la distancia
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Leapfrog para la simulación
def paso_leapfrog(cuerpo, otros_cuerpos, dt):
    if cuerpo.velocidad_media is None:  # Inicializar la velocidad media si es necesario
        aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
        cuerpo.velocidad_media = cuerpo.velocidad + 0.5 * dt * aceleracion

    cuerpo.posicion += dt * cuerpo.velocidad_media  # Actualizar la posición
    aceleracion_completa = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad = cuerpo.velocidad_media + 0.5 * dt * aceleracion_completa
    cuerpo.velocidad_media += dt * aceleracion_completa

    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Guardar la posición actual

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_leapfrog(cuerpo, otros_cuerpos, dt)

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes):
    figura = plt.figure(figsize=(10, 8))
    eje = figura.add_subplot(111, projection='3d')

    for cuerpo in cuerpos_celestes:
        posiciones = np.array(cuerpo.posiciones)
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=cuerpo.nombre)

    eje.set_xlabel('X (m)')
    eje.set_ylabel('Y (m)')
    eje.set_zlabel('Z (m)')
    eje.set_title('Órbitas del Sistema Solar')
    eje.legend()

    plt.show()

# Datos de los planetas proporcionados por el usuario
datos_cuerpos_celestes = {
    "Mercurio": {"mass": 3.285 * (10**23), "semi_major_axis": 0.3871 * 1.496e11, "orbital_velocity": 47.9 * 1000},
    "Venus": {"mass": 4.867 * (10**24), "semi_major_axis": 0.7233 * 1.496e11, "orbital_velocity": 35.0 * 1000},
    "Tierra": {"mass": 5.972 * (10**24), "semi_major_axis": 1.000 * 1.496e11, "orbital_velocity": 29.8 * 1000},
    "Marte": {"mass": 6.39 * (10**23), "semi_major_axis": 1.5273 * 1.496e11, "orbital_velocity": 24.1 * 1000},
    "Júpiter": {"mass": 1.898 * (10**27), "semi_major_axis": 5.2028 * 1.496e11, "orbital_velocity": 13.1 * 1000},
    "Saturno": {"mass": 5.683 * (10**26), "semi_major_axis": 9.5388 * 1.496e11, "orbital_velocity": 9.6 * 1000},
    "Urano": {"mass": 8.681 * (10**25), "semi_major_axis": 19.1914 * 1.496e11, "orbital_velocity": 6.8 * 1000},
    "Neptuno": {"mass": 1.024 * (10**26), "semi_major_axis": 30.0611 * 1.496e11, "orbital_velocity": 5.4 * 1000}
}

# Crear los objetos CuerpoCeleste
cuerpos_celestes = []
for nombre, datos in datos_cuerpos_celestes.items():
    cuerpo = CuerpoCeleste(nombre, datos["mass"], datos["semi_major_axis"], datos["orbital_velocity"])
    cuerpos_celestes.append(cuerpo)

# Asumiendo que el Sol está en el origen y no se mueve
sol = CuerpoCeleste("Sol", 1.989 * (10**30), 0, 0)
cuerpos_celestes.insert(0, sol)  # Agregar el Sol al principio de la lista

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas
visualizar_orbitas(cuerpos_celestes)


# ### Simulacion orbitas sistema solar interno 20 años leapfrog

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste en la simulación
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array(posicion, dtype=float)  # Posición inicial
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad inicial
        self.velocidad_media = None  # Velocidad en el punto medio (para el método Leapfrog)
        self.posiciones = []  # Almacena todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicializada a cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Distancia entre cuerpos
            if distancia < 1e-10:  # Evitar división por cero
                continue
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)  # Magnitud de la fuerza
            fuerza_total += magnitud_fuerza * r / distancia  # Fuerza total
    return fuerza_total / cuerpo.masa  # Aceleración

# Paso del método Leapfrog
def paso_leapfrog(cuerpo, otros_cuerpos, dt):
    if cuerpo.velocidad_media is None:  # Inicializar la velocidad media
        aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
        cuerpo.velocidad_media = cuerpo.velocidad + 0.5 * dt * aceleracion

    cuerpo.posicion += dt * cuerpo.velocidad_media  # Actualizar posición
    aceleracion_completa = aceleracion_gravitacional(cuerpo, otros_cuerpos)  # Aceleración al final del paso completo
    cuerpo.velocidad = cuerpo.velocidad_media + 0.5 * dt * aceleracion_completa  # Actualizar velocidad
    cuerpo.velocidad_media += dt * aceleracion_completa  # Actualizar velocidad media

    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Almacenar la posición actual

# Simular el sistema solar durante un número de pasos
def simular_sistema_solar(cuerpos_celestes, numero_pasos, dt):
    todas_posiciones = {cuerpo.nombre: [] for cuerpo in cuerpos_celestes}  # Diccionario para almacenar posiciones

    for paso in range(numero_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_leapfrog(cuerpo, otros_cuerpos, dt)
            todas_posiciones[cuerpo.nombre].append(cuerpo.posicion.copy())

    return todas_posiciones

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes, todas_posiciones, titulo):
    figura = plt.figure(figsize=(12, 10))
    eje = figura.add_subplot(111, projection='3d')
    colores = ['yellow', 'grey', 'orange', 'blue', 'red', 'brown', 'pink', 'lightblue', 'green']

    eje.scatter([0], [0], [0], color='yellow', label='Sol', marker='o', s=300)  # Representar el Sol

    for i, cuerpo in enumerate(cuerpos_celestes):
        posiciones = np.array(todas_posiciones[cuerpo.nombre])
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=f'Órbita de {cuerpo.nombre}', color=colores[i % len(colores)])

    eje.set_xlabel("Posición en el eje x (m)")
    eje.set_ylabel("Posición en el eje y (m)")
    eje.set_zlabel("Posición en el eje z (m)")
    eje.set_title(titulo)
    eje.legend()
    plt.show()

if __name__ == "__main__":
    # Definir los cuerpos celestes del sistema solar
    cuerpos_celestes = [
        CuerpoCeleste("Sol", 1.989 * (10**30), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        CuerpoCeleste("Mercurio", 3.285 * (10**23), [57.9e9, 0.0, 0.0], [0.0, 47870.0, 0.0]),
        CuerpoCeleste("Venus", 4.867 * (10**24), [108.2e9, 0.0, 0.0], [0.0, 35020.0, 0.0]),
        CuerpoCeleste("Tierra", 5.972 * (10**24), [149.6e9, 0.0, 0.0], [0.0, 29783.0, 0.0]),
        CuerpoCeleste("Marte", 6.39 * (10**23), [227.9e9, 0.0, 0.0], [0.0, 24007.0, 0.0])
    ]

    dt_inicial = 86400  # Un día en segundos
    numero_pasos = 365 * 20  # 20 años

    todas_posiciones = simular_sistema_solar(cuerpos_celestes, numero_pasos, dt_inicial)

    visualizar_orbitas(cuerpos_celestes, todas_posiciones, "Sistema Solar Interno")


# ### Simulación sistema solar externo leapfrog 50 años

# In[10]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definición de la clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array(posicion, dtype=float)  # Posición inicial
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad inicial
        self.velocidad_media = None  # Velocidad media para el método Leapfrog
        self.posiciones = []  # Lista para almacenar todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicialmente en cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Calcular la distancia
            if distancia < 1e-10:  # Evitar división por cero
                continue
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Leapfrog para la simulación
def paso_leapfrog(cuerpo, otros_cuerpos, dt):
    if cuerpo.velocidad_media is None:  # Inicializar la velocidad media si es necesario
        aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
        cuerpo.velocidad_media = cuerpo.velocidad + 0.5 * dt * aceleracion

    cuerpo.posicion += dt * cuerpo.velocidad_media  # Actualizar la posición
    aceleracion_completa = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad = cuerpo.velocidad_media + 0.5 * dt * aceleracion_completa
    cuerpo.velocidad_media += dt * aceleracion_completa

    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Guardar la posición actual

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    todas_posiciones = {cuerpo.nombre: [] for cuerpo in cuerpos_celestes}
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_leapfrog(cuerpo, otros_cuerpos, dt)
            todas_posiciones[cuerpo.nombre].append(cuerpo.posicion.copy())
    return todas_posiciones

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes, todas_posiciones, titulo):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    colores = ['yellow', 'orange', 'brown', 'blue', 'grey']

    ax.scatter([0], [0], [0], color='yellow', label='Sol', marker='o', s=300)  # Representar el Sol

    for i, cuerpo in enumerate(cuerpos_celestes):
        posiciones = np.array(todas_posiciones[cuerpo.nombre])
        ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=f'Órbita de {cuerpo.nombre}', color=colores[i % len(colores)])

    ax.set_xlabel("Posición en el eje x (m)")
    ax.set_ylabel("Posición en el eje y (m)")
    ax.set_zlabel("Posición en el eje z (m)")
    ax.set_title(titulo)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    # Crear los cuerpos celestes del sistema solar
    cuerpos_celestes = [
        CuerpoCeleste("Sol", 1.989 * (10**30), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        CuerpoCeleste("Júpiter", 1.898 * (10**27), [778.5e9, 0.0, 0.0], [0.0, 13070.0, 0.0]),
        CuerpoCeleste("Saturno", 5.683 * (10**26), [1433.5e9, 0.0, 0.0], [0.0, 9690.0, 0.0]),
        CuerpoCeleste("Urano", 8.681 * (10**25), [2872.5e9, 0.0, 0.0], [0.0, 6800.0, 0.0]),
        CuerpoCeleste("Neptuno", 1.024 * (10**26), [4495.1e9, 0.0, 0.0], [0.0, 5430.0, 0.0])
    ]

    dt = 86400  # Un día en segundos
    num_pasos = 365 * 50  # 50 años

    todas_posiciones = simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

    visualizar_orbitas(cuerpos_celestes, todas_posiciones, "Órbitas de Júpiter a Neptuno (con el Sol)")


# ### Simulación sistema solar externo leapfrog 84 años

# In[13]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definición de la clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array(posicion, dtype=float)  # Posición inicial
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad inicial
        self.velocidad_media = None  # Velocidad media para el método Leapfrog
        self.posiciones = []  # Lista para almacenar todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicialmente en cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Calcular la distancia
            if distancia < 1e-10:  # Evitar división por cero
                continue
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Leapfrog para la simulación
def paso_leapfrog(cuerpo, otros_cuerpos, dt):
    if cuerpo.velocidad_media is None:  # Inicializar la velocidad media si es necesario
        aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
        cuerpo.velocidad_media = cuerpo.velocidad + 0.5 * dt * aceleracion

    cuerpo.posicion += dt * cuerpo.velocidad_media  # Actualizar la posición
    aceleracion_completa = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad = cuerpo.velocidad_media + 0.5 * dt * aceleracion_completa
    cuerpo.velocidad_media += dt * aceleracion_completa

    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Guardar la posición actual

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    todas_posiciones = {cuerpo.nombre: [] for cuerpo in cuerpos_celestes}
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_leapfrog(cuerpo, otros_cuerpos, dt)
            todas_posiciones[cuerpo.nombre].append(cuerpo.posicion.copy())
    return todas_posiciones

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes, todas_posiciones, titulo):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    colores = ['yellow', 'orange', 'brown', 'blue', 'grey']

    ax.scatter([0], [0], [0], color='yellow', label='Sol', marker='o', s=300)  # Representar el Sol

    for i, cuerpo in enumerate(cuerpos_celestes):
        posiciones = np.array(todas_posiciones[cuerpo.nombre])
        ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=f'Órbita de {cuerpo.nombre}', color=colores[i % len(colores)])

    ax.set_xlabel("Posición en el eje x (m)")
    ax.set_ylabel("Posición en el eje y (m)")
    ax.set_zlabel("Posición en el eje z (m)")
    ax.set_title(titulo)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    # Crear los cuerpos celestes del sistema solar
    cuerpos_celestes = [
        CuerpoCeleste("Sol", 1.989 * (10**30), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        CuerpoCeleste("Júpiter", 1.898 * (10**27), [778.5e9, 0.0, 0.0], [0.0, 13070.0, 0.0]),
        CuerpoCeleste("Saturno", 5.683 * (10**26), [1433.5e9, 0.0, 0.0], [0.0, 9690.0, 0.0]),
        CuerpoCeleste("Urano", 8.681 * (10**25), [2872.5e9, 0.0, 0.0], [0.0, 6800.0, 0.0]),
        CuerpoCeleste("Neptuno", 1.024 * (10**26), [4495.1e9, 0.0, 0.0], [0.0, 5430.0, 0.0])
    ]

    dt = 86400  # Un día en segundos
    num_pasos = 365 * 84  # 84 años

    todas_posiciones = simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

    visualizar_orbitas(cuerpos_celestes, todas_posiciones, "Órbitas de Júpiter a Neptuno (con el Sol)")


# ### Simulación estrella pasajera cerca del sistema solar

# ### simulación del sistema solar con Euler cromer 10 años

# In[18]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, eje_semi_mayor, velocidad_orbital):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array([eje_semi_mayor, 0.0, 0.0], dtype=float)  # Posición inicial
        self.velocidad = np.array([0.0, velocidad_orbital, 0.0], dtype=float)  # Velocidad orbital
        self.posiciones = []  # Lista para almacenar todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicialmente en cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Calcular la distancia
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Euler-Cromer para la simulación
def paso_euler_cromer(cuerpo, otros_cuerpos, dt):
    aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)  # Calcular la aceleración
    cuerpo.velocidad += dt * aceleracion  # Actualizar la velocidad
    cuerpo.posicion += dt * cuerpo.velocidad  # Actualizar la posición
    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Guardar la posición actual

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_euler_cromer(cuerpo, otros_cuerpos, dt)

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes):
    figura = plt.figure(figsize=(10, 8))
    eje = figura.add_subplot(111, projection='3d')

    for cuerpo in cuerpos_celestes:
        posiciones = np.array(cuerpo.posiciones)
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=cuerpo.nombre)

    eje.set_xlabel('X (m)')
    eje.set_ylabel('Y (m)')
    eje.set_zlabel('Z (m)')
    eje.set_title('Órbitas del Sistema Solar')
    eje.legend()

    plt.show()

# Datos de los planetas proporcionados por el usuario
datos_cuerpos_celestes = {
    "Mercurio": {"mass": 3.285 * (10**23), "semi_major_axis": 0.3871 * 1.496e11, "orbital_velocity": 47.9 * 1000},
    "Venus": {"mass": 4.867 * (10**24), "semi_major_axis": 0.7233 * 1.496e11, "orbital_velocity": 35.0 * 1000},
    "Tierra": {"mass": 5.972 * (10**24), "semi_major_axis": 1.000 * 1.496e11, "orbital_velocity": 29.8 * 1000},
    "Marte": {"mass": 6.39 * (10**23), "semi_major_axis": 1.5273 * 1.496e11, "orbital_velocity": 24.1 * 1000},
    "Júpiter": {"mass": 1.898 * (10**27), "semi_major_axis": 5.2028 * 1.496e11, "orbital_velocity": 13.1 * 1000},
    "Saturno": {"mass": 5.683 * (10**26), "semi_major_axis": 9.5388 * 1.496e11, "orbital_velocity": 9.6 * 1000},
    "Urano": {"mass": 8.681 * (10**25), "semi_major_axis": 19.1914 * 1.496e11, "orbital_velocity": 6.8 * 1000},
    "Neptuno": {"mass": 1.024 * (10**26), "semi_major_axis": 30.0611 * 1.496e11, "orbital_velocity": 5.4 * 1000}
}

# Crear los objetos CuerpoCeleste
cuerpos_celestes = []
for nombre, datos in datos_cuerpos_celestes.items():
    cuerpo = CuerpoCeleste(nombre, datos["mass"], datos["semi_major_axis"], datos["orbital_velocity"])
    cuerpos_celestes.append(cuerpo)

# Asumiendo que el Sol está en el origen y no se mueve
sol = CuerpoCeleste("Sol", 1.989 * (10**30), 0, 0)
cuerpos_celestes.insert(0, sol)  # Agregar el Sol al principio de la lista

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas
visualizar_orbitas(cuerpos_celestes)


# ### simulación del sistema solar interno con Euler Cromer 20 años

# In[14]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste en la simulación
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array(posicion, dtype=float)  # Posición inicial
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad inicial
        self.posiciones = []  # Almacena todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicializada a cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Distancia entre cuerpos
            if distancia < 1e-10:  # Evitar división por cero
                continue
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)  # Magnitud de la fuerza
            fuerza_total += magnitud_fuerza * r / distancia  # Fuerza total
    return fuerza_total / cuerpo.masa  # Aceleración

# Paso del método Euler-Cromer
def paso_euler_cromer(cuerpo, otros_cuerpos, dt):
    aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)  # Calcular la aceleración
    cuerpo.velocidad += dt * aceleracion  # Actualizar la velocidad
    cuerpo.posicion += dt * cuerpo.velocidad  # Actualizar la posición
    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Almacenar la posición actual

# Simular el sistema solar durante un número de pasos
def simular_sistema_solar(cuerpos_celestes, numero_pasos, dt):
    todas_posiciones = {cuerpo.nombre: [] for cuerpo in cuerpos_celestes}  # Diccionario para almacenar posiciones

    for paso in range(numero_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_euler_cromer(cuerpo, otros_cuerpos, dt)  # Usar el método Euler-Cromer
            todas_posiciones[cuerpo.nombre].append(cuerpo.posicion.copy())

    return todas_posiciones

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes, todas_posiciones, titulo):
    figura = plt.figure(figsize=(12, 10))
    eje = figura.add_subplot(111, projection='3d')
    colores = ['yellow', 'grey', 'orange', 'blue', 'red', 'brown', 'pink', 'lightblue', 'green']

    eje.scatter([0], [0], [0], color='yellow', label='Sol', marker='o', s=300)  # Representar el Sol

    for i, cuerpo in enumerate(cuerpos_celestes):
        posiciones = np.array(todas_posiciones[cuerpo.nombre])
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=f'Órbita de {cuerpo.nombre}', color=colores[i % len(colores)])

    eje.set_xlabel("Posición en el eje x (m)")
    eje.set_ylabel("Posición en el eje y (m)")
    eje.set_zlabel("Posición en el eje z (m)")
    eje.set_title(titulo)
    eje.legend()
    plt.show()

if __name__ == "__main__":
    # Definir los cuerpos celestes del sistema solar
    cuerpos_celestes = [
        CuerpoCeleste("Sol", 1.989 * (10**30), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        CuerpoCeleste("Mercurio", 3.285 * (10**23), [57.9e9, 0.0, 0.0], [0.0, 47870.0, 0.0]),
        CuerpoCeleste("Venus", 4.867 * (10**24), [108.2e9, 0.0, 0.0], [0.0, 35020.0, 0.0]),
        CuerpoCeleste("Tierra", 5.972 * (10**24), [149.6e9, 0.0, 0.0], [0.0, 29783.0, 0.0]),
        CuerpoCeleste("Marte", 6.39 * (10**23), [227.9e9, 0.0, 0.0], [0.0, 24007.0, 0.0])
    ]

    dt_inicial = 86400  # Un día en segundos
    numero_pasos = 365 * 20  # 20 años

    todas_posiciones = simular_sistema_solar(cuerpos_celestes, numero_pasos, dt_inicial)

    visualizar_orbitas(cuerpos_celestes, todas_posiciones, "Sistema Solar Interno")


# ### simulación del sistema solar externo con Euler Cromer 50 años

# In[15]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definición de la clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array(posicion, dtype=float)  # Posición inicial
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad inicial
        self.posiciones = []  # Lista para almacenar todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicialmente en cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Calcular la distancia
            if distancia < 1e-10:  # Evitar división por cero
                continue
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Euler-Cromer para la simulación
def paso_euler_cromer(cuerpo, otros_cuerpos, dt):
    aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)  # Calcular la aceleración
    cuerpo.velocidad += dt * aceleracion  # Actualizar la velocidad
    cuerpo.posicion += dt * cuerpo.velocidad  # Actualizar la posición
    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Guardar la posición actual

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    todas_posiciones = {cuerpo.nombre: [] for cuerpo in cuerpos_celestes}
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_euler_cromer(cuerpo, otros_cuerpos, dt)
            todas_posiciones[cuerpo.nombre].append(cuerpo.posicion.copy())
    return todas_posiciones

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes, todas_posiciones, titulo):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    colores = ['yellow', 'orange', 'brown', 'blue', 'grey']

    ax.scatter([0], [0], [0], color='yellow', label='Sol', marker='o', s=300)  # Representar el Sol

    for i, cuerpo in enumerate(cuerpos_celestes):
        posiciones = np.array(todas_posiciones[cuerpo.nombre])
        ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=f'Órbita de {cuerpo.nombre}', color=colores[i % len(colores)])

    ax.set_xlabel("Posición en el eje x (m)")
    ax.set_ylabel("Posición en el eje y (m)")
    ax.set_zlabel("Posición en el eje z (m)")
    ax.set_title(titulo)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    # Crear los cuerpos celestes del sistema solar
    cuerpos_celestes = [
        CuerpoCeleste("Sol", 1.989 * (10**30), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        CuerpoCeleste("Júpiter", 1.898 * (10**27), [778.5e9, 0.0, 0.0], [0.0, 13070.0, 0.0]),
        CuerpoCeleste("Saturno", 5.683 * (10**26), [1433.5e9, 0.0, 0.0], [0.0, 9690.0, 0.0]),
        CuerpoCeleste("Urano", 8.681 * (10**25), [2872.5e9, 0.0, 0.0], [0.0, 6800.0, 0.0]),
        CuerpoCeleste("Neptuno", 1.024 * (10**26), [4495.1e9, 0.0, 0.0], [0.0, 5430.0, 0.0])
    ]

    dt = 86400  # Un día en segundos
    num_pasos = 365 * 50  # 50 años

    todas_posiciones = simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

    visualizar_orbitas(cuerpos_celestes, todas_posiciones, "Órbitas de Júpiter a Neptuno (con el Sol)")


# ### simulación del sistema solar externo con Euler Cromer 84 años

# In[16]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definición de la clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.masa = masa  # Masa del cuerpo
        self.posicion = np.array(posicion, dtype=float)  # Posición inicial
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad inicial
        self.posiciones = []  # Lista para almacenar todas las posiciones durante la simulación

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))  # Constante gravitacional
    fuerza_total = np.zeros(3)  # Fuerza total inicialmente en cero
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion  # Vector de distancia
            distancia = np.linalg.norm(r)  # Calcular la distancia
            if distancia < 1e-10:  # Evitar división por cero
                continue
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Euler-Cromer para la simulación
def paso_euler_cromer(cuerpo, otros_cuerpos, dt):
    aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)  # Calcular la aceleración
    cuerpo.velocidad += dt * aceleracion  # Actualizar la velocidad
    cuerpo.posicion += dt * cuerpo.velocidad  # Actualizar la posición
    cuerpo.posiciones.append(cuerpo.posicion.copy())  # Guardar la posición actual

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    todas_posiciones = {cuerpo.nombre: [] for cuerpo in cuerpos_celestes}
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_euler_cromer(cuerpo, otros_cuerpos, dt)
            todas_posiciones[cuerpo.nombre].append(cuerpo.posicion.copy())
    return todas_posiciones

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes, todas_posiciones, titulo):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    colores = ['yellow', 'orange', 'brown', 'blue', 'grey']

    ax.scatter([0], [0], [0], color='yellow', label='Sol', marker='o', s=300)  # Representar el Sol

    for i, cuerpo in enumerate(cuerpos_celestes):
        posiciones = np.array(todas_posiciones[cuerpo.nombre])
        ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=f'Órbita de {cuerpo.nombre}', color=colores[i % len(colores)])

    ax.set_xlabel("Posición en el eje x (m)")
    ax.set_ylabel("Posición en el eje y (m)")
    ax.set_zlabel("Posición en el eje z (m)")
    ax.set_title(titulo)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    # Crear los cuerpos celestes del sistema solar
    cuerpos_celestes = [
        CuerpoCeleste("Sol", 1.989 * (10**30), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        CuerpoCeleste("Júpiter", 1.898 * (10**27), [778.5e9, 0.0, 0.0], [0.0, 13070.0, 0.0]),
        CuerpoCeleste("Saturno", 5.683 * (10**26), [1433.5e9, 0.0, 0.0], [0.0, 9690.0, 0.0]),
        CuerpoCeleste("Urano", 8.681 * (10**25), [2872.5e9, 0.0, 0.0], [0.0, 6800.0, 0.0]),
        CuerpoCeleste("Neptuno", 1.024 * (10**26), [4495.1e9, 0.0, 0.0], [0.0, 5430.0, 0.0])
    ]

    dt = 86400  # Un día en segundos
    num_pasos = 365 * 84  # 84 años

    todas_posiciones = simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

    visualizar_orbitas(cuerpos_celestes, todas_posiciones, "Órbitas de Júpiter a Neptuno (con el Sol)")


# ### Alpha centauri a como estrella pasajera usando leapfrog

# In[28]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre
        self.masa = masa
        self.posicion = np.array(posicion, dtype=float)  # Posición como un array
        self.velocidad = np.array(velocidad, dtype=float)  # Velocidad como un array
        self.velocidad_media = None
        self.posiciones = []

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))
    fuerza_total = np.zeros(3)
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion
            distancia = np.linalg.norm(r)
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Leapfrog para la simulación
def paso_leapfrog(cuerpo, otros_cuerpos, dt):
    if cuerpo.velocidad_media is None:
        aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
        cuerpo.velocidad_media = cuerpo.velocidad + 0.5 * dt * aceleracion

    cuerpo.posicion += dt * cuerpo.velocidad_media
    aceleracion_completa = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad = cuerpo.velocidad_media + 0.5 * dt * aceleracion_completa
    cuerpo.velocidad_media += dt * aceleracion_completa

    cuerpo.posiciones.append(cuerpo.posicion.copy())

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_leapfrog(cuerpo, otros_cuerpos, dt)

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes):
    figura = plt.figure(figsize=(10, 8))
    eje = figura.add_subplot(111, projection='3d')

    for cuerpo in cuerpos_celestes:
        posiciones = np.array(cuerpo.posiciones)
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=cuerpo.nombre)

    eje.set_xlabel('X (m)')
    eje.set_ylabel('Y (m)')
    eje.set_zlabel('Z (m)')
    eje.set_title('Órbitas del Sistema Solar')
    eje.legend()

    plt.show()

# Datos de los planetas proporcionados por el usuario
datos_cuerpos_celestes = {
    "Mercurio": {"mass": 3.285 * (10**23), "semi_major_axis": 0.3871 * 1.496e11, "orbital_velocity": 47.9 * 1000},
    "Venus": {"mass": 4.867 * (10**24), "semi_major_axis": 0.7233 * 1.496e11, "orbital_velocity": 35.0 * 1000},
    "Tierra": {"mass": 5.972 * (10**24), "semi_major_axis": 1.000 * 1.496e11, "orbital_velocity": 29.8 * 1000},
    "Marte": {"mass": 6.39 * (10**23), "semi_major_axis": 1.5273 * 1.496e11, "orbital_velocity": 24.1 * 1000},
    "Júpiter": {"mass": 1.898 * (10**27), "semi_major_axis": 5.2028 * 1.496e11, "orbital_velocity": 13.1 * 1000},
    "Saturno": {"mass": 5.683 * (10**26), "semi_major_axis": 9.5388 * 1.496e11, "orbital_velocity": 9.6 * 1000},
    "Urano": {"mass": 8.681 * (10**25), "semi_major_axis": 19.1914 * 1.496e11, "orbital_velocity": 6.8 * 1000},
    "Neptuno": {"mass": 1.024 * (10**26), "semi_major_axis": 30.0611 * 1.496e11, "orbital_velocity": 5.4 * 1000}
}

# Crear los objetos CuerpoCeleste
cuerpos_celestes = []
for nombre, datos in datos_cuerpos_celestes.items():
    cuerpo = CuerpoCeleste(nombre, datos["mass"], [datos["semi_major_axis"], 0.0, 0.0], [0.0, datos["orbital_velocity"], 0.0])
    cuerpos_celestes.append(cuerpo)

# Añadir Alpha Centauri A como una estrella pasajera
masa_alpha_centauri_A = 2.18 * (10**30)
posicion_inicial_alpha_centauri_A = [5.0 * 1.496e12, 0.0, 1.0 * 1.496e12]  # 5 UA en X, 1 UA en Z
velocidad_alpha_centauri_A = [-5.0 * 1000, 0.0, 0.0]  # Movimiento hacia el negativo del eje X
alpha_centauri_A = CuerpoCeleste("Alpha Centauri A", masa_alpha_centauri_A, posicion_inicial_alpha_centauri_A, velocidad_alpha_centauri_A)
cuerpos_celestes.append(alpha_centauri_A)

# Asumiendo que el Sol está en el origen y no se mueve
sol = CuerpoCeleste("Sol", 1.989 * (10**30), [0, 0, 0], [0, 0, 0])
cuerpos_celestes.insert(0, sol)

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas
visualizar_orbitas(cuerpos_celestes)


# ### Alpha centauri a como estrella pasajera usando leapfrog

# In[29]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre
        self.masa = masa
        self.posicion = np.array(posicion, dtype=float)
        self.velocidad = np.array(velocidad, dtype=float)
        self.posiciones = []

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))
    fuerza_total = np.zeros(3)
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion
            distancia = np.linalg.norm(r)
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Euler-Cromer para la simulación
def paso_euler_cromer(cuerpo, otros_cuerpos, dt):
    aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad += dt * aceleracion
    cuerpo.posicion += dt * cuerpo.velocidad
    cuerpo.posiciones.append(cuerpo.posicion.copy())

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_euler_cromer(cuerpo, otros_cuerpos, dt)

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes):
    figura = plt.figure(figsize=(10, 8))
    eje = figura.add_subplot(111, projection='3d')

    for cuerpo in cuerpos_celestes:
        posiciones = np.array(cuerpo.posiciones)
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=cuerpo.nombre)

    eje.set_xlabel('X (m)')
    eje.set_ylabel('Y (m)')
    eje.set_zlabel('Z (m)')
    eje.set_title('Órbitas del Sistema Solar')
    eje.legend()

    plt.show()

# Datos de los planetas proporcionados por el usuario
datos_cuerpos_celestes = {
    "Mercurio": {"mass": 3.285 * (10**23), "semi_major_axis": 0.3871 * 1.496e11, "orbital_velocity": 47.9 * 1000},
    "Venus": {"mass": 4.867 * (10**24), "semi_major_axis": 0.7233 * 1.496e11, "orbital_velocity": 35.0 * 1000},
    "Tierra": {"mass": 5.972 * (10**24), "semi_major_axis": 1.000 * 1.496e11, "orbital_velocity": 29.8 * 1000},
    "Marte": {"mass": 6.39 * (10**23), "semi_major_axis": 1.5273 * 1.496e11, "orbital_velocity": 24.1 * 1000},
    "Júpiter": {"mass": 1.898 * (10**27), "semi_major_axis": 5.2028 * 1.496e11, "orbital_velocity": 13.1 * 1000},
    "Saturno": {"mass": 5.683 * (10**26), "semi_major_axis": 9.5388 * 1.496e11, "orbital_velocity": 9.6 * 1000},
    "Urano": {"mass": 8.681 * (10**25), "semi_major_axis": 19.1914 * 1.496e11, "orbital_velocity": 6.8 * 1000},
    "Neptuno": {"mass": 1.024 * (10**26), "semi_major_axis": 30.0611 * 1.496e11, "orbital_velocity": 5.4 * 1000}
}

# Crear los objetos CuerpoCeleste
cuerpos_celestes = []
for nombre, datos in datos_cuerpos_celestes.items():
    cuerpo = CuerpoCeleste(nombre, datos["mass"], [datos["semi_major_axis"], 0.0, 0.0], [0.0, datos["orbital_velocity"], 0.0])
    cuerpos_celestes.append(cuerpo)

# Añadir Alpha Centauri A como una estrella pasajera
masa_alpha_centauri_A = 2.18 * (10**30)
posicion_inicial_alpha_centauri_A = [5.0 * 1.496e12, 0.0, 1.0 * 1.496e12]  # 5 UA en X, 1 UA en Z
velocidad_alpha_centauri_A = [-5.0 * 1000, 0.0, 0.0]  # Movimiento hacia el negativo del eje X
alpha_centauri_A = CuerpoCeleste("Alpha Centauri A", masa_alpha_centauri_A, posicion_inicial_alpha_centauri_A, velocidad_alpha_centauri_A)
cuerpos_celestes.append(alpha_centauri_A)

# Asumiendo que el Sol está en el origen y no se mueve
sol = CuerpoCeleste("Sol", 1.989 * (10**30), [0, 0, 0], [0, 0, 0])
cuerpos_celestes.insert(0, sol)

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas
visualizar_orbitas(cuerpos_celestes)


# In[41]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre
        self.masa = masa
        self.posicion = np.array(posicion, dtype=float)
        self.velocidad = np.array(velocidad, dtype=float)
        self.velocidad_media = None  # Velocidad media para el método Leapfrog
        self.posiciones = []

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))
    fuerza_total = np.zeros(3)
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion
            distancia = np.linalg.norm(r)
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Leapfrog para la simulación
def paso_leapfrog(cuerpo, otros_cuerpos, dt):
    if cuerpo.velocidad_media is None:
        aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
        cuerpo.velocidad_media = cuerpo.velocidad + 0.5 * dt * aceleracion

    cuerpo.posicion += dt * cuerpo.velocidad_media
    aceleracion_completa = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad = cuerpo.velocidad_media + 0.5 * dt * aceleracion_completa
    cuerpo.velocidad_media += dt * aceleracion_completa

    cuerpo.posiciones.append(cuerpo.posicion.copy())

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_leapfrog(cuerpo, otros_cuerpos, dt)

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes):
    figura = plt.figure(figsize=(10, 8))
    eje = figura.add_subplot(111, projection='3d')

    for cuerpo in cuerpos_celestes:
        posiciones = np.array(cuerpo.posiciones)
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=cuerpo.nombre)

    eje.set_xlabel('X (m)')
    eje.set_ylabel('Y (m)')
    eje.set_zlabel('Z (m)')
    eje.set_title('Órbitas del Sistema Solar')
    eje.legend()

    plt.show()

# Datos de los planetas proporcionados por el usuario
datos_cuerpos_celestes = {
  "Mercurio": {"mass": 3.285 * (10**23), "semi_major_axis": 0.3871 * 1.496e11, "orbital_velocity": 47.9 * 1000},
    "Venus": {"mass": 4.867 * (10**24), "semi_major_axis": 0.7233 * 1.496e11, "orbital_velocity": 35.0 * 1000},
    "Tierra": {"mass": 5.972 * (10**24), "semi_major_axis": 1.000 * 1.496e11, "orbital_velocity": 29.8 * 1000},
    "Marte": {"mass": 6.39 * (10**23), "semi_major_axis": 1.5273 * 1.496e11, "orbital_velocity": 24.1 * 1000},
    "Júpiter": {"mass": 1.898 * (10**27), "semi_major_axis": 5.2028 * 1.496e11, "orbital_velocity": 13.1 * 1000},
    "Saturno": {"mass": 5.683 * (10**26), "semi_major_axis": 9.5388 * 1.496e11, "orbital_velocity": 9.6 * 1000},
    "Urano": {"mass": 8.681 * (10**25), "semi_major_axis": 19.1914 * 1.496e11, "orbital_velocity": 6.8 * 1000},
    "Neptuno": {"mass": 1.024 * (10**26), "semi_major_axis": 30.0611 * 1.496e11, "orbital_velocity": 5.4 * 1000}
}
# Crear los objetos CuerpoCeleste
cuerpos_celestes = []
for nombre, datos in datos_cuerpos_celestes.items():
    cuerpo = CuerpoCeleste(nombre, datos["mass"], [datos["semi_major_axis"], 0.0, 0.0], [0.0, datos["orbital_velocity"], 0.0])
    cuerpos_celestes.append(cuerpo)

# Añadir la Super Gigante Roja como una estrella pasajera
masa_super_gigante_roja = 3.978 * (10**31)  # Masa aproximada
posicion_inicial_super_gigante_roja = [8.0 * 1.496e12, 0.0, 2.0 * 1.496e12]  # 8 UA en X, 2 UA en Z
velocidad_super_gigante_roja = [-7.0 * 1000, 0.0, 0.0]  # Movimiento hacia el negativo del eje X
super_gigante_roja = CuerpoCeleste("Super Gigante Roja", masa_super_gigante_roja, posicion_inicial_super_gigante_roja, velocidad_super_gigante_roja)
cuerpos_celestes.append(super_gigante_roja)

# Asumiendo que el Sol está en el origen y no se mueve
sol = CuerpoCeleste("Sol", 1.989 * (10**30), [0, 0, 0], [0, 0, 0])
cuerpos_celestes.insert(0, sol)

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas
visualizar_orbitas(cuerpos_celestes)


# In[43]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para representar un cuerpo celeste
class CuerpoCeleste:
    def __init__(self, nombre, masa, posicion, velocidad):
        self.nombre = nombre
        self.masa = masa
        self.posicion = np.array(posicion, dtype=float)
        self.velocidad = np.array(velocidad, dtype=float)
        self.posiciones = []

# Función para calcular la aceleración gravitacional
def aceleracion_gravitacional(cuerpo, otros_cuerpos):
    G = 6.674 * (10**(-11))
    fuerza_total = np.zeros(3)
    for otro_cuerpo in otros_cuerpos:
        if cuerpo != otro_cuerpo:
            r = otro_cuerpo.posicion - cuerpo.posicion
            distancia = np.linalg.norm(r)
            magnitud_fuerza = (G * cuerpo.masa * otro_cuerpo.masa) / (distancia**2)
            fuerza_total += magnitud_fuerza * r / distancia
    return fuerza_total / cuerpo.masa

# Implementación del paso Euler-Cromer para la simulación
def paso_euler_cromer(cuerpo, otros_cuerpos, dt):
    aceleracion = aceleracion_gravitacional(cuerpo, otros_cuerpos)
    cuerpo.velocidad += dt * aceleracion
    cuerpo.posicion += dt * cuerpo.velocidad
    cuerpo.posiciones.append(cuerpo.posicion.copy())

# Simular el sistema solar
def simular_sistema_solar(cuerpos_celestes, num_pasos, dt):
    for paso in range(num_pasos):
        for cuerpo in cuerpos_celestes:
            otros_cuerpos = [otro for otro in cuerpos_celestes if otro != cuerpo]
            paso_euler_cromer(cuerpo, otros_cuerpos, dt)

# Visualizar las órbitas de los cuerpos celestes
def visualizar_orbitas(cuerpos_celestes):
    figura = plt.figure(figsize=(10, 8))
    eje = figura.add_subplot(111, projection='3d')

    for cuerpo in cuerpos_celestes:
        posiciones = np.array(cuerpo.posiciones)
        eje.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2], label=cuerpo.nombre)

    eje.set_xlabel('X (m)')
    eje.set_ylabel('Y (m)')
    eje.set_zlabel('Z (m)')
    eje.set_title('Órbitas del Sistema Solar')
    eje.legend()

    plt.show()

# Datos de los planetas proporcionados por el usuario
datos_cuerpos_celestes = {
  "Mercurio": {"mass": 3.285 * (10**23), "semi_major_axis": 0.3871 * 1.496e11, "orbital_velocity": 47.9 * 1000},
    "Venus": {"mass": 4.867 * (10**24), "semi_major_axis": 0.7233 * 1.496e11, "orbital_velocity": 35.0 * 1000},
    "Tierra": {"mass": 5.972 * (10**24), "semi_major_axis": 1.000 * 1.496e11, "orbital_velocity": 29.8 * 1000},
    "Marte": {"mass": 6.39 * (10**23), "semi_major_axis": 1.5273 * 1.496e11, "orbital_velocity": 24.1 * 1000},
    "Júpiter": {"mass": 1.898 * (10**27), "semi_major_axis": 5.2028 * 1.496e11, "orbital_velocity": 13.1 * 1000},
    "Saturno": {"mass": 5.683 * (10**26), "semi_major_axis": 9.5388 * 1.496e11, "orbital_velocity": 9.6 * 1000},
    "Urano": {"mass": 8.681 * (10**25), "semi_major_axis": 19.1914 * 1.496e11, "orbital_velocity": 6.8 * 1000},
    "Neptuno": {"mass": 1.024 * (10**26), "semi_major_axis": 30.0611 * 1.496e11, "orbital_velocity": 5.4 * 1000}
}


# Crear los objetos CuerpoCeleste
cuerpos_celestes = []
for nombre, datos in datos_cuerpos_celestes.items():
    cuerpo = CuerpoCeleste(nombre, datos["mass"], [datos["semi_major_axis"], 0.0, 0.0], [0.0, datos["orbital_velocity"], 0.0])
    cuerpos_celestes.append(cuerpo)
    
# Añadir la Super Gigante Roja como una estrella pasajera
masa_super_gigante_roja = 3.978 * (10**31)  # Masa aproximada
posicion_inicial_super_gigante_roja = [8.0 * 1.496e12, 0.0, 2.0 * 1.496e12]  # 8 UA en X, 2 UA en Z
velocidad_super_gigante_roja = [-7.0 * 1000, 0.0, 0.0]  # Movimiento hacia el negativo del eje X
super_gigante_roja = CuerpoCeleste("Super Gigante Roja", masa_super_gigante_roja, posicion_inicial_super_gigante_roja, velocidad_super_gigante_roja)
cuerpos_celestes.append(super_gigante_roja)

# Asumiendo que el Sol está en el origen y no se mueve
sol = CuerpoCeleste("Sol", 1.989 * (10**30), [0, 0, 0], [0, 0, 0])
cuerpos_celestes.insert(0, sol)

# Parámetros de la simulación
dt = 86400  # Un día en segundos
num_pasos = 365 * 10  # 10 años

# Realizar la simulación
simular_sistema_solar(cuerpos_celestes, num_pasos, dt)

# Visualizar las órbitas
visualizar_orbitas(cuerpos_celestes)

