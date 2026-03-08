from app.models.answer_option import AnswerOption
from app.utils.test_config import AXES_CONFIGURATION


class ScoringService:

    @staticmethod
    def calculate_scores(answers):

        scores = {}

        for axis_name, config in AXES_CONFIGURATION.items():

            total = 0
            count = 0

            for bloc_name, questions in config.items():

                if bloc_name == "invert":
                    continue

                for q_id in questions:

                    answer_option_id = answers.get(q_id)

                    if not answer_option_id:
                        continue

                    option = AnswerOption.query.get(answer_option_id)

                    score = option.score_value

                    # vérifier inversion
                    for inv_bloc, inv_q in config.get("invert", []):
                        if inv_q == q_id:
                            score = 6 - score

                    total += score
                    count += 1

            scores[axis_name] = round(total / count, 2) if count else 0

        return scores