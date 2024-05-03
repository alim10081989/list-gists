from flask import Flask, jsonify
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/users"

class GistsAPI:
    def __init__(self):
        pass

    def check_response(self, url):
        """
        Execute API request and send response

        Args:
          url (str): Github API Url e.g. https://api.github.com/users or https://api.github.com/users/sample-user

        Returns:
          Executed API response

        """
        response = requests.get(url)
        return response

    def search_gists(self, username):
        """
        Search public available gists for user

        Args:
          username (str): Username to search public available gists.

        Returns:
          List of public available gists for mentioned user
        """
        url = f"{GITHUB_API_URL}/{username}/gists"

        try:
            response = self.check_response(url)
            if response.status_code == 200:
                gists_data = response.json()
                if len(gists_data) == 0:
                    return {"message": f"No public gists found for {username}"}
                else:
                    gists_list = [
                        {"id": gist["id"], "url": gist["html_url"]} for gist in gists_data
                    ]
                    return gists_list
            else:
                return {"error": f"Failed to fetch gists from github"}, 500

        except Exception as e:
            return jsonify({"error": str(e)}), 500

api = GistsAPI()

@app.route("/")
def index():
    """
    Main Welcome Page
    """
    return jsonify(
        {
            "message": "Welcome to Gists API. Use '/gists/<username>' endpoint to retrieve user public available Gists."
        }
    )

@app.route("/gists/")
def gists_guide():
    """
    Missing username response page
    """
    return jsonify(
        {
            "message": "Username missing. Use '/gists/<username>' endpoint to retrieve user public available Gists."
        }
    )

@app.route("/<page_name>")
def other_page(page_name):
    response = jsonify({"error": f"The page named {page_name} does not exist."}), 404
    return response

@app.route("/gists/<username>")
def verify_user(username):
    """
    Validate user account availability and display public available gists for mentioned user

    Args:
      username (str): Username to search public available gists. Passed from URL.

    Returns:
      User validation response and list of public available gists for mentioned user

    """
    url = f"{GITHUB_API_URL}/{username}"

    try:
        response = api.check_response(url)

        if response.status_code == 200:
            gists_output = api.search_gists(username)
            return jsonify(gists_output)
        elif response.status_code == 404:
            return jsonify({"error": f"User {username} does not exist"}), 404
        else:
            return jsonify({"error": "Failed to check user"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
