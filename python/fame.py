import pandas as pd
import numpy as np

# 1. Base de datos de propiedades de componentes puros (FAMEs individuales a 40°C)
# Datos aproximados de literatura técnica (Knothe et al.)
# Viscosidad en mm2/s (cSt), Densidad en kg/m3
fame_props = {
    'C16:0 (Palmitato)': {'visc': 4.38, 'dens': 855}, # Saturado
    'C18:0 (Estearato)': {'visc': 5.85, 'dens': 853}, # Saturado
    'C18:1 (Oleato)':    {'visc': 4.51, 'dens': 860}, # Monoinsaturado
    'C18:2 (Linoleato)': {'visc': 3.65, 'dens': 870}, # Poliinsaturado
    'C18:3 (Linolenato)':{'visc': 3.14, 'dens': 878}  # Poliinsaturado
}

# 2. Definición de perfiles de ácidos grasos (Fracción másica aproximada 0.0 - 1.0)
oils_composition = {
    'Soja FAME':    {'C16:0 (Palmitato)': 0.11, 'C18:0 (Estearato)': 0.04, 'C18:1 (Oleato)': 0.23, 'C18:2 (Linoleato)': 0.54, 'C18:3 (Linolenato)': 0.08},
    'Palma FAME':   {'C16:0 (Palmitato)': 0.44, 'C18:0 (Estearato)': 0.05, 'C18:1 (Oleato)': 0.39, 'C18:2 (Linoleato)': 0.10, 'C18:3 (Linolenato)': 0.00}, # Resto minoritarios
    'Girasol FAME': {'C16:0 (Palmitato)': 0.06, 'C18:0 (Estearato)': 0.05, 'C18:1 (Oleato)': 0.30, 'C18:2 (Linoleato)': 0.59, 'C18:3 (Linolenato)': 0.00}
}

def calculate_mixture_properties(composition, props_db):
    """Calcula densidad (regla lineal) y viscosidad (regla logarítmica)"""
    mix_dens = 0
    mix_visc_log = 0
    total_mass = sum(composition.values()) # Normalizar si no suma 1
    
    for component, fraction in composition.items():
        if component in props_db:
            xi = fraction / total_mass
            p_dens = props_db[component]['dens']
            p_visc = props_db[component]['visc']
            
            # Regla lineal para densidad
            mix_dens += xi * p_dens
            # Regla logarítmica para viscosidad
            mix_visc_log += xi * np.log(p_visc)
            
    mix_visc = np.exp(mix_visc_log)
    return mix_dens, mix_visc

# 3. Ejecución y Reporte
results = []
for oil_name, comp in oils_composition.items():
    dens, visc = calculate_mixture_properties(comp, fame_props)
    results.append({
        'Disolvente (Origen)': oil_name,
        'Densidad Estimada @40C (kg/m3)': round(dens, 2),
        'Viscosidad Estimada @40C (cSt)': round(visc, 3)
    })

df_results = pd.DataFrame(results)
print(df_results.to_markdown(index=False))