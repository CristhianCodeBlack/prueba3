import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def cargar_datos():
    df = pd.read_csv("partidos_2015_2025.csv")
    df.dropna(inplace=True)
    df["Resultado"] = np.where(df["Goles Local"] > df["Goles Visitante"], 1,
                                np.where(df["Goles Local"] < df["Goles Visitante"], 2, 0))
    return df

def entrenar_modelo(df):
    label_encoder = LabelEncoder()
    df["Equipo Local Encoded"] = label_encoder.fit_transform(df["Equipo Local"])
    df["Equipo Visitante Encoded"] = label_encoder.transform(df["Equipo Visitante"])
    
    equipo_dict = dict(zip(df["Equipo Local Encoded"], df["Equipo Local"]))
    
    X = df[["Equipo Local Encoded", "Equipo Visitante Encoded"]]
    y = df["Resultado"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    
    return modelo, label_encoder, df, equipo_dict

def predecir_partido(modelo, label_encoder, equipo_dict, equipo_local, equipo_visitante):
    if equipo_local not in label_encoder.classes_ or equipo_visitante not in label_encoder.classes_:
        return "⚠️ Uno o ambos equipos no están en el conjunto de datos."
    
    equipo_local_encoded = label_encoder.transform([equipo_local])[0]
    equipo_visitante_encoded = label_encoder.transform([equipo_visitante])[0]
    
    entrada = pd.DataFrame([[equipo_local_encoded, equipo_visitante_encoded]], columns=["Equipo Local Encoded", "Equipo Visitante Encoded"])
    prediccion = modelo.predict(entrada)[0]
    
    if prediccion == 1:
        return f"🏆 {equipo_local} GANARÁ el partido."
    elif prediccion == 2:
        return f"🏆 {equipo_visitante} GANARÁ el partido."
    else:
        return "⚖️ EMPATE probable."

def seleccionar_equipo(lista_equipos):
    print("Selecciona un equipo:")
    for i, equipo in enumerate(lista_equipos, start=1):
        print(f"{i}. {equipo}")
    
    while True:
        try:
            opcion = int(input("Ingrese el número del equipo: "))
            if 1 <= opcion <= len(lista_equipos):
                return lista_equipos[opcion - 1]
            else:
                print("Número fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Ingresa un número válido.")

if __name__ == "__main__":
    df = cargar_datos()
    modelo, label_encoder, df, equipo_dict = entrenar_modelo(df)
    lista_equipos = sorted(df["Equipo Local"].unique())
    
    print("⚽ Predicción de partidos ⚽")
    equipo_local = seleccionar_equipo(lista_equipos)
    equipo_visitante = seleccionar_equipo(lista_equipos)
    
    print(predecir_partido(modelo, label_encoder, equipo_dict, equipo_local, equipo_visitante))
