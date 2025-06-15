import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Spotify Dashboard", layout="wide")
st.title("🎵 Analyse des chansons les plus streamées sur Spotify")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("Most-Streamed-Songs.csv")
    df["streams"] = df["streams"].astype(str).str.replace(",", "").astype(float)
    return df

df = load_data()

# Filtrage par année
years = sorted(df['released_year'].unique())
selected_year = st.sidebar.selectbox("Filtrer par année de sortie:", options=years)
df_year = df[df['released_year'] == selected_year]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("🎧 Nombre total de chansons", len(df))
col2.metric("📆 Année sélectionnée", selected_year)
col3.metric("📊 Moyenne de streams (M)", f"{df_year['streams'].mean()/1e6:.2f}M")

# Top 10 chansons les plus streamées
st.subheader(f"🔝 Top 10 chansons les plus streamées en {selected_year}")
top_10 = df_year.sort_values(by='streams', ascending=False).head(10)
st.dataframe(top_10[['track_name', 'artist(s)_name', 'streams']], use_container_width=True)

# Graphique : Top 10 artistes avec noms commençant par C
st.subheader("🎤 Top 10 artistes (commençant par C) les plus streamés")
df_C = df[df['artist(s)_name'].str.startswith('C')].groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
df_C.plot(kind='barh', ax=ax, color='skyblue')
ax.set_xlabel("Total des streams")
ax.set_title("Artistes commençant par 'C'")
st.pyplot(fig)

# Répartition des streams par continent (simplifiée)
st.subheader("🌍 Répartition des streams par continent (approximation par pays)")
continent_map = {
    'US': 'Amérique du Nord', 'GB': 'Europe', 'CA': 'Amérique du Nord', 'AU': 'Océanie',
    'BR': 'Amérique du Sud', 'MX': 'Amérique du Nord', 'DE': 'Europe', 'FR': 'Europe',
    'NG': 'Afrique', 'ZA': 'Afrique', 'IN': 'Asie', 'KR': 'Asie', 'JP': 'Asie'
    # Remplir selon tes besoins
}
df['continent'] = df['cover_url'].apply(lambda x: 'Amérique du Nord')  # Valeur fictive si on n'a pas la géo
continent_streams = df.groupby('continent')['streams'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots()
continent_streams.plot(kind='bar', ax=ax2, color='coral')
ax2.set_ylabel("Total des streams")
ax2.set_title("Streams par continent (approx.)")
st.pyplot(fig2)

# Heatmap de corrélation
st.subheader("📈 Corrélation entre les caractéristiques musicales")
features = ['bpm', 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%',
            'instrumentalness_%', 'liveness_%', 'speechiness_%']
correlation_matrix = df[features].corr()
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax3)
ax3.set_title("Corrélation entre variables musicales")
st.pyplot(fig3)

# Footer
st.markdown("""
---
🎓 Réalisé par Daphné Moesha Fotso | Master Big Data & IA — Projet Data Science 2025
""")
