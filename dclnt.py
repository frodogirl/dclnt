import ast
import os
import collections
import itertools

import nltk
from nltk import word_tokenize

if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')

""" Some supporing functions """
def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return list(itertools.chain(*_list))

def is_verb(pos_info):
    return pos_info[1] in ('VB', 'VBD', 'VBG', 'VBN')

def is_special_name(word):
    """ The name is specific if starts and ends with '__' """
    return word.startswith('__') and word.endswith('__')

def get_top(iterator, top_size=10):
    """ Return a list of the top_size most common elements and their counts from iterator """
    return collections.Counter(iterator).most_common(top_size)
    

def get_trees(path, with_file_names=False, with_file_content=False, file_count=100):
    """ 
        Return a list of abstract syntax trees for every .py file in the path.
        If boolean parameters with_file_names or with_file_content are true,
        it returns a list of tuple with (file_name, file_content, tree) resp.
    """
    def get_python_files(file_names, dir_name, files):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
        return file_names 

    def get_file_content(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as attempt_handler:
                return attempt_handler.read()
        except IOError as e:
            print(e)
            return ''

    def get_tree(content):
        try:
            return ast.parse(content)
        except SyntaxError as e:
            print(e)
            return None

    file_names = []
    trees = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        file_names = get_python_files(file_names, dir_name, files) 
        #if len(file_names) > file_count:
        #    file_names = file_names[0: file_count]
        #    break
    print('total %s files' % len(file_names))
    
    for file_name in file_names:
        file_content = get_file_content(file_name)
        tree = get_tree(file_content)
        
        if tree:
            if with_file_names and with_file_content:
                trees.append((file_name, file_content, tree))
            elif with_file_names:
                trees.append((file_name, tree))
            else:
                trees.append(tree)
    print('trees generated')
    
    return trees

def split_snake_case_name_to_words(name):
    """ 'snake_case_name' -> ['snake', 'case', 'name'] """
    return [n for n in name.split('_') if n]

def get_names_in_tree(tree):
    """ Return a list of node's names from the one abstract syntax tree """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]

def get_function_names_in_tree(tree):
    """ Return a list of function's names from the one abstract syntax tree """
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def get_verbs_from_function_name(function_name):
    """ Return a list of verbs in function_name """
    return [word for word in nltk.pos_tag(split_snake_case_name_to_words(function_name)) if is_verb(word)]

def get_all_words_in_path(path):
    """ Return a list of the words in names from the path """
    trees = get_trees(path)
    all_names = [f for f in flat(map(get_names_in_tree, trees)) if not is_special_name(f)]
    return flat(map(split_snake_case_name_to_words, all_names))

def get_top_verbs_in_path(path, top_size=10):
    """ Return a list of the top_size most common verbs in function's names and their counts from the path """
    trees = get_trees(path)
    function_names = [f for f in flat(map(get_function_names_in_tree, trees)) if not is_special_name(f)]
    verbs = flat(map(get_verbs_from_function_name, function_names))
    return get_top(verbs, top_size)

def get_top_functions_names_in_path(path, top_size=10):
    """ Return a list of the top_size most common names of function and their counts from the path """
    trees = get_trees(path)
    function_names = [f for f in flat(map(get_all_function_names, trees)) if not is_special_name(f)]
    return get_top(function_names, top_size)


if __name__ == "__main__":
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)


    top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurence in get_top(wds, top_size):
        print(word, occurence)