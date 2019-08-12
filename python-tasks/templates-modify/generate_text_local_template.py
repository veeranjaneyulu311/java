# Veeranjaneyulu

import json
import urllib.parse
import urllib.request


# location of template
file_path = "E:\\python-workspace\\python\\templates\\updated\\TEMPLATE_TEMP_PASSWORD_EMAIL_LINK_SMS.vm"


def generate_template():
    with open(file_path, 'r') as input_line:
        message_content = input_line.read()
        message_content = message_content.replace('\n', '%n')
        parameter_exists = True
        while parameter_exists:
            start = message_content.find('${')
            end = message_content[start:].find('}') + start
            if start != -1:
                parameter_name = message_content[start + 2: end]
                max_length = input('enter max length of ' + parameter_name + '\n')
                parameter_length_type = {'inputtype': 'text', 'maxlength': max_length}
                substitute_parameter_value = "%%|{}^{}%%".format(parameter_name, json.dumps(parameter_length_type))
                message_content = message_content[:start] + substitute_parameter_value + message_content[end+1:]
            else:
                parameter_exists = False
    with open("output.txt", 'a+') as output_line:
        # append to a file in new line
        output_line.write(message_content+"\r\n")


def send_sms(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    print(data)
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)


# url encoding
# print(urllib.parse.quote('hello hi % a | b { c } d ^ ', ' %^{}|'))
# 34,49
# for sending sms
resp = send_sms('bUhKBqSsd5E-Wxx2thIMTfjxgCZzgSQZWxdZnJZdB6', '8500036890',
               'DRUCRE', 'Hello alpha%nPlease Click on 192.168.1.101:8080/#/dru/signup/provider?key=forgotpasswordlink&token=XRA864NQ&userName=alpha_247 to reset your Drucare Account password%n')
print(resp)


# generate_template()


# print(len("imgadmin,srinivas_t,thehulk,receptionist,andrew,imgdoctor,generalnurse,opthdoct,opthdoctor,imgtechnician,harvy123,pedidoctor,surya_s,anvesh_thomas,anirudh_sg,mywarehouse,warehouse,signup_test,chaitanya_dru,marvel,branchadmin,hanuvemu"))