"""
ANÁLISIS GLOBAL DE MUERTES POR ENFERMEDADES (1990-2019)
Versión Mejorada - Andres Alonso CEI

Este módulo proporciona herramientas completas para analizar y visualizar
datos de mortalidad global por diferentes causas de enfermedad.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

DISEASE_MAPPING = {
    'por_meningitis': 'Meningitis',
    'por_alzheimer': 'Alzheimer',
    'por_parkinson': 'Parkinson',
    'por_deficiencia_nutricional': 'Deficiencia Nutricional',
    'por_malaria': 'Malaria',
    'por_ahogo': 'Ahogamiento',
    'por_violencia_interpersonal': 'Violencia Interpersonal',
    'por_trastornos_maternos': 'Trastornos Maternos',
    'por_vih_sida': 'VIH/SIDA',
    'por_uso_drogas': 'Uso de Drogas',
    'por_tuberculosis': 'Tuberculosis',
    'por_enfermedades_cardiovasculares': 'Enfermedades Cardiovasculares',
    'por_infecciones_respiratorias_leves': 'Infecciones Respiratorias Leves',
    'por_trastornos_neonatales': 'Trastornos Neonatales',
    'por_uso_alcohol': 'Uso de Alcohol',
    'por_autolesiones': 'Autolesiones',
    'por_fuerzas_de_la_naturaleza': 'Fuerzas de la Naturaleza',
    'por_enfermedades__diarreicas': 'Enfermedades Diarreicas',
    'por_exposicion_al_calor_o_frio': 'Exposición a Calor/Frío',
    'por_neoplasias': 'Neoplasias (Cáncer)',
    'por_guerras_terrorismo': 'Guerras y Terrorismo',
    'por_diabetes_mellitus': 'Diabetes Mellitus',
    'por_enfermerdad_renal_cronica': 'Enfermedad Renal Crónica',
    'por_envenenamiento': 'Envenenamiento',
    'por_desnutricion': 'Desnutrición',
    'por_accidentes_de_transito': 'Accidentes de Tránsito',
    'por_enfermerdades_respirtatorias_cronicas': 'Enfermedades Respiratorias Crónicas',
    'por_enfermedades_linfaticas_cronicas': 'Enfermedades Linfáticas Crónicas',
    'por_enfermedades_digestivas': 'Enfermedades Digestivas',
    'por_sustancias_de_calor_fuego': 'Quemaduras',
    'por_hepatitis_aguda': 'Hepatitis Aguda'
}

CONTINENTS = {
    'Afghanistan': 'Asia', 'Albania': 'Europa', 'Algeria': 'África',
    'Argentina': 'América del Sur', 'Australia': 'Oceanía',
    'Austria': 'Europa', 'Bangladesh': 'Asia', 'Belgium': 'Europa',
    'Brazil': 'América del Sur', 'Canada': 'América del Norte',
    'China': 'Asia', 'Colombia': 'América del Sur', 'Denmark': 'Europa',
    'Egypt': 'África', 'France': 'Europa', 'Germany': 'Europa',
    'India': 'Asia', 'Indonesia': 'Asia', 'Italy': 'Europa',
    'Japan': 'Asia', 'Mexico': 'América del Norte', 'Nigeria': 'África',
    'Pakistan': 'Asia', 'Russia': 'Asia', 'South Africa': 'África',
    'South Korea': 'Asia', 'Spain': 'Europa', 'United States': 'América del Norte',
    'United Kingdom': 'Europa', 'Vietnam': 'Asia'
}

# ============================================================================
# CLASE PRINCIPAL DE ANÁLISIS
# ============================================================================

class DiseaseAnalyzer:
    """Analizador completo de datos de mortalidad por enfermedades."""

    def __init__(self, csv_path):
        """Inicializar el analizador con datos."""
        self.df_raw = None
        self.df_clean = None
        self.df_normalized = None
        self.load_and_clean_data(csv_path)

    def load_and_clean_data(self, csv_path):
        """Cargar y limpiar los datos."""
        print("📂 Cargando datos...")
        self.df_raw = pd.read_csv(csv_path)

        # Eliminar columnas innecesarias
        self.df_raw = self.df_raw.drop(columns=['code', 'terrorism'], errors='ignore')

        # Eliminar agregaciones (organizaciones, no países)
        unwanted = ['World', 'G20', 'World Bank', 'WHO', 'OECD', 'Region of',
                   'United States Virgin Islands', 'Northern Mariana Islands']
        mask = ~self.df_raw['country'].str.contains('|'.join(unwanted), case=False, na=False)
        self.df_raw = self.df_raw[mask]

        # Eliminar nulos
        self.df_raw = self.df_raw.dropna()

        # Convertir floats a int
        float_cols = self.df_raw.select_dtypes(include=['float64']).columns
        self.df_raw[float_cols] = self.df_raw[float_cols].astype('int64')

        # Renombrar columnas en español
        self.df_raw = self.df_raw.rename(columns={
            'country': 'pais',
            'year': 'año'
        })

        self.df_clean = self.df_raw.copy()
        self.df_clean['pais'] = self.df_clean['pais'].astype('category')

        print(f"✅ Datos cargados: {len(self.df_clean)} registros, {self.df_clean['pais'].nunique()} países")

    def get_top_diseases(self, top_n=15):
        """Obtener las enfermedades más mortales."""
        disease_cols = [col for col in self.df_clean.columns if col.startswith('por_')]
        totals = self.df_clean[disease_cols].sum().sort_values(ascending=False)

        result = pd.DataFrame({
            'Enfermedad': [DISEASE_MAPPING.get(col, col) for col in totals.index[:top_n]],
            'Total Muertes': totals.values[:top_n],
            'Promedio Anual': (totals.values[:top_n] / 30).astype(int)
        })

        return result

    def get_top_countries(self, top_n=20, disease=None):
        """Obtener los países con más muertes."""
        if disease:
            disease_col = [col for col in self.df_clean.columns
                          if DISEASE_MAPPING.get(col, '').lower() == disease.lower()]
            if not disease_col:
                print(f"⚠️  Enfermedad '{disease}' no encontrada")
                return None
            disease_col = disease_col[0]
            grouped = self.df_clean.groupby('pais')[disease_col].sum()
        else:
            disease_cols = [col for col in self.df_clean.columns if col.startswith('por_')]
            grouped = self.df_clean.groupby('pais')[disease_cols].sum().sum(axis=1)

        return grouped.sort_values(ascending=False).head(top_n)

    def calculate_trends(self, disease, paises=None):
        """Calcular tendencia de una enfermedad."""
        disease_col = [col for col in self.df_clean.columns
                      if DISEASE_MAPPING.get(col, '').lower() == disease.lower()]

        if not disease_col:
            print(f"⚠️  Enfermedad '{disease}' no encontrada")
            return None

        disease_col = disease_col[0]

        if paises:
            df_filtered = self.df_clean[self.df_clean['pais'].isin(paises)]
        else:
            df_filtered = self.df_clean

        # Calcular cambio porcentual
        grouped = df_filtered.groupby('año')[disease_col].sum()
        pct_change = grouped.pct_change() * 100

        # Regresión lineal
        x = np.array(grouped.index).reshape(-1, 1)
        y = grouped.values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x.flatten(), y)

        return {
            'enfermedad': DISEASE_MAPPING.get(disease_col),
            'datos': grouped,
            'cambio_porcentual': pct_change,
            'tendencia': 'Aumentando' if slope > 0 else 'Disminuyendo',
            'tasa_cambio': slope,
            'r_cuadrado': r_value**2,
            'p_valor': p_value
        }

    def compare_countries(self, paises, disease=None):
        """Comparar países específicos."""
        df_filtered = self.df_clean[self.df_clean['pais'].isin(paises)]

        if disease:
            disease_col = [col for col in self.df_clean.columns
                          if DISEASE_MAPPING.get(col, '').lower() == disease.lower()]
            if disease_col:
                disease_col = disease_col[0]
                return df_filtered.groupby('pais')[disease_col].sum().sort_values(ascending=False)

        disease_cols = [col for col in df_filtered.columns if col.startswith('por_')]
        return df_filtered.groupby('pais')[disease_cols].sum().sum(axis=1).sort_values(ascending=False)

    def get_disease_correlation(self):
        """Calcular matriz de correlación entre enfermedades."""
        disease_cols = [col for col in self.df_clean.columns if col.startswith('por_')]
        totals_by_country = self.df_clean.groupby('pais')[disease_cols].sum()
        correlation = totals_by_country.corr()

        # Renombrar columnas para mejor legibilidad
        disease_names = {col: DISEASE_MAPPING.get(col, col) for col in disease_cols}
        correlation.rename(columns=disease_names, index=disease_names, inplace=True)

        return correlation

    def export_results(self, output_dir='resultados'):
        """Exportar resultados a archivos."""
        Path(output_dir).mkdir(exist_ok=True)

        # Exportar datos limpios
        self.df_clean.to_csv(f'{output_dir}/datos_limpios.csv', index=False)

        # Top enfermedades
        self.get_top_diseases(15).to_csv(f'{output_dir}/top_enfermedades.csv', index=False)

        # Top países
        self.get_top_countries(20).to_frame().to_csv(f'{output_dir}/top_paises.csv')

        print(f"✅ Resultados exportados a {output_dir}/")


# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def plot_top_diseases(analyzer, top_n=15):
    """Gráfico de las enfermedades más mortales."""
    data = analyzer.get_top_diseases(top_n)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(range(len(data)), data['Total Muertes'], color=plt.cm.Spectral(np.linspace(0, 1, len(data))))

    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data['Enfermedad'])
    ax.set_xlabel('Total de Muertes (1990-2019)', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Enfermedades Más Mortales Globalmente', fontsize=14, fontweight='bold')

    # Agregar valores en las barras
    for i, (bar, val) in enumerate(zip(bars, data['Total Muertes'])):
        ax.text(val, i, f' {val:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    return fig


def plot_disease_trend(analyzer, disease, paises=None):
    """Gráfico de tendencia de una enfermedad."""
    result = analyzer.calculate_trends(disease, paises)

    if result is None:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))

    datos = result['datos']
    ax.plot(datos.index, datos.values, marker='o', linewidth=2.5, markersize=6, label='Datos Reales')

    # Línea de tendencia
    z = np.polyfit(datos.index, datos.values, 1)
    p = np.poly1d(z)
    ax.plot(datos.index, p(datos.index), "--", color='red', linewidth=2, label='Tendencia Linear', alpha=0.8)

    ax.set_xlabel('Año', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de Muertes', fontsize=12, fontweight='bold')
    ax.set_title(f'Evolución: {result["enfermedad"]} (R² = {result["r_cuadrado"]:.3f})',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Anotación con estadísticas
    tendencia_text = f"Tendencia: {result['tendencia']}\nCambio/año: {result['tasa_cambio']:.0f} muertes"
    ax.text(0.02, 0.98, tendencia_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    return fig


def plot_top_countries(analyzer, top_n=20):
    """Gráfico de los países con más muertes."""
    data = analyzer.get_top_countries(top_n)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(range(len(data)), data.values, color=plt.cm.viridis(np.linspace(0, 1, len(data))))

    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index)
    ax.set_xlabel('Total de Muertes (1990-2019)', fontsize=12, fontweight='bold')
    ax.set_title('Top 20 Países con Mayor Mortalidad', fontsize=14, fontweight='bold')

    for i, (bar, val) in enumerate(zip(bars, data.values)):
        ax.text(val, i, f' {val:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    return fig


def plot_comparison(analyzer, paises, disease=None):
    """Comparar evolución de países específicos."""
    disease_cols = [col for col in analyzer.df_clean.columns if col.startswith('por_')]

    if disease:
        disease_col = [col for col in disease_cols
                      if DISEASE_MAPPING.get(col, '').lower() == disease.lower()]
        if disease_col:
            disease_cols = disease_col

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, disease_col in enumerate(disease_cols[:4]):
        ax = axes[idx]
        for pais in paises:
            data = analyzer.df_clean[analyzer.df_clean['pais'] == pais].groupby('año')[disease_col].sum()
            ax.plot(data.index, data.values, marker='o', label=pais, linewidth=2)

        disease_name = DISEASE_MAPPING.get(disease_col, disease_col)
        ax.set_title(f'{disease_name}', fontweight='bold')
        ax.set_xlabel('Año')
        ax.set_ylabel('Muertes')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_correlation_heatmap(analyzer):
    """Matriz de correlación de enfermedades."""
    corr = analyzer.get_disease_correlation()

    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(corr, cmap='coolwarm', center=0, square=True, ax=ax,
                cbar_kws={"shrink": 0.8}, vmin=-1, vmax=1)

    ax.set_title('Correlación entre Enfermedades', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    return fig


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Cargar datos
    analyzer = DiseaseAnalyzer('annual_deaths_by_causes.csv')

    # Mostrar top enfermedades
    print("\n" + "="*60)
    print("TOP 15 ENFERMEDADES MÁS MORTALES")
    print("="*60)
    print(analyzer.get_top_diseases(15).to_string(index=False))

    # Mostrar top países
    print("\n" + "="*60)
    print("TOP 20 PAÍSES CON MAYOR MORTALIDAD")
    print("="*60)
    print(analyzer.get_top_countries(20))

    # Analizar tendencias
    print("\n" + "="*60)
    print("ANÁLISIS DE TENDENCIAS")
    print("="*60)

    for disease in ['Enfermedades Cardiovasculares', 'Malaria', 'Tuberculosis']:
        result = analyzer.calculate_trends(disease)
        if result:
            print(f"\n{result['enfermedad']}:")
            print(f"  Tendencia: {result['tendencia']} ({result['tasa_cambio']:.0f} muertes/año)")
            print(f"  Ajuste R²: {result['r_cuadrado']:.3f}")

    # Exportar resultados
    print("\n" + "="*60)
    analyzer.export_results()
    print("="*60)
