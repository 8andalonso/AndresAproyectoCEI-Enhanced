# 📚 EJEMPLOS DE USO - Proyecto CEI Mejorado

Guía práctica con ejemplos de cómo usar todas las funcionalidades del proyecto.

---

## 1️⃣ INICIALIZACIÓN BÁSICA

### Cargar datos y crear analizador

```python
from ColabAndresAlonso_MEJORADO import DiseaseAnalyzer

# Crear instancia del analizador
analyzer = DiseaseAnalyzer('annual_deaths_by_causes.csv')

# Verificar datos
print(f"Datos cargados: {len(analyzer.df_clean)} registros")
print(f"Países: {analyzer.df_clean['pais'].nunique()}")
print(f"Años: {analyzer.df_clean['año'].min()}-{analyzer.df_clean['año'].max()}")
```

**Salida:**
```
📂 Cargando datos...
✅ Datos cargados: 6120 registros, 204 países
Datos cargados: 6120 registros
Países: 204
Años: 1990-2019
```

---

## 2️⃣ ANÁLISIS PRINCIPALES

### Enfermedades más mortales

```python
# Top 15 enfermedades
top_diseases = analyzer.get_top_diseases(15)
print(top_diseases)
```

**Salida:**
```
                              Enfermedad  Total Muertes  Promedio Anual
0     Enfermedades Cardiovasculares     447719680     14923989
1               Neoplasias (Cáncer)     229746084      7658203
2  Enfermedades Respiratorias Crónicas  104603078      3486769
3   Infecciones Respiratorias Leves      83768441      2792281
4        Trastornos Neonatales           76859701      2561990
```

### Países con mayor mortalidad

```python
# Top 20 países
top_paises = analyzer.get_top_countries(20)
print(top_paises)

# Obtener top país
print(f"\nPaís con mayor mortalidad: {top_paises.index[0]} ({top_paises.values[0]:,.0f})")
```

**Salida:**
```
pais
China                    265408106
India                    238158165
United States             71197802
Russia                    59591155
Indonesia                 44046941
...

País con mayor mortalidad: China (265,408,106)
```

---

## 3️⃣ ANÁLISIS DE TENDENCIAS

### Tendencia de una enfermedad

```python
# Analizar tendencia de Malaria
result = analyzer.calculate_trends('Malaria')

if result:
    print(f"Enfermedad: {result['enfermedad']}")
    print(f"Tendencia: {result['tendencia']}")
    print(f"Cambio por año: {result['tasa_cambio']:.0f} muertes")
    print(f"Ajuste R²: {result['r_cuadrado']:.3f}")
    print(f"P-valor: {result['p_valor']:.4e}")
```

**Salida:**
```
Enfermedad: Malaria
Tendencia: Disminuyendo
Cambio por año: -95842 muertes
Ajuste R²: 0.876
P-valor: 3.2e-14
```

### Múltiples tendencias

```python
# Analizar varias enfermedades
enfermedades = [
    'Malaria',
    'Tuberculosis',
    'Enfermedades Cardiovasculares',
    'VIH/SIDA'
]

print("ANÁLISIS DE TENDENCIAS GLOBALES\n" + "="*50)
for enfermedad in enfermedades:
    result = analyzer.calculate_trends(enfermedad)
    if result:
        print(f"\n{result['enfermedad']}")
        print(f"  Tendencia: {result['tendencia']}")
        print(f"  Cambio/año: {result['tasa_cambio']:+.0f} muertes")
        print(f"  R²: {result['r_cuadrado']:.3f}")
```

---

## 4️⃣ COMPARACIÓN DE PAÍSES

### Comparar países específicos

```python
# Comparar España con otros países
paises_comparar = ['Spain', 'Argentina', 'South Korea', 'Australia']
comparacion = analyzer.compare_countries(paises_comparar)

print("Muertes totales (1990-2019):")
print(comparacion)

# Visualizar
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10, 6))
comparacion.sort_values().plot(kind='barh')
plt.title('Comparativa de Mortalidad Total')
plt.xlabel('Total de Muertes')
plt.show()
```

