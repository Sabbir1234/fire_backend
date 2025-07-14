import functions_framework
import replicate
import os
from flask import Request, jsonify

replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

@functions_framework.http
def generate_image(request: Request):
    request_json = request.get_json()

    input_image = request_json.get("input_image")
    iconic_location = request_json.get("iconic_location")

    if not input_image or not iconic_location:
        return jsonify({"error": "Missing input_image or iconic_location"}), 400

    try:
        output = replicate_client.run(
            "flux-kontext-apps/iconic-locations:6ab67e15971723f0ec7767cc8c5178c5a97382fa7ea2f9e445ea16094391b504",
            input={
                "input_image": input_image,
                "iconic_location": iconic_location
            }
        )
        # If output is a list, return the first item
        if isinstance(output, list):
            output = output[0]
        return jsonify({"image_url": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500