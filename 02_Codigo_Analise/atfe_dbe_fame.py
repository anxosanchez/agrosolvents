import numpy as np
import matplotlib.pyplot as plt
from thermo import Mixture

# --- CONFIGURACIÓN DE UNIDADES ---
def C_to_K(c): return c + 273.15
def K_to_C(k): return k - 273.15
def bar_to_Pa(b): return b * 100000.0

# --- 1. PARÁMETROS DE DISEÑO (ATFE) ---
L = 3.0             # Longitud (m)
D = 0.5             # Diámetro (m)
Area_total = np.pi * D * L
N_steps = 50        # Nodos de simulación
dA = Area_total / N_steps

# Condiciones de Operación
P_op_bar = 0.1      # 100 mbar (Vacío)
P_op_Pa = bar_to_Pa(P_op_bar)
T_wall_C = 170.0    # Temperatura del aceite térmico
T_wall_K = C_to_K(T_wall_C)

# Modelo de Viscosidad y U
U_ref = 1500.0      # W/m2K (Referencia para fluido limpio)
mu_ref = 0.0004     # Pa.s (Viscosidad referencia)
exponent_n = 0.3    # Factor de amortiguamiento mecánico

# Definición Química (Biodiésel + Disolvente Ligero/DBE)
# Usamos Oleato de Metilo como 'proxy' del Biodiésel
comps = ['methyl oleate', 'methanol'] 

# --- 2. ALIMENTACIÓN ---
flujo_masico_total = 500.0 / 3600.0  # kg/s
w_biodiesel = 0.20                   # 20% Biodiésel (Residuo pesado)
w_light = 0.80                       # 80% Disolvente a recuperar
T_feed_C = 50.0
T_curr_K = C_to_K(T_feed_C)

# Arrays de resultados
len_axis = []
temp_profile = []
conc_profile = []
visc_profile = []
U_profile = []

m_liquid = flujo_masico_total
w_curr_bio = w_biodiesel
w_curr_light = w_light

print("--- Iniciando Simulación ATFE ---")

# --- 3. BUCLE ITERATIVO (Diferencias Finitas) ---
for i in range(N_steps):
    # A. Propiedades Termodinámicas (Librería Thermo)
    try:
        mix = Mixture(comps, ws=[w_curr_bio, w_curr_light], T=T_curr_K, P=P_op_Pa)
        
        # Viscosidad Dinámica
        mu_liq = mix.mul if mix.mul else mu_ref
        
        # Equilibrio Líquido-Vapor (Bubble Point)
        phase_eq = mix.flash(P=P_op_Pa, T=mix.bubble_point_at_P(P_op_Pa).T)
        T_boiling_K = phase_eq.T
        
        # Entalpías y Cp
        H_vap_J_kg = mix.Hvapm / (mix.MW / 1000.0) 
        Cp_liq = mix.Cplm / (mix.MW / 1000.0)
    except:
        break # Salir si hay error numérico (seco)

    # B. Ajuste de U por Viscosidad
    # Teoría de penetración modificada: U decae si mu aumenta
    ratio = mu_ref / mu_liq
    U_local = U_ref * (ratio ** exponent_n)
    U_local = np.clip(U_local, 100.0, 2000.0)

    # C. Transferencia de Calor
    Q_watts = U_local * dA * (T_wall_K - T_curr_K)

    # D. Balances de Masa y Energía
    m_evap = 0.0
    if T_curr_K < T_boiling_K:
        # Calentamiento Sensible
        dT = Q_watts / (m_liquid * Cp_liq)
        T_curr_K += dT
        if T_curr_K > T_boiling_K: T_curr_K = T_boiling_K
    else:
        # Evaporación Latente
        m_evap = Q_watts / H_vap_J_kg
        m_available = m_liquid * w_curr_light
        if m_evap > m_available: m_evap = m_available

    # Actualizar flujos para siguiente nodo
    m_liquid_new = m_liquid - m_evap
    m_bio_abs = m_liquid * w_curr_bio
    
    if m_liquid_new > 1e-6:
        w_curr_bio = m_bio_abs / m_liquid_new
        w_curr_light = 1.0 - w_curr_bio
    else:
        w_curr_bio = 1.0

    # Guardar datos
    len_axis.append(i * (L/N_steps))
    temp_profile.append(K_to_C(T_curr_K))
    conc_profile.append(w_curr_bio)
    visc_profile.append(mu_liq * 1000) # cP
    U_profile.append(U_local)
    
    m_liquid = m_liquid_new

# --- 4. VISUALIZACIÓN ---
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('Longitud (m)')
ax1.set_ylabel('Conc. Biodiésel (w/w)', color='green')
ax1.plot(len_axis, conc_profile, 'g-', linewidth=2, label='Concentración')
ax1.tick_params(axis='y', labelcolor='green')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel('Viscosidad (cP) / Coef U', color='blue')
ax2.plot(len_axis, U_profile, 'b-', label='U (W/m2K)')
ax2.plot(len_axis, visc_profile, 'r--', label='Viscosidad (cP)')
ax2.tick_params(axis='y', labelcolor='blue')

plt.title('Simulación ATFE: Efecto de la Viscosidad en la Eficiencia')
fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
plt.tight_layout()
plt.show()


