from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Jenkins Configuration
JENKINS_URL = "http://ari24-vm-09407.cust.itsystems.global:8080"
JOB_NAME_VERSION = "jira_version"
JOB_NAME_DATES = "Jira_automation_task_status"  # Updated job name
JENKINS_USER = "kotal"
JENKINS_TOKEN = "113b32a8a923ba406b11c6611df9295769"   


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/trigger-jenkins', methods=['POST'])
def trigger_jenkins():
    data = request.json
    print("DEBUG: Received Data:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    if "version" in data and "clientMail" in data:
        build_url = f"{JENKINS_URL}/job/{JOB_NAME_VERSION}/buildWithParameters"
        params = {
            "Version": data["version"],
            "ClientMail": data["clientMail"]
        }
    elif "fromDate" in data and "toDate" in data and "clientMail" in data:
        build_url = f"{JENKINS_URL}/job/{JOB_NAME_DATES}/buildWithParameters"
        params = {
            "FromDate": data["fromDate"],
            "ToDate": data["toDate"],
            "ClientMail": data["clientMail"]
        }
    else:
        return jsonify({"error": "Invalid or missing parameters"}), 400

    response = requests.post(build_url, auth=(JENKINS_USER, JENKINS_TOKEN), params=params)

    if response.status_code == 201:
        return jsonify({"message": "Jenkins job triggered successfully!"}), 200
    else:
        return jsonify({"error": f"Failed to trigger Jenkins job: {response.text}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
