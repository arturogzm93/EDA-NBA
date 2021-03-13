
# IMPORTAR LIBRERIAS

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# CARGAR LAS BASES DE DATOS

stats = pd.read_csv('../../BBDD/Seasons_Stats.csv')
players = pd.read_csv('../../BBDD/Players.csv')

# SE JUNTAN AMBAS BASES DE DATOS A TRAVES DE LA COLUMNA JUGADOR

nba = pd.merge(stats, players, on = 'Player')

# SE MUESTRAN LAS 5 PRIMERAS FILAS DEL DATAFRAME

nba.head()

# VISTA GENERAL DEL DATAFRAME

nba.info()

# COMPROBAR LA CANTIDAD DE VALORES NULOS O NAN

nba.isnull().sum()

# SE COMPRUEBA EL TOTAL DE COLUMNAS CON SUS NOMBRES

nba.columns

# BORRAR COLUMNAS INNECESARIAS

nba.drop(columns = ['Unnamed: 0_x', 'Unnamed: 0_y', 'blanl', 'blank2', 'Age', 'Tm', 'GS', 'MP', 'PER', 'TS%', '3PAr', 'FTr',
 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%','BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 
 'FG', 'FG%', '3P', '3P%', '2P', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'BLK', 'PF', 'birth_city', 'birth_state', 
 'collage', 'born'], inplace = True)

 # ASIGNAR NUEVO ORDEN A LAS COLUMNAS

nba = nba[['Year', 'Player', 'Pos', 'height', 'weight', 'G', 'FGA', '3PA', '2PA', 'TRB', 'AST', 'STL', 'TOV', 'PTS']]

# COMPROBAR LAS DIFERENTES POSICIONES EXISTENTES

nba['Pos'].unique()

# SE ESTABLECEN Y SE AGRUPAN TODAS LAS POSICIONES EXISTENTES EN 3 POSICIONES NUEVAS

nba.loc[nba['Pos'] == 'SG', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'PG', 'Pos'] = 'G'
nba.loc[nba['Pos'] == 'PF', 'Pos'] = 'C'
nba.loc[nba['Pos'] == 'SF', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'SF-SG', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'PF-C', 'Pos'] = 'C'
nba.loc[nba['Pos'] == 'SG-PG', 'Pos'] = 'G'
nba.loc[nba['Pos'] == 'SG-PF', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'C-SF', 'Pos'] = 'C'
nba.loc[nba['Pos'] == 'SG-SF', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'C-PF', 'Pos'] = 'C'
nba.loc[nba['Pos'] == 'PG-SG', 'Pos'] = 'G'
nba.loc[nba['Pos'] == 'SF-PF', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'PF-SF', 'Pos'] = 'F'
nba.loc[nba['Pos'] == 'PG-SF', 'Pos'] = 'F'

# RESETEAR LOS VALORES DEL INDICE

nba.reset_index(drop = True, inplace = True)

# CAMBIAR LOS TIPOS DE LAS COLUMNAS

nba = nba.astype({'Year': 'int64',
'FGA': 'int64',
'3PA': 'int64'})

# CREAR NUEVA COLUMNA LLAMADA 'DECADE'

nba['Decade'] = nba['Year']

# CREAR Y EDITAR VALORES EN LA COLUMNA DECADE EN BASE A LOS AÑOS

nba.loc[nba['Decade'] < 1990, 'Decade'] = 1980
nba.loc[(nba['Decade'] > 1989) & (nba['Decade'] < 2000), 'Decade'] = 1990
nba.loc[(nba['Decade'] > 1999) & (nba['Decade'] < 2010), 'Decade'] = 2000
nba.loc[nba['Decade'] > 2009, 'Decade'] = 2010

 # ORDENAR COLUMNAS

nba = nba[['Decade', 'Year', 'Player', 'Pos', 'height', 'weight', 'FGA', '3PA', '2PA', 'PTS', 'TRB', 'AST', 'STL', 'TOV']]

# INFORMACION GENERAL DEL DATAFRAME

nba.info()

# ESTADISTICOS DEL DATAFRAME

round(nba.describe(), 2)

# CORRELACIONES ENTRE VARIABLES

plt.figure(figsize=(20,10))
sns.heatmap(nba.corr(),
           vmin = -1,
           vmax = 1,
           cmap=sns.color_palette("coolwarm", as_cmap=True),
           square = True,
           linewidths = 0.5,);

# SUMATORIOS TOTALES DEL DATAFRAME POR DECADA Y POSICION

round(nba.groupby(['Decade', 'Pos']).sum(), 2)

# SUMATORIOS TOTALES DEL DATAFRAME POR AÑO

round(nba.groupby(['Year']).sum(), 2)

# MEDIAS DE ALTURA Y PESO POR POSICION Y DECADA

plt.figure(figsize=(20,5))

# ALTURA
plt.subplot(1, 2, 1)
sns.barplot(data= nba, x="Decade", y="height", hue='Pos', hue_order=('G', 'F', 'C'))
plt.title('MEDIA DE ALTURAS POR POSICION')
plt.legend().remove()
plt.yticks(np.arange(0, 221, 10))

# PESO
plt.subplot(1, 2, 2)
sns.barplot(data= nba, x="Decade", y="weight", hue='Pos', hue_order=('G', 'F', 'C'))
plt.title('MEDIA DE PESOS POR POSICION')
plt.yticks(np.arange(0, 121, 10));

# CANTIDAD DE TIROS TOTALES

plt.figure(figsize=(20,5))

