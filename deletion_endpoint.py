import hashlib
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
load_dotenv()
app = Flask(__name__)
verification_token=os.getenv("EBAY_VERFICATION_TOKEN")
endpoint_url=os.getenv("EBAY_ENDPOINT_URL")
@app.route("/ebay/deletion", methods=["GET", "POST"])
def ebay_deletion():
    if request.method=="GET":
        challenge_code=request.args.get("challenge_code")
        if not challenge_code:
            return "missing challenge_code", 400
        to_hash = challenge_code +verification_token+endpoint_url
        digest=hashlib.sha256(to_hash.encode("utf-8")).hexdigest()
        return jsonify({"challengeResponse":digest}), 200
    print("Deletion notification received")
    return "",200
if __name__ == "__main__":
    app.run(port=5000)