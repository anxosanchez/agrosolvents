import numpy as np
import matplotlib.pyplot as plt
from thermo import Mixture

# --- CONVERSIONES ---
def C_to_K(c): return c + 273.15
def K_to_C(k): return k - 273.15
def bar_to_Pa(b): return b * 100000.0

# ==========================================
# 1. DEFINICIÓN DEL SISTEMA (ATFE)
# ==========================================
L = 3.0             # Metros
D = 0.5             # Metros
Area_total = np.pi * D * L
N_steps = 50        
dA = Area_total / N_steps

# Operación: Alto Vacío para proteger el DBE y Biodiésel
P_op_bar = 0.05     # 50 mbar (Vacío fuerte)
P_op_Pa = bar_to_Pa(P_op_bar)

# Calefacción: Cuidado, el DBE hierve a >200°C a atm, pero menos a vacío.
T_wall_C = 180.0    
T_wall_K = C_to_K(T_wall_C)

# Coeficiente U Base
U_ref = 1200.0      
mu_ref = 0.0005     # Pa.s (Referencia)
exponent_n = 0.25   

# ==========================================
# 2. COMPONENTES QUÍMICOS (MEZCLA TERNARIA)
# ==========================================
# 1. Methanol (Muy volátil - Impureza ligera)
# 2. Dimethyl Adipate (DBE - Volátil medio - El disolvente valioso)
# 3. Methyl Oleate (Biodiésel - No volátil - La base pesada)
comps = ['methanol', 'dimethyl adipate', 'methyl oleate']

# Alimentación (Ejemplo: Un residuo de limpieza)
# 5% Metanol (Restos de lavado)
# 45% DBE (Disolvente a recuperar o mantener)
# 50% Biodiésel (Base lubricante)
m_dot_feed = 500.0 / 3600.0  # kg/s
ws_feed = [0.05, 0.45, 0.50] # Fracciones másicas iniciales

# Temperatura de entrada
T_feed_C = 60.0
T_curr_K = C_to_K(T_feed_C)

# Inicialización de flujos por componente
# m_i = m_total * fraccion_i
m_comps = [m_dot_feed * w for w in ws_feed] 

# Arrays para gráficas
len_axis = []
temp_profile = []
visc_profile = []
# Guardaremos la fracción de CADA componente a lo largo del tubo
profiles_w = {c: [] for c in comps}
vapor_loss_profile = [] # Cuánto evaporamos en total

print(f"--- Iniciando Simulación Ternaria: {comps} ---")

# ==========================================
# 3. BUCLE DE SIMULACIÓN
# ==========================================
for i in range(N_steps):
    
    # Calcular masa total líquida y fracciones actuales
    m_liq_total = sum(m_comps)
    if m_liq_total <= 0: break
    
    ws_curr = [m / m_liq_total for m in m_comps]
    
    # A. TERMODINÁMICA LOCAL
    try:
        # Creamos la mezcla en el estado actual
        mix = Mixture(comps, ws=ws_curr, T=T_curr_K, P=P_op_Pa)
        
        # 1. Viscosidad (para ajustar U)
        mu_liq = mix.mul if mix.mul else mu_ref
        
        # 2. Punto de Burbuja (Bubble Point)
        # ¿A qué T hierve esta mezcla específica a 50 mbar?
        phase_eq = mix.flash(P=P_op_Pa, T=mix.bubble_point_at_P(P_op_Pa).T)
        T_boiling_K = phase_eq.T
        
        # 3. Composición del VAPOR en equilibrio (yi)
        # Esto es clave: phase_eq.y nos dice qué componente quiere irse al gas
        ys_vap = phase_eq.y # Fracciones molares del vapor
        # Convertimos fracciones molares de vapor a másicas (para el balance)
        MWs = mix.MWs
        MW_avg_vap = sum(y*mw for y, mw in zip(ys_vap, MWs))
        ws_vap = [(y*mw)/MW_avg_vap for y, mw in zip(ys_vap, MWs)]
        
        # Propiedades térmicas
        Cp_liq = mix.Cplm / (mix.MW / 1000.0)
        H_vap_mix = mix.Hvapm / (mix.MW / 1000.0) # J/kg aprox

    except Exception as e:
        print(f"Error termo en paso {i}: {e}")
        break

    # B. TRANSFERENCIA DE CALOR (U Variable)
    ratio = mu_ref / mu_liq
    U_local = U_ref * (ratio ** exponent_n)
    U_local = np.clip(U_local, 150.0, 2500.0)
    
    Q_watts = U_local * dA * (T_wall_K - T_curr_K)
    
    # C. BALANCE DE MASA Y ENERGÍA
    m_evap_total = 0.0
    
    if T_curr_K < T_boiling_K:
        # Calentamiento Sensible (Subir T)
        dT = Q_watts / (m_liq_total * Cp_liq)
        T_curr_K += dT
        # Si sobrepasa el punto de ebullición, corregimos al límite
        if T_curr_K > T_boiling_K: T_curr_K = T_boiling_K
        
    else:
        # Ebullición (Latente)
        # Asumimos que toda la Q evapora masa con la composición de equilibrio ws_vap
        m_evap_total = Q_watts / H_vap_mix
        
        # Límite de seguridad: no evaporar más de lo que hay
        if m_evap_total > m_liq_total: m_evap_total = m_liq_total
        
        # Restar masa a cada componente individualmente
        # Masa evaporada del componente i = Masa_total_evap * Fracción_masica_vapor_i
        for k in range(len(comps)):
            m_removed = m_evap_total * ws_vap[k]
            # Actualizamos la masa del componente en el líquido
            m_comps[k] -= m_removed
            if m_comps[k] < 0: m_comps[k] = 0.0

    # D. GUARDAR DATOS
    len_axis.append(i * (L/N_steps))
    temp_profile.append(K_to_C(T_curr_K))
    visc_profile.append(mu_liq * 1000)
    vapor_loss_profile.append(m_evap_total * 3600)
    
    for k, c in enumerate(comps):
        profiles_w[c].append(ws_curr[k])

# ==========================================
# 4. VISUALIZACIÓN
# ==========================================
plt.figure(figsize=(12, 10))

# GRÁFICA 1: Perfil de Composición (Lo más importante)
plt.subplot(3,1,1)
plt.title('Evolución de la Composición en el ATFE (Ternario)')
plt.plot(len_axis, profiles_w['methanol'], 'r--', label='Metanol (Ligero)')
plt.plot(len_axis, profiles_w['dimethyl adipate'], 'b-', linewidth=2, label='DBE (Medio)')
plt.plot(len_axis, profiles_w['methyl oleate'], 'g-', linewidth=2, label='Biodiésel (Pesado)')
plt.ylabel('Fracción Másica Líquida')
plt.legend()
plt.grid(True)

# GRÁFICA 2: Temperatura vs Pared
plt.subplot(3,1,2)
plt.plot(len_axis, temp_profile, 'k-', label='Temperatura Líquido')
plt.axhline(y=T_wall_C, color='r', linestyle=':', label='Temp Pared')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)

# GRÁFICA 3: ¿Qué estamos evaporando? (Tasa total)
plt.subplot(3,1,3)
plt.plot(len_axis, vapor_loss_profile, 'm-', label='Tasa Evaporación Total (kg/h)')
plt.xlabel('Longitud del Equipo (m)')
plt.ylabel('kg/h Evaporados')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Resultado final
print(f"--- RESULTADO SALIDA (FONDO) ---")
m_final = sum(m_comps)
ws_final = [m/m_final for m in m_comps]
for c, w in zip(comps, ws_final):
    print(f"{c}: {w*100:.2f} %")

