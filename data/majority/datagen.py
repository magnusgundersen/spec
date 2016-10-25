import random
def generate_majority_file(filename, vector_size, number_of_vectors, difficulty):
    """
    creates a file with the given name, with a given number of vectors
    1: a large part if full with ones
    2: 50-50
    3: a good mix of all possibilities

    :param filename:
    :param vector_size:
    :param difficulty:
    :return:
    """
    content = ""


    for _ in range(number_of_vectors):
        temp_content = ""
        if difficulty==1:
            probability_ones = random.randrange(80,100)
        elif difficulty==2:
            probability_ones = random.randrange(45,55)
        elif difficulty==3:
            probability_ones = random.randrange(0,100)

        number_of_ones = 0
        number_of_zeros = 0
        for _ in range(vector_size):
            rand = random.random()
            if rand >(probability_ones/100):
                temp_content += "0"
                number_of_zeros += 1

            else:
                temp_content += '1'
                number_of_ones += 1

        if number_of_ones >= number_of_zeros:
            temp_content += " 1"
            content += temp_content
        elif number_of_zeros >= number_of_ones:
            temp_content += " 0"
            content += temp_content
        else:
            continue
        content += "\n"

    with open(filename,'w+') as f:
        f.write(content)


generate_majority_file('12_bit_mix_5000',12,5000,2)


