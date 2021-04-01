# https://developer.typeform.com/create/reference/retrieve-form/

# Convention : Les resultats s'appellent "res_{formid}.csv"
# Rule : Results are named "res_{formid}.csv"

import requests # pip install request // si necessaire 
import json
import pandas as pd

# Elimine les options qui n'ont jamais ete selectionnees
# label est la liste des options possibles pour une questions
# Values correspond au dataframe associe
def clean_lists(labels = [], values = []) :
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

def dropdown_subresults(main_dtf=[], l_options = [], q_name='') :
    labels = []
    dtfs = []
    for i in range(len(l_options)) :
        dftemp = main_dtf[main_dtf[q_name]==l_options[i]]
        dtfs.append(dftemp)
        labels.append(l_options[i])
    return labels, dtfs


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
        qidx_ing = 0
        if qid == '' :
            return
            print('Please give question id.')
        if gidx == -1 :
            print('Please give group idex.')
            return
        else :
            group_questions = self.form_fields[gidx]['properties']['fields']
            for i in range(len(group_questions)) :
                if group_questions[i]['id'] == qid :
                    qidx_ing = i
                    qtitle = group_questions[i]['title']
                    print(qtitle)
                    qtype = group_questions[i]['type']
                    print(qtype)
                    if qtype == 'dropdown' :
                        qoptions = self._get_dp_options(gidx=gidx, qid=qid, qidx=qidx_ing)
                        qvalues = self._get_dp_values (qname=qtitle, qlabels=qoptions)
                    elif qtype == 'yes_no' :
                        qoptions = ['oui', 'non']
                        qvalues = self._get_yn_values(qname=qtitle)
                    elif qtype == 'picture_choice' :
                        qoptions = self._get_pc_ou_mc_options(gidx=gidx, qid=qid, qidx=qidx_ing)
                        qvalues = self._get_pc_ou_mc_values (qname=qtitle, qlabels=qoptions)
                    elif qtype == 'multiple_choice' :
                        qoptions = self._get_pc_ou_mc_options(gidx=gidx, qid=qid, qidx=qidx_ing)
                        qvalues = self._get_pc_ou_mc_values (qname=qtitle, qlabels=qoptions)
    
        return qtitle, qoptions, qvalues


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


    # get yes_no values
    # returns dataframe of yes and dataframe of no
    def _get_yn_values(self, qname='') :
        dp_values = []
        df_res_y = self.form_results[self.form_results[qname]==1]
        df_res_n = self.form_results[self.form_results[qname]==0]
        dp_values.append(df_res_y)
        dp_values.append(df_res_n)
        return dp_values


    # get picture_choice options
    # returns list of label options
    def _get_pc_ou_mc_options(self, gidx=-1, qid='', qidx=-1) :
        choices = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['choices']
        other_o = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['allow_other_choice']
        multiple_c = self.form_fields[gidx]['properties']['fields'][qidx]['properties']['allow_multiple_selection']

        lastchoicefound = False

        labels = []
        for j in range(len(choices)) :
            # print(choices[j]["label"])
            labels.append(choices[j]["label"])
        

        if other_o == 'true' :
            for col in self.form_results.columns :
                if lastchoicefound :
                    labels.append(col)
                    lastchoicefound = False
                if col == labels[-1] :
                    lastchoicefound = True

        return labels


    # get picture_choice values
    # returns 
    def _get_pc_ou_mc_values(self, qname='', qlabels = []) :
        dp_values = []

        for i in range(len(qlabels)) :
            if qlabels[i][:5] != 'Other' :
                df_res = self.form_results[self.form_results[qname]==qlabels[i]]
                # print(str(df_res.shape[0]))
                dp_values.append(df_res)
            else :
                df_res = self.form_results[self.form_results[qlabels[i]]!='']
                dp_values.append(df_res)
        return dp_values


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


