import json
import requests

def grade_lab():
    user_ns = tuple(get_ipython().user_ns.items())
    user_id = ''
    lab_name = ''
    import os
    # if value_type == int:
    for name, value in user_ns:
	#print(name,'::', value)
        if name == 'user_id':
            user_id = value
        if name == 'nb_name':
            lab_name = value
            lab_name = os.path.basename(lab_name).split('.')[0]

    input_content_file = lab_name + '.ipynb'
    parsed_json = ''
    with open(input_content_file) as json_data:
        parsed_json = json.load(json_data)

    code_content = ''
    cells = parsed_json['cells']
    for cell in cells:
        cell_type = cell['cell_type']

        if 'metadata' not in cell:
            # raise ValueError("No metadata found")
            code_cell = cell['source']
            for code_line in code_cell:
                code_content = code_content + '\n' + code_line

        if cell_type == 'code':
            if cell['metadata'].get('tags') == None or cell['metadata'].get('tags')[0] not in ['grade', 'gradehelper']:

                code_cell = cell['source']
                for code_line in code_cell:
                    code_content = code_content + '\n' + code_line
    result = send_lab_for_grading(user_id, lab_name,code_content)
    return result


def send_lab_for_grading(user_id, lab_name,lab_content):
    # api-endpoint
    URL = "https://labgradeapi.herokuapp.com/rf/api/v1.0/lab"

    # defining a params dict for the parameters to be sent to the API
    data = {'code': lab_content, 'userid': user_id, 'labname': lab_name }

    # sending get request and saving the response as response object
    r = requests.post(url=URL, json=data)
    return r.text

