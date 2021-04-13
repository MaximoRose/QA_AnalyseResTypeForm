import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# For bar charts : https://www.geeksforgeeks.org/how-to-annotate-bars-in-barplot-with-matplotlib-in-python/
import pandas as pd
import seaborn as sns

#import plotly.express as px
import numpy as np
import plotly.graph_objects as px

# Retourne la moyenne generale d'une opinion ou d'un rating
def moyenne_generale_note (liste_notes = [], liste_dtfs = [], nbresp = 1) :
    moyenne = 0.0
    notetotale = 0
    if len(liste_dtfs) == len(liste_notes) :
        for i in range(len(liste_dtfs)) :
            notetotale += liste_dtfs[i].shape[0]*liste_notes[i]
    else :
        print('List of notes must be the same size as list of dtfs')
    if nbresp != 0 :
        moyenne = notetotale / nbresp
    else :
        print ('Cannot divide by 0')

    return moyenne

# Retourne la somme des reponses considerer dans les dataframe listes
def somme_response(liste_dtfs = []) :
    sumresp = 0
    for i in range(len(liste_dtfs)) :
        sumresp += liste_dtfs[i].shape[0]
    
    return sumresp


class plots_mbr_tf :

    def __init__(self, pie_colors=['#f2cb26', '#00a154', '#0083c6', '#dc0036', '#fc8934', '#99248B', '#fb85a7', '#00b3f0'], pie_faveclat = 0.005, pie_titlesize = 14, bar_ticksize = 12, bar_titlesize = 16, bar_axislabelsize = 14, bar_patchsize = 13, pie_autopct='%1.1f%%', pie_figsize =(10, 7), bar_xlbl_rotation = 50, mbar_figsize = (15,9)):
        self.pie_colors = pie_colors
        self.pie_faveclat = pie_faveclat
        self.pie_titlesize = pie_titlesize
        self.pie_autopct = pie_autopct
        self.pie_figsize = pie_figsize
        self.bar_ticksize = bar_ticksize
        self.bar_titlesize = bar_titlesize
        self.bar_axislabelsize = bar_axislabelsize
        self.bar_patchsize = bar_patchsize
        self.bar_xlbl_rotation = bar_xlbl_rotation
        self.mbar_figsize = mbar_figsize
        

    # Les camemberts servent a representer tous les resultats de Single Choice
    def plot_mbr_camembert(self, qtitle = '', list_labels = [], list_dtfs = [], fresh_lbls = []) :
        if (len (list_labels) > 0) and (len(list_labels) ==  len(list_dtfs)) :
            nb_responses = 0
            clean_labels = []
            clean_values = []

            # Delete unnecessary labels (if DTF is None)
            for i in range(len(list_labels)) :
                if list_dtfs[i].shape[0] != 0 :
                    if fresh_lbls != [] and len(fresh_lbls) == len(list_labels) :
                        clean_labels.append(fresh_lbls[i])
                    else :
                        clean_labels.append(list_labels[i])
                    clean_values.append(list_dtfs[i].shape[0])

            # Add number of responses beside label
            for i in range(len(clean_labels)) :
                clean_labels[i] += ' ('+str(clean_values[i])+')'
                nb_responses += clean_values[i]

            # explode slices 
            explode = (self.pie_faveclat,)*len(clean_labels)

            # show plot
            fig = plt.figure(figsize =self.pie_figsize)
            plt.pie(clean_values, labels = clean_labels, autopct=self.pie_autopct, colors=self.pie_colors, explode = explode)
            plt.title(qtitle +'\n (total = '+ str(nb_responses) +')', size = self.pie_titlesize)
            plt.show()

        else :
            print("Lists of labels and list of values don't have the same size")


        return


    # Les bar charts permettent de representer tant les multiple choice que les ratings, que les opinion scales
    def plot_mbr_barchart(self, qtitle = '', list_labels = [], list_dfs = [], bar_xlabel = '', bar_ylabel = '', fresh_lbls=[], nb_responses = 0) :
        nbresp = 0

        clean_labels = []
        clean_values = []
        if len(list_labels) != len(list_dfs) :
            print('labels and values are not the same size')
        elif len(list_labels) == 0 :
            print('no results found')
        else :
            for i in range(len(list_labels)) :
                if fresh_lbls != [] and len(fresh_lbls) == len(list_labels) :
                    clean_labels.append(fresh_lbls[i])
                else :
                    clean_labels.append(list_labels[i])
                clean_values.append(list_dfs[i].shape[0])

        # Get number of options selected
        for i in range(len(list_dfs)) :
            nbresp += list_dfs[i].shape[0]
        
        data = {"labels" : clean_labels, "dtfs" : clean_values}

        df = pd.DataFrame(data, columns=['labels', 'dtfs'])

        # Defining the plot size
        plt.figure(figsize=(14, 9))
        
        # Defining the values for x-axis, y-axis
        # and from which datafarme the values are to be picked
        plots = sns.barplot(x="labels", y="dtfs", data=df)
        
        # Iterrating over the bars one-by-one
        for bar in plots.patches: 
        # Using Matplotlib's annotate function and
        # passing the coordinates where the annotation shall be done
        # x-coordinate: bar.get_x() + bar.get_width() / 2
        # y-coordinate: bar.get_height()
        # free space to be left to make graph pleasing: (0, 8)
        # ha and va stand for the horizontal and vertical alignment
            plots.annotate(format(bar.get_height(), '.0f'), 
                        (bar.get_x() + bar.get_width() / 2, 
                            bar.get_height()), ha='center', va='center',
                        size=self.bar_patchsize, xytext=(0, 8),
                        textcoords='offset points')
        
        # Setting the label for x-axis
        plt.xlabel(bar_xlabel, size=self.bar_axislabelsize)
        
        # Setting the label for y-axis
        plt.ylabel(bar_ylabel, size=self.bar_axislabelsize)
        
        # Setting the title for the graph
        plt.title(qtitle + " \n (Reponses = "+str(nb_responses)+" / Options selectionnees = " + str(nbresp) + ")", size = self.bar_titlesize)

        plt.xticks(rotation=self.bar_xlbl_rotation, size = self.bar_ticksize)

        plt.show()
        
        return


    #     # Les camemberts servent a representer tous les resultats de Single Choice
    # def plot_mbr_heatmap(self, qtitle = '', xlist_labels = [], ylist_labels = [], list_sub_dtfs = [], fresh_lbls = []) :
    #     if (len(ylist_labels) ==  len(list_sub_dtfs)) :
    #         nb_responses = 0
    #         clean_labels = []

    #         heatmap_img = []

    #         # Delete unnecessary labels (if DTF is None)
    #         for i in range(len(ylist_labels)) :
    #             clean_values = []
    #             for j in range(len(list_sub_dtfs[i])) :
    #                 nbvote = list_sub_dtfs[i][j].shape[0]
    #                 clean_values.append(nbvote)
                
    #             if len(clean_values) > 0 :
    #                 if len(clean_values) != len(xlist_labels) :
    #                     print('Les elements de la liste des subdtf devrait avoir la taille de la liste des ylabels')
    #                     return
    #             else :
    #                 print('Les elements de la liste des subdtf devrait avoir la taille de la liste des ylabels')

    #             #heatmap_img.append(clean_values)

    #         # show plot
    #         fig = plt.figure(figsize =(15, 8))
    #         plt.imshow(heatmap_img)

    #         plt.xticks(ticks=np.arange(len(xlist_labels)), labels = xlist_labels, rotation=90)

    #         plt.yticks(ticks=np.arange(len(ylist_labels)), labels = ylist_labels)

    #         plt.show()


    #     else :
    #         print("La liste des labels de l'abscisses n'a pas autant d'elements que la liste des dtfs")


    #     return
    def plot_mbr_multiple_bars(self, qtitle = '', legends = [], xlist_labels = [], list_sub_dtfs = [], bar_indxs = []) :
        x_labels = xlist_labels

        if len(legends) != len(list_sub_dtfs) :
            print ('Please give a legend to each first category element of inputdtf')


        cln_legend_lbl = []
        l_cln_data = []
        l_nb_zer = []
        for i in range(len(list_sub_dtfs)) :
            if len(list_sub_dtfs[i]) > 0 :
                cln_legend_lbl.append(legends[i])
                #print(legends[i])
                # if len(list_sub_dtfs[i]) == len(x_labels) :
                #print("I'm in")
                cln_values = []
                for j in range(len(x_labels)) :
                    cln_values.append(list_sub_dtfs[i][j].shape[0])
            
                data = {"labels" : x_labels, "values" : cln_values}
                df = pd.DataFrame(data, columns=['labels', 'values'])
                nb_zer = df[df['values']==0].shape[0]
                l_nb_zer.append(nb_zer)
                l_cln_data.append(cln_values)


        cln_data = {"legend" : cln_legend_lbl, "dtfs_xlbl_values" : l_cln_data, "nbzeros" : l_nb_zer}
        # print ("cln_legend_lbl len : "+ str(len(cln_legend_lbl)))
        # print ("l_cln_data len : "+ str(len(l_cln_data)))
        # print ("l_nb_zer len : "+ str(len(l_nb_zer)))
        cln_df = pd.DataFrame(cln_data, columns=['legend', 'dtfs_xlbl_values', 'nbzeros'])

        # Il semblerait qu'il mette toujours le premier groupe sur l'undex
        # Le deuxime a une barre width, le troisieme a -1, etc.
        # Pour recentrer les barres en cas d'absence, il va falloir que je filtre sur les valeurs differentes de 0
        # Il faut aussi que je trouve comment agrandir la figure et donc bien definir le ticks
        # En fonction de la taille du dticks et de mon nombre de bar definir la largeur
        # ajuster la position en fonction du nombre de bar a afficher sur le ticks
        # Peut-etre faire des plots conditionnels

        #Rearranger les bar pour avoir une meilleure lisibilite
        # l_nb_zer = []
        # for i in range(len(l_cln_data)) :
        #     # retourne le nombre de lignes du dataframe des 0 => le nombre de 0 dans le dataframe
        #     nb_zer = l_cln_data.[i][l_cln_data.[i]['values']==0].shape[0]
        #     print('number of 0 = '+ nb_zer)
        #     l_nb_zer.append(nb_zer)



        nb_bar_par_index = cln_df.shape[0]
        #print("nb_bar_par_index : "+ str(nb_bar_par_index))
        bar_width = 0.8 / len(cln_legend_lbl)

        # TODO : Ajuster la position des bar : celui qui en a le moins devrait etre a l'extremite
        # Si je n'ai pas de vert, il faudrait que je puisse resserer

        ## Fonctionne pour les 4 barres
        # barvar = [-2*bar_width, 0, bar_width, -bar_width]

        # Fonctionne pour les 2 barres
        # barvar = [bar_width, 0, 2*bar_width, -bar_width]

        barvar = []
        for i in range(len(bar_indxs)) :
            barvar.append(bar_indxs[i]*bar_width)

        

        cln_df = cln_df.sort_values(by=['nbzeros'], ascending = True)

        plt.figure(figsize = self.mbar_figsize)
        # Plotting with numpy and pl
        # for i in range(len(cln_df.shape[0])) :
        cnt = 0
        for i, row in cln_df.iterrows():

            idata = row['dtfs_xlbl_values']
            
            X_axis = np.arange(len(xlist_labels))
            
            plt.bar(X_axis + barvar[i], idata, bar_width, label = row['legend'], color = self.pie_colors[cnt])

            cnt += 1
            #barvar = 0-barvar
            
        plt.xticks(X_axis, xlist_labels)
        # plt.xlabel("Pouet")
        # plt.ylabel("Number of votes")
        plt.title(qtitle)
        plt.legend()
        plt.show()

        return