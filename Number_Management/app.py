from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
port = 8008

request_timeout = 0.5  # seconds

# Helper function to fetch data from a URL with a timeout
def fetch_data(url):
    try:
        response = requests.get(url, timeout=request_timeout)
        return response.json().get('numbers', [])
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data from URL: {url}")
        return []

# Main API endpoint
@app.route('/numbers', methods=['GET'])
def get_numbers():
    url_param = request.args.get('url')

    if not url_param:
        return jsonify({'error': 'At least one URL is required.'}), 400

    urls = url_param if isinstance(url_param, list) else [url_param]

    # Fetch data from all provided URLs concurrently
    all_responses = [fetch_data(url) for url in urls]

    # Merge and sort unique integers
    merged_numbers = sorted(set([num for sublist in all_responses for num in sublist]))

    return jsonify({'numbers': merged_numbers})

# Start the server
if __name__ == '__main__':
    app.run(port=port)

