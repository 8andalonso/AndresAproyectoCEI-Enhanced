# 📊 ANÁLISIS GLOBAL DE MUERTES POR ENFERMEDADES (1990-2019)

**Proyecto CEI - Versión Mejorada**

Análisis completo y reproducible de datos de mortalidad global por 31 categorías de enfermedades en 204 países durante 30 años.

---

## 📁 Estructura del Proyecto

```
AndresAproyectoCEI/
├── annual_deaths_by_causes.csv          # Datos brutos (1.4 MB)
├── ColabAndresAlonso_MEJORADO.py        # Módulo principal mejorado
├── ColabAndresAlonso_MEJORADO.ipynb     # Notebook ejecutable
├── analisis_avanzado.py                 # Análisis adicionales
├── requirements.txt                      # Dependencias Python
├── README.md                             # Este archivo
├── DATA ANALIST- ANDRES ALONSO.pdf      # Informe original
├── tabla.xlsx                           # Datos completos
├── top20.xlsx                           # Top 20 países
├── espana.xlsx                          # Comparativa España
└── resultados/                          # Carpeta de salida
    ├── datos_limpios.csv
    ├── top_enfermedades.csv
    └── top_paises.csv
```

---

## 📈 Dataset

- **Registros:** 6,120 (204 países × 30 años)
- **Período:** 1990-2019
- **Enfermedades:** 31 categorías principales
- **Cobertura:** Global (204 países)

**Top 5 Causas de Muerte Globales:**
1. 🫀 Enfermedades Cardiovasculares: 447.7 millones
2. 🎗️ Neoplasias (Cáncer): 229.7 millones
3. 💨 Enfermedades Respiratorias Crónicas: 104.6 millones
4. 🤧 Infecciones Respiratorias: 83.8 millones
5. 👶 Trastornos Neonatales: 76.9 millones

**Top 5 Países (Total de Muertes):**
1. 🇨🇳 China: 265.4 millones
2. 🇮🇳 India: 238.2 millones
3. 🇺🇸 Estados Unidos: 71.2 millones
4. 🇷🇺 Rusia: 59.6 millones
5. 🇮🇩 Indonesia: 44.0 millones

---

## 🚀 Instalación y Uso

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Usar el Módulo Python

```python
from ColabAndresAlonso_MEJORADO import DiseaseAnalyzer, plot_top_diseases

# Cargar datos
analyzer = DiseaseAnalyzer('annual_deaths_by_causes.csv')

# Obtener top enfermedades
print(analyzer.get_top_diseases(15))

# Obtener top países
print(analyzer.get_top_countries(20))

# Analizar tendencias
result = analyzer.calculate_trends('Malaria')
print(result)

# Comparar países
analyzer.compare_countries(['Spain', 'Argentina', 'South Korea'])

# Exportar resultados
analyzer.export_results('resultados')

# Visualizar
import matplotlib.pyplot as plt
fig = plot_top_diseases(analyzer)
plt.show()
```

### 3. Usar el Notebook Jupyter

```bash
jupyter notebook ColabAndresAlonso_MEJORADO.ipynb
```

---

## 📊 Funcionalidades Principales

### Análisis Disponibles

| Función | Descripción |
|---------|-------------|
| `get_top_diseases()` | Top N enfermedades más mortales |
| `get_top_countries()` | Top N países con mayor mortalidad |
| `calculate_trends()` | Análisis de tendencias con regresión lineal |
| `compare_countries()` | Comparar múltiples países |
| `get_disease_correlation()` | Matriz de correlación entre enfermedades |
| `export_results()` | Exportar datos procesados |

### Visualizaciones

| Función | Tipo |
|---------|------|
| `plot_top_diseases()` | Gráfico de barras horizontal |
| `plot_top_countries()` | Gráfico de barras horizontal |
| `plot_disease_trend()` | Línea con tendencia lineal |
| `plot_comparison()` | Subplots comparativos |
| `plot_correlation_heatmap()` | Mapa de calor correlaciones |

---

## 🔬 Análisis Incluidos

### Análisis Básicos ✅
- [x] Limpieza de datos y validación
- [x] Eliminación de agregaciones (regiones, organizaciones)
- [x] Conversión de tipos de datos
- [x] Estadísticas descriptivas

