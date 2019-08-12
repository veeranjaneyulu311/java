# v2
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


file_path = "D:\\templates\\APPOINTMENT_CANCEL_SMS.vm"
parameter_list = []
new_lines = []


def generate_template():
    with open(file_path, 'r') as input_line:
        message_content = input_line.read()
        index = 0
        count = 0
        while index < len(message_content):
            x = message_content[index]
            if x == '$':
                parameter = {}
                start = flag = index
                parameter['start'] = start
                end = 1
                while start == flag:
                    y = message_content[start+end]
                    if y == '}':
                        parameter['end'] = start+end
                        parameter['name'] = message_content[start+2:start+end]
                        input_type = input('enter input type of '+parameter['name'] + '\n')
                        max_length = input('enter max length of '+parameter['name'] + '\n')
                        parameter['inputtype'] = input_type
                        parameter['maxlength'] = max_length
                        flag = start + 1
                    end = end + 1
                parameter_list.append(parameter)
                index = start+end
            elif x == '\n':
                new_lines.append(index)
                index = index + 1
            else:
                index = index+1
        print(parameter_list)
        print(new_lines)


generate_template()
