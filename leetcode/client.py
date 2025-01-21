import requests
from config import LEETCODE_SESSION_TOKEN, CSRF_TOKEN
from .queries import GET_QUESTIONS, GET_PYTHON_SOLUTIONS, GET_SOLUTION_DETAIL

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

    def get_python_solutions(self, question_slug):
        print(f"\nFetching solutions for question slug: {question_slug}")
        # First get the solution articles list
        variables = {
            "questionSlug": question_slug,
            "skip": 0,
            "first": 15,
            "orderBy": "HOT",
            "tagSlugs": ["python3"]
        }
        result = self.execute_query(GET_PYTHON_SOLUTIONS, variables)
        solutions = result['data']['ugcArticleSolutionArticles']['edges']
        print(f"Found {len(solutions)} initial solution entries")
        
        # Then get detailed content for each solution
        detailed_solutions = []
        for solution in solutions:
            node = solution['node']
            detail_vars = {
                "uuid": node['uuid'],
                "title": node['title'],
                "slug": node['slug'],
            }
            print(f"Fetching details for solution with vars: {detail_vars}")
            
            detail_result = self.execute_query(GET_SOLUTION_DETAIL, detail_vars)
            
            if 'data' in detail_result and detail_result['data']['ugcArticleSolutionArticle']:
                solution_data = detail_result['data']['ugcArticleSolutionArticle']
                detailed_solution = {
                    'summary': solution_data['summary'],
                    'author_name': solution_data['author']['userName'],
                    'created_at': solution_data['createdAt'],
                    'updated_at': solution_data['updatedAt']
                }
                print(f"Successfully extracted solution by {detailed_solution['author_name']}")
                detailed_solutions.append(detailed_solution)
            else:
                print(f"Failed to get details for uuid: {detail_vars['uuid']}")
                print(f"Response: {detail_result}")
        
        print(f"Returning {len(detailed_solutions)} detailed solutions\n")
        return detailed_solutions