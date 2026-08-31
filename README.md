# Kikin-Lab

Plantilla base del curso de Minería de Datos

**Kikin Lab**
**ENES Morelia, UNAM**

## Sobre el proyecto

## Reglas del desarrollo

- Toda la lógica de los algoritmos debe implementarse manualmente por el alumno dentro de su subpaquete correspondiente en `mintic/`.
- La única librería numérica permitida para los cálculos del algoritmo es **NumPy**. No está permitido usar `scikit-learn`, `scipy` u otras librerías que ya implementen el algoritmo asignado.
- `pandas` se permite únicamente para la carga y manipulación inicial de datos (lectura de CSV, por ejemplo).
- `matplotlib` se permite para la visualización de resultados.

## Estructura del repositorio

```
.
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── data/
│   └── sample_dataset.csv
└── mintic/
    ├── __init__.py
    ├── eda/
    │   └── __init__.py
    ├── ensemble/
    │   └── __init__.py
    ├── kmeans/
    │   └── __init__.py
    ├── dbscan/
    │   └── __init__.py
    ├── apriori/
    │   └── __init__.py
    └── pca/
        └── __init__.py
```
