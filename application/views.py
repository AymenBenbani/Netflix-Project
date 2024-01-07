import numpy as np
import pandas as pd
from django.shortcuts import render
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Définir une palette de couleurs personnalisée inspirée du style Netflix
netflix_colors = ['#E50914', '#B9090B', '#8A8A8A', '#000000', '#FFFFFF', '#F5F5F1']
new_netflix_colors = ['#FF6666', '#FFA07A', '#FFD700', '#FFA500', '#FF8C00', '#87CEEB', '#00BFFF', '#1E90FF', '#4682B4']

# --------------------------------{DASHBOARD}----------------------------------
def index(request):
    return render(request,"index.html")
#----------------------------------------------------------------------------------------


# fonction de creation de diagramme à bandes
def create_bar_chart(data, x_col, y_col, y_label, title):
    # Utilisation de la bibliothèque Plotly Express pour créer un diagramme à bandes
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        labels={'y': y_label},
        title=title,
        color_discrete_sequence=netflix_colors  # Utiliser la palette de couleurs personnalisée
    )
    # Désactiver le zoom et le déplacement (pan) sur les axes x et y
    fig.update_layout(
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',  # Couleur de fond de la zone entière du graphique
        font=dict(color='#FFFFFF'),  # Changer la couleur du texte du titre en blanc
        showlegend=False  # Masquer la légende (si nécessaire)
    )
    # Convertir le graphique en format HTML sans inclure la page complète
    plot_html = fig.to_html(full_html=False)
    return plot_html

# fonction de creation de graphique en courbes empilées
def stacked_line_chart(data):
    # Regrouper les données par année de sortie et type (Movie/TV Show) et calculer le nombre d'occurrences
    donnee = data.groupby(['release_year', 'type']).size().reset_index(name='count')
    # Définir une palette de couleurs pour chaque type (Movie/TV Show)
    color_discrete_map = {'Movie': '#E50914', 'TV Show': '#000000'}
    # Utiliser Plotly Express pour créer un graphique en courbes empilées
    fig = px.area(donnee, x='release_year', y='count', color='type',
                  labels={'count': 'Count', 'release_year': 'Release Year'},
                  title='Number of Titles Over the Years',
                  line_shape='linear', color_discrete_map=color_discrete_map)
    # Personnaliser la mise en page du graphique
    fig.update_layout(
        xaxis=dict(fixedrange=True, showgrid=False),  # Désactiver le zoom et masquer la grille sur l'axe x
        yaxis=dict(fixedrange=True, showgrid=False),  # Désactiver le zoom et masquer la grille sur l'axe y
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',  # Couleur de fond de la zone entière du graphique
        font=dict(color='#FFFFFF'),  # Changer la couleur du texte du titre en blanc
        showlegend=True,  # Afficher la légende
    )
    # Définir une plage spécifique pour l'axe x
    fig.update_layout(xaxis=dict(range=[1942, 2020]))
    # Convertir le graphique en format HTML sans inclure la page complète
    return fig.to_html(full_html=False)


# diagramme à bandes pour les films
def plot_movies(data):
    # Filtrer les données pour ne conserver que les films
    movies = data[data['type'] == 'Movie']
    # Obtenir les dix premiers pays avec le plus grand nombre de films
    top_10_movie_countries = movies['country'].value_counts().head(10)
    # Utiliser la fonction create_bar_chart pour créer le diagramme à bandes
    plot_movies_html = create_bar_chart(
        top_10_movie_countries,
        x_col=top_10_movie_countries.index,
        y_col=top_10_movie_countries.values,
        y_label='Number of Movies',
        title='Top 10 Countries with Most Movies'
    )
    # Retourner le diagramme généré
    return plot_movies_html


