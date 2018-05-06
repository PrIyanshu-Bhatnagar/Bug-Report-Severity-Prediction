import json


class NaiveBayes():
    
    def __init__(self, severity_class, bag_of_words):
        self.severity_class = severity_class
        self.bag_of_words = bag_of_words

    def run(self, job1_dict, job2_dict):
        try:
            none_list = []
            probability_of_class = None
            for each_word in self.bag_of_words:
                for each_obj in job1_dict[each_word]:
                    if each_obj['class'] == self.severity_class:

                        if probability_of_class is None and each_obj['probability'] is not None:
                            probability_of_class = each_obj['probability']

                        elif probability_of_class is not None and each_obj['probability'] is not None:
                            probability_of_class = probability_of_class * each_obj['probability']
            
                        break
                
                if probability_of_class is None:
                    none_list.append(each_word)
            
            if probability_of_class is None:
                return 0
            
            total_severity_classes = 0

            for each_sev_class in job2_dict.keys():
                total_severity_classes += job2_dict[each_sev_class]

            probability_of_class *= (job2_dict[self.severity_class]/total_severity_classes)
            return probability_of_class

        except Exception as exception:
            with open('naive-bayes-naive-log.txt','a') as fp_log:
                fp_log.write(str(exception) + "\n")
            return 0


def deserialize():
    try:
        with open('../output/job1_output.txt', 'r') as fp_job1_output, open('../output/job2_output.txt', 'r') as fp_job2_output, open('../output/job3_output.txt', 'r') as fp_job3_output:
            # JOB 1 Deserialize
            job1_dict = {}
            for line in fp_job1_output:
                word, sev_list = line.split('\t')
                job1_dict[json.loads(word)] = json.loads(sev_list)
            
            # JOB 2 Deserialize
            job2_dict = {}
            for line in fp_job2_output:
                word, count = line.split('\t')
                job2_dict[json.loads(word)] = int(count)

            # JOB 3 Deserialize
            job3_dict = {}
            for line in fp_job3_output:
                word, word_list = line.split('\t')
                job3_dict[json.loads(word)] = json.loads(word_list)

            return job1_dict, job2_dict, job3_dict

    except Exception as exception:
        with open('naive-bayes-log.txt', 'a') as fp_log:
            fp_log.write(str(exception) + "\n")


def deserialize_normalised_data():
        with open('Test-Data/bug-report-normalized.txt', 'r') as fp_normalized:
            normailized_dict = {}
            for line in fp_normalized:
                try:
                    bug_id, text, sev = line.split('\t\t')
                    normailized_dict[bug_id] = sev.strip()
                except Exception as exception:
                    with open('naive-bayes-deserialize-log.txt', 'a') as fp_log:
                        fp_log.write(str(exception) + "\n")
                    continue
            
            return normailized_dict
        


def get_actual_severity(bug_id, normalized_dict):
    try:
        return normalized_dict[bug_id]      
    except Exception as exception:
        with open('naive-bayes-log.txt', 'a') as fp_log:
            fp_log.write(str(exception) + "\n")



if __name__ == '__main__':
    job1_dict, job2_dict, job3_dict = deserialize()
    normalized_dict = deserialize_normalised_data()
    
    for each_bug_id in job3_dict.keys():
        list_of_probabilities = []
        max_prob = 0
        max_dict = {
                    "severity_class" : None,
                    "probability": None
                }
        for each_sev_class in job2_dict.keys():
            obj = NaiveBayes(each_sev_class, job3_dict[each_bug_id])
            prob = obj.run(job1_dict, job2_dict)
            temp_dict = {
                    "severity_class" : each_sev_class,
                    "probability": prob
                }
            if prob is not None and prob >= max_prob:
                max_dict = temp_dict
                max_prob = prob

            list_of_probabilities.append(temp_dict)

        print(each_bug_id,'\t', max_dict['severity_class'], '\t', get_actual_severity(each_bug_id, normalized_dict))
        # 
        # print(list_of_probabilities)




