from mrjob.job import MRJob
import re
import random

"""Regex of a Word in a file.
"""
WORD_RE = re.compile(r"[\w']+")


class CountofSeverityJob(MRJob):
    """Job defined for counting severity in a bug report.
    
    Arguments:
        mrjob {class} -- This class contains methods that define the steps of our job.
    """ 

    def mapper(self, _, line):
        try:
            bug_id, text, severity = line.split('\t\t')
            # print("Mapper: ", word, rand_number)
            yield severity.lower(), 1 # Bug Severity Class
        except Exception as exception:
            with open('job2-logs.txt', 'w') as fp_job2_log:
                fp_job2_log.write(str(exception))

    def reducer(self, key, values):
        try:
            yield key, sum(values)
        except Exception as exception:
            with open('job2-logs.txt', 'w') as fp_job2_log:
                fp_job2_log.write(str(exception))


if __name__ == '__main__':
    CountofSeverityJob.run()