# diagramme à bandes pour les émissions de télévision
def plot_tv_shows(data):
    # Filtrer les données pour ne conserver que les émissions de télévision
    tv_shows = data[data['type'] == 'TV Show']
    # Obtenir les dix premiers pays avec le plus grand nombre d'émissions de télévision
    top_10_tv_show_countries = tv_shows['country'].value_counts().head(10)
    # Utiliser la fonction create_bar_chart pour créer le diagramme à bandes
    plot_tv_shows_html = create_bar_chart(
        top_10_tv_show_countries,
        x_col=top_10_tv_show_countries.index,
        y_col=top_10_tv_show_countries.values,
        y_label='Number of TV Shows',
        title='Top 10 Countries with Most TV Shows'
    )
    # Retourner le code HTML du diagramme généré
    return plot_tv_shows_html

# diagramme circulaire pour les titres Netflix
def title_pie(data):
    # Compter le nombre de TV Shows et de Films
    count_by_type = data['type'].value_counts()
    # Créer un graphique circulaire avec Plotly Express en utilisant la palette de couleurs personnalisée
    fig_pie = px.pie(
    count_by_type,
    labels=count_by_type.index,
    values=count_by_type.values,
    title='Percentage of Titles on Netflix',
    color_discrete_sequence=netflix_colors,  # Utiliser la palette de couleurs personnalisée
    names=count_by_type.index)  # Ajouter une légende en utilisant les noms des catégories
    fig_pie.update_layout(
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',  # Couleur de fond de la zone entière du graphique
        font=dict(color='#FFFFFF')  # Changer la couleur du texte du titre en blanc
    )
      # Ajouter une légende en utilisant les noms des catégories

    # Retourner le code HTML du diagramme généré
    return fig_pie.to_html(full_html=False)

# Générer le nuage de mots
def wordcloud(data):
    # Concaténer tous les titres en un seul texte
    titles_text = ' '.join(data['title'].dropna())
    # Créer un objet WordCloud avec des paramètres personnalisés
    wordcloud = WordCloud(
        background_color='black',
        width=365,
        height=450,
        colormap='Reds',  # Choisir une palette de couleurs qui correspond au thème Netflix
        collocations=False  # Désactiver le regroupement des mots fréquents
    ).generate(titles_text)
    # Convertir le nuage de mots en image
    img_buffer = BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    # Convertir l'image en chaîne encodée en base64
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    # Construire la balise HTML pour l'image
    wordcloud_html = f'<img src="data:image/png;base64, {img_str}" alt="Word Cloud">'
    # Retourner la balise HTML du nuage de mots généré
    return wordcloud_html

# diagramme circulaire pour la classification d'âge
def rating_pie(data):
    # Compter le nombre d'occurrences pour chaque classification d'âge
    rating_counts = data['rating'].value_counts()
    # Créer un diagramme circulaire avec des sections concentriques
    fig = px.pie(
        names=rating_counts.index,
        values=rating_counts.values,
        title='Distribution of Age Ratings on Netflix',
        hole=0.4,  # Contrôle le rayon du trou central (plus petit => sections concentriques)
        color_discrete_sequence=new_netflix_colors  # Utiliser la palette de couleurs personnalisée
    )
    # Désactiver le zoom et le déplacement (pan) sur le graphique
    fig.update_layout(
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',  # Couleur de fond de la zone entière du graphique
        font=dict(color='#FFFFFF')  # Changer la couleur du texte du titre en blanc
    )
    # Convertir le graphique en format HTML sans inclure la page complète
    fig_html = fig.to_html(full_html=False)
    # Retourner le code HTML du diagramme généré
    return fig_html

