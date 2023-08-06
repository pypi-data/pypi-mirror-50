from server import app

@app.route("/api/pos/cpuInit", methods=["POST", "GET"])
def init_data():
    return 'Hello Flask!'