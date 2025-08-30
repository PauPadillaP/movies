
# Dashboard de Filmes (Streamlit + Firestore)

Este repositorio contiene un **dashboard interactivo** hecho en **Streamlit** que lee y escribe en **Firestore**.
Incluye un **Notebook** para analizar `movies.csv` y **migrar** los datos a Firestore.

## Estructura
- `app.py` — App de Streamlit.
- `requirements.txt` — Dependencias para Streamlit Cloud.
- `.streamlit/secrets.toml.template` — Plantilla de secretos para correr en local.
- `notebooks/migrate_and_eda.ipynb` — Colab/Notebook para EDA + migración CSV→Firestore.

## Pasos rápidos (resumen)
1. Crea un proyecto en Firebase y habilita **Firestore** (modo production).
2. Crea una **cuenta de servicio** y descarga el JSON de credenciales.
3. **Colab/Notebook**: Sube `movies.csv` y el JSON de la cuenta de servicio; ejecuta la celda de migración para crear la colección `movies`.
4. **Streamlit Cloud**: Crea un repositorio público en GitHub con estos archivos y despliega. En **App secrets** pega el JSON completo bajo la clave `gcp_service_account`.
5. Abre el dashboard y usa:
   - ✔️ Checkbox para ver todos los filmes
   - 🔎 Búsqueda por título (contains, case-insensitive)
   - 🎬 Filtro por director (selectbox + botón)
   - ➕ Formulario para insertar un nuevo filme

## Seguridad
- **No** subas el JSON de credenciales al repo. Usa **Streamlit Secrets**.
- En local, copia la plantilla de `secrets.toml` y pon tus credenciales reales (no lo confirmes en Git).

---

_Hecho para el reto académico: migración CSV→Firestore y visualización con Streamlit._
