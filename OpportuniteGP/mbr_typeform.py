# https://developer.typeform.com/create/reference/retrieve-form/

# Convention : Les resultats s'appellent "res_{formid}.csv"
# Rule : Results are named "res_{formid}.csv"

import requests # pip install request // si necessaire 
import json
import pandas as pd


###############################################################################################################################
# Fonction permettant de nettoyer les resultats pour des graphs un peu plus agreable
# + Quelques fonctions de traitement des dataset en fonction de parametre de formulaires
###############################################################################################################################

# Elimine les options qui n'ont jamais ete selectionnees pour dropdowns et autre signe choices
# label est la liste des options possibles pour une questions
# Values correspond au dataframe associe
def clean_lists_for_cheesepie(labels = [], values = []) :
    clean_labels = []
    clean_values = []
    if len(labels) != len(values) :
        print('labels and values are not the same size')
    elif len(labels) == 0 :
        print('no results found')
    else :
        for i in range(len(labels)) :
            if values[i].shape[0] != 0 :
                clean_labels.append(labels[i])
                clean_values.append(values[i].shape[0])
    return clean_labels, clean_values


# Elimine les options qui n'ont jamais ete selectionnees pour multiple choices
# label est la liste des options possibles pour une questions
# Values correspond au dataframe associe
# nnbreps est le nombre de repondants du questionnaire, ou la totalite sur laquelle on veut faire les taux
def clean_lists_multiplechoices_histogramme(labels = [], values = [], nbreps = 1) :
    clean_labels = []
    clean_values = []
    if len(labels) != len(values) :
        print('labels and values are not the same size')
    elif len(labels) == 0 :
        print('no results found')
    else :
        for i in range(len(labels)) :
            clean_labels.append(labels[i])
            clean_values.append(values[i].shape[0])
    return clean_labels, clean_values


# Recupere les dataframes associe a chaque valeur possible d'une colonne de sinngle choice
# get subresults of dataframe based on single columns values
def df_singlecolumn_subresults(main_dtf=[], l_options = [], q_name='') :
    labels = []
    dtfs = []
    if main_dtf is not None :
        for i in range(len(l_options)) :
            dftemp = main_dtf[main_dtf[q_name]==l_options[i]]
            dtfs.append(dftemp)
            labels.append(l_options[i])
    else :
        print('No result found for '+q_name)
    return labels, dtfs



###############################################################################################################################
# Class tf_struct is more that a struct
# It gives all the functions needed to cross-analyze form structure (given by API) and form results (dropped as CSV)
###############################################################################################################################

