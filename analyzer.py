"""
================================================================================
ANÁLISIS GLOBAL DE MUERTES POR ENFERMEDADES (1990-2019)
Proyecto CEI - Versión 2.0 Mejorada

DESCRIPCIÓN GENERAL:
Este módulo proporciona herramientas completas para analizar y visualizar
datos de mortalidad global por diferentes causas de enfermedad en 204 países
durante 30 años.

AUTOR: Andrés Alonso
EMAIL: ahw.alonso@gmail.com
FECHA: Septiembre 2026
VERSIÓN: 2.0 - Refactorizado a OOP

CARACTERÍSTICAS:
- Carga automática y limpieza de datos
- 15+ métodos de análisis diferentes
- Visualizaciones profesionales
- Tests estadísticos integrados
- Exportación de resultados
================================================================================
"""

# IMPORTACIONES
# ==============================================================================
# Importar librerías necesarias para análisis y visualización

import numpy as np  # Computación numérica (arrays, operaciones matemáticas)
import pandas as pd  # Manipulación de datos (DataFrames, Series)
import matplotlib.pyplot as plt  # Visualización de gráficos
import seaborn as sns  # Visualizaciones estadísticas mejoradas
from scipy import stats  # Tests estadísticos (regresión, distribuciones)
from pathlib import Path  # Manejo de rutas del filesystem
import warnings  # Para controlar advertencias

# Suprimir warnings innecesarios para salida más limpia
warnings.filterwarnings('ignore')

# CONFIGURACIÓN GLOBAL
# ==============================================================================
# Configurar estilos y colores por defecto para todos los gráficos

plt.style.use('seaborn-v0_8-darkgrid')  # Estilo de gráficos
sns.set_palette("husl")  # Paleta de colores armónica

# DICCIONARIO DE MAPEO DE ENFERMEDADES
# ==============================================================================
# Este diccionario mapea los nombres de columnas técnicos a nombres legibles
# Ejemplo: 'por_meningitis' → 'Meningitis'
# Útil para mostrar información al usuario de forma clara

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

# CLASE PRINCIPAL: ANALIZADOR DE ENFERMEDADES
# ==============================================================================
# Esta clase encapsula toda la funcionalidad de análisis
# Permite crear un objeto que carga los datos y proporciona métodos para
# realizar diferentes tipos de análisis

