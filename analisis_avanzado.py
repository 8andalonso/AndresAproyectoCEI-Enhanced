"""
ANÁLISIS AVANZADO - Andres Alonso CEI
Análisis estadísticos avanzados y segmentación de datos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# ANÁLISIS AVANZADOS
# ============================================================================

class AdvancedAnalyzer:
    """Análisis estadísticos avanzados de datos de mortalidad."""

    def __init__(self, df_clean, disease_mapping=None):
        """Inicializar con dataframe limpio."""
        self.df = df_clean.copy()
        self.disease_mapping = disease_mapping or {}
        self.disease_cols = [col for col in self.df.columns if col.startswith('por_')]

    def normalize_by_population(self, population_df=None):
        """Normalizar tasas por población (si se proporciona)."""
        if population_df is None:
            print("⚠️  Sin datos de población. Use normalizacion relativa.")
            return None

        # Dividir por población para obtener tasas per cápita
        result = self.df.copy()
        for col in self.disease_cols:
            result[col + '_per_capita'] = result[col] / (population_df[col] / 100000)

        return result

    def ranking_dinamico(self, enfermedad, años_comparar=10):
        """Analizar cambio en ranking de un país a lo largo del tiempo."""
        disease_col = [col for col in self.disease_cols
                      if self.disease_mapping.get(col, '').lower() == enfermedad.lower()]

        if not disease_col:
            return None

        disease_col = disease_col[0]

        # Primeros N años vs últimos N años
        first_years = self.df[self.df['año'] <= self.df['año'].min() + años_comparar]
        last_years = self.df[self.df['año'] >= self.df['año'].max() - años_comparar]

        ranking_inicio = first_years.groupby('pais')[disease_col].sum().sort_values(ascending=False)
        ranking_final = last_years.groupby('pais')[disease_col].sum().sort_values(ascending=False)

        # Calcular cambio en posición
        cambios = pd.DataFrame({
            'posicion_inicio': ranking_inicio.rank(ascending=False),
            'posicion_final': ranking_final.rank(ascending=False),
            'muertes_inicio': ranking_inicio,
            'muertes_final': ranking_final
        })

        cambios['cambio_posicion'] = cambios['posicion_inicio'] - cambios['posicion_final']
        cambios['cambio_muertes'] = cambios['muertes_final'] - cambios['muertes_inicio']

        return cambios.sort_values('cambio_posicion', ascending=False)

    def analisis_desigualdad(self, enfermedad):
        """Analizar desigualdad en mortalidad (Gini, Lorenz)."""
        disease_col = [col for col in self.disease_cols
                      if self.disease_mapping.get(col, '').lower() == enfermedad.lower()]

        if not disease_col:
            return None

        disease_col = disease_col[0]
        totales = self.df.groupby('pais')[disease_col].sum().sort_values(ascending=False)

        # Calcular Gini
        cumsum = np.cumsum(totales.values)
        n = len(totales)
        gini = (2 * np.sum(np.arange(1, n+1) * totales.values)) / (n * np.sum(totales.values)) - (n + 1) / n

        return {
            'gini': gini,
            'desigualdad': 'Alta' if gini > 0.6 else 'Media' if gini > 0.4 else 'Baja',
            'top_3_porcentaje': (totales.head(3).sum() / totales.sum() * 100),
            'top_10_porcentaje': (totales.head(10).sum() / totales.sum() * 100)
        }

    def identificar_outliers(self, enfermedad, metodo='iqr'):
        """Identificar países outliers en una enfermedad."""
        disease_col = [col for col in self.disease_cols
                      if self.disease_mapping.get(col, '').lower() == enfermedad.lower()]

        if not disease_col:
            return None

        disease_col = disease_col[0]
        datos = self.df.groupby('pais')[disease_col].sum()

        if metodo == 'iqr':
            Q1 = datos.quantile(0.25)
            Q3 = datos.quantile(0.75)
            IQR = Q3 - Q1

            outliers = datos[(datos < Q1 - 1.5*IQR) | (datos > Q3 + 1.5*IQR)]
        else:  # z-score
            z_scores = np.abs(stats.zscore(datos))
            outliers = datos[z_scores > 3]

        return outliers.sort_values(ascending=False)

    def clustering_paises(self, n_clusters=5, metodo='kmeans'):
        """Segmentar países por perfil de enfermedades."""
        # Preparar datos
        totales_por_pais = self.df.groupby('pais')[self.disease_cols].sum()

        # Normalizar
        scaler = StandardScaler()
        datos_normalizados = scaler.fit_transform(totales_por_pais)

        if metodo == 'kmeans':
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(datos_normalizados)
        else:  # hierarchical
            linkage_matrix = linkage(datos_normalizados, method='ward')
            # Aquí normalmente usarías fcluster, pero KMeans es más simple
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(datos_normalizados)

        resultado = pd.DataFrame({
            'pais': totales_por_pais.index,
            'cluster': clusters
        }).sort_values('cluster')

        return resultado, kmeans

    def analisis_estacionalidad_temporal(self, enfermedad):
        """Analizar si hay patrones temporales en la enfermedad."""
        disease_col = [col for col in self.disease_cols
                      if self.disease_mapping.get(col, '').lower() == enfermedad.lower()]

        if not disease_col:
            return None

        disease_col = disease_col[0]

        # Tendencia global
        temporal = self.df.groupby('año')[disease_col].sum()

        # Análisis Fourier para detectar ciclos
        from scipy.fft import fft

        # FFT para detectar frecuencias dominantes
        fft_values = fft(temporal.values - temporal.values.mean())
        power = np.abs(fft_values)**2
        freq = np.fft.fftfreq(len(temporal))

        # Top frecuencias (excluyendo DC)
        top_freq_idx = np.argsort(power)[-3:][::-1]

        return {
            'tendencia': temporal,
            'top_frecuencias': freq[top_freq_idx],
            'power': power[top_freq_idx],
            'periodograma': pd.DataFrame({
                'frecuencia': freq[top_freq_idx],
                'poder': power[top_freq_idx]
            })
        }

    def proyeccion_simple(self, enfermedad, años_futuros=5):
        """Proyección simple basada en tendencia lineal."""
        disease_col = [col for col in self.disease_cols
                      if self.disease_mapping.get(col, '').lower() == enfermedad.lower()]

        if not disease_col:
            return None

        disease_col = disease_col[0]

        temporal = self.df.groupby('año')[disease_col].sum()

        # Regresión lineal
        x = np.array(temporal.index).reshape(-1, 1)
        y = temporal.values

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(x, y)

        # Proyectar
        años_futuros_arr = np.array(range(temporal.index.max() + 1,
                                         temporal.index.max() + años_futuros + 1)).reshape(-1, 1)
        proyecciones = model.predict(años_futuros_arr)

        return pd.DataFrame({
            'año': años_futuros_arr.flatten(),
            'proyeccion': proyecciones,
            'intervalo_confianza_bajo': proyecciones * 0.9,
            'intervalo_confianza_alto': proyecciones * 1.1
        })

    def coeficiente_variacion(self):
        """Calcular variabilidad de enfermedades."""
        totales = self.df.groupby('pais')[self.disease_cols].sum()
        cv = (totales.std() / totales.mean()) * 100

        return cv.sort_values(ascending=False).head(20)


# ============================================================================
# FUNCIONES DE VISUALIZACIÓN AVANZADA
# ============================================================================

def plot_desigualdad_lorenz(analyzer, enfermedad):
    """Curva de Lorenz para visualizar desigualdad."""
    disease_col = [col for col in analyzer.disease_cols
                  if analyzer.disease_mapping.get(col, '').lower() == enfermedad.lower()]

    if not disease_col:
        return None

    disease_col = disease_col[0]
    totales = analyzer.df.groupby('pais')[disease_col].sum().sort_values(ascending=False)

    # Calcular Lorenz
    cumsum_valores = np.cumsum(totales.values)
    cumsum_paises = np.arange(1, len(totales) + 1)

    # Normalizar
    lorenz = cumsum_valores / cumsum_valores[-1]
    igualdad = cumsum_paises / len(totales)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(igualdad, lorenz, 'b-', linewidth=2.5, label='Curva de Lorenz')
    ax.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Igualdad Perfecta')

    ax.fill_between(igualdad, lorenz, igualdad, alpha=0.3)

    ax.set_xlabel('Proporción Acumulada de Países', fontsize=12, fontweight='bold')
    ax.set_ylabel('Proporción Acumulada de Muertes', fontsize=12, fontweight='bold')
    ax.set_title(f'Curva de Lorenz: {analyzer.disease_mapping.get(disease_col)}',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    return fig


def plot_clusters(analyzer, n_clusters=5):
    """Visualizar clusters de países."""
    totales_por_pais = analyzer.df.groupby('pais')[analyzer.disease_cols].sum()
    scaler = StandardScaler()
    datos_normalizados = scaler.fit_transform(totales_por_pais)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(datos_normalizados)

    # PCA para visualización 2D
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    datos_2d = pca.fit_transform(datos_normalizados)

    fig, ax = plt.subplots(figsize=(12, 8))

    colores = plt.cm.Set3(np.linspace(0, 1, n_clusters))
    for i in range(n_clusters):
        mask = clusters == i
        ax.scatter(datos_2d[mask, 0], datos_2d[mask, 1],
                  c=[colores[i]], label=f'Cluster {i+1}', s=100, alpha=0.6)

    # Centroides
    centroides_2d = pca.transform(kmeans.cluster_centers_)
    ax.scatter(centroides_2d[:, 0], centroides_2d[:, 1],
              c='red', marker='X', s=300, edgecolors='black', linewidth=2, label='Centroides')

    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} varianza)',
                 fontsize=11, fontweight='bold')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} varianza)',
                 fontsize=11, fontweight='bold')
    ax.set_title('Segmentación de Países por Perfil de Enfermedades',
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    return fig


def plot_ranking_dinamico(cambios_df):
    """Visualizar cambios en ranking."""
    top_cambios = pd.concat([
        cambios_df.head(10),
        cambios_df.tail(10)
    ])

    fig, ax = plt.subplots(figsize=(12, 8))

    colores = ['green' if x > 0 else 'red' for x in top_cambios['cambio_posicion']]
    barras = ax.barh(range(len(top_cambios)), top_cambios['cambio_posicion'], color=colores, alpha=0.7)

    ax.set_yticks(range(len(top_cambios)))
    ax.set_yticklabels(top_cambios.index, fontsize=9)
    ax.set_xlabel('Cambio en Posición (+ = Mejora, - = Empeora)', fontsize=11, fontweight='bold')
    ax.set_title('Top Cambios en Ranking de Países', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(True, alpha=0.3, axis='x')

    return fig


if __name__ == "__main__":
    print("Módulo de análisis avanzado cargado correctamente")
    print("Funciones disponibles:")
    print("  - normalize_by_population()")
    print("  - ranking_dinamico()")
    print("  - analisis_desigualdad()")
    print("  - identificar_outliers()")
    print("  - clustering_paises()")
    print("  - analisis_estacionalidad_temporal()")
    print("  - proyeccion_simple()")
    print("  - coeficiente_variacion()")
