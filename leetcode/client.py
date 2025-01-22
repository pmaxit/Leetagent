import requests
from config import LEETCODE_SESSION_TOKEN, CSRF_TOKEN
from .queries import GET_QUESTIONS, GET_PYTHON_SOLUTIONS, GET_SOLUTION_DETAIL
from database.models import Attempt, DifficultyRating

class LeetCodeClient:
    def __init__(self, base_url='https://leetcode.com/graphql'):
        self.base_url = base_url
        self.headers = {
            'Cookie': f'LEETCODE_SESSION={LEETCODE_SESSION_TOKEN}',
            'x-csrftoken': CSRF_TOKEN,
            'Content-Type': 'application/json'
        }

    def execute_query(self, query, variables=None):
        response = requests.post(self.base_url, json={'query': query, 'variables': variables}, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_questions(self, limit=50, skip=0):
        variables = {
            "categorySlug": "all-code-essentials",
            "limit": limit,
            "skip": skip,
            "filters": {}
        }
        result = self.execute_query(GET_QUESTIONS, variables)
        return result['data']['problemsetQuestionList']['questions']

    def get_total_questions(self):
        return 5000

    def get_python_solutions(self, question_slug, skip=0, first=15, order_by="HOT", tag_slugs=["python3"]):
        # First get the solution articles list
        variables = {
            "questionSlug": question_slug,
            "skip": skip,
            "first": first,
            "orderBy": order_by,
            "tagSlugs": tag_slugs
        }
        result = self.execute_query(GET_PYTHON_SOLUTIONS, variables)
        solutions = result['data']['ugcArticleSolutionArticles']['edges']
        
        # Then get detailed content for each solution
        detailed_solutions = []
        for solution in solutions:
            node = solution['node']
            detail_vars = {
                "topicId": node['topicId']
            }
            
            detail_result = self.execute_query(GET_SOLUTION_DETAIL, detail_vars)
            
            if 'data' in detail_result and detail_result['data']['ugcArticleSolutionArticle']:
                solution_data = detail_result['data']['ugcArticleSolutionArticle']
                detailed_solution = {
                    'content': solution_data['content'],
                    'summary': solution_data['summary'],
                    'author_name': solution_data['author']['userName'],
                    'created_at': solution_data['createdAt'],
                    'updated_at': solution_data['updatedAt']
                }
                detailed_solutions.append(detailed_solution)
            else:
                print(f"Failed to get details for topicId: {detail_vars['topicId']}")
                print(f"Response: {detail_result}")
        
        return detailed_solutions

    def record_attempt(self, question_id: int, difficulty: DifficultyRating, session):
        """
        Record an attempt for a question and calculate next review date
        
        Args:
            question_id: ID of the question attempted
            difficulty: DifficultyRating enum value (HARD/MEDIUM/EASY)
            session: SQLAlchemy session
        
        Returns:
            Attempt: The created attempt object
        """
        attempt = Attempt(
            question_id=question_id,
            difficulty_rating=difficulty
        )
        
        # Calculate next review date using SM-2 algorithm
        attempt.calculate_next_review(difficulty)
        
        # Add and commit to database
        session.add(attempt)
        session.commit()
        
        print(f"\nRecorded attempt for question {question_id}")
        print(f"Next review scheduled for: {attempt.next_review_at}")
        
        return attempt