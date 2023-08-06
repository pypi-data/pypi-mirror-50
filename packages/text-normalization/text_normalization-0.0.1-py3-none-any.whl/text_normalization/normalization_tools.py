import re
from num2words import num2words
from text_normalization.language_variables import language_variables


class Text:
    def __init__(self, file_name, lang='en', sentence_delimiters='.!?'):
        # define instance variables
        self.filename = file_name
        self.text = [line.strip() for line in open(self.filename, 'r').readlines()]
        self.language = lang
        self.delimiters = sentence_delimiters
        self.datesReplace()
        self.removeNameAbbrevs()
        self.replaceSpecialChars()
        self.replaceNumsWithCommas()
        self.numbersToText()

    # define methods

    def datesReplace(self):
        reg_1 = r'\b(\d{2}|\d{1})[/-](\d{2}|\d{1})[/-](\d{2}|\d{4})\b'  # DD/-MM/-YY(YY)
        reg_2 = r'\b(\d{4})[/-](\d{1}|\d{2})[/-](\d{2}|\d{1})\b'  # YYYY/-M(M)/-D(D)
        text_no_dates = []
        for line in self.text:
            while re.search(reg_1, line):
                obj = re.search(reg_1, line).group()
                tmp = line.replace(obj, self.dateToStr(obj, self.language, form='1'))
                line = tmp
            while re.search(reg_2, line):
                obj = re.search(reg_2, line).group()
                tmp = line.replace(obj, self.dateToStr(obj, self.language, form='2'))
                line = tmp
            text_no_dates.append(line)
        self.text = text_no_dates

    def dateToStr(self, d, form):
        # Input Arg1: d is a string that represents a date
        # Input Arg2: form it the format of the date
        #             --> '1' for DD/-MM/-YYYY  -->'2' for YYYY/-MM/-DD
        splitted = re.split(r'/|-', d)
        months = language_variables.months_all[self.language]
        if form == '1':
            try:
                month_str = months[splitted[1]]
                day_str = num2words(int(splitted[0]), lang=self.language, ordinal=True)
            except KeyError:
                month_str = months[splitted[0]]
                day_str = num2words(int(splitted[1]), lang=self.language, ordinal=True)
            finally:
                year_str = self.yearToStr(splitted[2], self.language)
        else:
            try:
                month_str = months[splitted[1]]
                day_str = num2words(int(splitted[2]), lang=self.language, ordinal=True)
            except KeyError:
                month_str = months[splitted[2]]
                day_str = num2words(int(splitted[1]), lang=self.language, ordinal=True)
            finally:
                year_str = self.yearToStr(splitted[0], self.language)
        return day_str + ' ' + month_str + ' ' + year_str

    def yearToStr(self, a):
        if len(a) == 2:
            return num2words(int(a) + 2000, lang=self.language)
        else:
            return num2words(int(a), lang=self.language)

    def removeNameAbbrevs(self):
        text_no_name_abbrs = []
        for line in self.text:
            line_ = re.sub(r'[A-Z]\.\s', '', line)
            text_no_name_abbrs.append(line_)
        self.text = text_no_name_abbrs

    def replaceSpecialChars(self):
        text_no_percentage = []
        for line in self.text:
            while re.search(r'\b[0-9][%]\s', line):
                obj = re.search(r'\b[0-9][%]\s', line)
                line_ = line.replace(obj.group(), obj.group()[:-2] + language_variables.percentage[self.language])
                line = line_
            text_no_percentage.append(line)
        text_no_slashes = []
        for line in text_no_percentage:
            line_ = line.replace('/', language_variables.slash[self.language])
            text_no_slashes.append(line_)
        self.text = text_no_slashes

    def replaceNumsWithCommas(self):
        # Input Arg1: text is a list of strings that represent lines
        # Output: a list of strings in which no numbers with commas will exist
        regExpr_no_pt = r'\b[0-9]+[,][0-9]+\b'
        regExpr_pt = r'\b[0-9]+[.][0-9]+\b'
        text_no_commas = []
        for line in self.text:
            matches_no_pt = re.findall(regExpr_no_pt, line)
            matches_pt = re.findall(regExpr_pt,line)
            tmp = line
            if self.language != 'pt':
                for match in matches_no_pt:
                    tmp = tmp.replace(match, ''.join(match.split(',')))
            else:
                for match in matches_pt:
                    tmp = tmp.replace(match, ''.join(match.split('.')))
            text_no_commas.append(tmp)
        self.text = text_no_commas


    def numbersToText(self):
        # Input Arg1: text is a list of strings that represent lines
        # Input Arg2: language is a string that represents the language
        #             which numbers are converted to
        # Output: a list of strings with "texted" numbers
        text_no_nums = []
        for line in self.text:
            line_no_nums = ''
            words = line.split()
            for word in words:
                flag = False
                if word[-1] in ',!:?': # special case: number is the last word
                    flag = True
                    tmp = word[-1]
                    word = word[:-1]
                try:
                    float(word)
                    if flag:
                        line_no_nums = line_no_nums + num2words(word, lang=self.language) + tmp
                    elif word[-1] == '.':
                        line_no_nums = line_no_nums + num2words(word, lang=self.language) + '.'
                    else:
                        line_no_nums = line_no_nums + num2words(word, lang=self.language)
                except ValueError:
                    line_no_nums = line_no_nums + word
                finally:
                    line_no_nums = line_no_nums + ' '
            text_no_nums.append(line_no_nums[:-1])
        self.text = text_no_nums

    def textToSentences(self):
        # Input: text is a list of strings without numbers that represent lines
        # Output: a list of strings that represent sentences
        regex_pattern = '|'.join(map(re.escape, self.delimiters))
        # print(regex_pattern)

        sentenced_text = []
        for line in self.text:
            for sentence in re.split(regex_pattern, line):
                sentenced_text.append(sentence)
        no_commas = []
        for line in sentenced_text:
            no_commas.append(line.replace(',', ' '))
        self.text = no_commas

    def removeInvalidWords(self):
        # Input: text is a list os strings representing sentences
        # Output: a list of strings that represent sentences with valid chars in words
        text_valid_words = []
        for sentence in self.text:
            valid_words = re.findall(language_variables.regex_word[self.language], sentence)
            valid_sentence = ' '.join(valid_words)
            text_valid_words.append(valid_sentence)
        final_text = []
        for sent in text_valid_words:
            if not sent.strip():
                continue
            final_text.append(sent)
        self.text = final_text
