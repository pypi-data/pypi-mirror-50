

def build_idx_dict(l, dir_path):
    """
    Given list l, creates a dict with index-filepath pairs per element in the list l
    :param l: list of elements
    :param dir_path: path to the directory containing the files in l
    :return: dict with index-filepath pairs
    """
    d = {}
    for i in range(len(l)):
        d.update({i: dir_path + l[i]})

    return d
