from mrjob.job import MRJob
from nltk.stem import WordNetLemmatizer
from datetime import datetime
import sys
import re

"""Regex of a Word in a file.
"""
WORD_RE = re.compile(r"[\w']+")

class WordClassProbabilityJob(MRJob):
    """Job defined for a word & probability of each severity classes.
    
    Arguments:
        MRJob {class} -- This class contains methods that define the steps of our job.
    """
    def mapper(self, _, line):
        """Mapper for each word & severity classes in a bug report. 
        
        Arguments:
            _ {int} -- Line number
            line {string} -- Row in a bug report.
        """
        try:
            bug_id, text, severity = line.split('\t\t')
            for word in WORD_RE.findall(text):
                # print("Mapper: ", word, rand_number)
                lemmatizer = WordNetLemmatizer()
                yield lemmatizer.lemmatize(word.lower()), severity # Bug Severity Class
        except Exception as exception:
            with open('job1-logs.txt', 'w') as fp_job1_log:
                fp_job1_log.write(str(exception))

    def reducer(self, word, classes): # list of classes
        """Reducer for each word & severity class with its probability in a bug report.
        """
        try:
            output_list = []
            list_of_classes = list(classes)
            total_num_of_classes = len(list_of_classes)
            # print("Reducer: ", word, list_of_classes)
            encountered_list = []
            for each_class in list_of_classes:
                if each_class not in encountered_list:
                    count_of_class = 0
                    for each_element in list_of_classes:
                        if each_element == each_class:
                            count_of_class += 1
                    output_list.append(
                        {"class": each_class, "probability": (count_of_class/total_num_of_classes)}
                    )
                    encountered_list.append(each_class)
            yield word, output_list

        except Exception as exception:
            with open('job1-logs.txt', 'w') as fp_job1_log:
                fp_job1_log.write(str(exception))
            
            
            
            

if __name__ == '__main__':
    start_time = datetime.now()
    WordClassProbabilityJob.run()
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    sys.stderr.write(str(elapsed_time))