# --------------------------------{DASHBOARD}----------------------------------
def dashboard(request):
    # Charger les données depuis le fichier CSV
    data = pd.read_csv('data\suitable_data\clean_dashboard.csv')
    # Filtrer les données par type (TV Show ou Movie)
    tv_shows = data[data['type'] == 'TV Show']
    movies = data[data['type'] == 'Movie']
    # Calculer le nombre total de titres, de séries TV et de films
    total_title_count = len(data)
    total_tv_shows_count = len(tv_shows)
    total_movies_count = len(movies)
    # Créer des graphiques avec Plotly Express en utilisant la palette de couleurs personnalisée
    plot_tv_shows_html = plot_tv_shows(data)
    plot_movies_html = plot_movies(data) 
    # Créer un diagramme circulaire pour le pourcentage des titres
    title_pie_html = title_pie(data)
    # Créer le Word Cloud des titres Netflix
    wordcloud_html = wordcloud(data)
    # Créer un graphique en courbes empilées avec Plotly Express
    stacked_line_chart_html = stacked_line_chart(data)
    # Créer un diagramme circulaire avec des sections concentriques pour le rating
    rating_pie_html = rating_pie(data)
    # Transmettre les données et les graphiques à la page HTML
    context = {
        'plot_tv_shows': plot_tv_shows_html,
        'plot_movies': plot_movies_html,
        'plot_pie': title_pie_html,
        'wordcloud': wordcloud_html,
        'stacked_line_chart': stacked_line_chart_html,
        'total_tv_shows_count': total_tv_shows_count,  
        'total_movies_count': total_movies_count,
        'total_title_count': total_title_count,
        'age_rating_pie_chart': rating_pie_html,
    }
    # Rendre la page HTML avec les données et graphiques
    return render(request, 'dashboard.html', context)
# ---------------------------------------------------------------------------

# Recherche de posters de films à partir de leurs ID
def fetch_poster(movie_id):
    # Construire l'URL de l'API TMDb en utilisant l'ID du film
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    # Effectuer une requête GET à l'API TMDb
    data = requests.get(url)
    # Convertir la réponse en format JSON
    data = data.json()
    # Extraire le chemin de l'affiche du film à partir des données JSON
    poster_path = data['poster_path']
    # Construire le chemin complet de l'affiche en ajoutant le chemin à la base URL des affiches TMDb
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # Retourner l'URL complet de l'affiche
    return full_path

# Recommander les 5 films les plus similaires
def recommend(movie):
    # Charger le DataFrame contenant des informations sur les films
    movies = pd.read_csv("data\suitable_data\clean_recommender_system.csv")
    #Creating the object CountVectorizer
    cv=CountVectorizer(max_features=9985, stop_words='english')
    # Transforming to counting matrix
    vector=cv.fit_transform(movies['tags'].values.astype('U')).toarray()
    similarity=cosine_similarity(vector)
    # Trouver l'index du film donné dans le DataFrame
    index = movies[movies['title'] == movie].index[0]
    # Trier les distances de similarité en ordre décroissant
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    # Initialiser des listes pour stocker les recommandations de films et leurs affiches
    recommend_movie = []
    recommend_poster = []
    # Récupérer les titres et affiches des 5 films les plus similaires (à partir de l'index 1, car l'index 0 est le film lui-même)
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    # Retourner les titres et affiches des films recommandés
    return recommend_movie, recommend_poster
# --------------------------------{recommenderSystem}----------------------------------
def recommenderSystem(request):
    # Charger les données sur les films
    movies = pd.read_csv("data\suitable_data\clean_recommender_system.csv")
    # Obtenir la liste des titres de films
    movies_list = movies['title'].values
    # Initialisez la variable selected_movie à une valeur par défaut
    selected_movie = None  
    # Vérifier si le formulaire a été soumis (méthode POST)
    if request.method == 'POST':
        # Récupérer le film sélectionné depuis le formulaire
        selected_movie = request.POST.get('selected_movie', None)
        # Si un film est sélectionné
        if selected_movie:
            # Appeler la fonction recommend pour obtenir les recommandations
            movie_name, movie_poster = recommend(selected_movie)
            # Combinez les noms de films et les affiches dans une liste de tuples
            recommendations = list(zip(movie_name, movie_poster))
            # Rendre la page HTML avec les recommandations, la liste de films et le film sélectionné
            return render(
                request,
                'recommenderSystem.html',
                {'recommendations': recommendations, 'movies_list': movies_list, 'selected_movie': selected_movie}
            )
    # Si le formulaire n'a pas été soumis, rendre la page HTML avec la liste de films et le film sélectionné
    return render(
        request,
        'recommenderSystem.html',
        {'movies_list': movies_list, 'selected_movie': selected_movie}
    )    
