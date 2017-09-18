# Natural language statistical methods for Python's projects.

It allows to calculate some word's statistics. 

# Usage

'import dclnt'

verb_stat = dclnt.get_top_verbs_in_path("/django")

print('total %s verbs, %s unique' % (len(verb_stat), len(set(verb_stat))))

for verb, occurence in dclnt.get_top(verb_stat, top_size):
   print(verb, occurence)

It allows to get next information:

* get_all_words_in_path: a list of the words in names from the path 
* get_top_verbs_in_path: a list of the most common verbs in function's name and their counts from the path 
* get_top_functions_names_in_path: a list of the most common names of function and their counts from the path
* def get_verbs_from_function_name: a list of verbs in function_name

