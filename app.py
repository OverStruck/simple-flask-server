from flask import Flask, jsonify, request
from flask_cors import CORS
from decimal import *
import time
getcontext().prec = 100

app = Flask(__name__)
app.debug = True
CORS(app)

# route used for ALB health checks
@app.route("/health")
def health():
    return "We good fam!"

# route used for k8s liveness probes
@app.route("/healthz")
def healthz():
    return "Internal Check is Goodie..."

@app.route("/oomkill")
def oomkill():
    # allocate 20MB of memory
    x = bytearray(20000000)
    return "Did we die?"

@app.route('/calculatePI')
def main():
    # start timer
    st = time.time()
    # get query parameter reps, defaults to 1 if no query parameter is passed
    reps = request.args.get('reps', 1)
    # cast reps to an integer since it'd be a string
    reps = int(reps)
    # This is the actual start of the algorithm to calculate PI
    result = Decimal(3.0)
    op = 1
    n = 2
    for n in range(2, 2*reps+1, 2):
        result += 4/Decimal(n*(n+1)*(n+2)*op)
        op *= -1
    # end timer
    et = time.time()
    # calculate elapse time to see how long it took to calculate PI
    # experiment with different reps to see how long it takes to calculate PI
    # experiment with different resources limits to see how those affect time as well
    elapsed_time = et - st
    # return the result and elapsed time as a JSON object
    res = {
        "PI": result,
        "elapsed_time": elapsed_time
    }
    response = jsonify(res)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7878, threaded=True)
