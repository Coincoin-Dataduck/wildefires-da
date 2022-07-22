# Import des librairies utiles
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu # Nécessaire pour afficher correctement la sidebar
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import requests
import statistics
from sklearn import ensemble
from sklearn.ensemble import HistGradientBoostingClassifier
import math

sns.set_theme(palette='gist_heat_r') #fire theme :eyes:

# Configuration de la page
st.set_page_config(page_title="Projet Wildfires • Streamlit",
                   page_icon=":fire",
                   layout="wide")

# Réduction du padding top sur le volet main
st.write('<style>div.block-container{padding-top:30px;}</style>',
         unsafe_allow_html=True)

# Définition de la side bar
with st.sidebar:
    st.write('<style>div.css-1adrfps.e1fqkh3o2{padding-top:0px;}</style>',
             unsafe_allow_html=True)
    selected = option_menu(
        menu_title = "Projet Wildfires",
        options = ["Introduction", "Allons en Alaska", "Étude « Powerlines »", "Cartes Folium", "Et la sécheresse ?", "Prédiction de feu", "Conclusion"],
        menu_icon="mortarboard-fill",
        icons=["play-circle", "play-circle", "play-circle", "play-circle", "play-circle", "play-circle", "play-circle"]
    )
    st.sidebar.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 18px'><b>Parcours Data Analyst</b><br><i>Formation Continue<br>Promo \"Janvier 2022\"</i></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px'><b>Equipe projet</b><br><i>Clément FONTAINE<br>Fabien LAVERRIERE<br>Phuc NGUYEN DANG</i></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px'><b>Mentor</b><br><i>Gaspard<i></p>", unsafe_allow_html=True)

# Séquences de if pour la rédaction de chaque onglet
if selected == "Introduction":
    st.markdown("### Introduction")
    st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nisi nulla, volutpat sed euismod quis, hendrerit a odio. Integer dignissim volutpat ullamcorper. Integer commodo sapien finibus lacus tempus, sit amet consequat justo mollis. Quisque quis velit erat. In placerat scelerisque felis a laoreet. Curabitur sed justo ac lectus commodo scelerisque. Praesent ut nisi lectus. Vestibulum mollis varius ex sit amet placerat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam erat volutpat.')
    st.write("Streamlit version:", st.__version__)

if selected == "Allons en Alaska":
    st.markdown("### Allons en Alaska")
    st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nisi nulla, volutpat sed euismod quis, hendrerit a odio. Integer dignissim volutpat ullamcorper. Integer commodo sapien finibus lacus tempus, sit amet consequat justo mollis. Quisque quis velit erat. In placerat scelerisque felis a laoreet. Curabitur sed justo ac lectus commodo scelerisque. Praesent ut nisi lectus. Vestibulum mollis varius ex sit amet placerat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam erat volutpat.')

