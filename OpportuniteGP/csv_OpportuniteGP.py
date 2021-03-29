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
        self.brutrep = None
        self.men = None
        self.women = None
        self.nogenre = None
        self.fluid = None

    # ---------------------------------------------------
    # Create DataFrame Panda
    # ---------------------------------------------------
    def get_allreps(self, file) :
        dt_GP = pd.read_csv(file)
        # I'll be renaming all the colums, so the Jupyter NoteBook I will use to plot will be easier to write on the long term
        # I've split them in parts, just so it's easier to maintain. I print them for ease in jupyter + i'm tired so easy coding
        # Renommer les colonnes pour faciliter les traitements dans Jupyter
        # Afficher le nom des colonnes pour faciliter le travail dans Jupyter

        # "1. Apprendre a vous connaitre"
        dt_GP = dt_GP.rename(columns = {"Vous êtes...":'1sexe', "Quel est votre âge ?":"1age", "Vivez-vous en France ?":"1france", "Quel fut votre dernier diplôme ?":"1diplome", "Travaillez-vous dans le secteur public ?":"1s_public", "Travaillez-vous dans le secteur culturel ?":"1s_culture", "Quelle est votre spécialité ?":"1specialite", "Other":"1_spe_other"})
        print("1 - VOUS - 1 : 1sexe ; 1age ; 1france ; 1diplome ; 1s_public ; 1s_culture ; 1specialite ; 1_spe_other")
        print()

        # "2. Votre rapport au numerique"
        dt_GP = dt_GP.rename(columns = {"Quand utilisez-vous le plus souvent des outils numériques ?":"2whendoyouit", "Est-ce plutot par plaisir ou par necessite ?":"2forleasure", "Smartphone professionnel":"2sm_pro", "Smartphone personnel":"2sm_pers", "Ordinateur personnel":"2ord_pers", "Ordinateur professionnel":"2ord_pro", "Des objets connectés (Smart watch, Garmin, etc.)":"2iot", "Rien":"2noObject", "Si vous deviez noter votre aisance personnelle avec l'informatique, combien vous donneriez vous ?" : "2aisance", "Avez-vous l'impression de maîtriser les informations qui vous concernent sur Internet ?":"2maitrise_dcp", "Paramétrez-vous les cookies quand les sites vous le propose ?":"2cookies", "Avez-vous l'impression de recevoir trop de messages promotionnels sur votre boîte mail ?":"2spams", "Comment gerez-vous tous vos mots de passes des differents sites web ?" : "2gest_mdp", "Other.1":"2_gestmdp_other", "Pensez-vous que l'informatique soit une bénédiction ou une malédiction ?":"2bene"})
        print("2 - RAPPORT AU NUMERIQUE - 2 : 2whendoyouit ; 2forleasure ; 2sm_pro ; 2sm_pers ; 2ord_pers ; 2ord_pro ; 2iot ; 2noObject ; 2aisance... ")
        print("... 2maitrise_dcp ; 2cookies ; 2spams ; 2gest_mdp ; 2_gestmdp_other ; 2bene")
        print()

        # "3. Education"
        dt_GP = dt_GP.rename(columns = {"A l'école, vous a-t-on enseigné l'informatique ?":"3enseignement", "École primaire":"3ens_primaire", "Collège":"3ens_college", "Lycée":"3ens_lycee", "Études supérieures" : "3ens_sup", "Other.2":"3ens_other", "Avez-vous bénéficié de formations, dans le cadre de votre travail ou non, en informatique ?":"3form_pro", "Savez-vous écrire les nombres en binaire ?":"3doyoubin", "Et bien prouvez le ! Que vaut 0101 ?":"3binres", "Si je vous disais que je peux vous l'enseigner en une demi-heure, seriez-vous intéressés pour l'apprendre ?":"3wannalearn", "Même si ce devait-être payant ? ":"3wannapay" , "Combien seriez-vous pret a payer ?":"3howmuch", "Savez-vous ce qu'est un algorithme ?":"3whatisalgo", "Pensez-vous qu'il est important d'apprendre l'informatique à l'école ?":"3itatschool_pros", "Pourquoi ?" : "3whyitatsch", "A partir de quel age pensez-vous qu'on peut apprendre les sciences de l'information (écriture binaire, algorithmes, programmation) ?":"3learningage", "Lorsque vous avez un probleme d'informatique, le plus souvent, vous ...":"3howdoyoudebug"})
        print("3 - EDUCATION - 3 : 3enseignement ; 3ens_primaire ; 3ens_college ; 3ens_lycee ; 3ens_sup ; 3ens_other ; 3form_pro ; 3doyoubin...")
        print("... 3binres ; 3wannalearn ; 3wannapay ; 3howmuch ; 3whatisalgo ; 3itatschool_pros ; 3whyitatsch ; 3learningage ; 3howdoyoudebug")
        print()

        # "4. Culture"
        dt_GP = dt_GP.rename(columns = {"Par des abonnements bien sentis sur les reseaux sociaux":"4src_culture_rs", "En allant sur les sites des musées ou de leurs partenaires":"4src_culture_site", "Grâce à la télévision, la radio, les journaux ou les media web":"4src_culture_media", "Grâce au bouche à oreille":"4src_culture_friendos", "Je ne recherche pas activement de l’information sur ce sujet":"4src_culture_none", "Durant l'année 2020 avez-vous eu l'occasion de voir l'une des vidéos listées sur l'image ?":"4havuseentopvidz", "Pensez-vous en regarder une, maintenant que vous avez toutes les informations pour le faire ?":"4r_u_gonna_watch", "C'était comment ?":"4if_uwatch_howwas", "FaceBook":"4vid_plat_fb", "Youtube":"4vid_plat_yt", "Instagram":"4vid_plat_it", "Sur le site de l'instiution":"4vid_plat_site", "Other.3" : "4vid_plat_other" , "Aviez-vous un compte sur cette plateforme ?":"4vid_plat_account", "S'il existait un endroit sur Internet où trouver toutes les vidéos postées par les institutions culturelles (théâtre, danse, sciences, séminaires, conférences, etc.), iriez-vous le consulter de temps en temps ?":"4interest_inus", "Depuis le debut du confinement, avez-vous pris part à des activités numériques organisées par des institutions culturelles (musées, fondations, théâtres, cinéma, bibliothèque, etc.) ou par le service public de manière plus générale (e.g activités organisées par des mairies ou des associations) ?":"4publicactivities", "ANSSI":"4anssi", "CNIL":"4cnil", "DINUM":"4dinum", "INRIA":"4inria", "Aucune" : "4aucune"})
        print("4 - CULTURE - 4 : 4src_culture_rs ; 4src_culture_site ; 4src_culture_media ; 4src_culture_friendos ; 4src_culture_none ; 4havuseentopvidz ...")
        print("... 4r_u_gonna_watch ; 4if_uwatch_howwas ; 4vid_plat_fb ; 4vid_plat_yt ; 4vid_plat_it ; 4vid_plat_site ; 4vid_plat_other ; 4vid_plat_account")
        print("... 4interest_inus ; 4publicactivities ; 4anssi ; 4cnil ; 4dinum ; 4inria ; 4aucune")
        print()

        # "5. Interets IT & Structure"
        dt_GP = dt_GP.rename(columns = {"Protection des données personnelles, Rgpd":"5rqrmt_govit_rgpd", "Green IT et écoconception des services d'informations":"5rqrmt_govit_greenit", "Proposer des services accessibles aux personnes en situation de handicap":"5rqrmt_govit_handi", "Encourager les démarches d'accès universel à la connaissance (Open source)" : "5rqrmt_govit_os", "Rendre accessible les données publiques et favoriser l'interopérabilité pour automatiser, et donc accélerer, les démarches administratives":"5rqrmt_govit_autom", "Aucune.1":"5rqrmt_govit_aucune", "Other.4":"5rqrmt_govit_other", "Les sujets de transformation de la société par le numérique vous intéressent-ils ?":"5interest_init", "Toutes les dernieres tendances en matière d'innovation technologique" : "5int_latesttrends", "Comment le numérique influt-il sur nos droits et nos libertés ? Quels sont les risques et menaces (reconnaissance faciale, manipulation des masses, etc.)?":"5int_itthreats" , "Comment les technologies permettent la création de réseaux sociaux humains et l'émergence de sous-cultures ou de mouvements de mobilisation populaires":"5int_mass_culture", "Les nouveaux business qui émergent sur internet (le drop shipping, les NFTs, les cryptomonnaies, etc.)":"5int_business", "Les applications de l'informatique aux autres domaines de la connaissance : santé, social, astrophysique, architecture, design, mode, etc.":"5int_crossdomain", "Other.5" : "5int_other", "Je lis les articles sur ces sujets qui sont publiés dans mes quotidiens habituels":"5src_itinfo_quot", "Je suis abonnés à quelques institutions ou entreprises de l'informatique sur les réseaux":"5src_itinfo_rs" , "Je consulte régulièrement des sites ou magazines spécialisés":"5src_itinfo_spe", "Je vais régulièrement sur des sites type Reddit ou Hackernews où une communauté de passionnés partage ses articles":"5src_itinfo_rsspe", "Other.6":"5src_itinfo_other", "Y-a-t-il un sujet ou une question qui vous intéresse plus que les autres en ce qui concerne l'informatisation des sociétés ? ":"5pers_it_interest", "Avez-vous déjà entendu parler d'un musée des sciences de l'information ?" : "5it_musem_knowany", "Super ! Pourriez-vous m'indiquer son nom ?" : "5it_museum_gottaname", "Pensez-vous que ce serait une bonne chose d'en avoir un ?":"5it_museum_wantone", "Y a-t-il des contenus spécifiques liés à l'informatique ou au numérique auxquels vous souhaiteriez pouvoir accéder librement ? Des sujets sur lesquels vous souhaiteriez être mieux informés ? Une liste de logiciels de référence pour ne pas risquer d'avoir un virus ? N'importe quoi qui vous passe par la tête en lien avec notre sujet !":"5any_additionnal_subject", "Enfin, si un site Internet vous permettait d'accéder à des supports de formation, des ateliers, des articles d'actualités ou des conférences en lien avec les sciences de l'information ; si, en plus, il vous permettait d'accéder a tous les contenus culturels numériques produits par l'Etat ou ses partenaires ; vous pensez qu'il devrait être...":"5_publicouprive", "Other.7":"5_struct_other"})
        print("5 - INTERETS IT & STRUCTURE - 5 : 5rqrmt_govit_rgpd ; 5rqrmt_govit_greenit ; 5rqrmt_govit_handi, 5rqrmt_govit_os, 5rqrmt_govit_autom")
        print("... 5rqrmt_govit_aucune ; 5rqrmt_govit_other ; 5interest_init ; 5int_latesttrends ; 5int_itthreats ; 5int_mass_culture ; 5int_business")
        print("... 5int_crossdomain ; 5int_other ; 5src_itinfo_quot ; 5src_itinfo_rs ; 5src_itinfo_spe ; 5src_itinfo_rsspe ; 5src_itinfo_other")
        print("... 5pers_it_interest ; 5it_musem_knowany ; 5it_museum_gottaname ; 5it_museum_wantone ; 5any_additionnal_subject, 5_publicouprive")
        print("... 5_struct_other")

        self.brutrep = dt_GP
        return dt_GP

    # ---------------------------------------------------
    # Return dataFrame of sex proportions
    # Retourne la part de sexes
    # ---------------------------------------------------
    def have_sex(self) :
        df_male = self.brutrep[self.brutrep['1sexe']=='Un homme']
        df_female = self.brutrep[self.brutrep['1sexe']=='Une femme']
        df_nogenre = self.brutrep[self.brutrep['1sexe']=='Non genré']
        df_fluide = self.brutrep[self.brutrep['1sexe']=='Fluide']
        self.men = df_male
        self.women = df_female
        self.nogenre = df_nogenre
        self.fluid = df_fluide
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



