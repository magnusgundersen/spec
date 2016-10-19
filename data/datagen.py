import random
def generate_majority_file(filename, vector_size, number_of_vectors, difficulty):
    """
    creates a file with the given name, with a given number of vectors
    Difficulty goes from 1 to 5, where 5 is the hardest one

    :param filename:
    :param vector_size:
    :param percentage_ones:
    :return:
    """
    content = ""


    for _ in range(number_of_vectors):
        if difficulty==1:
            percentage_ones = random.randrange(80,100)
        elif difficulty==5:
            percentage_ones = random.randrange(45,55)
        for _ in range(vector_size):
            rand = random.random()
            if rand >(percentage_ones/100):
                content += "0"
            else:
                content += '1'

        if percentage_ones >= 50:
            content += " 1"
        else:
            content += " 0"
        content += "\n"

    with open(filename+".txt",'w+') as f:
        f.write(content)


generate_majority_file('majority_small',5,100,5)


