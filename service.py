"""
    :author: Mikhail V. Kozlov
    :date: 13 dec 2024
"""

import struct
import numpy as np
import wave
from io import BytesIO
from flask import Flask, request, make_response, send_file
from flask import Response, after_this_request

SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2
CHANNELS = 2


app = Flask(__name__)


@app.after_request
def remove_header(response):
    # Prepare all the local variables you need since the request context
    # will be gone in the callback function

    @response.call_on_close
    def process_after_request():
        del response.headers['Cache-Control']
        del response.headers['Connection']
        del response.headers['Server']

    return response


@app.route('/sound/api/generate', methods=["GET"])
def proc_request():

    bad_request = False
    second_freq = False

    if 'freq_start' not in request.form:
        bad_request = True

    if 'amplitude' not in request.form:
        bad_request = True

    if 'duration_seconds' not in request.form:
        bad_request = True

    if bad_request:
        return "Missing header entry", 400

    freq_0 = float(request.form['freq_start'])
    amplitude = int(request.form['amplitude'])
    duration = float(request.form['duration_seconds'])

    if 'freq_end' in request.form:
        freq_1 = float(request.form['freq_end'])
    else:
        second_freq = True

    if amplitude < 0:
        return "Bad parameter: negative amplitude", 400
    if amplitude > 32767:
        return "Bad parameter: amplitude is too large", 400


    mem = BytesIO()
    snd_output = wave.open(mem, 'w')
    snd_output.setparams((CHANNELS, SAMPLE_WIDTH, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
    sample_len = int(SAMPLE_RATE * duration)

    if not second_freq:
        arr = np.zeros(sample_len, dtype = np.int16)
        phi = 0.0

        for i in range(1, sample_len):
            freq = freq_0 + (freq_1 - freq_0) * i / sample_len
            phi += 2.0 * np.pi * freq / SAMPLE_RATE
            arr[i] = (amplitude * np.sin(phi)).astype(np.int16)
    else:
        factor = 2.0 * np.pi * freq_0 / SAMPLE_RATE
        arr = np.array([amplitude * np.sin(factor * x) for x in range(0, sample_len)]).astype(np.int16)

    values = []

    for x in arr:
        values.append(struct.pack('<hh', x, x)) # Pack as two signed shorts, little endian

    snd_output.writeframes(b''.join(values))
    snd_output.close()

    mem.seek(0)

    response = send_file(
        mem,
        mimetype = 'audio/wav',
        as_attachment = False,
    )

    return response