### Análisis Avanzados ✅
- [x] Tendencias temporales con regresión lineal
- [x] Correlación entre enfermedades
- [x] Comparativas multi-país
- [x] Cálculo de tasas de cambio
- [x] Tests estadísticos (p-value, R²)

### Por Implementar 🚀
- [ ] Análisis por continente
- [ ] Normalización por población (tasas per cápita)
- [ ] Proyecciones futuras (ARIMA, Prophet)
- [ ] Clustering de países por perfil de enfermedades
- [ ] Análisis de causalidad
- [ ] Dashboards interactivos (Plotly, Dash)

---

## 💡 Mejoras Implementadas

### vs. Versión Original

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Código** | Repetitivo, sin estructura | OOP, funciones reutilizables |
| **Análisis** | Solo gráficos básicos | Tendencias, correlaciones, tests estadísticos |
| **Documentación** | Ninguna | Docstrings, README completo |
| **Warnings** | FutureWarning pandas | Warnings eliminados |
| **Exportación** | Excel manual | Automatizada, CSV |
| **Reproducibilidad** | Baja | Alta (requirements.txt) |
| **Mantenibilidad** | Difícil | Fácil (modular) |

---

## 📊 Casos de Uso

### 1. Identificar Enfermedades Prioritarias
```python
top_diseases = analyzer.get_top_diseases(10)
# Enfoque en salud pública para las 10 más mortales
```

### 2. Analizar Progreso en Malaria
```python
result = analyzer.calculate_trends('Malaria')
# Verificar si hay disminución global
```

### 3. Comparar Política Sanitaria
```python
analyzer.compare_countries(['Spain', 'Argentina', 'Italy'], 'Tuberculosis')
# Comparar efectividad de políticas
```

### 4. Encontrar Correlaciones
```python
corr = analyzer.get_disease_correlation()
# Descubrir si ciertas enfermedades aparecen juntas
```

### 5. Análisis por Región
```python
result = analyzer.calculate_trends('Enfermedades Cardiovasculares', 
                                   paises=['Spain', 'Italy', 'France'])
# Tendencia en Europa
```

---

## 🔧 Requisitos Técnicos

- **Python:** 3.8+
- **Librerías:** pandas, numpy, matplotlib, seaborn, scipy
- **RAM:** 2+ GB recomendado
- **Disco:** 100 MB disponible
- **Sistema:** Windows, macOS, Linux

---

## 📈 Resultados Esperados

### Descubrimientos Clave

1. **Enfermedades Cardiovasculares Dominantes**
   - Responsables del 40% de todas las muertes
   - Tendencia al alza en países desarrollados

2. **Malaria Disminuyendo**
   - Reducción consistente debido a intervenciones sanitarias
   - Mejor control en última década

3. **Diferencias Geográficas Dramáticas**
   - China e India concentran 50% de muertes
   - Refleja tamaño de población

4. **Enfermedades Correlacionadas**
   - Respiratorias y cardiovasculares correlacionadas
   - Trastornos nutricionales correlacionan con infecciones

---

## 🐛 Solución de Problemas

### Error: "FileNotFoundError: annual_deaths_by_causes.csv"
```
Asegúrate que el CSV está en el mismo directorio que el script
```

### Error: "ModuleNotFoundError: pandas"
```bash
pip install -r requirements.txt
```

### Gráficos no se muestran
```python
import matplotlib.pyplot as plt
plt.show()  # Agregar después de cada plot
```

---

## 📚 Referencias

- **Datos:** Our World in Data - Global Deaths by Cause
- **Métodos:** Análisis exploratorio de datos (EDA)
- **Visualización:** matplotlib, seaborn
- **Estadística:** scipy.stats

---

## 📝 Changelog

### v2.0 (ACTUAL)
- ✅ Refactorización completa con OOP
- ✅ Análisis avanzados (tendencias, correlaciones)
- ✅ Documentación exhaustiva
- ✅ Funciones reutilizables
- ✅ Eliminación de warnings
- ✅ Tests estadísticos

### v1.0 (Original)
- Análisis básicos
- Gráficos simples
- Sin documentación

---

## 👤 Autor

**Andrés Alonso**  
Proyecto CEI - Data Analytics  
Septiembre 2026

---

## 📞 Contacto

Para preguntas o sugerencias sobre el análisis:
- Email: ahw.alonso@gmail.com

---

**Última actualización:** 14 de Septiembre de 2026