#----------------------------------------------------------------------------------------
# --------------------------------{weeklyRanking}---------------------------------------
def weeklyRanking(request):
    # Charger les données 
    donnees = pd.read_csv("data\suitable_data\clean_weekly_ranking.csv")
    # Obtenir les pays, les semaines et les catégories uniques dans les données
    countries = donnees['country_name'].unique()
    weeks = donnees['week'].unique()
    # Initialiser les variables de sélection à None
    selected_week = None
    selected_country = None
    selected_category = None
    # Vérifier si le formulaire a été soumis (méthode POST)
    if request.method == 'POST':
        # Récupérer les valeurs sélectionnées depuis le formulaire
        selected_week = request.POST.get('selected_week')
        selected_country = request.POST.get('selected_country')
        selected_category = request.POST.get('selected_category')  
        # Filtrer les données pour le pays, la catégorie et la semaine sélectionnés
        filtered_data = donnees[(donnees['country_name'] == selected_country) & 
                                (donnees['category'] == selected_category) & 
                                (donnees['week'] == selected_week)].head(10)
        # Convertir les données filtrées en un dictionnaire
        data = filtered_data.to_dict(orient='records')
    else:
        # Si le formulaire n'a pas été soumis, utiliser des valeurs par défaut
        default_country = countries[0]
        default_week = weeks[0] 
        # Filtrer les données avec les valeurs par défaut
        default_data = donnees[(donnees['country_name'] == default_country) & 
                               (donnees['category'] == 'Films') & 
                               (donnees['week'] == default_week)].head(10)
        # Convertir les données par défaut en un dictionnaire
        data = default_data.to_dict(orient='records')
    # Rendre la page HTML avec les données, les pays, les semaines et les catégories disponibles
    return render(request, 'weeklyRanking.html', {
        'data': data,
        'countries': countries,
        'weeks': weeks,
        'selected_country': selected_country,
        'selected_category': selected_category,
        'selected_week': selected_week,
    })
#----------------------------------------------------------------------------------------

# --------------------------------{mostPopular}-----------------------------------------
def mostPopular(request):
    # Charger les données 
    donnees = pd.read_csv("data\suitable_data\clean_most_popular.csv")
    # Obtenir les langues d'origine uniques dans les données
    languages = donnees['original_language'].unique()
    # Initialiser la variable de sélection à None
    selected_language = languages[0]
    # Vérifier si le formulaire a été soumis (méthode POST)
    if request.method == 'POST':
        # Récupérer la langue d'origine sélectionnée depuis le formulaire
        selected_language = request.POST.get('selected_language')
        # Filtrer les données pour la langue d'origine sélectionnée et obtenir les 10 films les plus populaires
        filtered_data = donnees[donnees['original_language'] == selected_language].nlargest(10, 'popularity')
        # Convertir les données filtrées en un dictionnaire
        data = filtered_data.to_dict(orient='records')
        # Ajouter le chemin du poster directement dans les données en utilisant la fonction fetch_poster
        for entry in data:
            entry['poster'] = fetch_poster(entry['id'])
    else:
        # Si le formulaire n'a pas été soumis, utiliser une valeur par défaut
        default_language = languages[0]
        # Filtrer les données avec la langue d'origine par défaut et obtenir les 10 films les plus populaires
        default_data = donnees[donnees['original_language'] == default_language].nlargest(10, 'popularity')
        # Convertir les données par défaut en un dictionnaire
        data = default_data.to_dict(orient='records')
        # Ajouter le chemin du poster directement dans les données en utilisant la fonction fetch_poster
        for entry in data:
            entry['poster'] = fetch_poster(entry['id'])    
    # Rendre la page HTML avec les données, les langues et la langue sélectionnée
    return render(request, 'mostPopular.html', {
        'data': data,
        'languages': languages,
        'selected_language': selected_language,
    })
#----------------------------------------------------------------------------------------