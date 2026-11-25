import numpy as np
import matplotlib.pyplot as plt

# 1. Inisialisasi Parameter Sistem Dinamika Suhu Ruangan
C = 50000.0     # Kapasitas termal ruangan (J/K)
P_max = 5000.0  # Daya maksimum heater (Watt)
UA = 100.0      # Koefisien kehilangan panas dinding (W/K)
T_out = 20.0    # Suhu lingkungan luar (°C)
T0 = 20.0       # Suhu awal ruangan (°C)

dt = 1.0        # Step size waktu (detik)
t_end = 3600    # Durasi simulasi 3600 detik (60 menit)
t = np.arange(0, t_end + dt, dt)

def simulate_room_temp(u_signal):
    T = np.zeros_like(t)
    T[0] = T0
    for i in range(1, len(t)):
        q_in = P_max * u_signal[i-1]
        q_loss = UA * (T[i-1] - T_out)
        dTdt = (q_in - q_loss) / C
        T[i] = T[i-1] + dTdt * dt
    return T

# 2. Definisi Sinyal Kontrol
u_step = np.where(t >= 300, 0.8, 0.0)
T_step = simulate_room_temp(u_step)

u_pulse = np.where((t >= 300) & (t <= 1500), 1.0, 0.0)
T_pulse = simulate_room_temp(u_pulse)

u_sin = 0.5 + 0.4 * np.sin(2 * np.pi * t / 1800.0)
T_sin = simulate_room_temp(u_sin)

# 3. Verifikasi Perhitungan Manual (t = 300..305 detik pada sinyal Step)
print("Verifikasi Perhitungan Manual (Step u=0.8 mulai t=300s):")
for idx in range(300, 306):
    print(f"t = {t[idx]:.0f}s | T(t) = {T_step[idx]:.4f} °C")
print(f"Suhu Steady State Teoritis: {T_out + (P_max * 0.8)/UA:.2f} °C")
print(f"Suhu Simulasi Akhir (t=3600s): {T_step[-1]:.4f} °C")

# 4. Visualisasi Grafik Step Response
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
ax1.plot(t/60, T_step, 'b-', linewidth=2, label='Suhu Ruangan T(t)')
ax1.axhline(60.0, color='r', linestyle='--', label='Steady State (60.0 °C)')
ax1.set_ylabel('Suhu (°C)')
ax1.set_title('Simulasi Sistem Dinamik Suhu Ruangan - Input Step (u = 80%)')
ax1.grid(True)
ax1.legend()

ax2.plot(t/60, u_step*100, 'g--', linewidth=2, label='Kontrol Heater u(t)')
ax2.set_ylabel('Daya Heater (%)')
ax2.set_xlabel('Waktu (Menit)')
ax2.grid(True)
ax2.legend()
plt.tight_layout()
plt.savefig('simulasi_ta06_step.png', dpi=150)
plt.show()