class tf_struct :

    def __init__(self, formid=''):
        self.formid = formid
        self.form_structure = None
        self.form_fields = None
        self.form_results = None


    # Call typeform API to get Form's structure
    def get_form_structure (self):
        if self.formid == '' : 
            print("Don't be ridiculous. Gibme a form ID")
        else :
            url = 'https://api.typeform.com/forms/'+self.formid
            json_url = requests.get(url)
            data = json.loads(json_url.text)
            self.form_structure = data
        return data


    # Retourne le titre du formulaire
    def get_title(self) :
        try :
            formtitle = self.form_structure['title']
        except  KeyError :
            print('no title found')
        return formtitle


    # Retourne l'ensemble des questions
    def get_fields(self) :
        try :
            formfields = self.form_structure['fields']
            self.form_fields = formfields
        except :
            print('no fields found in Form')
        return formfields


    # Retourne les questions du formulaire
    def get_form_responses(self, respfolder = "./responses/") :
        filename = respfolder + 'res_' + self.formid+'.csv'
        dt_GP = pd.read_csv(filename)
        self.form_results = dt_GP
        return dt_GP


    # Retourne le nombre de reponses au questionnaire
    def get_nb_responses(self) :
        nb_resp = self.form_results.shape[0]
        return nb_resp



    # Retourne les groupes trouves dans le formulaire
    def get_groups(self) :
        formgroups = []
        try :
            fields = self.form_structure['fields']
        except :
            print('no fields found in Form')
            return formgroups
        for i in range(len(fields)) :
            if fields[i]["type"] == "group" :
                formgroups.append({'id':fields[i]["id"],'title':fields[i]["title"]})
                print ('Group '+ str(len(formgroups)) + ' : '+fields[i]["title"])
            else :
                print('Following element was not grouped : '+fields[i])
        return formgroups



    # Retourne les options et les resultats par options pour une questions donnee dans un groupe donne
    def get_results(self, gidx=-1, qid='') :
        qoptions = []
        qvalues = []
        qtitle = ''
        qidx_ing = 0
        if qid == '' :
            print('Please give question id.')
            return
        if gidx == -1 :
            print('Please give group idex.')
            return
        else :
            group_questions = self.form_fields[gidx]['properties']['fields']

            for i in range(len(group_questions)) :

                if group_questions[i]['id'] == qid :
                    qidx_ing = i
                    qtitle = group_questions[i]['title']
                    # print(qtitle)
                    qtype = group_questions[i]['type']
                    # print(qtype)

                    if qtype == 'dropdown' :
                        qoptions = self._get_dp_options(gidx=gidx, qid=qid, qidx=qidx_ing)
                        qvalues = self._get_dp_values (qname=qtitle, qlabels=qoptions)


                    elif qtype == 'yes_no' :
                        qoptions = ['oui', 'non']
                        qvalues = self._get_yn_values(qname=qtitle)


                    elif qtype == 'picture_choice' or qtype == 'multiple_choice' :

                        multiple_c = self.form_fields[gidx]['properties']['fields'][qidx_ing]['properties']['allow_multiple_selection']
                        other_o = self.form_fields[gidx]['properties']['fields'][qidx_ing]['properties']['allow_other_choice']
                        qoptions = self._get_pc_ou_mc_options(gidx=gidx, qid=qid, qidx=qidx_ing, multiplec = multiple_c, otherchoice = other_o)

                        if not multiple_c :
                            qvalues = self._get_single_pc_ou_mc_values (qname=qtitle, qlabels=qoptions, otherchoice = other_o)
                        else :
                            qvalues = self._get_multiple_pc_ou_mc_values (qname=qtitle, qlabels=qoptions)
                    
                    elif qtype == 'opinion_scale' :
                        qoptions = self._get_opinion_options(gidx=gidx, qid=qid, qidx=qidx_ing)
                        # Dans le cas de l'opinion, les resultats retournes ne sont pas les resultats mais la taille de l'echelle
                        qvalues = self._get_opinion_size(gidx=gidx, qid=qid, qidx=qidx_ing)

                    elif qtype == 'rating' :
                        qoptions = self._set_rating_values(gidx=gidx, qid=qid, qidx=qidx_ing)
                        # Dans le cas de l'opinion, les resultats retournes ne sont pas les resultats mais la taille de l'echelle
                        qvalues = self._get_rating_values(qname=qtitle, qlabels=qoptions)

                    else :
                        print("Question type not found in function. There must be another way, or you'll have to modify code...")

                    break
    
        return qtitle, qoptions, qvalues


    



    # Retoune le type d'une question dans un groupe donne avec un identifiant passe en argument
    def get_qtype(self, gidx=-1, qid='') :
        qidx_ing = 0
        qtype = ''
        if qid == '' :
            print('Please give question id.')
            return
        if gidx == -1 :
            print('Please give group idex.')
            return
        else :
            group_questions = self.form_fields[gidx]['properties']['fields']
            for i in range(len(group_questions)) :
                if group_questions[i]['id'] == qid :
                    qidx_ing = i
                    qtype = group_questions[i]['type']
                    break
        
        return qtype


    # Return question title
    def get_q_title(self, gidx=-1, qid='') :
        qidx_ing = 0
        qtype = ''
        if qid == '' :
            print('Please give question id.')
            return
        if gidx == -1 :
            print('Please give group idex.')
            return
        else :
            group_questions = self.form_fields[gidx]['properties']['fields']
            for i in range(len(group_questions)) :
                if group_questions[i]['id'] == qid :
                    qidx_ing = i
                    qtype = group_questions[i]['title']
                    break
        
        return qtype
    


    # Retourne le dataframe des repondant pour une question donnee et une reponse attendue
    def get_question_specific_resp_dtf(self, gidx=-1, qid='', label ='', isnot = False) :
        qidx_ing = 0
        if qid == '' :
            print('Please give question id.')
            return
        if gidx == -1 :
            print('Please give group idex.')
            return
        else :
            group_questions = self.form_fields[gidx]['properties']['fields']
            for i in range(len(group_questions)) :
                if group_questions[i]['id'] == qid :
                    qidx_ing = i
                    qtitle = group_questions[i]['title']
                    # print(qtitle)
                    qtype = group_questions[i]['type']
                    # print(qtype)
                    if qtype in ['dropdown', 'yes_no'] :
                        qvalues = self._get_df_singlechoice_qvalue (qname=qtitle, rlabel=label, isnot=isnot)


                    elif qtype == 'picture_choice' or qtype == 'multiple_choice' :
                        multiple_c = self.form_fields[gidx]['properties']['fields'][qidx_ing]['properties']['allow_multiple_selection']
                        if not multiple_c :
                            qvalues = self._get_df_singlechoice_qvalue (qname=qtitle, rlabel=label, isnot=isnot)
                        else :
                            qvalues = self._get_df_multiplechoice_qvalue (rlabel=label, isnot=isnot)
                    
                    else :

                        int_label = int(label)

                        if qtype in ['opinion_scale', 'rating' ] :
                            qvalues = self.form_results[self.form_results[qtitle] == int_label]

                        else :
                            print ('Unknown question type')


        return qvalues


    

    # Retourne le dataframe des repondant pour une question donnee et une reponse attendue
    def get_sub_question_specific_dtf(self, gidx=-1, qid='', inputdtf = None) :
        qidx_ing = 0
        if qid == '' :
            print('Please give question id.')
            return
        if gidx == -1 :
            print('Please give group idex.')
            return
        if inputdtf is None :
            print('Please give inputdtf or use get_question_specific_resp_dtf().')
            return
        else :
            group_questions = self.form_fields[gidx]['properties']['fields']

            for i in range(len(group_questions)) :
                if group_questions[i]['id'] == qid :
                    qidx_ing = i
                    qtitle = group_questions[i]['title']
                    # print(qtitle)
                    qtype = group_questions[i]['type']
                    # print(qtype)

                    if qtype == 'dropdown' :
                        qoptions = self._get_dp_options(gidx=gidx, qid=qid, qidx=qidx_ing)
                        qvalues = self._get_subdf_dp_values (qname=qtitle, qlabels=qoptions, inputdtf=inputdtf)


                    elif qtype == 'yes_no' :
                        qoptions = ['oui', 'non']
                        qvalues = self._get_subdf_yn_values(qname=qtitle, inputdtf=inputdtf)


                    elif qtype == 'picture_choice' or qtype == 'multiple_choice' :
                        multiple_c = self.form_fields[gidx]['properties']['fields'][qidx_ing]['properties']['allow_multiple_selection']
                        other_o = self.form_fields[gidx]['properties']['fields'][qidx_ing]['properties']['allow_other_choice']
                        qoptions = self._get_pc_ou_mc_options(gidx=gidx, qid=qid, qidx=qidx_ing, multiplec = multiple_c, otherchoice = other_o)                       

                        if not multiple_c :
                            qvalues = self._get_subdf_sc_pc_mc_values(qname=qtitle, qlabels=qoptions, otherchoice = other_o, inputdtf=inputdtf)
                        else :
                            qvalues = self._get_subdtf_multiple_pc_mc_values(qname=qtitle, qlabels=qoptions, inputdtf=inputdtf)

                    break

        return qtitle, qoptions, qvalues


    # Get mean number of item selected for a multiple choice
    #-----------------------------------------------------------------------------------------------------------------------
    # Fonctions pour ne recuperer qu'un seul dataframe, celui de reponses a une question specifique
    # get dropdown values
    # returns number of hit for each label of dropdown
    def get_meanNbItem_in_multipleChoice(self, possiblechoices = [], label_expt = 'Howmuchwoodwouldawoodchuckchuckifawoodchuckcouldchuckwood') :
        list_res = []
        meanV = 0.0
        nb_excpt = 0
        if possiblechoices == [] :
            print('Liste of options empty')
            return
        else :
            df = self.form_results
            for index, row in df.iterrows():
                nb_opt = 0
                for i in range(len(possiblechoices)) :
                    if row[possiblechoices[i]] == possiblechoices[i] :
                        if row[possiblechoices[i]] != label_expt :
                            nb_opt += 1
                        else : 
                            nb_excpt += 1
                list_res.append(nb_opt)
            total = (len(list_res) + nb_excpt)
            seum = sum(list_res)
            meanV = seum / total

        return meanV



    #-------------------------------------------------
    # CLASS PROPRIETARY METHODS
    #-------------------------------------------------


    # get dropdown options
    # returns list of label options
    def _get_dp_options(self, gidx=-1, qid='', qidx=-1) :
        choices = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['choices']
        labels = []
        for j in range(len(choices)) :
            # print(choices[j]["label"])
            labels.append(choices[j]["label"])
        return labels



    # get dropdown values
    # returns number of hit for each label of dropdown
    def _get_dp_values(self, qname='', qlabels = []) :
        dp_values = []
        for i in range(len(qlabels)) :
            df_res = self.form_results[self.form_results[qname]==qlabels[i]]
            # print(str(df_res.shape[0]))
            dp_values.append(df_res)
        return dp_values

    # get dropdown values
    # returns number of hit for each label of dropdown
    def _get_subdf_dp_values(self, qname='', qlabels = [], inputdtf = None) :
        dp_values = []
        for i in range(len(qlabels)) :
            df_res = inputdtf[inputdtf[qname]==qlabels[i]]
            # print(str(df_res.shape[0]))
            dp_values.append(df_res)
        return dp_values


    # get yes_no values
    # returns dataframe of yes and dataframe of no
    def _get_yn_values(self, qname='') :
        dp_values = []
        df_res_y = self.form_results[self.form_results[qname]==1]
        df_res_n = self.form_results[self.form_results[qname]==0]
        dp_values.append(df_res_y)
        dp_values.append(df_res_n)
        return dp_values


    # get yes_no values
    # returns dataframe of yes and dataframe of no (results are 1 or 0)
    def _get_subdf_yn_values(self, qname='', inputdtf = None) :
        dp_values = []
        df_res_y = inputdtf[inputdtf[qname]==1]
        df_res_n = inputdtf[inputdtf[qname]==0]
        dp_values.append(df_res_y)
        dp_values.append(df_res_n)
        return dp_values




    #-----------------------------------------------------------------
    # PICTURE CHOICES  or MULTIPLE CHOICES - return possible options
    # get picture_choice options
    # returns list of label options
    # Integre le nom "Other.x" de la colonne associee dans le CSV
    def _get_pc_ou_mc_options(self, gidx=-1, qid='', qidx=-1, multiplec = False, otherchoice = False) :
        choices = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['choices']
        qt_Pi = self.form_fields[gidx]['properties']['fields'][qidx]['title']

        lastchoicefound = False

        labels = []
        for j in range(len(choices)) :
            # print(choices[j]["label"])
            labels.append(choices[j]["label"])

        # print(labels[-1])        

        if otherchoice :
            if multiplec :
                # print("I'm in")
                for col in self.form_results.columns :
                    if lastchoicefound :
                        labels.append(col)
                        lastchoicefound = False
                        break
                    if col == labels[-1] :
                        # print("Last choice found")
                        lastchoicefound = True
            else :
                # print("I'm in")
                for col in self.form_results.columns :
                    if lastchoicefound :
                        labels.append(col)
                        lastchoicefound = False
                        break
                    if col == qt_Pi :
                        # print("Last choice found")
                        lastchoicefound = True



        return labels



    #-----------------------------------------------------------------
    # PICTURE CHOICES  or MULTIPLE CHOICES - multiple choices = False
    # return data frames associated to each possible choice
    def _get_single_pc_ou_mc_values(self, qname='', qlabels = [],  otherchoice = False) :
        dp_values = []
        lastcolname = 'Neposezjamaisunequestionsouslaformeduneaffirmationonrisqueraitdelaprendrepouruneprescription'
        # If other choice, get colomn last name
        if otherchoice :
            lastcolname = qlabels[-1]
        for i in range(len(qlabels)) :
            # Verifier que le qlabel ne contienne pas Other ou Other.
            if qlabels[i] != lastcolname :
                df_res = self.form_results[self.form_results[qname]==qlabels[i]]
                dp_values.append(df_res)
            else :
                print ('POOOOO')
                df_res = self.form_results[self.form_results[lastcolname].notnull()]
                dp_values.append(df_res)

        return dp_values


    #-----------------------------------------------------------------
    # PICTURE CHOICES  or MULTIPLE CHOICES - multiple choices = False
    # return data frames associated to each possible choice
    def _get_subdf_sc_pc_mc_values(self, qname='', qlabels = [],  otherchoice = False, inputdtf = None) :
        dp_values = []
        lastcolname = 'Neposezjamaisunequestionsouslaformeduneaffirmationonrisqueraitdelaprendrepouruneprescription'
        # If other choice, get colomn last name
        if otherchoice :
            lastcolname = qlabels[-1]
        for i in range(len(qlabels)) :
            # Verifier que le qlabel ne contienne pas Other ou Other.
            if qlabels[i] != lastcolname :
                df_res = inputdtf[inputdtf[qname]==qlabels[i]]
                dp_values.append(df_res)
            else :
                #print ('POOOOO')
                df_res = inputdtf[inputdtf[lastcolname].notnull()]
                dp_values.append(df_res)

        return dp_values



    #-----------------------------------------------------------------
    # PICTURE CHOICES  or MULTIPLE CHOICES - multiple choices = True
    # return data frames associated to each possible choice
    def _get_multiple_pc_ou_mc_values(self, qname='', qlabels = []) :
        dp_values = []

        for i in range(len(qlabels)) :
            for col in self.form_results.columns :
                if col == qlabels[i]:
                    dft = self.form_results[self.form_results[qlabels[i]]==qlabels[i]]
                    dp_values.append(dft)

        return dp_values

    #-----------------------------------------------------------------
    # PICTURE CHOICES  or MULTIPLE CHOICES - multiple choices = True
    # return data frames associated to each possible choice
    def _get_subdtf_multiple_pc_mc_values(self, qname='', qlabels = [], inputdtf = None) :
        dp_values = []

        for i in range(len(qlabels)) :
            for col in inputdtf.columns :
                if col == qlabels[i]:
                    dft = inputdtf[inputdtf[qlabels[i]]==qlabels[i]]
                    dp_values.append(dft)

        return dp_values



    # Retourne les labels de min et max de l'opinion
    def _get_opinion_options(self, gidx=-1, qid='', qidx=-1) :
        choices = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['labels']

        labels = [choices['left'], choices['right']]

        return labels


    # Retourne les labels de min et max de l'opinion
    def _set_rating_values(self, gidx=-1, qid='', qidx=-1) :
        l_res = []
        size = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['steps']
        labels = [*range(1,size+1,1)]
        return labels


    # Retourne les labels de min et max de l'opinion
    def _get_rating_values(self, qname='', qlabels = []) :
        dp_values = []
        lastcolname = 'Neposezjamaisunequestionsouslaformeduneaffirmationonrisqueraitdelaprendrepouruneprescription'
    
        for i in range(len(qlabels)) :
            df_res = self.form_results[self.form_results[qname]==qlabels[i]]
            dp_values.append(df_res)

        return dp_values


    # Retourne les labels de min et max de l'opinion
    def _get_opinion_size(self, gidx=-1, qid='', qidx=-1) :
        l_res = []
        size = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['steps']
        startone = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['start_at_one']
        if startone :
            l_res = [*range(1,size,1)]
        else :
            l_res = [*range(0,size,1)]
        return l_res


    # Get SINGLE DATAFRAME : One option for one question
    #-----------------------------------------------------------------------------------------------------------------------
    # Fonctions pour ne recuperer qu'un seul dataframe, celui de reponses a une question specifique
    # get dropdown values
    # returns number of hit for each label of dropdown
    def _get_df_singlechoice_qvalue(self, qname='', rlabel = '', isnot = False) :
        if not isnot :
            df_res = self.form_results[self.form_results[qname]==rlabel]
        else :
            df_res = self.form_results[self.form_results[qname]!=rlabel]
        return df_res


    # reourne le dataframe associe a une reponse attendue
    def _get_df_multiplechoice_qvalue(self, rlabel = '', isnot = False) :
        if not isnot :
            df_res = self.form_results[self.form_results[rlabel]==rlabel]
        else :
            df_res = self.form_results[self.form_results[rlabel]!=rlabel]
        return df_res




    #-----------------------------------------------------------------
    # DROP FORM STRUCTURE IN A FILE
    # return data frames associated to each possible choice
    # Fonction aui dump le questionnaire dans un fichier, juste pour le plaisir de l'avoir.
    # On peut l'utiliser une fois
    def dump_tform_structure(self):
        if self.formid=='':
            print("Don't be ridiculous. Gibme a form ID")
        else :
            # Dumper un fichier json avec la structure du formulaire
            filename = './forms/'+self.formid+'.json'
            # ATTENTION : adressage de dossier facon LINUX 
            with open(filename, 'w') as mefile:
                json.dump(self.form_structure, mefile, indent=4)
                print('file dumped')

    
    

