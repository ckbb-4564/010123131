#Read function
def read_file(PATH):
    text = open(PATH, 'r')
    text_list = text.readlines()
    for index in range(len(text_list)):
        temp = text_list[index].replace('\n', '').strip('"')
        text_list[index] = temp
    return text_list