sns.lineplot(data = nba,
            x = 'Year',
            y = 'FGA',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#003FFB')

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2018, 1))
plt.xticks(rotation=-30)

plt.title('TOTAL DE TIROS POR AÑO');

# COMPARATIVA DE 2PA Y 3PA POR AÑO

plt.figure(figsize=(20, 5))

# TOTAL DE 2PA POR AÑO
plt.subplot(1, 2, 1)
sns.lineplot(data = nba,
            x = 'Year',
            y = '2PA',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#FF7400')
            
plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2018, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL DE 2PA POR AÑO');

# TOTAL DE 3PA POR AÑO
plt.subplot(1, 2, 2)
sns.lineplot(data = nba,
            x = 'Year',
            y = '3PA',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#9500FB')

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2018, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL DE 3PA POR AÑO');

# CANTIDAD DE 2PA Y 3PA POR POSICION Y AÑO

plt.figure(figsize=(20,5))

# FIGURA 2PA
plt.subplot(1, 2, 1)

sns.lineplot(data = nba,
            x = 'Year',
            y = '2PA',
            hue = 'Pos',
            hue_order=('G', 'F', 'C'),
            linewidth = 3,
            estimator= sum,
            ci= None);

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2019, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL DE TIROS DE 2 POR POSICION Y AÑO');

# FIGURA 3PA
plt.subplot(1, 2, 2)

sns.lineplot(data = nba,
            x = 'Year',
            y = '3PA',
            hue = 'Pos',
            hue_order=('G', 'F', 'C'),
            linewidth = 3,
            estimator= sum,
            ci= None);

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2019, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL DE TRIPLES POR POSICION Y AÑO');

# ROBOS Y PERDIDAS POR AÑO

plt.figure(figsize=(20,5))

# ROBOS
plt.subplot(1, 2, 1)
sns.barplot(x = 'Year',
           y = 'STL',
           palette = 'viridis',
           data = nba,
           ci = None,
           estimator=sum)

plt.xticks(rotation=-55)

plt.title('TOTAL ROBOS POR AÑO');

# PERDIDAS
plt.subplot(1, 2, 2)
sns.barplot(x = 'Year',
           y = 'TOV',
           palette = 'rocket_r',
           data = nba,
           ci = None,
           estimator=sum)

plt.xticks(rotation=-55)

plt.title('TOTAL PERDIDAS POR AÑO');

# CREAR DATAFRAME DE PIVOTS

center = nba[nba['Pos'] == 'C']

# EVOLUCION PIVOT 1

plt.figure(figsize=(20,5));

# TRIPLES
plt.subplot(1, 2, 1)
sns.barplot(x = '3PA',
           y = 'Decade',
           palette = 'ch:start=.2,rot=-.3',
           data = center,
           ci = None,
           estimator=sum,
           orient='h')
           
plt.title('TRIPLES TIRADOS POR DECADA');

# PUNTOS
plt.subplot(1, 2, 2)
sns.lineplot(data = center,
            x = 'Year',
            y = 'PTS',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#0AC577')

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2019, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL PUNTOS POR AÑO');

# EVOLUCION PIVOT 2

plt.figure(figsize=(20,5));

# REBOTES

plt.subplot(1, 2, 1)
sns.barplot(x = 'Year',
           y = 'TRB',
           palette = 'viridis',
           data = center,
           ci = None,
           estimator=sum)

plt.xticks(rotation=-55)

plt.title('TOTAL DE REBOTES POR AÑO');

# ASISTENCIAS
plt.subplot(1, 2, 2)
sns.lineplot(data = center,
            x = 'Year',
            y = 'AST',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#DE6B00')

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2019, 2))
plt.xticks(rotation=-55)

plt.title('TOTAL ASISTENCIAS POR AÑO');

# CREAR DATAFRAME DE BASES

guard = nba[nba['Pos'] == 'G']

# EVOLUCION BASE 1

plt.figure(figsize=(20,5));

# TIROS
plt.subplot(1, 2, 1)
sns.barplot(data = guard,
            x = 'Year',
            y = 'FGA',
            linewidth = 3,
            estimator= sum,
            ci= None,
            palette='crest')

plt.xticks(rotation=-55)

plt.title('TIROS TOTALES POR AÑO');

# PUNTOS
plt.subplot(1, 2, 2)
sns.lineplot(data = guard,
            x = 'Year',
            y = 'PTS',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#FB0000')

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2019, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL PUNTOS POR AÑO');

# EVOLUCION BASE 2

plt.figure(figsize=(20,5))

# ASISTENCIAS
plt.subplot(1, 2, 1)
sns.lineplot(data = guard,
            x = 'Year',
            y = 'AST',
            linewidth = 3,
            estimator= sum,
            ci= None,
            color='#003FFB')

plt.axvline(1980, color='#000000', linestyle='--')
plt.axvline(1990, color='#000000', linestyle='--')
plt.axvline(2000, color='#000000', linestyle='--')
plt.axvline(2010, color='#000000', linestyle='--')

plt.xticks(np.arange(1980, 2019, 2))
plt.xticks(rotation=-30)

plt.title('TOTAL ASISTENCIAS POR AÑO');

# REBOTES 
plt.subplot(1, 2, 2)
sns.barplot(x = 'Year',
           y = 'TRB',
           palette = 'dark:salmon_r',
           data = guard,
           ci = None,
           estimator=sum)

plt.xticks(rotation=-55)

plt.title('TOTAL DE REBOTES POR AÑO');
