import json
import sys

def main(num_of_bug_in_class):

    with open('./Test-Data/bug-report-mozilla-severity.json', 'rb') as fp_severity, open('./Test-Data/bug-report-mozilla-short-description.json', 'rb') as fp_short_desc, open('./Test-Data/bug-report-normalized-{}.txt'.format(num_of_bug_in_class), 'w') as fp_normalized:
        severity_dict = json.load(fp_severity)
        short_desc_dict = json.load(fp_short_desc)

        # fp_normalized.write("ID\t\tTEXT\t\tSEVERITY\n")
        class_checker = {}

        for key in short_desc_dict['short_desc'].keys():
            try:
                obj_1 = short_desc_dict['short_desc'][key][0]
                obj_2 = severity_dict['severity'][key][0]
                
                if obj_2['what'] in class_checker.keys():
                    class_checker[obj_2['what']] += 1
                else:
                    class_checker[obj_2['what']] = 1

                # print('... ', class_checker[obj_2['what']], '<=', num_of_bug_in_class, class_checker[obj_2['what']] <= num_of_bug_in_class)
                if class_checker[obj_2['what']] <= num_of_bug_in_class and obj_2['what'] is not ""  and obj_1['what'] is not "":
                    fp_normalized.write("{}\t\t{}\t\t{}\n".format(key, obj_1['what'], obj_2['what']))

            except Exception as exception:
                with open('./Test-Data/bugs-report-normalization-log-{}.txt'.format(num_of_bug_in_class), 'w') as fp_log:
                    fp_log.write(str(exception))

        print('Class Checker: ', class_checker)



if __name__ == "__main__":
    num_of_bug_in_class = sys.argv[1]
    main(int(num_of_bug_in_class))