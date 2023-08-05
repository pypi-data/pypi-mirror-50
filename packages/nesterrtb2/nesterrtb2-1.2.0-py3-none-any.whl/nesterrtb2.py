
""" This is a 'nester.py' module, and it provides one function called
print_lol() which prints lists that may or maynot include nested lists"""

def print_lol(the_list, level=0):
    """
    This function takes a positional largument called "The_list", which is any
    Python list(of,possibly,nested lists). Each data item in the provided list 
    is (recursively) printed to the screen on its own.
    
    A second argument called 'level' is used to instert tab-stops when a nested list is encountered
    """
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end = "")
            print(item)