class DiseaseAnalyzer:
    """
    Analizador profesional de datos de mortalidad por enfermedades.

    Esta clase proporciona métodos para:
    - Cargar y limpiar datos
    - Realizar análisis descriptivos (tops, estadísticas)
    - Analizar tendencias temporales
    - Comparar países
    - Calcular correlaciones
    - Exportar resultados

    Ejemplo de uso:
    ---------------
    analyzer = DiseaseAnalyzer('annual_deaths_by_causes.csv')
    top_diseases = analyzer.get_top_diseases(15)
    print(top_diseases)
    """

    def __init__(self, csv_path):
        """
        Constructor: Inicializa el analizador y carga los datos.

        Parámetros:
        -----------
        csv_path : str
            Ruta del archivo CSV con los datos de mortalidad

        Atributos creados:
        ------------------
        self.df_raw : DataFrame
            Datos originales sin procesar
        self.df_clean : DataFrame
            Datos limpios y listos para análisis
        self.disease_mapping : dict
            Mapeo de columnas técnicas a nombres legibles
        """
        # Inicializar atributos
        self.df_raw = None
        self.df_clean = None
        self.disease_mapping = DISEASE_MAPPING

        # Cargar y limpiar datos
        self.load_and_clean_data(csv_path)

    def load_and_clean_data(self, csv_path):
        """
        Carga y limpia los datos de mortalidad.

        Pasos realizados:
        ------------------
        1. Leer archivo CSV
        2. Eliminar columnas innecesarias
        3. Filtrar agregaciones (regiones, organizaciones)
        4. Eliminar filas con valores faltantes
        5. Convertir tipos de datos
        6. Renombrar columnas al español
        7. Optimizar tipos (category para pais)

        Parámetros:
        -----------
        csv_path : str
            Ruta del archivo CSV
        """
        print("📂 Cargando datos...")

        # PASO 1: Leer archivo CSV
        # Cargar datos desde archivo CSV a un DataFrame
        self.df_raw = pd.read_csv(csv_path)

        # PASO 2: Eliminar columnas innecesarias
        # Estas columnas no nos interesan para el análisis
        self.df_raw = self.df_raw.drop(columns=['code', 'terrorism'], errors='ignore')

        # PASO 3: Filtrar agregaciones (no queremos regiones, queremos países)
        # Palabras clave que indican que no es un país real
        unwanted_keywords = ['World', 'G20', 'World Bank', 'WHO', 'OECD', 'Region of',
                           'United States Virgin Islands', 'Northern Mariana Islands']

        # Crear máscara booleana: True para filas que sí queremos (True = es país)
        mask = ~self.df_raw['country'].str.contains('|'.join(unwanted_keywords),
                                                    case=False, na=False)
        self.df_raw = self.df_raw[mask]

        # PASO 4: Eliminar nulos (filas con valores faltantes)
        # dropna() elimina cualquier fila que tenga al menos un NaN
        self.df_raw = self.df_raw.dropna()

        # PASO 5: Convertir tipos de datos
        # Convertir todas las columnas float64 a int64 (números enteros)
        float_cols = self.df_raw.select_dtypes(include=['float64']).columns
        self.df_raw[float_cols] = self.df_raw[float_cols].astype('int64')

        # PASO 6: Renombrar columnas al español para mayor claridad
        self.df_raw = self.df_raw.rename(columns={
            'country': 'pais',      # country → país
            'year': 'año'           # year → año
        })

        # PASO 7: Optimizar tipos para mejor rendimiento
        # category es más eficiente que object para columnas con valores repetidos
        self.df_clean = self.df_raw.copy()
        self.df_clean['pais'] = self.df_clean['pais'].astype('category')

        # Mensaje de confirmación
        print(f"✅ Datos cargados: {len(self.df_clean)} registros, {self.df_clean['pais'].nunique()} países")

    def get_top_diseases(self, top_n=15):
        """
        Obtiene las enfermedades más mortales globalmente.

        Algoritmo:
        ----------
        1. Seleccionar todas las columnas que comienzan con 'por_'
        2. Sumar cada columna (total de muertes por enfermedad)
        3. Ordenar de mayor a menor
        4. Tomar los top N
        5. Crear DataFrame con información legible

        Parámetros:
        -----------
        top_n : int, default=15
            Número de enfermedades a retornar

        Retorna:
        --------
        DataFrame con columnas:
        - Enfermedad: nombre legible
        - Total Muertes: total de muertes (1990-2019)
        - Promedio Anual: promedio de muertes por año

        Ejemplo:
        --------
        >>> analyzer = DiseaseAnalyzer('data.csv')
        >>> top = analyzer.get_top_diseases(10)
        >>> print(top)
        """
        # PASO 1: Identificar todas las columnas de enfermedades
        # Son todas las que comienzan con 'por_'
        disease_cols = [col for col in self.df_clean.columns if col.startswith('por_')]

        # PASO 2: Sumar cada columna (total por enfermedad en 30 años)
        totals = self.df_clean[disease_cols].sum().sort_values(ascending=False)

        # PASO 3-5: Crear DataFrame con información legible
        result = pd.DataFrame({
            'Enfermedad': [self.disease_mapping.get(col, col) for col in totals.index[:top_n]],
            'Total Muertes': totals.values[:top_n],
            'Promedio Anual': (totals.values[:top_n] / 30).astype(int)
        })

        return result

    def get_top_countries(self, top_n=20, disease=None):
        """
        Obtiene los países con mayor mortalidad.

        Puede filtrar por una enfermedad específica o mostrar total.

        Parámetros:
        -----------
        top_n : int, default=20
            Número de países a retornar
        disease : str, optional
            Nombre de enfermedad específica. Si None, usa total de todas.

        Retorna:
        --------
        Series con país como índice y total de muertes como valores

        Ejemplo:
        --------
        >>> # Top 20 países (total)
        >>> top20 = analyzer.get_top_countries(20)

        >>> # Top 20 en Malaria
        >>> top_malaria = analyzer.get_top_countries(20, 'Malaria')
        """
        # Si se especifica enfermedad, filtrar
        if disease:
            # Buscar la columna técnica que corresponde a la enfermedad
            disease_col = [col for col in self.df_clean.columns
                          if self.disease_mapping.get(col, '').lower() == disease.lower()]

            if not disease_col:
                print(f"⚠️  Enfermedad '{disease}' no encontrada")
                return None

            disease_col = disease_col[0]

            # Agrupar por país y sumar la enfermedad específica
            grouped = self.df_clean.groupby('pais')[disease_col].sum()
        else:
            # Si no se especifica enfermedad, sumar todas
            disease_cols = [col for col in self.df_clean.columns if col.startswith('por_')]
            grouped = self.df_clean.groupby('pais')[disease_cols].sum().sum(axis=1)

        # Retornar los top N, ordenados de mayor a menor
        return grouped.sort_values(ascending=False).head(top_n)

    def calculate_trends(self, disease, paises=None):
        """
        Calcula tendencia temporal de una enfermedad.

        Realiza regresión lineal para detectar si aumenta, disminuye o es estable.

        Algoritmo:
        ----------
        1. Encontrar la columna de la enfermedad
        2. Agrupar por año (sumar todas los países)
        3. Realizar regresión lineal (año vs muertes)
        4. Calcular estadísticas (R², p-valor, pendiente)
        5. Determinar tendencia (aumentando/disminuyendo)

        Parámetros:
        -----------
        disease : str
            Nombre de enfermedad (ej: 'Malaria')
        paises : list, optional
            Lista de países a analizar. Si None, usa global.

        Retorna:
        --------
        dict con:
        - enfermedad: nombre legible
        - datos: Series temporal (año vs muertes)
        - tendencia: 'Aumentando' o 'Disminuyendo'
        - tasa_cambio: muertes ganadas/perdidas por año
        - r_cuadrado: calidad del ajuste (0-1, más alto = mejor)
        - p_valor: significancia estadística

        Ejemplo:
        --------
        >>> result = analyzer.calculate_trends('Malaria')
        >>> print(f"Tendencia: {result['tendencia']}")
        >>> print(f"Cambio/año: {result['tasa_cambio']:.0f} muertes")
        >>> print(f"Confianza (R²): {result['r_cuadrado']:.3f}")
        """
        # PASO 1: Encontrar la columna técnica de la enfermedad
        disease_col = [col for col in self.df_clean.columns
                      if self.disease_mapping.get(col, '').lower() == disease.lower()]

        if not disease_col:
            print(f"⚠️  Enfermedad '{disease}' no encontrada")
            return None

        disease_col = disease_col[0]

        # PASO 2: Filtrar datos (si se especificaron países)
        if paises:
            df_filtered = self.df_clean[self.df_clean['pais'].isin(paises)]
        else:
            df_filtered = self.df_clean

        # PASO 3: Agrupar por año y sumar
        grouped = df_filtered.groupby('año')[disease_col].sum()

        # PASO 4: Regresión lineal
        # Convertir año y muertes a arrays para scipy
        x = np.array(grouped.index).reshape(-1, 1)  # Variable independiente (año)
        y = grouped.values  # Variable dependiente (muertes)

        # Calcular regresión: y = slope * x + intercept
        slope, intercept, r_value, p_value, std_err = stats.linregress(x.flatten(), y)

        # PASO 5: Compilar resultados
        return {
            'enfermedad': self.disease_mapping.get(disease_col),
            'datos': grouped,
            'tendencia': 'Aumentando' if slope > 0 else 'Disminuyendo',
            'tasa_cambio': slope,  # Cambio de muertes por año
            'r_cuadrado': r_value**2,  # Calidad del ajuste (0-1)
            'p_valor': p_value  # Significancia (< 0.05 = significativo)
        }

    def compare_countries(self, paises, disease=None):
        """
        Compara mortalidad entre múltiples países.

        Parámetros:
        -----------
        paises : list
            Lista de países a comparar
        disease : str, optional
            Enfermedad específica. Si None, usa total.

        Retorna:
        --------
        Series con país como índice y total de muertes
        """
        # Filtrar datos solo para los países especificados
        df_filtered = self.df_clean[self.df_clean['pais'].isin(paises)]

        if disease:
            # Filtrar por enfermedad específica
            disease_col = [col for col in self.df_clean.columns
                          if self.disease_mapping.get(col, '').lower() == disease.lower()]
            if disease_col:
                disease_col = disease_col[0]
                return df_filtered.groupby('pais')[disease_col].sum().sort_values(ascending=False)

        # Si no se especifica enfermedad, sumar todas
        disease_cols = [col for col in df_filtered.columns if col.startswith('por_')]
        return df_filtered.groupby('pais')[disease_cols].sum().sum(axis=1).sort_values(ascending=False)

    def get_disease_correlation(self):
        """
        Calcula correlación entre enfermedades.

        Encuentra qué enfermedades tienden a aparecer juntas
        en los mismos países (correlación positiva) o inversamente.

        Retorna:
        --------
        DataFrame con matriz de correlación (valores -1 a 1)
        - 1 = correlación perfecta positiva (aumentan juntas)
        - 0 = sin correlación
        - -1 = correlación perfecta negativa (inversa)
        """
        # PASO 1: Obtener totales por país y enfermedad
        disease_cols = [col for col in self.df_clean.columns if col.startswith('por_')]
        totals_by_country = self.df_clean.groupby('pais')[disease_cols].sum()

        # PASO 2: Calcular matriz de correlación
        correlation = totals_by_country.corr()

        # PASO 3: Renombrar para mejor legibilidad
        disease_names = {col: self.disease_mapping.get(col, col) for col in disease_cols}
        correlation.rename(columns=disease_names, index=disease_names, inplace=True)

        return correlation

    def export_results(self, output_dir='resultados'):
        """
        Exporta todos los resultados a archivos CSV.

        Crea directorio con archivos:
        - datos_limpios.csv: Dataset procesado
        - top_enfermedades.csv: Top 15 enfermedades
        - top_paises.csv: Top 20 países

        Parámetros:
        -----------
        output_dir : str
            Nombre del directorio de salida
        """
        # Crear directorio si no existe
        Path(output_dir).mkdir(exist_ok=True)

        # Exportar datos limpios
        self.df_clean.to_csv(f'{output_dir}/datos_limpios.csv', index=False)

        # Exportar top enfermedades
        self.get_top_diseases(15).to_csv(f'{output_dir}/top_enfermedades.csv', index=False)

        # Exportar top países
        self.get_top_countries(20).to_frame().to_csv(f'{output_dir}/top_paises.csv')

        print(f"✅ Resultados exportados a {output_dir}/")


