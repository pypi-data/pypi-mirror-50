# Removing pairwise duplicate emails

import linecache
import math
import os
from collections import Counter
from collections import namedtuple
from operator import attrgetter
from tqdm import tqdm


def normalize_vector(vec: Counter, text: str) -> Counter:
    """
    Normalization of vectors

    :param vec:
    :param text:
    :return:
    """

    # normalize vector by dividing count of each word by length of string
    for key in vec.keys():
        vec[key] /= len(text.split())

    # return the normalized vector
    return vec


def get_cosine_similarity(text1_: str, text2_: str) -> float:
    """
    Calculate cosine similarity between two strings

    This code is taken from with few modifications:
    https://stackoverflow.com/a/15174569

    :param text1_:
    :param text2_:
    :return:
    """

    # convert text to vector and normalize the vector
    vec1 = normalize_vector(text_to_vector(text1_), text1_)
    vec2 = normalize_vector(text_to_vector(text2_), text2_)
    # get intersection of string sets
    intersection = set(vec1.keys()) & set(vec2.keys())
    # calculate numerator of cosine similarity formula
    numerator = sum([vec1[a] * vec2[a] for a in intersection])

    # calculate magnitude of vectors
    mag_a = sum([vec1[a] ** 2 for a in vec1.keys()])
    mag_b = sum([vec2[b] ** 2 for b in vec2.keys()])
    # calculate denominator of cosine similarity formula
    denominator = math.sqrt(mag_a) * math.sqrt(mag_b)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text: str) -> Counter:
    """
    Convert text to vector

    :param text:
    :return:
    """

    # split text into list of token/components
    words_ = text.split()
    # return counter object containing token/components and respective counts
    return Counter(words_)


def pick_lengthiest(text_list: list) -> str:
    """
    Pick the lengthiest of a list of similar texts
    by calculating cosine similarity score pairwise.

    :param text_list:
    :return:
    """
    # namedtuple to store pair wise cosine similarity scores
    similars = namedtuple('similars', 'score text1 text2')

    # create list of paired texts and their respective similarity score
    similarities = [similars(get_cosine_similarity(text_list[i_], j_), text_list[i_], j_)
                    for i_ in range(len(text_list) - 1)
                    for j_ in text_list[i_ + 1:]]

    # sort list in ascending order of similarity score
    similarities.sort(key=attrgetter('score'))

    # get the pair of texts with least similarity score
    text1_ = getattr(similarities[0], 'text1')
    text2_ = getattr(similarities[0], 'text2')

    # return the lengthiest text from the pair
    return text1_ if len(text1_) > len(text2_) else text2_


def verify_path(path: str) -> bool:
    """
    Validate file path. Raise an error if file path is invalid

    :param path:
    :return:
    """
    if not path:
        raise Exception('Invalid arguments')

    if not os.path.exists(path):
        raise OSError('File not found: ', path)

    return os.path.exists(path)


