import requests


class ThingsboardClient:
    def __init__(self, host):
        self.host = f"http://{host}/api/v1/"

    def send_telemetry(self, device_token, telemetry) -> int:
        response = requests.post(
            self.host + device_token + "/telemetry", json=telemetry
        )

        response.close()
        return response.status_code
