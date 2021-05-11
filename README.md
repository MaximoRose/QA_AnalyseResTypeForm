# Table of contents
* [ENGLISH](#english)
** [Introduction](##Introduction)
* [FRANCAIS](#francais)


# ENGLISH
## Introduction
I've made a code pretty easy to use in Jupyter NoteBook to produce plots for your TypeForm responses.

The point is to avoid making a spreadsheets everytime I export my results, as I can export them multiple times for a single Form, just because I'm impatient to see the tendencies.

I also like the Jupyter Notebook format as you can mix code, graphs and markups so that your work can be published as one element, limiting the anount of work, creating slides etc. to communicate the results.

Another personnal goal is to avoid using Google spreadsheet, eventhough it's a good product. I'm trying to degooglize myself, just a little. If you also start using this code, you can say, you engage with open source ;)

## How to use it ?
### Create a TypeForm with the proper structure
- When you create a TypeForm try regrouping all you questions, as for this code to work, every question must be in a group. This can feel as a limitation, but I like to think of it as a way to always structure my forms.

!["Question group" dans TypeForm](https://maximorose.eu/Ressources/Question_Group_TypeForm.png)

### Set up your working environment
- Download all the files on your PC, and put all of them in the same folder. You only really need the .py files, but the .ipynb can be used as examples of how to use the functions defined in the .py files.
- In said folder, create your own Jupyter Notebook (.ipynb file). Personnaly I use [Visual Studio Code](https://code.visualstudio.com/) to run all this. I Love it.
- From your TypeForm interface download all the answers as a .csv file [example](https://maximorose.eu/Ressources/Screenshot%20from%202021-05-11%2019-59-17.png)
- Put them in the folder ./responses/
- Name them : res_{TypeFormid}.csv

You can find your TypeForm ID in the link you share :
![where to find the typeform id](https://maximorose.eu/Ressources/TypeFormID.png)

You can see the form structure if you go to URL : https://api.typeform.com/forms/{form-id}

As an example, mine is : https://api.typeform.com/forms/YvBfAdHB (FireFox shows it in a readable manner)

You can also dump the structure in the json file, with the function "dump_tform_structure()", after you've initialised your TypeForm.

For example, the following code would dump the structure in a "YvBfAdHB.json" file in the ./forms/ folder
> import mbr_typeform as mbrtf
> 
> import mbr_plots as mbrpl
> 
> tfs = mbrtf.mbr_typeFrom(formid='YvBfAdHB')
> 
> tfs.dump_tform_structure()

The function : "mbr_typeFrom(formid='YvBfAdHB')" will initialize all the objects : the typeForm structure, and all the responses, based on the resp_xxx.csv file you've put in the ./responses/ folder.




### Identify question ids and group indexes
When you access your typeform API, you will see something like this : 

![typeform API structure](https://maximorose.eu/Ressources/tf_grpidx_qid.png)

- The first field index, "0" circled in red, correspond to the first group of questions' index.
- The ids circled in green are the questions' id.
- The "type" underlined will be needed to knwo which function to use.

On the picture above, if I want to get the 1st question name, its labels and its responses, I will use  index group 0 and question id oYqnhtesJuF5 with function get_results(gidx={group index},qid={question id})

> firstquestion_title, firstquestion_labels, firstquestion_responses = tfs.get_results(gidx=0,qid='oYqnhtesJuF5')

- "tfs" is the object defined above.
- "firstquestion_title" is a string : the question itself, used to name the plots.
- "firstquestion_labels" : are the possible answers, as a list of strings, used to label the plot.
- "firstquestion_responses" : is the list of each dataframe corresponding to each possible answer. 

"firstquestion_labels" and "firstquestion_responses" should be the same length.

Now, if I want to pie plot the results, I'll use function "plot_mbr_camembert()" in module "mbr_plots". 

__N.B :__ When considering plots, french people don't see pies they see "camembert", one of their round cheese, that's why the function is called so.

The complete code to initialize the objects, get the results of the first response and plot them would be : 

> import mbr_typeform as mbrtf #Import module with all the typeform functions
> 
> import mbr_plots as mbrpl #Import module with plot function
> 
> tfs = mbrtf.mbr_typeFrom(formid='YvBfAdHB') #Import all the objects and structure of the typeForm
> 
> myfig = mbrpl.plots_mbr_tf() #Initialize the plotting environment
> 
> firstquestion_title, firstquestion_labels, firstquestion_responses = tfs.get_results(gidx=0,qid='oYqnhtesJuF5')
> 
> yfig.plot_mbr_camembert(qtitle = firstquestion_title, list_labels = firstquestion_labels, list_dtfs = firstquestion_responses)

It corresponds to the first two blocks of my OpportuniteGP.ipynb file. You can use my file and just replace the form ID and the question ID.

### Use the right function for the right type of questions.

Pie charts, "camemberts", work with any type of single choice questions :

- Yes/No
- Dropdown
- Multiple choice (without multiple selection enabled) - it's multiplicity is only visual)
- Image choice (without multiple selection enabled)

Use the function myfig.plot_mbr_barchart(qtitle = question_title, list_labels = question_lables, list_dfs = question_responses) for :

- Multiple choices, with multiple choice enabled
- Opinion scale
- Ratings

For all other type of questions try to find your ways.

### Get cross results between questions
For the moment, I've just made some functions that can cross results between two questions, but I'm sure you can find your ways with the result dataframes you get with the previous functions.

Check "xOportuniteGP.ipynb" file for examples of these functions.



Hope it helps !

Take care

## Files and folders
- mbr_typeform.py : module with all the functions created to get answers to a specific question in a specific group of a typeform 
- mbr_plots.py : module with all plot functions
- OpportuniteGP.ipynb : the analysis of my form results where I use all the functions I've defined
- xOpportuniteGP.ipynb : a sandbox file where I practised cross-result analysis
- ./config/graph_params.json : parameters for plots, like colors, pie explode, title size, etc.
- ./Documentation/ : has printscreens of my form, to illustrate how it looked
- ./forms/ : I don't know why, but I like having a json file where I drop the structure of my forms. Maybe so I can work offline easy. So this is the folder where the structure is always dumps
- ./responses/ : is where you put the .csv file associated to the responses you had.

# FRANCAIS
## Introduction
J'ai essayé de faire un code assez simple à utiliser pour produire des graphs à partir des réponses à vos TypeForm.

L'objectif était d'éviter d'avoir à retravailler mes graphs dans Google Spreadsheet à chaque fois que je réccupérais mes résultats. Une fois mon Jupyter Notebook réalisé, il me suffit de remplacer le fichier de réponses par celui plus à jour pour que mes graphs se mettent tous à jour.

Et puis, j'aime bien le format Jupyter Notebook parce qu'il mélange code, graphs, textes enrichis, et permet donc de ne travailler que sur un seul fichier, sans avoir à formaliser une note à côté du code, ou des slides. Cela permet une plus grande transparence sur l'étude.

Enfin, j'essaie de me dégoogliser un peu. Si vous utilisez ce code, vous pourrez dire que vous soutenez les initiatives Open Source ! xD

## Comment l'utiliser ?
### Créer votre TtpeForm avec une structure appropriée
- Quand vous créer votre TypeForm, regroupez toutes vos questions dans des "groupes de questions". Si ça peut paraître limitant, cela force à bien structurer son questionnaire.

!["Question group" dans TypeForm](https://maximorose.eu/Ressources/Question_Group_TypeForm.png)

### Définissez votre environnement de travail
- Télécharger tous les fichiers de Github. Vous n'avez réellement besoin que des .py, mais les .ipynb peuvent vous servir d'exemples pour utiliser les différentes fonctions définis dans les .py.
- Dans ce dossier créer donc votre propre Jupyter NoteBook (fichier .ipynb). Personnellement j'utilise [Visual Studio Code](https://code.visualstudio.com/) et j'adore ça. Et, j'ai appris le python dans Jupyter en partant du cours Open classroom référencé dans [mon autre Repo](https://github.com/MaximoRose/JupyterNoteBook_OpenCR_Python)
- Depuis votre interface d'administration TypeForm récupérez les réponses à votre questionnaire [exemple](https://maximorose.eu/Ressources/Screenshot%20from%202021-05-11%2019-59-17.png)
- Mettez le fichier .csv dans le dossier ./responses/
- Et renommez-le res_{TypeFormid}.csv


Vous pouvez trouver l'ID de votre TypeForm dans le lien que vous envoyez quand vous le partagez :
![where to find the typeform id](https://maximorose.eu/Ressources/TypeFormID.png)

Pour voir la structure de votre questionnaire, accédez à l'URL : https://api.typeform.com/forms/{form-id}

Par exemple, celle de mon questionnaire se trouve ici : https://api.typeform.com/forms/YvBfAdHB (mieux vaut ouvrir ce lien avec FireFox pour avoir un truc un peu lisible)

Si vous voulez enregistrer la structure de votre questionnaire dans un fichier .json sur votre PC, vous pouvez utiliser la fonction "dump_tform_structure()", après avoir initialisé votre objet TypeForm.

Par exemple, le code suivant, tapé dans un bloc Jupyter, créera un fichier "YvBfAdHB.json" (id de mon questionnaire) dans le sous-dossier ./forms/ 

> import mbr_typeform as mbrtf
> 
> import mbr_plots as mbrpl
> 
> tfs = mbrtf.mbr_typeFrom(formid='YvBfAdHB')
> 
> tfs.dump_tform_structure()

La fonction : "mbr_typeFrom(formid='YvBfAdHB')" initialisera tous les objets nécessaires aux fonctions qui suivront. Elle se base sur l'ID de votre formulaire que vous lui passer en paramètres, et sur le fichier de réponses que vous avez déposez dans ./responses/.


### Identifier les groupes et les identifiants des questions
Quand vous accédez à l'API de votre TypeForm dans FireFox (ou au fichier .json que vous avez dumpé), vous devez voir quelque chose comme ça :

![typeform API structure](https://maximorose.eu/Ressources/tf_grpidx_qid.png)

- Le premier index sous "field", le "0" entouré en rouge, correspond à l'index du premier groupe de question.
- Les ids encerclé en vert correspondent aux id des question. Le premier est l'ID de la première question du groupe 0, le second est l'ID de la seconde question du groupe 0.
- Le "type", souligné en bleu, vous servira à choisir les fonctions à utiliser pour afficher vos résultats.

Sur la base de l'image ci-dessus, si je voulais récupérer le texte de la première question, toutes ses options possibles ainsi que toutes les réponses associées à cette question, j'utiliserais la fonction "get_results(gidx={group index},qid={question id})" à la suite du code précédent :

> premierequestion_titre, premierequestion_options, premierequestion_reponses = tfs.get_results(gidx=0,qid='oYqnhtesJuF5')

- "tfs" est l'objet qu'on a initialisé dans le code précédent.
- "premierequestion_titre" est une chaîne de caractères. C'est la question telle qu'elle est posée. Elle servira de titre aux graphiques qui suivront.
- "premierequestion_options" est une liste de chaînes de caractère, une chaîne pour chaque option possible pour cette premère question.
- "premierequestion_reponses" est une liste de dataframe pandas (i.e des tableaux peu ou prou). Un par option possibles. En gros, l'élément 0 est un dataframe qui correspond à l'ensemble des répondant ayant choisi l'option "0" (la première) à cette question.

"premierequestion_options" et "premierequestion_reponses" devrait faire la même taille.

Maintenant si vous voulez obtenir un camembert affichant les résultats de la première question, utilisez la fonction "plot_mbr_camembert()" du module "mbr_plots".

Le code complet pour charger les données et tracer les résultats serait donc: 

> import mbr_typeform as mbrtf #Import module with all the typeform functions
> 
> import mbr_plots as mbrpl #Import module with plot function
> 
> tfs = mbrtf.mbr_typeFrom(formid='YvBfAdHB') #Import all the objects and structure of the typeForm
> 
> myfig = mbrpl.plots_mbr_tf() #Initialize the plotting environment
> 
> firstquestion_title, firstquestion_labels, firstquestion_responses = tfs.get_results(gidx=0,qid='oYqnhtesJuF5')
> 
> yfig.plot_mbr_camembert(qtitle = firstquestion_title, list_labels = firstquestion_labels, list_dtfs = firstquestion_responses)
> 

Il correspond aux deux premiers blocs de mon fichier OpportuniteGP.ipynb. Vous pouvez partir de mon fichier et remplacer l'ID du formulaire, ainsi que l'ID de la première question. (normalement le group index est le même, si vous avez bien mis toutes vos questions dans des groupes)

### Utilisez les bonnes fonctions pour les bons types de questions.

Les camemberts sont idéals pour les questions de type :

- Yes/No (Oui/Non)
- Dropdown (Menu déroulant)
- Multiple choice (feux choix multiples - TypeForm propose de créer des questions de type "multiple choice", mais où on ne peut saisir qu'une réponse. Ce sont donc des "single choice", mais qui s'affichent simplement différement dans le formulaire)
- Image choice (choix d'image non multiples)

Pour les types suivants, privilégiez l'utilisation de graphiques en barres, via la fonction "myfig.plot_mbr_barchart(qtitle = question_title, list_labels = question_lables, list_dfs = question_responses)" :

- Multiple choices, with multiple choice enabled (vrais choix multiples)
- Opinion scale (Opinions)
- Ratings (notes)

Pour les autres types de questions, il vous faudra trouver votre voie.

### Croiser des réponses
Pour l'instant je n'ai fait que croiser deux questions max. J'ai préparé quelques fonctions, mais j'imagine que dans beaucoup de cas, il est préférable que vous appreniez à jouer avec les dataframes pour essayer d'obtenir vos propres résultats.

Si jamais, n'hésitez pas à regarder un peu "xopportunieGP.ipynb", j'y fais des tests de croisements de résultats.



J'espère que cela servira à certains d'entre vous,

Prenez soin de vous !

## Les fichiers et dossiers
- mbr_typeform.py : Module avec toutes les fonctions liées au TypeForm. La classe mbrtf permet de créer un objet ayant pour attribut la structure du questionnaire, son titre, les réponses associées (si elles sont bien dans le dossier dédié).  
- mbr_plots.py : module avec toutes mes fonctions de graphs
- OpportuniteGP.ipynb : L'analyse des résultats de mon formulaire, où vous trouverez des exemples de comment utiliser les différentes fonctions.
- xOpportuniteGP.ipynb : Un petit fichier bac à sable pour faire des analyses croisées des réponses aux questions.
- ./config/graph_params.json : paramètres des graphiques, comme les couleurs, la taille des titres, etc.
- ./Documentation/ : quelques printscreen de mon formulaire initial pour mettre en perspective mes fonctions si vous n'avez pas répondu à mon [questionnaire](https://j85vsp5f9lc.typeform.com/to/YvBfAdHB)
- ./forms/ : J'aime bien avoir la structure de mon questionnaire sous la forme d'un fichier.json, ça permet de travailler hors ligne. C'est dans ce dossier que son dumpés les fichiers avec la fonction dump()
- ./responses/ : C'est dans ce dossier qu'il faut déposer les fichiers .csv de réponse au questionnaire.



[Maximo Rose](https://maximorose.eu/)
