from mrjob.job import MRJob
from nltk.corpus import stopwords
import re
import random
import nltk
from nltk.stem import WordNetLemmatizer

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

"""Regex of a Word in a file.
"""
WORD_RE = re.compile(r"[\w']+")

class NormalizedBagofWordsInBugReport(MRJob):
    """Job defined for normalizing bug report description.
    
    Arguments:
        MRJob {class} -- This class contains methods that define the steps of our job.
    """
    def mapper(self, _, line):
        try:
            # print("Mapper: ", word, rand_number)
            bug_id, text, severity = line.split('\t\t')

            stop = set(stopwords.words('english'))
            lemmatizer = WordNetLemmatizer()

            yield bug_id, [lemmatizer.lemmatize(word.lower()) for word in WORD_RE.findall(text) if word not in stop] # Bug Report
        except Exception as exception:
            with open('job3-logs.txt', 'w') as fp_job3_log:
                fp_job3_log.write(str(exception))


if __name__ == '__main__':
    NormalizedBagofWordsInBugReport.run()