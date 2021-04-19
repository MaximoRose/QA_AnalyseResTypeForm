# https://developer.typeform.com/create/reference/retrieve-form/

# Convention : Les resultats s'appellent "res_{formid}.csv"
# Rule : Results are named "res_{formid}.csv"

import requests # pip install request // si necessaire 
import json
import pandas as pd


###############################################################################################################################
# Class tf_struct is more that a struct
# It gives all the functions needed to cross-analyze form structure (given by API) and form results (dropped as CSV)
###############################################################################################################################

class mbr_typeFrom :

    def __init__(self, formid=''):
        self.formid = formid
        if formid != '' :
            # Recupere toute la structure du questionnaire que retoune l'API
            self.form_structure = self.get_form_structure(formid = formid)
            # Recupere le titre du questionnaire
            self.form_title = self.get_form_title()
            # Recupere seulement les champs associes aux questions
            self.form_fields = self.get_form_fields()
            # Recupere le fichier de reponse dans le dossier 'responses'. Le fichier doit etre nomme "res_{id questionnaire}.csv"
            self.form_results = self.get_form_responses()
            # Retourne et ecrit les groupes definis dans le questionnaire
            self.form_groups = self.get_form_groups()
        else :
            self.form_structure = None
            self.form_title = None
            self.form_fields = None
            self.form_results = None
            self.form_groups = None


    # Call typeform API to get Form's structure
    def get_form_structure (self, formid=''):
        url = 'https://api.typeform.com/forms/'+formid
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        self.form_structure = data
        return data


    # Retourne le titre du formulaire
    def get_form_title(self) :
        try :
            formtitle = self.form_structure['title']
        except  KeyError :
            print('no title found')
        return formtitle


    # Retourne l'ensemble des questions
    def get_form_fields(self) :
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
    def get_form_groups(self) :
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
                        qoptions = self._get_opinion_options(gidx=gidx, qidx=qidx_ing)
                        # Dans le cas de l'opinion, les resultats retournes ne sont pas les resultats mais la taille de l'echelle
                        qvalues = self._get_opinion_dtfs(qname=qtitle, qlabels=qoptions)

                    elif qtype == 'rating' :
                        qoptions = self._set_rating_values(gidx=gidx, qidx=qidx_ing)
                        # Dans le cas de l'opinion, les resultats retournes ne sont pas les resultats mais la taille de l'echelle
                        qvalues = self._get_rating_values(qname=qtitle, qlabels=qoptions)

                    elif qtype == 'long_text' :
                        qoptions.append('Free speech')
                        qvalues = self._get_longtext_values(qname=qtitle)

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
    

    # Recupere les sous reponses d'une liste de dataframes passee en paramaetres
    def get_sub_reponses (self, subq_gidx=-1, subq_qid='', inputdtfs = []) :
        qname = ''
        qvalues = []
        qlabels = []

        if len(inputdtfs) > 0 :
            for i in range(len(inputdtfs)) :
                qname, qlabels, qdtf = self.get_sub_question_data(gidx=subq_gidx, qid=subq_qid, inputdtf = inputdtfs[i])
                # print("dtf "+ str(i) + " is length "+ str(len(qdtf)))
                qvalues.append(qdtf)
                # strdtflgth = ''
                # for k in range(len(qdtf)) :
                #     strdtflgth += str(qdtf[k].shape[0]) +', '
                # print('dtfs sizes = '+ strdtflgth)

        else :
            print('Gibme list of inputdtfs')
        
        
        return qname, qlabels, qvalues


    # Retourne le dataframe des repondant pour une question donnee et une reponse attendue
    def get_sub_question_data(self, gidx=-1, qid='', inputdtf = None) :
        qidx_ing = 0
        if qid == '' :
            print('Please give question id.')
            return
        if gidx == -1 :
            print('Please give group idex.')
            return
        if inputdtf is None :
            print('Please give inputdtf (dataframe of the parent question)')
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



                    elif qtype == 'opinion_scale' :
                        qoptions = self._get_opinion_options(gidx=gidx, qidx=qidx_ing)
                        qvalues = self._get_sub_opinion_dtfs(qname=qtitle, qlabels=qoptions, inputdtf=inputdtf)

                    elif qtype == 'rating' :
                        qoptions = self._set_rating_values(gidx=gidx, qidx=qidx_ing)
                        qvalues = self._get_sub_rating_values(qname=qtitle, qlabels=qoptions, inputdtf=inputdtf)

                    elif qtype == 'long_text' :
                        qoptions.append('Free speech')
                        qvalues = self._get_longtext_values(qname=qtitle)

                    else :
                        print("Question type not found in function. There must be another way, or you'll have to modify code...")

                    break

                    break

        return qtitle, qoptions, qvalues



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
                #print ('POOOOO')
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



    

    # Retourne les valeurs possible de la notation
    def _set_rating_values(self, gidx=-1, qid='', qidx=-1) :
        l_res = []
        size = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['steps']
        labels = [*range(1,size+1,1)]
        return labels


    # Retourne les dataframe associes a chaque note
    def _get_rating_values(self, qname='', qlabels = []) :
        dp_values = []
        
        for i in range(len(qlabels)) :
            df_res = self.form_results[self.form_results[qname]==qlabels[i]]
            dp_values.append(df_res)

        return dp_values

    # Retourne les dataframe associes a chaque note, au sein du dataframe passe en parametre
    def _get_sub_rating_values(self, qname='', qlabels = [], inputdtf = None) :
        dp_values = []
        
        for i in range(len(qlabels)) :
            df_res = inputdtf[inputdtf[qname]==qlabels[i]]
            dp_values.append(df_res)

        return dp_values



    # Retourne les labels de min et max de l'opinion
    def _get_opinion_options(self, gidx=-1, qidx=-1) :
        l_res = []
        size = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['steps']
        startone = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['start_at_one']
        if startone :
            l_res = [*range(1,size,1)]
        else :
            l_res = [*range(0,size,1)]

        return l_res



    # Retourne les labels de min et max de l'opinion
    def _get_opinion_dtfs(self, qname='', qlabels = []) :
        dp_values = []

        for i in range(len(qlabels)) :
            df_res = self.form_results[self.form_results[qname]==qlabels[i]]
            dp_values.append(df_res)
   
        return dp_values

    # Retourne les dataframe associes a chaque note, au sein du dataframe passe en parametre
    def _get_sub_opinion_dtfs(self, qname='', qlabels = [], inputdtf = None) :
        dp_values = []

        if inputdtf.shape[0] > 0 :
            for i in range(len(qlabels)) :
                df_res = inputdtf[inputdtf[qname]==qlabels[i]]
                dp_values.append(df_res)
        # else :
        #     print("Some sub opinion is None")
        return dp_values


    def _get_longtext_values(self, qname='') :
        res = []
        df_res = self.form_results[self.form_results[qname].notnull()]
        res.append(df_res)

        return res

    def _get_sub_longtext_values(self, qname='', inputdtf = None) :
        res = []
        df_res = inputdtf[inputdtf.notnull()]
        res.append(df_res)

        return res



    #-----------------------------------------------------------------
    # FONCTIONS DE CROSS RESULTS
    def get_x_res(self, gidx1 = -1, qid1=-1, gidx2=-1, qid2=-1) :
        q1_name, q1_lbls, q1_dtfs = self.get_results(gidx=gidx1,qid=qid1)
        q2_name, q2_lbls, q2_dtfs = self.get_sub_reponses(subq_gidx=gidx2, subq_qid=qid2, inputdtfs = q1_dtfs) 
        # Rappel des options :
        print(q1_name + ":\n ",q1_lbls)
        # Rappel des options :
        print(q2_name + ":\n ",q2_lbls)

        return q1_name, q1_lbls, q1_dtfs, q2_name, q2_lbls, q2_dtfs


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

    
    

