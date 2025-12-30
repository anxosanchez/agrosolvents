import numpy as np
import matplotlib.pyplot as plt

# --- 1. PARÁMETROS DE DESEÑO DO ATFE ---
L = 2.0           # Lonxitude do equipo (m)
D = 0.5           # Diámetro interno (m)
Area_total = np.pi * D * L
N_steps = 50      # Número de "fatias" para a simulación
dA = Area_total / N_steps
T_wall = 150.0    # Temperatura da parede (°C) (Aceite térmico ou vapor)
P_op = 0.1        # Presión de operación (bar) - BALEIRO é crucial

# --- 2. PROPIEDADES (Simplificadas para o exemplo) ---
# Aquí podes usar a libraría 'thermo' para facelo real
# Asumimos unha mestura binaria: [Biodiesel, Disolvente]
Heat_vap_solvente = 350.0  # kJ/kg (Calor latente aproximada)
Cp_mix = 2.0               # kJ/kg.K (Calor específica media)

# O coeficiente U varía coa viscosidade, pero empezamos cun valor fixo
# En ATFE, U adoita ser alto (1000 - 2000 W/m2K)
U = 1.2  # kW/m2.K 

# --- 3. CONDICIÓNS DE ENTRADA (FEED) ---
m_dot_feed = 500.0   # kg/h
x_biodiesel = 0.3    # 30% Biodiesel
x_solvent = 0.7      # 70% Disolvente
T_feed = 60.0        # Temperatura de entrada (°C)

# Temperatura de ebulición do disolvente a P_op (ex. 0.1 bar)
# Isto debería calcularse con Antoine ou termodinámica real
T_bp_solvent = 45.0  

# --- 4. SIMULACIÓN (Bucle ao longo da lonxitude) ---
# Arrays para gardar resultados
temp_profile = []
mass_flow_profile = []
composition_profile = []

# Inicialización
m_liquid = m_dot_feed
x_curr_bio = x_biodiesel
T_curr = T_feed

print(f"Iniciando simulación ATFE. Feed: {m_dot_feed} kg/h")

for i in range(N_steps):
    # 1. Quentar o líquido ata o punto de ebulición?
    # Se T_curr < T_bp, a calor úsase para calor sensible (subir T)
    # Se T_curr >= T_bp, a calor úsase para calor latente (evaporar)
    
    # Calor transferida neste segmento Q = U * A * dT
    Q_transferred = U * dA * (T_wall - T_curr) # kW
    
    m_evap = 0.0
    
    if T_curr < T_bp_solvent:
        # Só quentamento sensible
        dT = Q_transferred / (m_liquid * Cp_mix / 3600) # axuste unidades
        T_curr += dT
        # Límite físico: non pasar a T de ebulición nun só paso sen evaporar
        if T_curr > T_bp_solvent: T_curr = T_bp_solvent
    else:
        # Evaporación (Asumimos T constante durante ebulición pura do disolvente)
        # Q = m_evap * lambda
        m_evap = (Q_transferred * 3600) / Heat_vap_solvente # kg/h
        
        # Non podemos evaporar máis disolvente do que hai
        m_solvent_available = m_liquid * (1 - x_curr_bio)
        if m_evap > m_solvent_available:
            m_evap = m_solvent_available
            # Aquí a T empezaría a subir de novo (recalentamento do biodiesel)
            
    # Balances de masa
    m_liquid_new = m_liquid - m_evap
    
    # Balances de compoñentes (O biodiesel non evapora, é non-volátil aquí)
    m_bio = m_liquid * x_curr_bio
    if m_liquid_new > 0:
        x_new_bio = m_bio / m_liquid_new
    else:
        x_new_bio = 1.0 # Seco total (perigoso na realidade)

    # Actualizar variables para o seguinte paso
    m_liquid = m_liquid_new
    x_curr_bio = x_new_bio
    
    # Gardar datos
    temp_profile.append(T_curr)
    mass_flow_profile.append(m_liquid)
    composition_profile.append(x_curr_bio)

# --- 5. VISUALIZACIÓN ---
x_axis = np.linspace(0, L, N_steps)

plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(x_axis, mass_flow_profile, 'b-', label='Fluxo Líquido (kg/h)')
plt.ylabel('Caudal Másico')
plt.title('Perfil do ATFE')
plt.legend()

plt.subplot(2,1,2)
plt.plot(x_axis, composition_profile, 'r-', label='Fracción Biodiesel')
plt.xlabel('Lonxitude do Evaporador (m)')
plt.ylabel('Fracción Masica')
plt.legend()
plt.tight_layout()
plt.show()

print(f"Saída Final: {m_liquid:.2f} kg/h cunha pureza de {x_curr_bio*100:.1f}%")

