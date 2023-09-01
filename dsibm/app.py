from flask import Flask, request, render_template
import pickle
import requests
import json

app = Flask(__name__)
model = pickle.load(open('placement_data.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('input.html')



@app.route('/input', methods=['POST'])
def pred():
    gender = int(request.form.get('gender'))
    ssc_p = float(request.form.get('ssc_p'))
    ssc_b = int(request.form.get('ssc_b'))
    hsc_p = float(request.form.get('hsc_p'))
    hsc_b = int(request.form.get('hsc_b'))
    hsc_s = int(request.form.get('hsc_s'))
    degree_p = float(request.form.get('degree_p'))
    degree_t = int(request.form.get('degree_t'))
    workex = int(request.form.get('workex'))
    etest_p = float(request.form.get('etest_p'))
    specialisation = int(request.form.get('specialisation'))
    mba_p = float(request.form.get('mba_p'))

    #connecting with  watson_studio  machine_learmning model with API
    API_KEY = "vtc8FbvbLW2FeKLTOvQWPg2bJvfzD5UHg7KA-Kn_YaTF"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                         API_KEY,
                                                                                     "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    payload_scoring = {"input_data": [{"field": [ [
            'gender','ssc_p','ssc_b','hsc_p','hsc_b','hsc_s','degree_p','degree_t','workex','etest_p','specialisation','mba_p'
                        ]],
                                       "values": [[gender,ssc_p,ssc_b,hsc_p,hsc_b,hsc_s,degree_p,degree_t,workex,etest_p,specialisation,mba_p]]
    }]}

    response_scoring = requests.post(
        'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/6d90a728-8477-47bf-95e3-085fb8a29855/predictions?version=2021-05-01',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    st=response_scoring.json()
    print(st)
    if (st['predictions'][0]['values'][0][0]==0):
        op = "less chances/no chances to be placed for placements"
    else:
        op = "high chances to be placed for placements"
    #print(op)
    return render_template('input.html', Output=op)


if __name__ == '__main__':
    app.run(debug=True)
