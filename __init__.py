import os
import sqlalchemy
from flask import (
    Blueprint,
    Response,
    jsonify,
    render_template_string,
    current_app as app,
)
from itsdangerous import URLSafeSerializer, BadSignature
from CTFd.models import db, Solves, Challenges, Users
from CTFd.utils.user import authed, get_current_user
from CTFd.utils.decorators import admins_only
from CTFd.challenges import listing
from CTFd.plugins import register_plugin_asset, register_plugin_script

# Configuration and constants
SECRET_KEY = os.environ.get(
    "UNIQUE_TOKEN_SECRETKEY", "sdoisaudQWEoqweoiqwue98324uaODSUoiudso"
)
SALT = os.environ.get("UNIQUE_TOKEN_SALT", "asoiduaoisudasoidoasoiudaoiusdoiu")
SERIALIZER = URLSafeSerializer(SECRET_KEY)


# Helper functions
def generate_token_for_user(user_id):
    """Generate a token for a user ID"""
    return SERIALIZER.dumps(user_id, salt=SALT)


def validate_and_get_user_id(token):
    """Validate a token and return the user ID if valid, None otherwise"""
    try:
        return SERIALIZER.loads(token, salt=SALT)
    except BadSignature:
        return None


# Views
def load(app):
    register_plugin_asset(app, asset_path="/plugins/unique_token/unique_token.js")
    register_plugin_script("/plugins/unique_token/unique_token.js")

    token_blueprint = Blueprint(
        "user_token_plugin", __name__, template_folder="templates"
    )

    @token_blueprint.route("/get_user_token", methods=["GET"])
    def get_user_token():
        """Get a token for the current user"""
        if authed():
            user = get_current_user()
            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 403
            token = generate_token_for_user(user.id)
            return jsonify({"status": "success", "token": token})
        return jsonify({"status": "error", "message": "Login first"}), 403

    @token_blueprint.route("/admin-solve/<token>/<challenge_name>", methods=["GET"])
    @admins_only
    def submit_challenge(token, challenge_name):
        """Submit a challenge for a user"""
        user_id = validate_and_get_user_id(token)
        if not user_id:
            return jsonify({"message": "Invalid token", "status": "error"})

        user = Users.query.get(user_id)
        challenges = Challenges.query.filter(Challenges.name == challenge_name).all()

        if not user or not challenges:
            return (
                jsonify({"message": "User or challenge not found", "status": "error"}),
                400,
            )

        for challenge in challenges:
            solve_filters = {"user_id": user_id, "challenge_id": challenge.id}
            if user.team_id:
                solve_filters["team_id"] = user.team_id

            solve = Solves.query.filter_by(**solve_filters).first()
            if not solve:
                try:
                    new_solve = Solves(**solve_filters)
                    db.session.add(new_solve)
                    db.session.commit()
                    return jsonify(
                        {
                            "message": f"Challenge {challenge_name} for user {user.name} solved!",
                            "status": "success",
                        }
                    )
                except sqlalchemy.exc.IntegrityError:
                    db.session.rollback()
                    return jsonify(
                        {
                            "message": "Challenge already solved by another team member",
                            "status": "error",
                        }
                    )
            else:
                return jsonify(
                    {"message": "Challenge already solved", "status": "error"}
                )

    app.register_blueprint(token_blueprint)