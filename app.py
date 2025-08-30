
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

st.set_page_config(page_title="Filmes — Dashboard", page_icon="🎬", layout="wide")

# ---- Firestore client from Streamlit secrets ----
# In Streamlit Cloud, set the "gcp_service_account" secret with your service account JSON (as key-value)
# Example in Secrets:
#   [gcp_service_account]
#   type="service_account"
#   project_id="your-project-id"
#   private_key_id="..."
#   private_key="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
#   client_email="..."
#   client_id="..."
#   auth_uri="https://accounts.google.com/o/oauth2/auth"
#   token_uri="https://oauth2.googleapis.com/token"
#   auth_provider_x509_cert_url="https://www.googleapis.com/oauth2/v1/certs"
#   client_x509_cert_url="..."
#
# For local runs, create .streamlit/secrets.toml (see provided template file).

@st.cache_resource(show_spinner=False)
def get_db():
    creds_dict = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(dict(creds_dict))
    client = firestore.Client(credentials=credentials, project=creds_dict["project_id"])
    return client

db = get_db()

# ---- Data loading ----
@st.cache_data(show_spinner=False, ttl=60)
def load_movies():
    docs = db.collection("movies").stream()
    rows = []
    for d in docs:
        data = d.to_dict() or {}
        data["doc_id"] = d.id
        # Ensure expected keys exist for DataFrame consistency
        for k in ["name", "director", "genre", "company"]:
            data.setdefault(k, None)
        rows.append(data)
    return pd.DataFrame(rows)

df = load_movies()

# ---- Sidebar: Header & controls ----
st.sidebar.header("🎛️ Controles")

# Checkbox to show all movies + header
show_all = st.sidebar.checkbox("Ver todos los filmes recuperados", value=True)
st.sidebar.markdown("---")

# Search by title (case-insensitive 'contains')
st.sidebar.subheader("🔎 Búsqueda por título")
title_query = st.sidebar.text_input("Escribe parte del título", value="")
if st.sidebar.button("Buscar"):
    if title_query.strip():
        mask = df["name"].fillna("").str.contains(title_query.strip(), case=False, na=False)
        results = df[mask].copy()
        st.markdown(f"### Resultados de búsqueda para: `{title_query}`  •  {len(results)} filme(s)")
        st.dataframe(results.sort_values("name"), use_container_width=True)
    else:
        st.info("Escribe un texto para buscar por título.")

st.sidebar.markdown("---")

# Filter by director
st.sidebar.subheader("🎬 Filtrar por director")
directors = sorted([d for d in df["director"].dropna().unique()])
selected_director = st.sidebar.selectbox("Selecciona un director", options=directors if directors else ["(sin datos)"])
if st.sidebar.button("Filtrar por director"):
    if directors:
        sub = df[df["director"] == selected_director].copy()
        st.markdown(f"### Filmes de **{selected_director}**  •  {len(sub)} filme(s)")
        st.dataframe(sub.sort_values("name"), use_container_width=True)
    else:
        st.info("No hay directores disponibles para filtrar.")

st.sidebar.markdown("---")

# Form to insert a new movie
st.sidebar.subheader("➕ Insertar nuevo filme")
with st.sidebar.form("new_movie_form", clear_on_submit=True):
    nm = st.text_input("Título (name)")
    dr = st.text_input("Director")
    ge = st.text_input("Género (genre)")
    co = st.text_input("Compañía (company)")
    submitted = st.form_submit_button("Insertar")
    if submitted:
        if not nm:
            st.sidebar.error("El título es obligatorio.")
        else:
            doc = {"name": nm, "director": dr or None, "genre": ge or None, "company": co or None}
            db.collection("movies").add(doc)
            st.sidebar.success(f"'{nm}' insertado correctamente.")
            # refresh cached data
            load_movies.clear()
            df = load_movies()

# ---- Main area ----
st.title("🎥 Dashboard de Filmes")
st.caption("Fuente de datos: Firestore (colección `movies`)")

if show_all:
    st.markdown("### Todos los filmes recuperados")
    if df.empty:
        st.warning("No hay datos en la colección `movies`. Inserta algunos filmes desde el formulario en el sidebar o ejecuta la migración CSV→Firestore.")
    else:
        st.dataframe(df.sort_values("name"), use_container_width=True)
