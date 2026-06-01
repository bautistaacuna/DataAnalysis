# Spotify Global Music Analysis (2009–2025)

Exploratory and visual analysis of Spotify's global dataset, focusing on music genres, temporal trends and the platform's most popular artists.

---

## Problem Context

Which music genres dominate Spotify? How has explicit content evolved over the years? Is there a relationship between an artist's popularity and their follower count?

This analysis answers these questions through interactive visualizations built with **Plotly**.

---

## Project Structure

```
Spotify - Bar Plot/
├── README.md
├── Spotify.ipynb
├── spotify_data clean.csv
├── generos_todos.png
├── generos_top30.png
├── generos_explicito.png
├── canciones_por_ano.png
├── explicito_por_ano.png
├── generos_top5.png
├── generos_top_5_facet.png
└── artistas_top20.png
```

---

## Dataset

- **Source:** [Spotify Global Music Dataset 2009–2025 — Kaggle](https://www.kaggle.com/datasets/wardabilal/spotify-global-music-dataset-20092025)
- **Description:** Global dataset with songs, artists, genres, popularity and followers
- **Key variables:** `artist_name`, `artist_genres`, `artist_popularity`, `artist_followers`, `track_name`, `track_popularity`, `explicit`, `album_release_date`

---

## Technologies Used

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

---

## Methodology

1. **Initial load and exploration** — shape, dtypes, first rows
2. **Data cleaning:**
   - Converting `album_release_date` to datetime and extracting the year
   - Identifying and handling null values
   - Removing duplicates
   - Creating `main_genre` column from the artist's first genre
3. **Visualizations** — 8 interactive charts with Plotly

---

## Analysis and Findings

### 1. Top 30 music genres by song count
Bar chart with the most represented genres in the dataset, excluding entries without a classified genre.

### 2. Explicit content by genre
Comparison of explicit vs non-explicit song volume for the top 30 genres. Identifies which genres have the highest proportion of explicit content.

### 3. Song releases evolution over time
Time series showing the growth in music production recorded on Spotify from 2009 to 2025.

### 4. Explicit vs non-explicit releases over time
Analysis of how explicit content presence varied year by year, revealing a sustained growth trend.

### 5. Top 5 genres evolution over time
Filtered view of the 5 most popular genres and their evolution year by year.

### 6. Top 20 artists: followers vs popularity (Bubble Chart)
Multidimensional scatter plot where:
- **X Axis:** Number of followers (logarithmic scale)
- **Y Axis:** Artist popularity (0–100)
- **Bubble size:** Number of songs in the dataset
- **Color:** Main music genre

---

## Main Conclusions

- **Pop** and its subgenres dominate the platform by far in terms of song count
- Explicit content has grown steadily since 2015, especially in **rap** and **hip-hop** genres
- There is no perfect linear correlation between followers and popularity: artists with fewer followers can have high popularity due to recent streams
- Music production recorded on Spotify shows a pronounced peak between 2020 and 2023

---

## How to Run the Project

```bash
# 1. Clone the repository
git clone https://github.com/bautistaacuna/DataAnalysis.git

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Open the notebook
jupyter notebook Spotify.ipynb
```

> The `spotify_data clean.csv` file must be in the same folder as the notebook.

---

## Author

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
