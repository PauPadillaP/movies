Dashboard de Filmes

Este proyecto se desarrolló como parte del reto **“Construcción y despliegue en producción de un dashboard interactivo”**.  
La idea principal fue trabajar con un dataset de películas (`movies.csv`) y llevarlo a un entorno real donde los datos pudieran almacenarse en **Firestore** y visualizarse en un dashboard hecho con **Streamlit**.

---

Qué hace la aplicación?

La aplicación permite:
- Consultar todos los filmes almacenados en la base de datos.
- Buscar películas por título (sin importar mayúsculas o minúsculas).
- Filtrar resultados por director.
- Insertar nuevas películas a través de un formulario.
- Descargar los resultados en formato CSV.
- Ver métricas rápidas (cantidad de filmes, directores únicos y compañías).

Puedes probar la app aquí:  
[**App en Streamlit Cloud**](https://movies-8pkj3p9zlk8dwja3juu2xt.streamlit.app/)

---

Dataset

El punto de partida fue el archivo `movies.csv`, con 1000 registros de películas.  
Desde ahí se realizó:
1. Un análisis exploratorio básico en Jupyter Notebook.  
2. La migración del CSV a Firestore.  
3. La verificación de que la app leyera los datos directamente desde Firestore.

---

Entregables del reto

- **Notebook (EDA + migración)**: [`notebooks/migrate_and_eda.ipynb`](notebooks/migrate_and_eda.ipynb)  
- **Repositorio en GitHub**: [https://github.com/PauPadillaP/movies](https://github.com/PauPadillaP/movies)  
- **App publicada en Streamlit Cloud**: [https://movies-8pkj3p9zlk8dwja3juu2xt.streamlit.app/](https://movies-8pkj3p9zlk8dwja3juu2xt.streamlit.app/)

---

Cómo ejecutarlo en local

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/PauPadillaP/movies.git
   cd movies