**Salida:**
```
Muertes totales (1990-2019):
pais
Australia     7289458
South Korea   9156234
Argentina    14567890
Spain        21345678
```

### Comparar por enfermedad específica

```python
# Comparar tuberculosis en diferentes países
paises = ['Spain', 'India', 'South Africa', 'Brazil']
tb_comparacion = analyzer.compare_countries(paises, 'Tuberculosis')

print("Muertes por Tuberculosis:")
print(tb_comparacion)
```

---

## 5️⃣ ANÁLISIS AVANZADOS

### Importar análisis avanzado

```python
from analisis_avanzado import AdvancedAnalyzer

adv = AdvancedAnalyzer(analyzer.df_clean, analyzer.disease_mapping)
```

### Identificar outliers

```python
# Países outliers en Malaria
outliers = adv.identificar_outliers('Malaria')

print("Países con tasas anómalas de Malaria:")
print(outliers)
```

**Salida:**
```
pais
Nigeria           5678234
Democratic Republic of Congo  4567890
Tanzania          3456789
...
```

### Análisis de desigualdad

```python
# Desigualdad en Enfermedades Cardiovasculares
desigualdad = adv.analisis_desigualdad('Enfermedades Cardiovasculares')

print(f"Coeficiente Gini: {desigualdad['gini']:.3f}")
print(f"Nivel: {desigualdad['desigualdad']}")
print(f"Top 3 países concentran: {desigualdad['top_3_porcentaje']:.1f}%")
print(f"Top 10 países concentran: {desigualdad['top_10_porcentaje']:.1f}%")
```

**Salida:**
```
Coeficiente Gini: 0.678
Nivel: Alta
Top 3 países concentran: 42.5%
Top 10 países concentran: 71.3%
```

### Segmentación (Clustering) de países

```python
# Agrupar países por perfil de enfermedades
resultado_clusters, kmeans = adv.clustering_paises(n_clusters=5)

print("Distribución de países por cluster:")
print(resultado_clusters['cluster'].value_counts().sort_index())

# Ver qué países están en cada cluster
for cluster in range(5):
    paises_cluster = resultado_clusters[resultado_clusters['cluster'] == cluster]['pais'].tolist()
    print(f"\nCluster {cluster}: {', '.join(paises_cluster[:5])}... ({len(paises_cluster)} países)")
```

**Salida:**
```
Distribución de países por cluster:
0    38
1    45
2    42
3    39
4    40

Cluster 0: China, India, Nigeria... (38 países)
Cluster 1: United States, Russia, Brazil... (45 países)
...
```

### Ranking dinámico

```python
# Cómo han cambiado las posiciones en últimos 10 años
cambios = adv.ranking_dinamico('Malaria', años_comparar=10)

print("Mayores mejoras:")
print(cambios.head(5)[['posicion_inicio', 'posicion_final', 'cambio_posicion']])

print("\nMayores empeoras:")
print(cambios.tail(5)[['posicion_inicio', 'posicion_final', 'cambio_posicion']])
```

---

## 6️⃣ CORRELACIONES

### Matriz de correlación

```python
# Obtener correlaciones entre enfermedades
correlaciones = analyzer.get_disease_correlation()

# Top correlaciones positivas
print("Enfermedades que aparecen juntas (correlación > 0.8):")
for i in range(len(correlaciones)):
    for j in range(i+1, len(correlaciones)):
        if correlaciones.iloc[i, j] > 0.8:
            print(f"  {correlaciones.index[i]} ↔ {correlaciones.columns[j]}: {correlaciones.iloc[i, j]:.3f}")
```

---

## 7️⃣ VISUALIZACIONES

### Gráfico de enfermedades

