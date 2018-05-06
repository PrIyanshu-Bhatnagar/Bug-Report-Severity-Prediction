import json

with open('./Test-Data/bug-report-mozilla-severity.json', 'rb') as fp_severity, open('./Test-Data/bug-report-mozilla-short-description.json', 'rb') as fp_short_desc, open('./Test-Data/bug-report-normalized.txt', 'w') as fp_normalized:
    severity_dict = json.load(fp_severity)
    short_desc_dict = json.load(fp_short_desc)

    total_sev_class_count_dict = {}

    # fp_normalized.write("ID\t\tTEXT\t\tSEVERITY\n")

    for key in short_desc_dict['short_desc'].keys():
        try:
            obj_1 = short_desc_dict['short_desc'][key][0]
            obj_2 = severity_dict['severity'][key][0]

            print(key, '  ', obj_1['what'], '  ', obj_2['what'])
            fp_normalized.write("{}\t\t{}\t\t{}\n".format(key, obj_1['what'], obj_2['what']))

            try:
                total_sev_class_count_dict[obj_2['what']] += 1
            except:
                total_sev_class_count_dict[obj_2['what']] = 1

        except Exception as exception:
            with open('./Test-Data/bugs-report-normalization-log.txt', 'w') as fp_log:
                fp_log.write(str(exception))

    print('Total Severity Classes: ', total_sev_class_count_dict)
