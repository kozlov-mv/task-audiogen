import requests
from datetime import datetime
import argparse, sys


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-f0", "--freq0", required = True, help = "freq_start, Hz, double precision value")
    parser.add_argument("-f1", "--freq1", help = "freq_end, Hz, double presicion value")
    parser.add_argument("-d", "--duration", required = True, help = "duration_seconds, seconds, double presicion value")
    parser.add_argument("-a", "--amplitude", required = True, help = "amplitude, unsigned integer in absolute values")

    args = parser.parse_args()

    url = 'http://127.0.0.1:8000/sound/api/generate'
    header = {'Content-Type': 'application/json'}

    params = {}
    params["freq_start"] = args.freq0
    if args.freq1 is not None:
        params["freq_end"] = args.freq1
    params["duration_seconds"] = args.duration
    params["amplitude"] = args.amplitude

    try:
        resp = requests.get(url, data = params)

        print(resp.status_code)
        print(resp.headers)

        filename = "snd_" + datetime.now().strftime("%Y%m%d-%H%M%S.%f") + ".wav"

        # Write the binary content
        with open(filename, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        print(f'TEST FAILED. Cought {type(e)}')
        exit()

