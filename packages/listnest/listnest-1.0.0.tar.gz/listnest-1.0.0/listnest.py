'''This is listnest module and it provides one function called print_lol() which prints
lists that may or may not include nested list'''

def print_lol(the_list):
    '''This function takes a positional argument called "the_list",which is
        any Python list(of,possibly nested lists). each data item in the provided
        list is recursively printed to the screen on its own'''
    
    for eachitem in the_list:
            if isinstance(eachitem,list):
                print_lol(eachitem)
            else:
                print(eachitem)