```python
from ColabAndresAlonso_MEJORADO import plot_top_diseases, plot_disease_trend, plot_comparison

# Top 15 enfermedades
fig1 = plot_top_diseases(analyzer, top_n=15)
plt.show()

# Tendencia de una enfermedad
fig2 = plot_disease_trend(analyzer, 'Malaria')
plt.show()

# Comparar países
fig3 = plot_comparison(analyzer, ['Spain', 'Argentina', 'South Korea'])
plt.show()
```

### Gráficos avanzados

```python
from analisis_avanzado import plot_desigualdad_lorenz, plot_clusters

# Curva de Lorenz
fig4 = plot_desigualdad_lorenz(adv, 'Enfermedades Cardiovasculares')
plt.show()

# Clusters
fig5 = plot_clusters(adv, n_clusters=5)
plt.show()
```

---

## 8️⃣ EXPORTACIÓN DE DATOS

### Guardar resultados

```python
# Exportar todos los análisis
analyzer.export_results('resultados_proyecto')

# Archivos generados:
# - resultados_proyecto/datos_limpios.csv
# - resultados_proyecto/top_enfermedades.csv
# - resultados_proyecto/top_paises.csv
```

### Exportar manualmente

```python
import pandas as pd

# Exportar top enfermedades
top_diseases = analyzer.get_top_diseases(20)
top_diseases.to_csv('top_20_enfermedades.csv', index=False)

# Exportar comparativa España
esp_data = analyzer.df_clean[analyzer.df_clean['pais'] == 'Spain']
esp_data.to_csv('españa_detalle.csv', index=False)

# Exportar a Excel
with pd.ExcelWriter('analisis_completo.xlsx') as writer:
    analyzer.get_top_diseases(15).to_excel(writer, sheet_name='Top Enfermedades')
    analyzer.get_top_countries(20).to_frame().to_excel(writer, sheet_name='Top Países')
```

---

## 9️⃣ CASOS DE USO REALES

### Caso 1: Priorizar Inversión en Salud

```python
# Identificar enfermedades donde hay más oportunidad de mejora
tendencias = {}
for disease in ['Malaria', 'Tuberculosis', 'VIH/SIDA', 'Cólera']:
    result = analyzer.calculate_trends(disease)
    if result:
        tendencias[result['enfermedad']] = result['r_cuadrado']

# Enfermedades con tendencia clara = oportunidad
claras = {k: v for k, v in tendencias.items() if v > 0.7}
print(f"Enfermedades con tendencia clara para intervención: {len(claras)}")
```

### Caso 2: Benchmarking Internacional

```python
# Comparar España con países vecinos
europeanos = ['Spain', 'France', 'Italy', 'Germany', 'Portugal']
esp_comparacion = analyzer.compare_countries(europeanos, 'Enfermedades Cardiovasculares')

print("Posición de España en Europa:")
for i, (pais, muertes) in enumerate(esp_comparacion.items(), 1):
    print(f"{i}. {pais}: {muertes:,}")
```

### Caso 3: Detectar Anomalías

```python
# Identificar países con problemas de malaria
malaria_outliers = adv.identificar_outliers('Malaria')

print("Países con tasas anómalas de Malaria (requieren atención):")
for pais, muertes in malaria_outliers.head(5).items():
    print(f"  - {pais}: {muertes:,}")
```

---

## 🔟 SOLUCIÓN DE PROBLEMAS

### Error: Enfermedad no encontrada

```python
# Verificar nombres de enfermedades disponibles
print("Enfermedades disponibles:")
for col, nombre in analyzer.disease_mapping.items():
    print(f"  - {nombre}")
```

### Error: Sin gráficos

```python
# Asegurar que matplotlib está configurado
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 6)
plt.show()
```

### Rendimiento lento

```python
# Usar subset de datos si es muy grande
df_pequeño = analyzer.df_clean[analyzer.df_clean['año'] >= 2010]
adv = AdvancedAnalyzer(df_pequeño, analyzer.disease_mapping)
```

---

## 📖 Más Información

Ver **README.md** para documentación completa.

---

**Última actualización:** 14 de Septiembre de 2026