def block_filtering(preprocessed_file: str = None,
                    unprocessed_text_file: str = None,
                    preprocessed_filtered_file: str = './preprocessed_filtered.txt',
                    preprocessed_duplicates_file: str = './preprocessed_duplicates.txt',
                    unprocessed_filtered_file: str = './unprocessed_filtered.txt',
                    unprocessed_duplicates_file: str = './unprocessed_duplicates.txt',
                    threshold: float = 0.5) -> None:
    """
    Remove duplicate texts in the input file and save unique texts to preprocessed_filtered_file.
    At the same time save unique unprocessed texts to unprocessed_filtered_file.
    Save the duplicate texts to preprocessed_duplicates_file and unprocessed_duplicates_file.
    See read me for examples

    :param preprocessed_file: preprocessed unfiltered file
    :param unprocessed_text_file:
    :param preprocessed_filtered_file:
    :param preprocessed_duplicates_file:
    :param unprocessed_filtered_file:
    :param unprocessed_duplicates_file:
    :param threshold:
    :return:
    """
    pff, pdf, uff, udf = None, None, None, None

    # validate the input file paths
    if verify_path(preprocessed_file):
        pff = open(preprocessed_filtered_file, 'w')
        pdf = open(preprocessed_duplicates_file, 'w')

    if unprocessed_text_file and verify_path(unprocessed_text_file):
        uff = open(unprocessed_filtered_file, 'w')
        udf = open(unprocessed_duplicates_file, 'w')

    # temporary list to store similar texts
    duplicates = []
    # temporary list to store index of similar texts
    duplicates_idx = []

    number_of_lines = len(open(preprocessed_file).readlines())

    # iterate through all the texts
    for i in tqdm(range(number_of_lines)):

        # read two texts at a time
        text1 = linecache.getline(preprocessed_file, i + 1)
        text2 = linecache.getline(preprocessed_file, i + 2)

        # calculate cosine similarity score
        cosine = get_cosine_similarity(text1, text2)

        # if cosine similarity score is greater than given threshold
        # append the text to a temporary list and its respective index
        if cosine > threshold:
            duplicates.append(text1)
            duplicates_idx.append(i + 1)
        # if there is break in similarity i.e. if cosine similarity score is less than the threshold
        else:
            # if there are no texts in the temp list
            if not duplicates and not duplicates_idx:
                # append text to the file
                pff.write(text1)
                # get the original text and write to original filtered fle
                line = linecache.getline(unprocessed_text_file, i + 1)
                if uff: uff.write(line)
            else:
                # if the list is not empty
                # append the text and its respective index to the list
                duplicates.append(text1)
                duplicates_idx.append(i + 1)

                # pick the lengthiest of the texts from the list
                lengthiest = pick_lengthiest(duplicates)

                # get the index of lengthiest text in temp list
                lengthiest_list_ind = duplicates.index(lengthiest)

                # pop the lengthiest text from the list
                duplicates.pop(lengthiest_list_ind)

                # pop index of lengthiest text from duplicates_idx to get
                # index of text from original file
                lengthiest_file_ind = duplicates_idx.pop(lengthiest_list_ind)

                # create list of remaining texts
                remaining = [linecache.getline(unprocessed_text_file, k) for k in duplicates_idx]

                # write lengthiest text to 'preprocessed_filtered.txt' and
                # original text to 'unprocessed_filtered.txt'
                pff.write(lengthiest)
                if uff: uff.write(linecache.getline(unprocessed_text_file, lengthiest_file_ind))

                # write the remaining similar texts to the 'preprocessed_duplicates.txt'
                # and remaining original similar texts to the 'unprocessed_duplicates.txt'
                pdf.writelines(duplicates)
                if udf: udf.writelines(remaining)

                # clear the lists after writing to files
                duplicates.clear()
                duplicates_idx.clear()

        # print('\n', i, ' Cosine similarity:', cosine)

    # close all the file handles
    pff.close()
    pdf.close()

    if uff and udf:
        uff.close()
        udf.close()


