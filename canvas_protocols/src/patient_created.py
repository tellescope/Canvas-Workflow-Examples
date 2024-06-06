from canvas_workflow_kit.utils import (
    send_notification,
)
from canvas_workflow_kit.protocol import (
    ClinicalQualityMeasure,
    ProtocolResult,
    STATUS_NOT_APPLICABLE,
)
from canvas_workflow_kit.constants import (
  CHANGE_TYPE,
)

class MyNotificationProtocol(ClinicalQualityMeasure):
    class Meta:
        version="v1.0.1"
        title='Tellescope Patient Create Webhook'
        description='Creates an Enduser in Tellescope when a Patient is created in Canvas'
        compute_on_change_types = [CHANGE_TYPE.PATIENT]
        notification_only = True

    def compute_results(self):
        result = ProtocolResult()
        result.status = STATUS_NOT_APPLICABLE

        if (result):
            [yyyy, mm, dd] = self.patient.date_of_birth.split('-')
            response = send_notification( # a post request
                (self.settings['ts-endpoint'] if 'ts-endpoint' in self.settings else 'https://api.tellescope.com') + '/v1/enduser', 
                {
                    "source": "Canvas",
                    "externalId": self.patient.patient['id'],
                    "fname": self.patient.first_name,
                    "lname": self.patient.last_name,
                    "dateOfBirth": mm + "-" + dd + '-' + yyyy,
                    "gender": (
                        "Male" if self.patient.is_male else "Female" if self.patient.is_female else "Unknown"
                    )
                }, 
                { "Authorization": "API_KEY " + (self.settings['ts-api-key'] if 'ts-api-key' in self.settings else 'NO_API_KEY_SET' ) } 
            )
            # print(response.status_code, response.reason)

        return result