if selected == "Étude « Powerlines »":
    st.markdown(" # Étude « Powerlines »")
    st.markdown(" ## L'anomalie")
    st.markdown('L\'étude de la fréquence des feux par cause révèle une anomalie particulière à partir de l\'année '
                '2011 : une hausse des feux liés aux lignes haute-tension sans précédant')

    tab2, tab1 = st.tabs(["📈 Graphique", "🧮 Classement des États par feu"])
    df_powerline = pd.read_csv('Powerline_db.csv', index_col = 'OBJECTID')

    tab1.subheader('**Classement des années en fonction du nombre de feu**')
    df_fire_by_year = df_powerline['FIRE_YEAR'].value_counts()
    tab1.write(df_fire_by_year.loc[df_fire_by_year > df_fire_by_year.mean()])



    fig = sns.displot(df_powerline['FIRE_YEAR'], kde=True, height=6, aspect=2,);
    plt.axhline(y=df_powerline['FIRE_YEAR'].value_counts().mean(),color='blue',label='Moyenne');
    plt.xlabel("Année")
    plt.ylabel('Feux par an')
    tab2.subheader("Nombre de feu par an dûs aux lignes électrique aux EUA")
    plt.legend();
    tab2.pyplot(fig)

    st.markdown('Quand on regarde l\'evolution de ces feux par état, en se concentrant sur les états qui rapportent plus de 500 '
                'feux, on constate que le texas est le plus gros contributeur de cette anomalie, et de loin.')

    col11, col21 = st.columns(2)
    Top_state = df_powerline['STATE'].value_counts()
    Top_state = Top_state.loc[Top_state > 500]
    Top_state = Top_state.index.tolist()

    with col11:
        selected_state = st.radio("Sélectionnez l'État que vous souhaitez afficher",Top_state)
    with col21:
        if selected_state == Top_state[0]:
            fig = sns.displot(df_powerline.loc[df_powerline['STATE'] == selected_state, 'FIRE_YEAR'], kde=True, height=5, aspect=2);
            plt.axhline(y=df_powerline['FIRE_YEAR'].value_counts().mean()/50, color='blue', label='Moyenne sur l\'ensemble des États');
            plt.title(f'Nombre de feu par an pour {selected_state}', fontsize=15)
            plt.legend();
            st.pyplot(fig)
            st.markdown('L\'échelle est tellement ecrasée que les précédents enregistrements du Texas ne sont pas visible avant '
                        'l\'anomalie, la moyenne inter-état est affichée sur le 0 tellement les écarts de valeurs sont importants.')

        if selected_state == Top_state[1]:
            fig = sns.displot(df_powerline.loc[df_powerline['STATE'] == selected_state, 'FIRE_YEAR'], kde=True, height=5, aspect=2);
            plt.axhline(y=df_powerline['FIRE_YEAR'].value_counts().mean()/50, color='blue', label='Moyenne sur l\'ensemble des états');
            plt.title(f'Nombre de feu par an pour {selected_state}', fontsize=15)
            plt.legend();
            st.pyplot(fig)

        if selected_state == Top_state[2]:
            fig = sns.displot(df_powerline.loc[df_powerline['STATE'] == selected_state, 'FIRE_YEAR'], kde=True, height=5, aspect=2);
            plt.axhline(y=df_powerline['FIRE_YEAR'].value_counts().mean()/50, color='blue', label='Moyenne sur l\'ensemble des états');
            plt.title(f'Nombre de feu par an pour {selected_state}', fontsize=15)
            plt.legend();
            st.pyplot(fig)

        if selected_state == Top_state[3]:
            fig = sns.displot(df_powerline.loc[df_powerline['STATE'] == selected_state, 'FIRE_YEAR'], kde=True, height=5, aspect=2);
            plt.axhline(y=df_powerline['FIRE_YEAR'].value_counts().mean()/50, color='blue', label='Moyenne sur l\'ensemble des états');
            plt.title(f'Nombre de feu par an pour {selected_state}', fontsize=15)
            plt.legend();
            st.pyplot(fig)

        if selected_state == Top_state[4]:
            fig = sns.displot(df_powerline.loc[df_powerline['STATE'] == selected_state, 'FIRE_YEAR'], kde=True, height=5, aspect=2);
            plt.axhline(y=df_powerline['FIRE_YEAR'].value_counts().mean()/50, color='blue', label='Moyenne sur l\'ensemble des états');
            plt.title(f'Nombre de feu par an pour {selected_state}', fontsize=15)
            plt.legend();
            st.pyplot(fig)

    st.markdown('## La recette du Texas pour les feux.')
    with st.expander('Un réseau exposé'):
        st.markdown('Le texas est principalement équipé de lignes aériennes du fait de son réseau ancien et du coût important'
                    ' des lignes enterrées. La majorité du réseau texans est donc très exposé aux incidents qui déclenchent'
                    ' les incendies. ')
        st.markdown('**Les lignes tombées au sol** – Les lignes électriques peuvent tomber au sol (pour de nombreuses raisons), '
        'les disjoncteurs devraient se déclencher, mais dans 30 % des cas, ils consomment trop peu de courant pour '
        'fonctionner correctement et la ligne peut arquer pendant une longue période avant que le courant ne soit coupé')
        st.markdown('**Les contacts avec la végétation** – Les arbres et autres végétaux qui s\'immiscent dans les lignes électriques '
        'peuvent provoquer des incendies de multiples façons, comme la chute d\'un arbre sur une ligne ou une branche qui '
        'touche deux caténaires.')
        st.markdown('**Un contact entre les caténaires** – Les caténaires doivent être suffisamment espacés mais, dans certaines '
        'conditions (comme un vent fort), ils se touchent, forment des arcs et répandent des particules métalliques chaudes '
        'qui peuvent enflammer la végétation sèche alentour.')
        st.markdown('**Une défaillance de l\'équipement** – De nombreux composants des lignes électriques sont conçus pour servir un '
        'certain nombre d\'années et doivent être remplacés à intervalles réguliers. Sinon, ils tombent en panne.')

    with st.expander('Le Texas a son propre réseau électrique'):
        st.markdown('Le Texas est le seul État américain dont le réseau électrique n\'est pas interconnecté au reste du pays. C\'est '
        'l\'une des raisons de la panne massive de l\'hivers 2021. Ainsi, les infrastructures électriques ne sont pas contrôlées au '
        'niveau fédéral et sont gérées de manière incohérente avec le reste des États-Unis.')

    with st.expander('Des infrastructures vieillissantes'):
        st.markdown('Des rapports provenant de nombreuses régions des États-Unis montrent que les compagnies d\'électricité sont '
        'poursuivies pour avoir négligé l\'infrastructure des lignes électriques, notamment au Texas où une grande partie de'
        'l\'infrastructure appartient à des sociétés privées. De par leur conception, elles doivent donner un retour sur '
        'investissement, et non pas fonctionner au profit du plus grand nombre en opposition avec l\'État. Le résultat est '
        'qu\'elles font le minimum pour éviter une défaillance systémique, la plupart du temps c\'est suffisant, mais en cas '
        'de conditions inhabituelles, cela conduit à des événements catastrophiques : comme en 2011.')


    with st.expander('2011'):
        st.markdown('2011 est une année de La Niña, un phénomène météorologique connu pour provoquer la sécheresse au Texas. Cette '
        'condition météorologique entraîne l\'une des pires sécheresses de l\'histoire de l\'État.'
        'Voici une petite analyse des données de la NOA :')

        #import data
        df_drougth = pd.read_csv('4101-pdsi-all-4-1992-2015.csv')
        #conerting to date
        df_drougth['Month'] = df_drougth['Date'].astype('str').apply(lambda x: x[-2:])
        df_drougth['Year'] = df_drougth['Date'].astype('str').apply(lambda x: x[0:4])
        df_drougth['Day'] = '01'
        df_drougth['Date'] = pd.to_datetime(df_drougth[['Month','Year', 'Day']])
        df_drougth.drop(['Month','Year', 'Day'], inplace=True, axis=1) #cleaning
        # seting-up the hue value
        df_drougth['anomaly symbol'] = 1
        df_drougth.loc[df_drougth['Value'] < 0, 'anomaly symbol'] = -1
        df_drougth['x_label'] = df_drougth['Date'].dt.year #seting up the plot
        fig = plt.figure(figsize = (20,6))
        ax = fig.add_subplot(111)
        sns.barplot(x='x_label', y='Value', hue='anomaly symbol', data=df_drougth, ax=ax);
        plt.xticks(rotation=45)
        plt.xlabel("Année")
        plt.ylabel('Index de sévérité de Palmer. 0 = Normal')
        plt.title("Évolution de l'index de sévérité de Palmer", fontsize=20)
        ax.legend_.remove();
        st.pyplot(fig)

        st.markdown('On voit ici très bien la sécheresse qui a été classée comme la pire des 127 dernières années.')

    st.markdown('## Conclusion')
    st.markdown('On peut ici laisser de côté un problème dans l\'enregistrement des données, car en dehors de la période '
                'de sécheresse l\'anomalie disparait. ')
    st.markdown('Ce qui nous laisse une conjonction de facteurs pouvant expliquer l\'anomalie :')
    st.markdown('- Des standards de gestion du réseau électrique très différents du reste de l\'Union')
    st.markdown('- Une sècheresse parmi les plus dures jamais enregistrée')
    st.markdown('- Des equipments vieillissants maintenant dans les conditions tout juste satisfaisante pour la '
                'continuité de l\'activité dans les conditions d\'opération normales')
    st.markdown('On peut craindre que les phénomènes exceptionnels se multipliants ce type d\'anomalie sera amené à '
                'se reproduire')

