import numpy as np
import matplotlib.pyplot as plt
from thermo import Mixture

# --- FUNCIÓNS AUXILIARES ---
def C_to_K(c): return c + 273.15
def K_to_C(k): return k - 273.15
def bar_to_Pa(b): return b * 100000.0

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
L = 3.0             
D = 0.5             
Area_total = np.pi * D * L
N_steps = 50        
dA = Area_total / N_steps

P_op_bar = 0.1      
P_op_Pa = bar_to_Pa(P_op_bar)
T_wall_C = 170.0    # Subimos un pouco a T parede para compensar a perda de U
T_wall_K = C_to_K(T_wall_C)

# --- MODELO DE U VARIABLE ---
# Definimos un U de referencia para o disolvente puro ou a alimentación
U_ref = 1500.0      # W/m2K (Moi bo ao principio)
mu_ref = 0.0004     # Pa.s (Viscosidade aprox. do metanol/feed quente ~0.4 cP)
exponent_n = 0.3    # Factor de amortiguamento das aspas

comps = ['methyl oleate', 'methanol']

# Alimentación
flujo_masico_total = 500.0 / 3600.0 
w_biodiesel = 0.20                   
w_methanol = 0.80                    
T_feed_C = 50.0
T_curr_K = C_to_K(T_feed_C)

# Arrays para gardar datos
len_axis = []
temp_profile = []
w_bio_profile = []
viscosity_profile = [] # NOVO
U_profile = []         # NOVO

m_liquid = flujo_masico_total
w_curr_bio = w_biodiesel
w_curr_meth = w_methanol

print("Iniciando simulación con Viscosidade Dinámica...")

for i in range(N_steps):
    # 1. PROPIEDADES TERMODINÁMICAS E DE TRANSPORTE
    mix = Mixture(comps, ws=[w_curr_bio, w_curr_meth], T=T_curr_K, P=P_op_Pa)
    
    # Viscosidade do líquido (mix.mul devolve Pa.s)
    try:
        mu_liq = mix.mul 
        if mu_liq is None: mu_liq = mu_ref # Fallback se falla o cálculo
    except:
        mu_liq = mu_ref

    # 2. RECALCULAR U BASEADO NA VISCOSIDADE
    # Fórmula: U_actual = U_ref * (mu_ref / mu_actual)^n
    # Evitamos división por cero ou valores absurdos
    ratio = mu_ref / mu_liq
    U_local = U_ref * (ratio ** exponent_n)
    
    # Límite de seguridade (U non pode ser case 0 nin infinito)
    if U_local < 100: U_local = 100.0 
    if U_local > 2000: U_local = 2000.0

    # 3. EQUILIBRIO E BALANCE (Igual que antes)
    try:
        phase_eq = mix.flash(P=P_op_Pa, T=mix.bubble_point_at_P(P_op_Pa).T)
        T_boiling_K = phase_eq.T
        H_vap_J_kg = mix.Hvapm / (mix.MW / 1000.0) 
        Cp_liq = mix.Cplm / (mix.MW / 1000.0)
    except:
        break

    Q_watts = U_local * dA * (T_wall_K - T_curr_K)
    
    m_evap = 0.0
    if T_curr_K < T_boiling_K:
        dT = Q_watts / (m_liquid * Cp_liq)
        T_curr_K += dT
        if T_curr_K > T_boiling_K: T_curr_K = T_boiling_K
    else:
        m_evap = Q_watts / H_vap_J_kg
        m_meth_available = m_liquid * w_curr_meth
        if m_evap > m_meth_available:
            m_evap = m_meth_available

    # Balances
    m_liquid_new = m_liquid - m_evap
    m_bio_abs = m_liquid * w_curr_bio
    
    if m_liquid_new > 0.00001:
        w_curr_bio = m_bio_abs / m_liquid_new
        w_curr_meth = 1.0 - w_curr_bio
    else:
        w_curr_bio = 1.0
        w_curr_meth = 0.0

    # Gardar datos
    len_axis.append(i * (L/N_steps))
    temp_profile.append(K_to_C(T_curr_K))
    w_bio_profile.append(w_curr_bio)
    viscosity_profile.append(mu_liq * 1000) # Convertir a cP (centipoise) para ver mellor
    U_profile.append(U_local)
    
    m_liquid = m_liquid_new

# ==========================================
# 4. VISUALIZACIÓN MULTI-VARIABLE
# ==========================================
fig, ax1 = plt.subplots(figsize=(10, 6))

# Eixe Y esquerdo: Concentración
ax1.set_xlabel('Lonxitude do Evaporador (m)')
ax1.set_ylabel('Fracción Biodiesel', color='green')
ax1.plot(len_axis, w_bio_profile, color='green', linewidth=2, label='Conc. Biodiesel')
ax1.tick_params(axis='y', labelcolor='green')
ax1.grid(True)

# Eixe Y dereito: Viscosidade e U
ax2 = ax1.twinx() 
ax2.set_ylabel('Viscosidade (cP) / Coef U (W/m2K)', color='blue')

# Graficamos U (Liña sólida azul)
ax2.plot(len_axis, U_profile, color='blue', linestyle='-', label='Coef. Transferencia U')
# Graficamos Viscosidade (Liña punteada vermella)
ax2.plot(len_axis, viscosity_profile, color='red', linestyle='--', label='Viscosidade (cP)')
ax2.tick_params(axis='y', labelcolor='blue')

plt.title('Impacto da Viscosidade na Eficiencia do ATFE')
fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
plt.tight_layout()
plt.show()

print(f"Viscosidade Entrada: {viscosity_profile[0]:.2f} cP | Viscosidade Saída: {viscosity_profile[-1]:.2f} cP")
print(f"U Entrada: {U_profile[0]:.0f} W/m2K | U Saída: {U_profile[-1]:.0f} W/m2K")

