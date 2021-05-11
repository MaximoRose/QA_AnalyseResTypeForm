# English
## Introduction
I've made a code easy to use in Jupyter NoteBook to produce graphs of your TypeForm.

The point is to avoid making a spreadsheets everytime I export my results, as I can export them multiple times for a single Form, just because I'm impatient to see the tendencies.

I also like the Jupyter Notebook format as you can mix code, graphs and markups so that your work can be published as one element, limiting the anount of work, creating slides etc. to communicate the results.

Another personnal goal is to avoid using Google spreadsheet, eventhough it's a good product. I'm trying to degooglize myself, just a little. If you also start using this code, you can say, you engage with open source ;)

## How to use it ?
### Create a TypeForm and set up your directories
- When you create a TypeForm try regrouping all you questions, as for this code to work, every question must be in a group. This can feel as a limitation, but I like to think of it as a way to always structure my forms.
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

- "tfs" is the objecti defined above.
- "firstquestion_title" is a string : the question itself, used to name the plots.
- "firstquestion_labels" : are the possible answers, used to label the plot.
- "firstquestion_responses" : is the list of dataframes corresponding to each possible answer. 

"firstquestion_labels" and "firstquestion_responses" should be the same length.



### Use the right function for the right type of questions.

## Files
- mbr_typeform.py : module with all the functions created to get answers to a specific question in a specific group of a typeform 



N.B : 

1. Pour les questions a choix unique on ne fait que des camemberts.
1. Pour les questions a choix multiple, opinion scale, ratings, on fait des barcharts

Quand on fera des croisements on sera plus original, on aura des teckels et des chihuahua degeneres



# QA_AnalyseResTypeForm
Code to analyze responses to a TypeForm Form

You won't have to adapt it too much if you try to group the questions in your forms as the main function is based on group index and question id. The question id is searched inside the associated group.

The  module mbr_typeform.py is dedicated to all the typeform associated functions
The Jupyter Notebook, OpportuniteGP.ipynb, is used for plotting results. It's here as an example. It's based on this form (link to put). I'll try to push the results every now and then as an example dataset.

But every time you create a new form you can create a new Jupyter Notebook to analyze your results. It should work as soon as you bend to the following rules :
- Group all your questions. Out of groups should only be Welcome and Goodbye Page
- Single choice questions will be pie-charts
- Opinion scale and ratings will be bars



# How to
Most important function is "mbr_typeform.get_results(gidx=gidx,qid=qid)".
- gdix is the group's index (first group is of index 0)
- qid is the question's id

To have this info, you can access the API of your form at URL : https://api.typeform.com/forms/ {id of your form}
Or you can use the "mbr_typeform.dump_tform_structure()" function to dump the structure into a .json file in the "forms" folder

__Example :__

import mbr_typeform as mbr

tfs = mbr.tf_struct(formid='yourid')

struct_d = tfs.get_form_structure()

tfs.dump_tform_structure()



This way you can get the id of any of your question.





#### Various sources :
1. Customiser les pies charts : https://www.askpython.com/python/plot-customize-pie-chart-in-python
