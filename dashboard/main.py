from flask import Flask, render_template, request, session
from oauth import Oauth

app = Flask(__name__)
app.config["SECRET_KEY"] = "test123"

@app.route("/")
def home():
	return render_template("index.html",discord_url= Oauth.discord_login_url)

@app.route("/login")
def login():
	code = request.args.get("code")
	print("here")
	at = Oauth.get_access_token(code)
	session["token"] = at

	user = Oauth.get_user_json(at)
	user_name, user_id = user.get("username"), user.get("discriminator")
	
	return f"Success, logged in as {user_name}#{user_id}"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
