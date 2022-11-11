from flashtext import KeywordProcessor


class AddMultiKeywords:

    def __init__(self, text, keyword_dict):
        self.text = text
        self.keyword_dict = keyword_dict

    def addkey(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keywords_from_dict(self.keyword_dict)  # excepts dictionary checks if values are lists then creates a new dictionary as a class variable.
        extractedKeyword = keyword_processor.extract_keywords(self.text)  # if a sentence consist of a value persent in corpus dictionary created by above line in KeywordProcessor class then that key is selected  and put in to list
        return extractedKeyword                                            # this list is returned

    def key_value(self):
        keyword_spotting = {}
        for i in self.keyword_dict.keys():
            for j in self.keyword_dict[i]:
                if j in self.text:
                    keyword_spotting["key"] = i
                    keyword_spotting["value"] = j
                    keyword_spotting["text"] = self.text

        return keyword_spotting
