import pandas as pd
import matplotlib.pyplot as plt

# Leer el CSV
data = pd.read_csv("costos.csv")

# Asegurarse de que los nombres de columnas estén en minúsculas
data.columns = data.columns.str.lower()

# Crear gráfico
plt.figure(figsize=(10, 6))
plt.plot(data["tiempo"], data["costo"], marker='o', color='blue')

# Etiquetas de ejes
plt.xlabel("Tiempo (s)")
plt.ylabel("Costo")
plt.title("Evolución del Costo a lo Largo del Tiempo")
plt.grid(True)

# Anotar cada punto con su coordenada
for tiempo, costo in zip(data["tiempo"], data["costo"]):
    plt.text(tiempo, costo + 1.5, f"({tiempo:.2f}, {costo})", fontsize=8, rotation=45)

plt.tight_layout()
plt.show()
