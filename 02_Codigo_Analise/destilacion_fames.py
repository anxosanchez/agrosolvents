import numpy as np
import matplotlib.pyplot as plt
from thermo import Mixture

# --- CONVERSIÓN DE UNIDADES AUXILIARES ---
def C_to_K(c): return c + 273.15
def K_to_C(k): return k - 273.15
def bar_to_Pa(b): return b * 100000.0

# ==========================================
# 1. PARÁMETROS DEL EQUIPO (ATFE)
# ==========================================
L = 3.0             # Metros (Es un equipo grande)
D = 0.5             # Metros
Area_total = np.pi * D * L
N_steps = 50        # Nodos de simulación
dA = Area_total / N_steps

# Condiciones de Operación (BALEIRO / VACÍO)
P_op_bar = 0.1      # 100 mbar (Vacío moderado)
P_op_Pa = bar_to_Pa(P_op_bar)

# Calefacción (Aceite térmico o Vapor en la camisa)
T_wall_C = 160.0    
T_wall_K = C_to_K(T_wall_C)

# Coeficiente de Transferencia de Calor (U)
# En un ATFE real, esto baja al final cuando aumenta la viscosidad.
# Aquí usamos un promedio conservador.
U = 1200.0          # W/(m2.K) (Nota: Watts, no kW)

# ==========================================
# 2. ALIMENTACIÓN (FEED)
# ==========================================
flujo_masico_total = 500.0 / 3600.0  # kg/s (convertido de kg/h)
w_biodiesel = 0.20                   # 20% Biodiesel en peso
w_methanol = 0.80                    # 80% Metanol en peso
T_feed_C = 50.0
T_curr_K = C_to_K(T_feed_C)

# Definimos los componentes químicos para 'thermo'
# CAS del Oleato de Metilo (Biodiesel): 112-62-9
# CAS del Metanol: 67-56-1
comps = ['methyl oleate', 'methanol']

print(f"--- Iniciando Simulación Rigurosa con Thermo ---")
print(f"Presión: {P_op_bar} bar | T Pared: {T_wall_C} °C")

# Arrays para gráficas
len_axis = []
temp_profile = []
w_bio_profile = []
evap_rate_profile = []

m_liquid = flujo_masico_total
w_curr_bio = w_biodiesel
w_curr_meth = w_methanol

for i in range(N_steps):
    # --- A. LLAMADA A THERMO (El "Cerebro") ---
    # Creamos la mezcla en el estado actual
    # Usamos fracciones másicas (ws)
    mix = Mixture(comps, ws=[w_curr_bio, w_curr_meth], T=T_curr_K, P=P_op_Pa)
    
    # Calculamos el punto de burbuja (Bubble Point) a la presión de operación
    # Esto nos dice la temperatura real a la que hierve ESTA mezcla específica
    try:
        # Buscamos el equilibrio líquido-vapor
        phase_eq = mix.flash(P=P_op_Pa, T=mix.bubble_point_at_P(P_op_Pa).T)
        T_boiling_K = phase_eq.T
        
        # Calor Latente de Vaporización de la mezcla (J/kg)
        # Thermo lo da en J/mol, así que hacemos una aproximación con el MW
        H_vap_J_kg = mix.Hvapm / (mix.MW / 1000.0) 
        
        # Calor Específico del líquido (J/kg.K)
        Cp_liq = mix.Cplm / (mix.MW / 1000.0)
        
    except Exception as e:
        # Si falla (ej. si se seca todo el disolvente), usamos valores previos
        print(f"Aviso en paso {i}: {e}")
        break

    # --- B. TRANSFERENCIA DE CALOR ---
    # Q = U * A * (T_pared - T_liquido)
    Q_watts = U * dA * (T_wall_K - T_curr_K)
    
    # --- C. BALANCE DE ENERGÍA Y MATERIA ---
    m_evap = 0.0
    
    if T_curr_K < T_boiling_K:
        # ZONA DE CALENTAMIENTO (Sensible)
        # Toda la energía sube la temperatura, no hay evaporación
        dT = Q_watts / (m_liquid * Cp_liq)
        T_curr_K += dT
        # Si nos pasamos del punto de ebullición en este paso, corregimos
        if T_curr_K > T_boiling_K: T_curr_K = T_boiling_K
        
    else:
        # ZONA DE EVAPORACIÓN (Latente)
        # La temperatura se mantiene (o sube ligeramente por cambio de composición)
        # Asumimos que toda la Q va a evaporar
        m_evap = Q_watts / H_vap_J_kg
        
        # Límite físico: No podemos evaporar más disolvente del que existe
        m_meth_available = m_liquid * w_curr_meth
        if m_evap > m_meth_available:
            m_evap = m_meth_available
            # Si se evapora todo, la T subiría, pero simplificamos aquí

    # Actualizar flujos
    m_liquid_new = m_liquid - m_evap
    m_bio_abs = m_liquid * w_curr_bio # El biodiesel no se evapora (asunción)
    
    # Actualizar fracciones másicas
    if m_liquid_new > 0.00001:
        w_curr_bio = m_bio_abs / m_liquid_new
        w_curr_meth = 1.0 - w_curr_bio
    else:
        w_curr_bio = 1.0 # Puro residuo sólido/viscoso
        w_curr_meth = 0.0

    # Guardar datos
    len_axis.append(i * (L/N_steps))
    temp_profile.append(K_to_C(T_curr_K))
    w_bio_profile.append(w_curr_bio)
    evap_rate_profile.append(m_evap * 3600) # Guardar en kg/h para visualizar
    
    # Avanzar variables
    m_liquid = m_liquid_new
    # (En la zona de ebullición, la T del siguiente paso será la nueva T de burbuja
    # que calculará 'thermo' al inicio del loop debido a la nueva composición)

# ==========================================
# 3. RESULTADOS Y GRÁFICAS
# ==========================================
print(f"--- Fin de Simulación ---")
print(f"Salida Líquida: {m_liquid*3600:.2f} kg/h")
print(f"Pureza Biodiesel: {w_curr_bio*100:.2f} %")

plt.figure(figsize=(10, 8))

plt.subplot(3,1,1)
plt.plot(len_axis, temp_profile, 'r', label='Temperatura Líquido (°C)')
plt.axhline(y=T_wall_C, color='k', linestyle='--', alpha=0.5, label='Temp Pared')
plt.ylabel('Temp (°C)')
plt.title('Perfil Térmico dentro del ATFE')
plt.legend()
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(len_axis, w_bio_profile, 'g', label='Fracción Biodiesel (w/w)')
plt.ylabel('Concentración')
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(len_axis, evap_rate_profile, 'b', label='Tasa Evaporación (kg/h)')
plt.xlabel('Longitud del Evaporador (m)')
plt.ylabel('Evaporación')
plt.grid(True)

plt.tight_layout()
plt.show()

