# v1
'''
input:
======
Dear ${patientName},
Your appointment with Dr. ${doctorName} at ${orgName} on ${bookigDate} is scheduled.
Call ${hospitalNumbers} for any query .

Thanks,
Drucare

output:
=======
Dear %%|patientName^{"inputtype" : "text", "maxlength" : "20"}%%,
Your appointment with Dr. %%|doctorName^{"inputtype" : "text", "maxlength" : "20"}%% at %%|orgName^{"inputtype" : "text", "maxlength" : "25"}%% on %%|bookigDate^{"inputtype" : "text", "maxlength" : "12"}%% is scheduled.
Call %%|hospitalNumbers^{"inputtype" : "text", "maxlength" : "27"}%% for any query.

Thanks,
Drucare

'''
import json
import re

# D:\\ui\\local-qa-jar\\qajars\\arch\\templates\\APPOINTMENT_CANCEL_SMS.vm
file_path = "D:\\templates\\TEMPLATE_APPOINTMENT_SEND_SMS.vm"


def generate_template():
    with open(file_path, 'r') as input_line:
        generated_response_string = ""
        for line in input_line:
                # Get rid of the trailing newline (if any).
            for word in line.split():
                if re.match(r"^\$\{.*\}", word):
                    modified_word = re.sub('[${},]', '', word)
                    input_type = input("enter input type of "+modified_word + "\n")
                    max_length = input("enter max length of "+modified_word + "\n")
                    param_values = {'inputtype' : input_type, 'maxlength' : max_length}
                    replace_placeholder = "%%|{}^{}%%".format(modified_word, json.dumps(param_values))
                    if ',' in word:
                        replace_placeholder = replace_placeholder+','
                    line = line.replace(word, replace_placeholder)

            line = line.rstrip('\n') + '%n'
            generated_response_string = generated_response_string + line
        generated_response_string = generated_response_string.rstrip('%n')
    with open("output.txt", 'a+') as output_line:
        output_line.write(generated_response_string+"\r\n")


generate_template()
