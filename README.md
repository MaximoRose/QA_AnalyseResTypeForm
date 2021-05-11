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
- From your TypeForm interface download all the answers as a .csv file
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

Hope it helps !

Take care

## Files
- mbr_typeform.py : module with all the functions created to get answers to a specific question in a specific group of a typeform 

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

La fonction : "mbr_typeFrom(formid='YvBfAdHB')" will initialize all the objects : the typeForm structure, and all the responses, based on the resp_xxx.csv file you've put in the ./responses/ folder.