if selected == "Cartes Folium":
    st.markdown("### L'évolution des feux aux Etats-Unis en 3 cartes")
    st.write('Quelle métrique souhaitez-vous suivre par état sur la période 1992-2015 ?')
    genre = st.radio('Faites un choix :',
                     ('Nombre cumulé de feux', 'Surface brûlée cumulée', 'Pourcentage cumulé du territoire brûlé'), index=0)
    st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nisi nulla, volutpat sed euismod quis, hendrerit a odio. Integer dignissim volutpat ullamcorper. Integer commodo sapien finibus lacus tempus, sit amet consequat justo mollis. Quisque quis velit erat. In placerat scelerisque felis a laoreet. Curabitur sed justo ac lectus commodo scelerisque. Praesent ut nisi lectus. Vestibulum mollis varius ex sit amet placerat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam erat volutpat.')

if selected == "Et la sécheresse ?":
    st.markdown("### Et la sécheresse ?")
    st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nisi nulla, volutpat sed euismod quis, hendrerit a odio. Integer dignissim volutpat ullamcorper. Integer commodo sapien finibus lacus tempus, sit amet consequat justo mollis. Quisque quis velit erat. In placerat scelerisque felis a laoreet. Curabitur sed justo ac lectus commodo scelerisque. Praesent ut nisi lectus. Vestibulum mollis varius ex sit amet placerat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam erat volutpat.')