def loop_filtering(preprocessed_file: str = None,
                   unprocessed_text_file: str = None,
                   output_file: str = r'./preprocessed_filtered.txt',
                   unprocessed_filtered_file: str = r'./unprocessed_filtered.txt',
                   saved_file: str = None,
                   threshold: float = 0.99):
    """
    Filter texts using double for loop and save the unique texts to new file.

    :param preprocessed_file:
    :param unprocessed_text_file:
    :param output_file:
    :param unprocessed_filtered_file:
    :param saved_file:
    :param threshold:
    :return:
    """
    texts, unprocessed_texts = [], []

    # validate the input file paths
    if verify_path(preprocessed_file):
        texts = open(preprocessed_file).readlines()

    if unprocessed_text_file and verify_path(unprocessed_text_file):
        unprocessed_texts = open(unprocessed_text_file).readlines()

    temp_texts = {}  # containing indices for looking up the actual texts, these contain the texts that are similar

    # use the deleted list containing indices to delete the texts from the non preprocessed file
    # add the indices of the ones to delete
    delete_texts = set()
    # write filtered texts and duplicate texts in separate files
    start_i = 0

    if saved_file:
        if verify_path(saved_file):
            line = open(saved_file, 'r').readlines()
            dict_obj = eval(line[0])
            start_i = dict_obj['position']
            texts = dict_obj['text']
            if unprocessed_texts: unprocessed_texts = dict_obj['text_orig']

    for i in tqdm(range(start_i, len(texts) - 1)):
        # print("\nIteration: ", i, "\n")
        # every 100 iterations, prompt user to see if they want to stop
        if (i + 1) % 100 == 0:
            USER_INPUT = input("Would you like to STOP? If yes, please enter 'y'. If no, please enter 'n': ")
            if USER_INPUT == 'y':
                new_dict = {"position": i + 1, "text": texts, "text_orig": unprocessed_texts}
                # save the status file to the current directory
                # This status file will be later used to resume the filtering process
                with open(r'./saved_file.txt', 'w') as new_file:
                    new_file.write(str(new_dict))
                exit()

        text1 = texts[i]
        # If the first text is '@@@', then skip the current iteration
        if text1 == '@@@':
            continue

        for j in range(i + 1, len(texts)):
            text2 = texts[j]

            # If the second text is '@@@', then skip the current iteration
            if text2 == '@@@':
                continue

            # calculate cosine similarity score
            cosine = get_cosine_similarity(text1, text2)

            # if cosine similarity score is greater than given threshold
            # add the text to the temp_texts dictionary with index as its key
            if cosine > threshold:
                temp_texts[j] = text2
            else:
                continue

        # if there are texts in temp_texts, then print the similar texts to the screen
        if temp_texts:
            print('\n', '-' * 45)
            print('TEXT 1: ', text1)
            for k, v in temp_texts.items():
                print(k, ': ', v, '\n')
        else:
            continue

        # ensure that the inputs match the ones in the dict temp_texts
        delete_lst = ''

        # Prompt for user input of indices to delete
        while not delete_lst:
            delete_lst = input(
                'Enter the indices of the texts to delete and separated with '
                'spaces. Otherwise to KEEP ALL TEXTS, ENTER -1. To DELETE ALL TEXTS, ENTER -2: ')

        # Ask for user input until right indices are entered
        while True:
            if delete_lst == '-1':
                break
            if delete_lst == '-2':
                break

            if [x for x in delete_lst.split() if int(x) not in temp_texts.keys()]:
                print(
                    "ERROR: you have entered an index that is not in temp_texts. Please enter an index that is in temp_texts")
                delete_lst = input(
                    'Enter the indices of the texts to delete and separate with spaces. '
                    'Otherwise to keep ALL TEXTS, ENTER -1: ')
                continue
            else:
                break

        print()

        # Keep all texts
        if delete_lst == '-1':
            temp_texts.clear()
            delete_texts.clear()
            continue

        # Delete all texts
        if delete_lst == '-2':
            for x in temp_texts.keys():
                delete_texts.add(int(x))

            for idx in delete_texts:
                # Replace the texts to be deleted with '@@@'
                texts[idx] = '@@@'
                unprocessed_texts[idx] = '@@@'

            temp_texts.clear()
            delete_texts.clear()

            continue

        # Delete select texts
        lst = delete_lst.split(' ')  # return a list containing the indices
        for x in lst:
            delete_texts.add(int(x))

        for idx in delete_texts:
            # Replace the texts to be deleted with '@@@'
            texts[idx] = '@@@'
            unprocessed_texts[idx] = '@@@'

        print('DELETED TEXTS: ', delete_texts)
        temp_texts.clear()
        delete_texts.clear()

    # after everything is finished, write to file
    with open(output_file, 'w') as f:
        for text in texts:
            if text == '@@@':
                continue
            f.write(text)

    # after everything is finished, write to file
    with open(unprocessed_filtered_file, 'w') as orig_file:
        for text in unprocessed_texts:
            if text == '@@@':
                continue
            orig_file.write(text)
