def file_data(file_name):
    """Reads data from the file passed in the parameter.
    Returns a collection data type with each element from the file. 
    """
    file = open(file_name, "r")
    data = file.readlines()
    file.close()
    return data

def data_list(file):
    """Creates a list data to store the data from file
    Returns the data from the file in 2D list
    """
    data = []
    for each in file:
        data.append(each.replace("\n", "").split(","))
    return data

