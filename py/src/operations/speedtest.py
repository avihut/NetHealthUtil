from operations.base_operation import Operation, OperationResult, OperationDelegate
import requests
import time

class SpeedTestOpDelegate(OperationDelegate):
    def speedtest_started(self, op):
        pass

    def speedtest_finished(self, op, result):
        pass

    def speedtest_new_speed_measurement(self, op, speed, progress):
        pass

    def speedtest_failed(self, op, error_message):
        pass

class SpeedTestResult(OperationResult):
    def __init__(self, url, average_download_speed, timestamp=None):
        super().__init__(timestamp=timestamp)
        self.url = url
        self.average_download_speed = average_download_speed

DEV_NULL_PATH = '/dev/null'
CHUNK_SIZE = 10240

class SpeedTestOp(Operation):
    def __init__(self, url, delegate=None):
        if delegate and not isinstance(delegate, SpeedTestOpDelegate):
            raise TypeError('delegate must be of type %s' % SpeedTestOpDelegate.__name__)

        super().__init__(delegate=delegate)
        self.url = url

    def run(self):
        delegate = self.delegate
        delegate.speedtest_started(self) if delegate else None

        with open(DEV_NULL_PATH, 'wb') as dev_null:
            try:
                r = requests.get(self.url, stream=True)
            except requests.exceptions.ConnectionError as e:
                delegate.speedtest_failed(self, 'Failed to establish connection. Please make sure the URL is correct.') if delegate else None
                return

            download_size = r.headers.get('content-length')
            downloaded = 0
            if download_size:
                download_size = int(download_size)
                start = time.time()
                for chunk in r.iter_content(CHUNK_SIZE):
                    downloaded += len(chunk)
                    dev_null.write(chunk)
                    speed = int(downloaded / (time.time() - start)) * 8
                    progress = downloaded / download_size
                    delegate.speedtest_new_speed_measurement(self, speed, progress)
        download_time = time.time() - start

        result = SpeedTestResult(self.url, download_size / download_time * 8)
        delegate.speedtest_finished(self, result)
        return result