if selected == "Prédiction de feu":
    model_clf = joblib.load('alaska_model.pkl')

    st.markdown("## Prédiction de feu en Alaska à partir de la Météo du jour ")
    tab1, tab2 = st.tabs(["👀 Essayer le model", "🛠️ Info de construction"])

    with tab1:
        st.header('Test du modèle')
        st.markdown('#### Prédiction actuelles')
        response = requests.request("GET", 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/346836?apikey=H7SbkuzPeNt2SAzWnDyQQ9ZSEbFUoe13&details=True&metrics=True')
        weather_data=pd.DataFrame([[statistics.mean([response.json()[hour]['Temperature']['Value'] for hour in range(0,11)]),
                                    statistics.mean([response.json()[hour]['DewPoint']['Value'] for hour in range(0,11)]),
                                    statistics.mean([response.json()[hour]['Wind']['Speed']['Value'] for hour in range(0,11)]),
                                    statistics.mean([response.json()[hour]['WindGust']['Speed']['Value'] for hour in range(0,11)]),
                                    max([response.json()[hour]['Temperature']['Value'] for hour in range(0,11)]),
                                    min([response.json()[hour]['Temperature']['Value'] for hour in range(0,11)]),
                                    statistics.mean([response.json()[hour]['TotalLiquid']['Value'] for hour in range(0,11)])]],
                                  columns=['TEMP', 'DEWP', 'WDSP', 'GUST', 'MAX', 'MIN', 'PRCP'])
        
        prediction = model_clf.predict_proba(weather_data)
        

        pas_feu, feu = st.columns(2)
        pas_feu.metric("Probabilité d'avoir aucun feu", round(prediction[0][0], 2), "🌳", delta_color='off')
        feu.metric("Probabilité d'avoir un feu", round(prediction[0][1], 2), "🔥", delta_color='off')
        
        st.markdown('Cette prédiction est donnée par rapport au prédiction météo actuelle pour la journée de demain par accuweather pour l\'Alaska')
        temp, maxi, mini, dwpt, wind, gust, precip = st.columns(7)
        temp.metric('Temperature (°C)', round((statistics.mean([response.json()[hour]['Temperature']['Value'] for hour in range(0,11)])-32)*1.8, 2))
        maxi.metric('Temperature max (°C)', round((max([response.json()[hour]['Temperature']['Value'] for hour in range(0,11)])-32)*1.8, 2))
        mini.metric('Temperature min (°C)', round((min([response.json()[hour]['Temperature']['Value'] for hour in range(0,11)])-32)*1.8, 2))
        dwpt.metric('Point de rosé (°C)', round((statistics.mean([response.json()[hour]['DewPoint']['Value'] for hour in range(0,11)])-32)*1.8, 2))
        wind.metric('Vitesse du vent (km/h)',round(statistics.mean([response.json()[hour]['Wind']['Speed']['Value'] for hour in range(0,11)]), 2))
        gust.metric('Rafales de vent (km/h)', round(statistics.mean([response.json()[hour]['WindGust']['Speed']['Value'] for hour in range(0,11)]), 2))
        precip.metric('Hygrometrie',round(statistics.mean([response.json()[hour]['TotalLiquid']['Value'] for hour in range(0,11)]), 2))

        st.markdown('#### Testez vos propres données')

    with tab2:
        st.markdown('Construction')

if selected == "Conclusion":
    st.markdown("### Conclusion")
    st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nisi nulla, volutpat sed euismod quis, hendrerit a odio. Integer dignissim volutpat ullamcorper. Integer commodo sapien finibus lacus tempus, sit amet consequat justo mollis. Quisque quis velit erat. In placerat scelerisque felis a laoreet. Curabitur sed justo ac lectus commodo scelerisque. Praesent ut nisi lectus. Vestibulum mollis varius ex sit amet placerat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam erat volutpat.')

