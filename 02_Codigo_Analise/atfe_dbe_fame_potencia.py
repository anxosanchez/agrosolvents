import numpy as np
import matplotlib.pyplot as plt
from thermo import Mixture

# --- CONVERSIONES ---
def C_to_K(c): return c + 273.15
def K_to_C(k): return k - 273.15
def bar_to_Pa(b): return b * 100000.0

# ==========================================
# 1. PARÁMETROS MECÁNICOS Y DE DISEÑO
# ==========================================
L = 3.0             # Metros
D = 0.5             # Metros
Area_total = np.pi * D * L
N_steps = 50        
dA = Area_total / N_steps

# --- DATOS DEL ROTOR (NUEVO) ---
RPM = 300.0                     # Velocidad de giro típica
Tip_Speed = (RPM * np.pi * D) / 60.0  # Velocidad periférica (m/s)
Film_Thickness = 0.001          # 1 mm (Espesor típico de película)

print(f"Velocidad de Punta (Tip Speed): {Tip_Speed:.2f} m/s")

# Condiciones de Proceso
P_op_bar = 0.05     
P_op_Pa = bar_to_Pa(P_op_bar)
T_wall_C = 190.0    # T alta para intentar recuperar el DBE
T_wall_K = C_to_K(T_wall_C)

# Modelo de U
U_ref = 1200.0      
mu_ref = 0.0005     
exponent_n = 0.25   

# ==========================================
# 2. ALIMENTACIÓN (MEZCLA COMPLEJA)
# ==========================================
comps = ['methanol', 'dimethyl adipate', 'methyl oleate']
m_dot_feed = 500.0 / 3600.0 
ws_feed = [0.05, 0.45, 0.50] # 5% Ligero, 45% DBE, 50% Biodiésel

m_comps = [m_dot_feed * w for w in ws_feed] 
T_feed_C = 60.0
T_curr_K = C_to_K(T_feed_C)

# Arrays para resultados
len_axis = []
visc_profile = []
power_profile = []   # NUEVO: Potencia por sección (Watts)
cumulative_power = 0.0

print(f"--- Iniciando Simulación Electromecánica ---")

# ==========================================
# 3. BUCLE DE SIMULACIÓN
# ==========================================
for i in range(N_steps):
    
    m_liq_total = sum(m_comps)
    if m_liq_total <= 1e-6: break
    
    ws_curr = [m / m_liq_total for m in m_comps]
    
    # A. TERMODINÁMICA
    try:
        mix = Mixture(comps, ws=ws_curr, T=T_curr_K, P=P_op_Pa)
        mu_liq = mix.mul if mix.mul else mu_ref
        
        # Flash / Bubble Point
        phase_eq = mix.flash(P=P_op_Pa, T=mix.bubble_point_at_P(P_op_Pa).T)
        T_boiling_K = phase_eq.T
        
        # Propiedades vapor
        ys_vap = phase_eq.y 
        MWs = mix.MWs
        MW_avg_vap = sum(y*mw for y, mw in zip(ys_vap, MWs))
        ws_vap = [(y*mw)/MW_avg_vap for y, mw in zip(ys_vap, MWs)]
        
        H_vap_mix = mix.Hvapm / (mix.MW / 1000.0) 
        Cp_liq = mix.Cplm / (mix.MW / 1000.0)

    except:
        break

    # B. CÁLCULO DE POTENCIA DEL MOTOR (NUEVO)
    # P = mu * A * (v^2 / delta)
    # Calculamos la potencia consumida SOLO en este segmento dA
    shear_rate = (Tip_Speed**2) / Film_Thickness
    Power_segment_Watts = mu_liq * dA * shear_rate
    
    cumulative_power += Power_segment_Watts

    # C. TRANSFERENCIA DE CALOR
    ratio = mu_ref / mu_liq
    U_local = U_ref * (ratio ** exponent_n)
    U_local = np.clip(U_local, 150.0, 2500.0)
    
    Q_watts = U_local * dA * (T_wall_K - T_curr_K)
    
    # D. BALANCES
    m_evap_total = 0.0
    if T_curr_K < T_boiling_K:
        dT = Q_watts / (m_liq_total * Cp_liq)
        T_curr_K += dT
        if T_curr_K > T_boiling_K: T_curr_K = T_boiling_K
    else:
        m_evap_total = Q_watts / H_vap_mix
        if m_evap_total > m_liq_total: m_evap_total = m_liq_total
        
        for k in range(len(comps)):
            m_removed = m_evap_total * ws_vap[k]
            m_comps[k] -= m_removed
            if m_comps[k] < 0: m_comps[k] = 0.0

    # Guardar datos
    len_axis.append(i * (L/N_steps))
    visc_profile.append(mu_liq * 1000) # cP
    power_profile.append(Power_segment_Watts) # Watts
    
# ==========================================
# 4. RESULTADOS DE INGENIERÍA
# ==========================================
print(f"--- RESULTADOS FINALES ---")
print(f"Potencia TOTAL Viscosa en el Eje: {cumulative_power/1000:.3f} kW")
# Se suele añadir un 20-30% extra por pérdidas mecánicas en rodamientos/sellos
print(f"Potencia de Motor Recomendada (+30%): {cumulative_power*1.3/1000:.3f} kW")

plt.figure(figsize=(10, 6))

ax1 = plt.gca()
ax1.set_xlabel('Longitud del Evaporador (m)')
ax1.set_ylabel('Viscosidad (cP)', color='blue')
ax1.plot(len_axis, visc_profile, 'b-', label='Viscosidad')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel('Potencia Local (Watts)', color='red')
ax2.plot(len_axis, power_profile, 'r--', label='Consumo Potencia')
ax2.tick_params(axis='y', labelcolor='red')
ax2.set_title('Perfil de Potencia Mecánica y Viscosidad')

plt.tight_layout()
plt.show()


