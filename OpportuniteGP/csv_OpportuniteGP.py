#-------------------------------------------------------------------------
# Attention toute modification des questions induits modification du code
# Toute modification des questions aussi
#--------------------------------------------------------------------------

import pandas as pd

# --------------------------------------------------------------------
# Objet DataSets associe a mon questionnaire TypeForm : OpportuniteGP
# Python class to treat response of a TypeForm Form : https://j85vsp5f9lc.typeform.com/to/YvBfAdHB
# Questionnaire accessible ici : https://j85vsp5f9lc.typeform.com/to/YvBfAdHB
# --------------------------------------------------------------------

class csv_opGP :

    def __init__(self) :
        self.questions = None
        self.brutrep = None
        self.men = None
        self.women = None
        self.nogenre = None
        self.fluid = None

    # ---------------------------------------------------
    # Return dataFrame of sex proportions
    # Retourne la part de sexes
    # ---------------------------------------------------
    def have_sex(self,colname='') :
        if colname == '' :
            print('colname not defined')
            return None, None, None, None
        else :
            try :
                df_male = self.brutrep[self.brutrep[colname]=='Un homme']
                df_female = self.brutrep[self.brutrep[colname]=='Une femme']
                df_nogenre = self.brutrep[self.brutrep[colname]=='Non genré']
                df_fluide = self.brutrep[self.brutrep[colname]=='Fluide']
                self.men = df_male
                self.women = df_female
                self.nogenre = df_nogenre
                self.fluid = df_fluide
            except KeyError :
                print('colname not found')
                return None, None, None, None
        return df_male, df_female, df_nogenre, df_fluide

    # ---------------------------------------------------
    # Return dataFrame of ages proportions
    # Retourne la part des tranches d'ages
    # ---------------------------------------------------
    def get_age(self, df=None) :
        if df is None :
            df_minor = self.brutrep[self.brutrep['1age']=='Moins de 18 ans']
            df_young = self.brutrep[self.brutrep['1age']=='Entre 18 et 25 ans']
            df_old = self.brutrep[self.brutrep['1age']=='Entre 26 et 35 ans']
            df_older1 = self.brutrep[self.brutrep['1age']=='Entre 36 et 50 ans']
            df_older_old = self.brutrep[self.brutrep['1age']=='Entre 35 et 50 ans']
            df_olderer = self.brutrep[self.brutrep['1age']=='Entre 51 et 75 ans']
            df_oldest = self.brutrep[self.brutrep['1age']=='76 ans et plus']
            df_older = pd.concat([df_older1, df_older_old])
        else :
            df_minor = df[df['1age']=='Moins de 18 ans']
            df_young = df[df['1age']=='Entre 18 et 25 ans']
            df_old = df[df['1age']=='Entre 26 et 35 ans']
            df_older1 = df[df['1age']=='Entre 36 et 50 ans']
            df_older_old = df[df['1age']=='Entre 35 et 50 ans']
            df_olderer = df[df['1age']=='Entre 51 et 75 ans']
            df_oldest = df[df['1age']=='76 ans et plus']
            df_older = pd.concat([df_older1, df_older_old])
        return df_minor, df_young, df_old, df_older, df_olderer, df_oldest

    # ---------------------------------------------------
    # Return dataFrame of ages proportions by sexe
    # Retourne la part des tranches d'ages par sexes
    # ---------------------------------------------------
    # Param sex = men ; women ; nogenre ; fluid
    # N.B : Par defaut la question retourne le resultat pour les hommes, c'est mon biais. Cheh !
    def trancher_le_sexe(self, sexe='men') :
        df = self._get_sex_df(sexe)

        if df is None :
            print("FR : Sexe non trouve.")
            print("EN : Sex not found.")
            return None
        else :
            return self.get_age(df)

    # ---------------------------------------------------
    # Return dataFrame of sex in paramater
    # Retourne le dataframe du sexe en parametre
    # ---------------------------------------------------
    # Param sex = men ; women ; nogenre ; fluid
    # N.B : Par defaut la question retourne le resultat pour les hommes, c'est mon biais. Cheh !
    def _get_sex_df(self, sexe='men') : 
        if sexe == 'men':
            if self.men is not None :
                df = self.men
            else :
                print ("Pas de messieurs. N'oubliez pas d'executer have_sex() avec d'appeler trancher_les_sexes()")
                print ("Sex not found. Don't forget to run have_sex() before calling trancher_les_sexes()")
        elif sexe == 'women' : 
            if self.women is not None :
                df = self.women
            else :
                print ("Sexe non trouve. N'oubliez pas d'executer have_sex() avec d'appeler trancher_les_sexes()")
                print ("Sex not found. Don't forget to run have_sex() before calling trancher_les_sexes()")
        elif sexe == 'nogenre' : 
            if self.nogenre is not None :
                df = self.nogenre
            else :
                print ("Sexe non trouve. N'oubliez pas d'executer have_sex() avec d'appeler trancher_les_sexes()")
                print ("Sex not found. Don't forget to run have_sex() before calling trancher_les_sexes()")
        elif sexe == 'fluid' : 
            if self.fluid is not None :
                df = self.fluid
            else :
                print ("Sexe non trouve. N'oubliez pas d'executer have_sex() avec d'appeler trancher_les_sexes()")
                print ("Sex not found. Don't forget to run have_sex() before calling trancher_les_sexes()")
        else :
            print("Desole ce sexe n'a pas ete parametre")
            print("Sorry this sex was not configured")
            return None
        return df


    #################################################################################################################################################
    #
    # GRAPH FUNCTIONS
    #
    #################################################################################################################################################

    def data_labels_sex(self, df=None) :
    # Rappels options : messieurs, dames, nongenre, fluide
        data = []
        genres = []
        if df is None :
            if self.men.shape[0] > 0 :
                data.append(self.men.shape[0])
                genres.append('messieurs')
            if self.women.shape[0] > 0 :
                data.append(self.women.shape[0])
                genres.append('dames')
            if self.nogenre.shape[0] > 0 :
                data.append(self.nogenre.shape[0])
                genres.append('nongenre')
            if self.fluid.shape[0] > 0 :
                data.append(self.fluid.shape[0])
                genres.append('fluide')
            return data, genres
        else :
            if self.men.shape[0] > 0 :
                data.append(self.men.shape[0])
                genres.append('messieurs')
            if self.women.shape[0] > 0 :
                data.append(self.women.shape[0])
                genres.append('dames')
            if self.nogenre.shape[0] > 0 :
                data.append(self.nogenre.shape[0])
                genres.append('nongenre')
            if self.fluid.shape[0] > 0 :
                data.append(self.fluid.shape[0])
                genres.append('fluide')
            return data, genres




