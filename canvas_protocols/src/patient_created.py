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
        compute_on_change_types = [CHANGE_TYPE.PATIENT]
        notification_only = True

    def compute_results(self):
        result = ProtocolResult()
        result.status = STATUS_NOT_APPLICABLE

        if (result.created):
            [yyyy, mm, dd] = self.patient.date_of_birth.split('-')
            send_notification( # a post request
                (self.settings['ts-endpoint'] or 'https://api.tellescope.com') + '/v1/enduser', 
                {
                    "source": "Canvas",
                    "externalId": result.canvas_patient_key,
                    "fname": self.patient.first_name,
                    "lname": self.patient.last_name,
                    "dateOfBirth": mm + "-" + dd + '-' + yyyy,
                    "gender": (
                        "Male" if self.patient.is_male else "Female" if self.patient.is_female else "Unknown"
                    )
                }, 
                { "Authorization: API_KEY " + self.settings['ts-api-key']}
            )

        return result

