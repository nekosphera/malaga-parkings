# Databricks notebook source
# Lectura de los datos desde el Git folder (haz "Pull" antes para tener la última versión)
import os, glob

# Ruta del repo dentro del workspace (ajusta tu usuario si hace falta)
usuario = spark.sql("SELECT current_user()").first()[0]
repo = f"/Workspace/Users/{usuario}/malaga-parkings"

# --- Última foto ---
import pandas as pd
actual = pd.read_csv(f"{repo}/data/ocupacion_actual.csv", sep=None, engine="python", encoding="latin-1")
df_actual = spark.createDataFrame(actual)
display(df_actual)

# COMMAND ----------
# --- Histórico completo, con la fecha de cada descarga ---
partes = []
for f in sorted(glob.glob(f"{repo}/data/historico/*/*.csv")):
    p = pd.read_csv(f, sep=None, engine="python", encoding="latin-1")
    p["fecha_descarga"] = os.path.basename(f).replace(".csv", "")
    partes.append(p)

df_hist = spark.createDataFrame(pd.concat(partes, ignore_index=True).astype(str))
display(df_hist)

# COMMAND ----------
# Guardar como tabla para usarla en SQL / dashboards
df_hist.write.mode("overwrite").saveAsTable("workspace.default.aparcamientos_malaga_historico")