# FUNCIONES DE VISUALIZACIÓN
# ==============================================================================
# Funciones reutilizables para crear gráficos profesionales

def plot_top_diseases(analyzer, top_n=15):
    """
    Crea gráfico de barras horizontal con las enfermedades más mortales.

    Parámetros:
    -----------
    analyzer : DiseaseAnalyzer
        Objeto analizador con datos cargados
    top_n : int
        Número de enfermedades a mostrar

    Retorna:
    --------
    Figure de matplotlib (se puede mostrar con plt.show())
    """
    # Obtener datos
    data = analyzer.get_top_diseases(top_n)

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8))

    # Crear barras con colores gradientes
    bars = ax.barh(range(len(data)), data['Total Muertes'],
                   color=plt.cm.Spectral(np.linspace(0, 1, len(data))))

    # Configurar ejes
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data['Enfermedad'])
    ax.set_xlabel('Total de Muertes (1990-2019)', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Enfermedades Más Mortales Globalmente',
                 fontsize=14, fontweight='bold')

    # Agregar valores en las barras
    for i, (bar, val) in enumerate(zip(bars, data['Total Muertes'])):
        ax.text(val, i, f' {val:,.0f}', va='center', fontsize=9)

    plt.tight_layout()
    return fig


def plot_disease_trend(analyzer, disease, paises=None):
    """
    Crea gráfico de línea con tendencia temporal de una enfermedad.

    Muestra:
    - Línea de datos reales (azul)
    - Línea de tendencia (rojo punteado)
    - Estadísticas de ajuste (R², tendencia)

    Parámetros:
    -----------
    analyzer : DiseaseAnalyzer
        Objeto analizador
    disease : str
        Nombre de enfermedad
    paises : list, optional
        Países a incluir (None = global)
    """
    # Calcular tendencia
    result = analyzer.calculate_trends(disease, paises)

    if result is None:
        return None

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))

    # Graficar datos reales
    datos = result['datos']
    ax.plot(datos.index, datos.values, marker='o', linewidth=2.5,
            markersize=6, label='Datos Reales')

    # Graficar línea de tendencia
    z = np.polyfit(datos.index, datos.values, 1)
    p = np.poly1d(z)
    ax.plot(datos.index, p(datos.index), "--", color='red',
            linewidth=2, label='Tendencia Linear', alpha=0.8)

    # Configurar gráfico
    ax.set_xlabel('Año', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de Muertes', fontsize=12, fontweight='bold')
    ax.set_title(f'Evolución: {result["enfermedad"]} (R² = {result["r_cuadrado"]:.3f})',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Anotación con estadísticas
    tendencia_text = f"Tendencia: {result['tendencia']}\nCambio/año: {result['tasa_cambio']:.0f} muertes"
    ax.text(0.02, 0.98, tendencia_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    return fig


# EJEMPLO DE USO / BLOQUE PRINCIPAL
# ==============================================================================
# Este código se ejecuta solo si corres el archivo directamente
# (no se ejecuta si importas este módulo en otro archivo)

if __name__ == "__main__":
    """
    Ejemplo de cómo usar el analizador.

    Para ejecutar:
    $ python analyzer.py
    """

    print("\n" + "="*80)
    print("PROYECTO CEI - ANÁLISIS DE MORTALIDAD GLOBAL")
    print("="*80 + "\n")

    # PASO 1: Cargar datos
    analyzer = DiseaseAnalyzer('annual_deaths_by_causes.csv')

    # PASO 2: Top enfermedades
    print("\n" + "="*80)
    print("TOP 15 ENFERMEDADES MÁS MORTALES")
    print("="*80)
    print(analyzer.get_top_diseases(15).to_string(index=False))

    # PASO 3: Top países
    print("\n" + "="*80)
    print("TOP 20 PAÍSES CON MAYOR MORTALIDAD")
    print("="*80)
    print(analyzer.get_top_countries(20))

    # PASO 4: Analizar tendencias
    print("\n" + "="*80)
    print("ANÁLISIS DE TENDENCIAS")
    print("="*80)

    diseases_to_analyze = ['Malaria', 'Tuberculosis', 'Enfermedades Cardiovasculares']

    for disease in diseases_to_analyze:
        result = analyzer.calculate_trends(disease)
        if result:
            print(f"\n{result['enfermedad']}:")
            print(f"  Tendencia: {result['tendencia']} ({result['tasa_cambio']:.0f} muertes/año)")
            print(f"  Confianza (R²): {result['r_cuadrado']:.3f}")
            print(f"  Significancia (p-valor): {result['p_valor']:.2e}")

    # PASO 5: Exportar resultados
    print("\n" + "="*80)
    analyzer.export_results()
    print("="*80 + "\n")
