import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# For bar charts : https://www.geeksforgeeks.org/how-to-annotate-bars-in-barplot-with-matplotlib-in-python/
import pandas as pd
import seaborn as sns

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

    def __init__(self, pie_colors=['#f2cb26', '#00a154', '#0083c6', '#dc0036', '#fc8934', '#99248B', '#fb85a7', '#00b3f0'], pie_faveclat = 0.005, pie_titlesize = 14, bar_ticksize = 12, bar_titlesize = 16, bar_axislabelsize = 14, bar_patchsize = 13, pie_autopct='%1.1f%%', pie_figsize =(10, 7), bar_xlbl_rotation = 50):
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
            fig = plt.figure(figsize =(10, 7))
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