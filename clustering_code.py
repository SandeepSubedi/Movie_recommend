import pre_processing
from sklearn.cluster import KMeans
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def clustered_final_df(df):
    df['Cluster_Id']=None

    kmeans=KMeans(n_clusters=20)
    features=df[['P_Genre','S_Genre','T_Genre']]
    kmeans.fit(features)
    df['Cluster_Id']=kmeans.predict(features)
    return df

def cluster_everything(input_movie):
    df=pre_processing.pre_process_all()
    df=clustered_final_df(df)
    #print(df)
    # plt.scatter(df['P_Genre'],df['Cluster_Id'])
    # plt.show()
    df.to_csv("Dataset_to_plot.csv")
    
    input_movie=input_movie.lower()
    try:
        movie_not_found=df.loc[~df['Movie'].str.contains(input_movie)]
        #print(movie_not_found)
        if len(movie_not_found)==0:
            print("Movie not found")
            return 0
        get_cluster=df['Cluster_Id'].loc[df['Movie'].str.contains(input_movie)].values[0]
        similar_movies_list=df['Movie'].loc[df['Cluster_Id']==get_cluster].values
        #print("found")
        return similar_movies_list
    except:
        print("Movie not found")
        return 0

test=cluster_everything('beast')


