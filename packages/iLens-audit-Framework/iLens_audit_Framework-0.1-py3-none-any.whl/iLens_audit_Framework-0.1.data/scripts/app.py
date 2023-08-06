from flask import Flask, request
from flask_cors import CORS
from bin.common import AppConfigurations
import traceback
from bin.core.applications import AuditManagement
from bin.core.services.audit_service import audit_configuration_blueprint
from bin.common import AppConfigurations

app = Flask(__name__)
# result = AuditManagement.save_audit_entry()
# print(result)

app.register_blueprint(audit_configuration_blueprint)
CORS(app, resources={r"/*": {"origins": "*"}})

app.run(host='0.0.0.0', port=AppConfigurations.PORT, debug=False, threaded=True, use_reloader=False)
# if __name__ == '__main__':
#     try:
#         app.run(host='0.0.0.0', port=int(AppConfigurations.PORT), debug=True, threaded=True, use_reloader=False)
#         print("going")
#         result = AuditManagement.save_audit_entry()
#         print(result)
#     except:
#         traceback.print_exc()