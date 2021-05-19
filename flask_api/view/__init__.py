import jwt
from flask import request, jsonify, current_app, Response, g, Flask
from flask.json import JSONEncoder
from functools import wraps


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return JSONEncoder.default(self, o)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                payload = None
            if payload is None:
                return Response(status=401)

            user_id = payload['user_id']
            g.user_id = user_id
            g.user = get_user(user_id) if user_id else None
        else:
            return Response(status=401)
        return f(*args, **kwargs)
    return decorated_function


def create_endpoints(app: Flask, services):
    app.json_encoder = CustomJSONEncoder
    user_service = services.user_service
    tweet_service = services.tweet_service

    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"

    @app.route("/login", methods=["POST"])
    def login():
        credential = request.json
        email = credential['email']
        password = credential['password']
        row = database.execute(text("""
            SELECT id, hashed_password FROM users WHERE email=:email
        """), {"email": email}).fetchone()

        if row and bcrypt.checkpw(password.encode('UTF-8'), row['hashed_password'].encode('UTF-8')):
            user_id = row["id"]
            payload = {
                'user_id': user_id,
                'exp': datetime.datetime.utcnow() + timedelta(seconds=60*60*24)
            }
            token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], 'HS256')
            return jsonify({'access_token': token.decode('UTF-8')})
        else:
            return '', 401

    @app.route("/sign-up", methods=["POST"])
    def sign_up():
        new_user = request.json
        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('UTF-8'),
                                             bcrypt.gensalt())
        new_user_id = insert_user(new_user)
        new_user = get_user(new_user_id)
        return jsonify(new_user)

    @app.route("/tweet", methods=["POST"])
    @login_required
    def tweet():
        user_tweet = request.json
        tweet_str = user_tweet['tweet']
        if len(tweet_str) > 300:
            return '300자를 초과했습니다.', 400
        insert_tweet(user_tweet)
        return '', 200

    @app.route("/follow", methods=['POST'])
    @login_required
    def follow():
        payload = request.json
        insert_follow(payload)
        return '', 200

    @app.route('/unfollow', methods=['POST'])
    @login_required
    def unfollow():
        payload = request.json
        insert_unfollow(payload)
        return '', 200

    @app.route('/timeline/<int:user_id>', methods=['GET'])
    @login_required
    def timeline(user_id):
        return jsonify({
            'user_id': user_id,
            'timeline': get_timeline(user_id)
        })

    return app