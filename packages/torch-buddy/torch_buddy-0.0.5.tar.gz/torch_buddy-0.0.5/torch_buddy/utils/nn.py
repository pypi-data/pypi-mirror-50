# @Author: yican.kz
# @Date: 2019-08-02 11:41:06
# @Last Modified by:   yican.kz
# @Last Modified time: 2019-08-02 11:41:06

import string
import unicodedata


# ==============================================================================
# 自然语言相关
# ==============================================================================
def word_idx(sentences):
    """
        sentences should be a 2-d array like [['a', 'b'], ['c', 'd']]
    """
    word_2_idx = {}
    for sentence in sentences:
        for word in sentence:
            if word not in word_2_idx:
                word_2_idx[word] = len(word_2_idx)

    idx_2_word = dict(zip(word_2_idx.values(), word_2_idx.keys()))
    num_unique_words = len(word_2_idx)
    return word_2_idx, idx_2_word, num_unique_words


def unicode_to_ascii(s):
    """
        Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
        Example: print(unicode_to_ascii('Ślusàrski'))
    """
    all_letters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn" and c in all_letters)
