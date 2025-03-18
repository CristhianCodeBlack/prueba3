import requests
import pandas as pd
from datetime import datetime

# Ligas a consultar (Premier League, LaLiga, Serie A, Bundesliga, Ligue 1)
ligas = ["PL", "PD", "SA", "BL1", "FL1"]
headers = {"X-Auth-Token": "c6de318d1df446bc8599a72e4f7615df"}  # Reemplaza con tu API Key válida

# Lista para almacenar todos los partidos
matches = []

for liga in ligas:
    for year in range(2015, 2026):  # Desde 2015 hasta 2025
        url = f"https://api.football-data.org/v4/competitions/{liga}/matches?season={year}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            for match in data["matches"]:
                # Convertir fecha UTC a formato estándar
                fecha_utc = match["utcDate"]
                fecha_formateada = datetime.strptime(fecha_utc, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

                # Filtrar solo partidos finalizados
                if match["status"] == "FINISHED":
                    matches.append({
                        "Fecha": fecha_formateada,
                        "Liga": match["competition"]["name"],
                        "Equipo Local": match["homeTeam"]["name"],
                        "Equipo Visitante": match["awayTeam"]["name"],
                        "Goles Local": match["score"]["fullTime"]["home"],  
                        "Goles Visitante": match["score"]["fullTime"]["away"]
                    })
        else:
            print(f"⚠️ Error {response.status_code} en liga {liga} ({year}): {response.text}")

# Convertir a DataFrame y ordenar por fecha
df = pd.DataFrame(matches)
df.sort_values(by="Fecha", ascending=True, inplace=True)

# Guardar en CSV con miles de registros
df.to_csv("partidos_2015_2025.csv", index=False, encoding="utf-8")

print(f"✅ Se guardaron {len(df)} partidos en 'partidos_2015_2025.csv'")
