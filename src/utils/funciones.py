import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns




def cardinalidad(df_in, umbral_categoria, umbral_countinua):
    cardinalidad = [df_in[col].nunique() for col in df_in.columns]
    cardinalidad_por = [df_in[col].nunique()/len(df_in[col]) * 100 for col in df_in.columns]
    dict_df = {"Card": cardinalidad, "%_Card": cardinalidad_por}
    nuevo_df = pd.DataFrame(dict_df, index=df_in.columns)
    nuevo_df["Tipo_var"] = "Categórica"
    nuevo_df.loc[nuevo_df["Card"] == 2, "Tipo_var"] = "Binaria"
    nuevo_df.loc[nuevo_df["Card"] >= umbral_categoria, "Tipo_var"] = "Numerica Discreta"
    nuevo_df.loc[nuevo_df["%_Card"] >= umbral_countinua, "Tipo_var"] = "Numerica Continua"
    return nuevo_df




def pinta_histograma(df, columnas_num, bins = "auto", kde = True):
    
    num_columnas = len(columnas_num)
    num_filas = (num_columnas // 2) + (num_columnas % 2)
    fig, axs = plt.subplots(num_filas, 2, figsize = (15, 5 * num_filas))
    axs = axs.flatten()
    for i, col in enumerate(columnas_num):
        if type(bins) == list:
            sns.histplot(x = col, kde = kde, data=df, bins=bins[i], ax = axs[i])
        else:
            sns.histplot(x = col, kde = kde, data=df, bins=bins, ax = axs[i])
            
        axs[i].set_title(f"Histograma y KDE de {col}")
        axs[i].set_ylabel('Número de valores')
    
    for j in range(i + 1, num_filas * 2):
        axs[j].axis('off')

    plt.tight_layout()
    plt.show();


def pinta_categoricas(df, columnas_cat, relativa = False):
    num_columnas = len(columnas_cat)
    num_filas = (num_columnas // 2) + (num_columnas % 2)
    fig, axs = plt.subplots(num_filas, 2, figsize = (15, 5 * num_filas))
    axs = axs.flatten()
    for i, col in enumerate(columnas_cat):
        if relativa:
            columna = pd.DataFrame(df[col].value_counts(normalize = True) * 100)
            columna.columns = ["frecuencias_relativas"]
            sns.barplot(x = columna.index, y = columna["frecuencias_relativas"], palette="viridis", data=columna, hue=columna.index, ax = axs[i])
            axs[i].set_title(f"Distribución de {col}")
            for k in axs[i].containers:
                labels = [f"{v.get_height():.1f}" for v in k]
                axs[i].bar_label(k, labels = labels)
            
        else:
            sns.countplot(x = col, data=df, palette="viridis", hue=col, ax = axs[i])
            axs[i].set_title(f"Distribución de {col}")
            axs[i].set_ylabel('Frecuencia')
            for k in axs[i].containers:
                axs[i].bar_label(k,)
    for j in range(i + 1, num_filas * 2):
        axs[j].axis('off')
    plt.tight_layout()
    plt.show();



def pinta_hist_box(df, columnas_num, bins = "auto", kde = True, whisker = 1.5):
    if type(columnas_num) == list:
        num_columnas = len(columnas_num)
        fig, axs = plt.subplots(num_columnas, 2, figsize = (15, 5 * num_columnas))
        for i, col in enumerate(columnas_num):
            if df[col].dtype in ['int64', 'float64']:
                # Hist y KDE
                if num_columnas > 1:
                    if type(bins) == list and len(bins) == num_columnas:
                        sns.histplot(x = col, kde = kde, data=df, bins=bins[i], ax = axs[i,0])
                    else:
                        sns.histplot(x = col, kde = kde, data=df, bins=bins, ax = axs[i,0])
                    axs[i,0].set_title(f"Histograma y KDE de {col}")
                    axs[i,0].set_ylabel('Número de valores')
                else:
                    sns.histplot(x = col, kde = kde, data=df, bins=bins, ax = axs[0])
                    axs[0].set_title(f"Histograma y KDE de {col}")
                    axs[0].set_ylabel('Número de valores')

                # Boxplot
                if num_columnas > 1:
                    sns.boxplot(x=col, data = df, ax=axs[i,1], whis=whisker)
                    axs[i,1].set_title(f'Boxplot de {col}')
                else:
                    sns.boxplot(x=col, data = df, ax=axs[1], whis=whisker)
                    axs[1].set_title(f'Boxplot de {col}')
    

        plt.tight_layout()
        plt.show();




def pinta_histogramas_cat_num(df, columna_cat, columna_num, bins = "auto", kde = True):
    
    num_columnas = df[columna_cat].nunique()
    num_filas = (num_columnas // 3)
    if num_columnas % 3 != 0:
        num_filas += 1
    fig, axs = plt.subplots(num_filas, 3, figsize = (12, 4 * num_filas))
    axs = axs.flatten()
    for i, val in enumerate(df[columna_cat].unique()):
        valores_x = df.loc[df[columna_cat] == val, columna_num]
        sns.histplot(x = valores_x, kde = kde, data=df, bins=bins, ax = axs[i], hue=columna_cat)
            
        axs[i].set_title(f"Histograma y KDE de {columna_num}, {val}")
        axs[i].set_ylabel('Número de valores')

        plt.legend([], [], frameon = False)
    
    for j in range(i + 1, num_filas * 3):
        axs[j].axis('off')

    plt.tight_layout()
    plt.show();



def comparacion_categoricas(df, col_1, col_2, col_3 = None, relativa = False):
    if col_3:
        columnas = [col_1, col_2, col_3]
    else:
        columnas = [col_1, col_2]
        tabla_contingencia = pd.crosstab(df[col_1], df[col_2], margins=False)
        print(tabla_contingencia)
    fig, axs = plt.subplots(1,len(columnas), figsize = (10, 6))
    fig.suptitle(f"Comparacion de {", ".join(columnas)} ")
    
    for i, col in enumerate(columnas):

        if relativa:
            relativas = pd.DataFrame(df[col].value_counts(normalize = True) * 100)
            relativas.columns = ["frecuencias_relativas"]
            sns.barplot(x = relativas.index , y = "frecuencias_relativas", data = relativas, hue= relativas.index, ax = axs[i])
            axs[i].set_title(f"Gráfico de barras de {col}")
            axs[i].set_ylabel("Frecuencia absoluta")
            for k in axs[i].containers:
                labels = [f"{v.get_height():.1f}%" for v in k]
                axs[i].bar_label(k, labels = labels)

        else:
            sns.countplot(x = col, data = df, hue= col, ax = axs[i])
            axs[i].set_title(f"Gráfico de barras de {col}")
            axs[i].set_ylabel("Frecuencia absoluta")
            for k in axs[i].containers:
                axs[i].bar_label(k,)

            
    plt.tight_layout();

    if relativa:
        if col_3:
            relativas = df.groupby([col_2, col_3], as_index = False)[col_1].value_counts(normalize = True)
            relativas["proportion"] *= 100
            fig2 = sns.catplot(x = col_1, y = "proportion", col = col_2, hue = col_3, data= relativas, kind = "bar")
            for ax in fig2.axes.ravel():
                for k in ax.containers:
                    labels = [f"{v.get_height():.1f}%" for v in k]
                    ax.bar_label(k, labels = labels)
        else:
            relativas = df.groupby([col_2], as_index = False)[col_1].value_counts(normalize = True)
            relativas["proportion"] *= 100
            fig2 = sns.catplot(x = col_1, y = "proportion", col = col_2, hue = col_1, data= relativas, kind = "bar")
            for ax in fig2.axes.ravel():
                for k in ax.containers:
                    labels = [f"{v.get_height():.1f}%" for v in k]
                    ax.bar_label(k, labels = labels)
    else:
        if col_3:
            fig2 = sns.catplot(x = col_1, col = col_2, hue = col_3, data= df, kind = "count")
            for ax in fig2.axes.ravel():
                for k in ax.containers:
                    ax.bar_label(k,)
        else:
            fig2 = sns.catplot(x = col_1, col = col_2, hue = col_1, data= df, kind = "count")
            for ax in fig2.axes.ravel():
                for k in ax.containers:
                    ax.bar_label(k,)
    
    plt.show();


def pinta_serie_temp(df, columnas_num, una_grafica = False, col_temporal = None, col_temporal_index = True, minimo = None, maximo = None):
    num_columnas = len(columnas_num)
    num_filas = (num_columnas // 2) + (num_columnas % 2)
    
    if minimo and maximo:
        cond_max = df.index <= maximo
        cond_min = df.index >= minimo
        df = df[cond_max & cond_min]
    elif maximo:
        cond_max = df.index <= maximo
        df = df[cond_max]
    elif minimo:
        cond_min = df.index >= minimo
        df = df[cond_min]
    if una_grafica:
        fig, axs = plt.subplots(1,1, figsize = (10, 7))
        for i, col in enumerate(columnas_num):
            if col_temporal_index:
                sns.lineplot(x = df.index, y = col, data=df, ax = axs, label = f"{col}", alpha = 0.7)
            else:
                sns.lineplot(x = col_temporal, y = col, data=df, ax = axs, label = f"{col}", alpha = 0.7)
        
        axs.set_title(f"Series temporales de {" ".join(columnas_num)}")
        axs.set_ylabel("")
        plt.legend()
    else:
        fig, axs = plt.subplots(num_filas, 2, figsize = (18, 5 * num_filas))
        axs = axs.flatten()
        for i, col in enumerate(columnas_num):
            if col_temporal_index:
                sns.lineplot(x = df.index, y = col, data=df, ax = axs[i])
            else:
                sns.lineplot(x = col_temporal, y = col, data=df, ax = axs[i])
            axs[i].set_title(f"Serie temporal de {col}")
            
        
        for j in range(i + 1, num_filas * 2):
            axs[j].axis('off')

    plt.tight_layout()
    plt.show();


def dispersion_hasta_cuatro(df, col_x, col_y, col_color = None, size = None, escala = 1, multiplicador_tamano = 0.5):
    minimo = df[size].min() * multiplicador_tamano
    maximo = df[size].max() * multiplicador_tamano
    fig, axs = plt.subplots(1,1,figsize = (10,8))
    axs.set_title(f"Diagrama de dispersión de {col_x} y {col_y}")
    if size and col_color:
        if type(size) == str:
            scatter = sns.scatterplot(x = col_x, y = col_y, size = df[size] * escala, 
                            sizes = (minimo, maximo), hue = col_color, data=df, 
                            alpha = .7, palette = "viridis")
        else:
            scatter = sns.scatterplot(x = col_x, y = col_y, s = size, hue = col_color, 
                            data=df, alpha = .7)
    elif size:
        if type(size) == str:
            scatter= sns.scatterplot(x = col_x, y = col_y, size = df[size] * escala, 
                            sizes = (minimo, maximo), data=df, alpha = .7, 
                            color = "green")
        else:
            scatter = sns.scatterplot(x = col_x, y = col_y, s = size, data=df, alpha = .7,
                            color = "green")
    elif col_color:
        scatter = sns.scatterplot(x = col_x, y = col_y, hue = col_color, data=df,
                        alpha = .7, s = 35, palette = "viridis")
    else:
        scatter = sns.scatterplot(x = col_x, y = col_y, data=df, alpha = .7,
                        color = "green", s = 35)
    
    legend = axs.legend(ncol = 2, loc = "upper right", frameon = False, labelspacing = 2)

    
    plt.show();