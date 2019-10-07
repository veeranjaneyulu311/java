import boto3
# from flask import request, jsonify, Flask
#
# '''
# payload:
# --------
# uid : String
# node_id : String
# timestamp: Integer
# clid: String
# input: Integer
# '''
#
# app = Flask(__name__)
#
# departments = {'11111': ['Cardiology', 'Orthopedics', 'Neurology'], '22222': ['Dermatology', 'Anaesthetics', 'Gynecology', 'Nephrology']}
# doctors = {'11111': {'1': ['D1', 'D2', 'D3'], '2': ['Doctor4', 'Doctor5'], '3': ['D6']}, '67891': {'1': ['D7', 'D8', 'D9'], '2': ['D10', 'D11'], '3': ['D12', 'D13'], '4': ['D14', 'D15', 'D16']}}
# time_slots = {'11111-1': {'1': ['t1', 't2', 't3'], '2': ['t4', 't2'], '3': ['t5']}, '11111-2': {'1': ['t6', 't7'], '2': ['8 AM', '9 AM']}, '11111-3': {'1': ['t11', 't12', 't13']}}
#
#
# # storing users current_status
# users = {}
# response = {"action": 'tts', "value": ''}
#
#
# @app.route('/bookAppointment', methods=['POST'])
# def fetch_all():
#     global users
#
#
#     #request_data = request.get_json()
#     val = request.form["uid"]
#     print(val)
#
#     uid = request.form["uid"]
#     node_id = request.form['node_id']
#     clid = request.form['clid']
#
#     # departments for node id 1
#     # node_id1 '11111' and '22222' represents org_id's or hospitals
#     if node_id == '11111' or node_id == '22222':
#         users[clid] = [node_id]
#         data = ''
#         for i, department in enumerate(departments[node_id], 1):
#             data = data + 'Press ' + str(i) + ' for ' + department + " "
#         response["value"] = data
#         return jsonify(response)
#     # doctors
#     # node_id2 '33333' mapped to departments
#     elif node_id == '33333':
#         data = ''
#         input_option = str(request.form['input'])
#         users[clid].append(input_option)
#         usr = users[clid][0]
#         dr = doctors[usr]
#         dri = dr[input_option]
#         for i, doctor in enumerate(dri, 1):
#             data = data + 'Press ' + str(i) + ' for ' + doctor+ " "
#         response["value"] = data
#         return jsonify(response)
#     # time slots
#     # node_id3 '44444' mapped to time slots
#     elif node_id == '44444':
#         data = ''
#         input_option = str(request.form['input'])
#         users[clid].append(input_option)
#         hos_dep = users[clid][0]+'-'+users[clid][1]
#         for i, time_slot in enumerate(time_slots[hos_dep][input_option], 1):
#             data = data + 'Press ' + str(i) + ' for ' + time_slot+ " "
#         response["value"] = data
#         return jsonify(response)
#     elif node_id == '55555':
#         input_option = str(request.form['input'])
#         users[clid].append(input_option)
#         hos_dep = users[clid][0] + '-' + users[clid][1]
#
#         deptL = doctors[users[clid][0]]
#         drL = deptL[users[clid][1]]
#         dr = drL[int(users[clid][2])-1]
#         timeslots = time_slots[hos_dep][users[clid][2]]
#         slotf = timeslots[int(input_option)-1]
#         data = 'Your Appointment With Doctor '+dr+' at '+ slotf+' time is Booked'
#         response["value"] = data
#         response["operation"] = "hangup"
#         return jsonify(response)
#
#
# # new api for having time slots along with days
# # @app.route('/bookAppointmentNew', methods=['POST'])
# # def fetch_all_new():
# #     global users
# #     request_data = request.get_json()
# #     uid = request_data['uid']
# #     node_id = request_data['node_id']
# #     clid = request_data['clid']
# #     input_option = str(request_data['input'])
# #     # departments for node id 1
# #     if node_id == '11111' or node_id == '22222':
# #         users[clid] = [node_id]
# #         data = ''
# #         for i, department in enumerate(departments[node_id], 1):
# #             data = data + 'Press ' + str(i) + ' for ' + department + ','
# #         return jsonify(data)
# #     # doctors
# #     elif node_id == '33333':
# #         data = ''
# #         users[clid].append(input_option)
# #         for i, doctor in enumerate(doctors[users[clid][0]][input_option], 1):
# #             data = data + 'Press ' + str(i) + ' for ' + doctor + ','
# #         return jsonify(data)
# #     # time slots
# #     elif node_id == '44444':
# #         data = ''
# #         users[clid].append(input_option)
# #         hos_dep = users[clid][0]+'-'+users[clid][1]
# #         for i, time_slot in enumerate(time_slots[hos_dep][input_option][0], 1):
# #             data = data + 'Press ' + str(i) + ' for selecting appointment on' + time_slot + ','
# #         data = data + 'enter any of the following appointment times ' + time_slots[hos_dep][input_option][2]
# #         return jsonify(data.rstrip(','))
# #     elif node_id == '55555':
# #         return jsonify(
# #             'Your Appointment With Dr.' + doctors[users[clid][0]][users[clid][1]][int(users[clid][2])] + ' is Booked')
#
#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port="5000", debug=True)
# import datetime
#
# print(datetime.datetime.today().weekday())












