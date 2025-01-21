from leetcode.client import LeetCodeClient
from database.db import drop_and_init_db, SessionLocal
from database.models import Question, Solution

def main():
    # Drop and reinitialize the database
    print("Dropping and reinitializing database...")
    drop_and_init_db()
    
    client = LeetCodeClient()
    session = SessionLocal()

    print("Fetching questions...")
    # Fetch top 50 questions
    questions = client.get_questions(limit=50)

    for question_data in questions:
        # Create question entry
        question = Question(
            title=question_data['title'],
            title_slug=question_data['titleSlug'],
            difficulty=question_data['difficulty'],
            frontend_id=question_data['frontendQuestionId'],
            ac_rate=str(question_data['acRate'])
        )
        session.add(question)
        session.flush()  # This will assign an ID to the question

        print(f"Fetching solutions for question: {question.title}")
        # Fetch and create solutions for the question
        solutions = client.get_python_solutions(question_data['titleSlug'])
        print(f"Found {len(solutions)} solutions")
        
        for solution_data in solutions:
            print(f"Adding solution by {solution_data['author_name']}")
            solution = Solution(
                question_id=question.id,
                summary=solution_data['summary'],
                author_name=solution_data['author_name'],
                created_at=solution_data['created_at'],
                updated_at=solution_data['updated_at']
            )
            session.add(solution)
            
        # Add an explicit flush after adding solutions for each question
        session.flush()

    session.commit()
    print("Database population completed!")

if __name__ == "__main__":
    main()