def random_mod_string(input_string, change_word=0.8, change_char=0.3):
    import random, string

    word_list = input_string.split()

    # selecting any word at random for modification within the word
    for i, word in enumerate(word_list):
        if random.random() < change_word:
            # selecting any index within the word at random,
            # and modifying it with a random character in [0x0627, 0x0645]
            for j in range(len(word)):
                if random.random() < change_char:
                    word = word[:j] + random.choice(string.ascii_letters + string.digits) + word[j + 1:]

            word_list[i] = word

    return ' '.join(word_list)


def check_difflib_ratio():
    import string, random, difflib

    differ = difflib.Differ()
    min_ratio = 1.0

    for count in range(1000):
        length = random.randint(5, 100)
        s1 = ''.join(random.SystemRandom().choice(string.printable) for _ in range(length))
        s2 = random_mod_string(s1)

        sm = difflib.SequenceMatcher(None, s1, s2)
        ratio = sm.ratio()
        result = list(differ.compare([s1], [s2]))

        for line in result:
            if line.startswith('?'):
                if ratio < min_ratio:
                    min_ratio = ratio
                    break

    print('Minimum ratio which difflib considers as "change" is: {}'.format(min_ratio))


def see_arabic_chars_unicode():
    """
    Arabic character set ranges from 0600–06FF in unicode.
    """
    import unicodedata
    absent = 0
    present = 0
    for i in range(0x0600, 0x06FF + 1):
        try:
            print('{:04X} \t{} --> {}'.format(i, unicodedata.name(chr(i)), chr(i)))
            present += 1
        except ValueError:
            absent += 1
    else:
        print('\nTotal present: {}'.format(present))
        print('\nTotal absent: {}'.format(absent))


def test_pre_processors():
    import sqlite3
    from qurantextdiff.helpers.Preprocess import Cleaner, Splitter

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT verse FROM quran_non_diacritic')
    rows = cursor.fetchall()

    l = []
    for row in rows:
        l.append(row[0])

    input_text = '\n'.join(l)

    splitter = Splitter(input_text)
    split_rows = splitter.get_split_lines()

    cleaner = Cleaner(split_rows)
    cleaned_lines = cleaner.get_cleaned_lines()

    mismatch = 0
    for (row, cl) in zip(rows, cleaned_lines):
        row = row[0].replace('\n', '')
        if row != cl:
            mismatch += 1

    print('No. of mismatch (after running pre-processing on the source in database): {}'.format(mismatch))


if __name__ == '__main__':
    # check_difflib_ratio()
    # see_arabic_chars_unicode()
    test_pre_processors()
