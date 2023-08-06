import requests


class Bond:
    def __init__(self, bondIp, bondToken):
        self.bondIp = bondIp
        self.bondToken = bondToken

    def setFanSpeed(self, deviceId, speed):
        return self.doAction(deviceId, 'SetSpeed', {'argument': speed})

    def turnFanOn(self, deviceId):
        return self.doAction(deviceId, 'TurnOn')

    def turnFanOff(self, deviceId):
        return self.doAction(deviceId, 'TurnOff')

    def toggleLight(self, deviceId):
        return self.doAction(deviceId, 'ToggleLight')

    def turnLightOn(self, deviceId):
        return self.doAction(deviceId, 'TurnLightOn')

    def turnLightOff(self, deviceId):
        return self.doAction(deviceId, 'TurnLightOff')

    def doAction(self, deviceId, action, payload={}):
        print(f'http://{self.bondIp}/v2/devices/{deviceId}/actions/{action}')
        print(payload)
        r = requests.put(
            f'http://{self.bondIp}/v2/devices/{deviceId}/actions/{action}', headers={'BOND-Token': self.bondToken}, json=payload)
        return r.content

    def getDevices():
        r = requests.get(f'http://{bondIp}/v2/devices',
                         headers={'BOND-Token': bondToken})
        return r.content
