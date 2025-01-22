import argparse
from leetcode.client import LeetCodeClient
from database.db import drop_and_init_db, SessionLocal, init_db
from database.models import Question, Solution, Attempt, DifficultyRating
from datetime import datetime
from tqdm import tqdm
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial

async def fetch_batch(client, session, skip, batch_size):
    """Fetch a single batch of questions and their solutions"""
    questions = client.get_questions(limit=batch_size, skip=skip)
    batch_results = []
    
    for question_data in questions:
        question = Question(
            title=question_data['title'],
            title_slug=question_data['titleSlug'],
            difficulty=question_data['difficulty'],
            frontend_id=question_data['frontendQuestionId'],
            ac_rate=str(question_data['acRate'])
        )
        solutions = client.get_python_solutions(question_data['titleSlug'])
        
        batch_results.append({
            'question': question,
            'solutions': [
                Solution(
                    summary=sol['summary'],
                    content=sol['content'],
                    author_name=sol['author_name'],
                    created_at=sol['created_at'],
                    updated_at=sol['updated_at']
                ) for sol in solutions
            ]
        })
    
    return batch_results

def process_batch(start_idx, batch_size):
    """Process a batch in a separate process"""
    client = LeetCodeClient()  # Create new client instance for each process
    session = SessionLocal()  # Create new session for each process
    
    try:
        results = asyncio.run(fetch_batch(client, session, start_idx, batch_size))
        
        # Save results to database within the process
        for result in results:
            question = result['question']
            session.add(question)
            session.flush()
            
            for solution in result['solutions']:
                solution.question_id = question.id
                session.add(solution)
            
        session.commit()
        return len(results)
    except Exception as e:
        print(f"Error in process batch {start_idx}: {str(e)}")
        return 0
    finally:
        session.close()

async def fetch_questions(client, session, total_questions):
    """Fetch and store questions from LeetCode using multiple workers"""
    print(f"Total available questions: {total_questions}")
    
    # Configure batch processing
    num_workers = min(8, (total_questions + 49) // 50)  # Use up to 8 workers, or fewer if limit is small
    print(f"Using {num_workers} workers")
    batch_size = 50
    batches = [(i * batch_size, min(batch_size, total_questions - i * batch_size)) 
               for i in range((total_questions + batch_size - 1) // batch_size)]
    
    progress_bar = tqdm(total=total_questions, desc="Fetching questions")
    
    # Create process pool and execute batches
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for start_idx, size in batches:
            future = executor.submit(process_batch, start_idx, size)
            futures.append(future)
        
        # Monitor progress
        total_fetched = 0
        for future in futures:
            batch_count = future.result()
            total_fetched += batch_count
            progress_bar.update(batch_count)
    
    progress_bar.close()
    print(f"\nFetched {total_fetched} questions with their solutions!")

def show_statistics(session):
    """Display various statistics about questions and attempts"""
    total_questions = session.query(Question).count()
    total_attempts = session.query(Attempt).count()
    questions_with_solutions = session.query(Question).filter(Question.solutions.any()).count()
    
    print("\n=== LeetCode Statistics ===")
    print(f"Total Questions: {total_questions}")
    print(f"Questions with Solutions: {questions_with_solutions}")
    print(f"Total Attempts Made: {total_attempts}")
    
    # Difficulty breakdown
    for difficulty in ['Easy', 'Medium', 'Hard']:
        count = session.query(Question).filter(Question.difficulty == difficulty).count()
        print(f"Total {difficulty} Questions: {count}")
    
    # Recent attempts
    print("\nRecent Attempts:")
    recent_attempts = session.query(Attempt).order_by(Attempt.attempted_at.desc()).limit(5).all()
    for attempt in recent_attempts:
        question = attempt.question
        print(f"- {question.title} ({attempt.difficulty_rating.name}) - Next review: {attempt.next_review_at}")
    
    # Due reviews
    due_reviews = session.query(Attempt).filter(Attempt.next_review_at <= datetime.utcnow()).count()
    print(f"\nQuestions Due for Review: {due_reviews}")

def show_question_solutions(session):
    """Display the number of solutions for each question"""
    questions = session.query(Question).all()
    print("\n=== Solutions per Question ===")
    for question in questions:
        solution_count = len(question.solutions)
        print(f"{question.title}: {solution_count} solutions")

def main():
    parser = argparse.ArgumentParser(description='LeetCode Manager')
    parser.add_argument('--init-db', action='store_true', help='Drop and initialize the database')
    parser.add_argument('--fetch', type=int, metavar='N', help='Fetch N number of questions')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--solutions', action='store_true', help='Show number of solutions per question')
    parser.add_argument('--record-attempt', type=int, metavar='QUESTION_ID', help='Record an attempt for a question')
    parser.add_argument('--difficulty', choices=['EASY', 'MEDIUM', 'HARD'], help='Difficulty rating for the attempt')
    
    args = parser.parse_args()
    
    client = LeetCodeClient()
    session = SessionLocal()

    if args.init_db:
        print("Dropping and reinitializing database...")
        drop_and_init_db()

    if args.fetch:
        asyncio.run(fetch_questions(client, session, args.fetch))

    if args.stats:
        show_statistics(session)

    if args.solutions:
        show_question_solutions(session)

    if args.record_attempt:
        if not args.difficulty:
            print("Error: --difficulty is required when recording an attempt")
            return
        
        difficulty = DifficultyRating[args.difficulty]
        client.record_attempt(args.record_attempt, difficulty, session)
        print(f"Recorded {args.difficulty} attempt for question {args.record_attempt}")

    session.close()

if __name__ == "__main__":
    main()