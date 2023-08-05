def extract_pos(doc, pos, return_list = True, lower_case = True):
    tokens = [t.text for t in doc if t.pos_ == pos]


    if lower_case == True:
        tokens = [t.lower() for t in tokens]

    if return_list == False:
        tokens = ', '.join(tokens)

    return tokens
