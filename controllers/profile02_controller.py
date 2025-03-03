from flask_restx import Resource, reqparse, abort
from services.profile02_service import generate_profile

profile_parser = reqparse.RequestParser()
for i in range(7):
    profile_parser.add_argument(f"q{i+1}", type=int, required=True, help=f"Question {i+1} answer index cannot be blank")

class ProfileController(Resource):
    @classmethod
    def post(cls):
        args = profile_parser.parse_args()
        answer_indices = [args[f'q{i+1}'] for i in range(7)]

        try:
            profile = generate_profile(answer_indices)
            return profile, 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception as e:
            abort(500, str(e))