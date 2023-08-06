def remove(string):
    punctuations = """!()-[]{"""  +  """};:'"\,<>./?@#$%^&*_~"""
    my_str = string
    
    no_punct = ""
    for char in my_str:
       if char not in punctuations:
           no_punct = no_punct + char
    return no_punct