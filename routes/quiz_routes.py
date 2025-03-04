from flask_restx import Namespace
from controllers.quiz_controller import QuizQuestionsController, QuizListController

# 네임스페이스 등록
quiz_ns = Namespace("quiz", description="퀴즈 데이터 API")
quiz_table_ns = Namespace('quiz_table', description='홈 화면 퀴즈 표 html API')

# JSON 요청 파서 설정
quiz_parser = quiz_ns.parser()
quiz_parser.add_argument(
    "include_options",
    type=bool,
    required=False,
    default=True,
    help="선택지를 포함할지 여부 (기본값: True)"
)

# 컨트롤러와 연결 (Swagger에서 quiz_parser 사용)
@quiz_ns.route("/quiz-list")
@quiz_ns.expect(quiz_parser)
class QuizResource(QuizQuestionsController):
    pass