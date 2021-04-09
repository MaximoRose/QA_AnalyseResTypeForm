# English
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
