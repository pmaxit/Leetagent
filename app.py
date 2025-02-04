import argparse
from leetcode.client import LeetCodeClient
from database.db import drop_and_init_db, SessionLocal, init_db
from database.models import Question, Solution, Attempt, DifficultyRating
from datetime import datetime
from tqdm import tqdm
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from datasets import Dataset
from itertools import islice
import multiprocessing

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

def process_batch(batch_data, storage_type='db'):
    """Process a batch of questions in a worker process
    Args:
        batch_data (dict): Batch information containing start_idx and batch_size
        storage_type (str): Storage type - 'db' for database or 'file' for file storage
    """
    client = LeetCodeClient()  # New client per process
    session = None
    batch_results = []
    
    try:
        start_idx = batch_data['start_idx']
        batch_size = batch_data['batch_size']
        questions = client.get_questions(limit=batch_size, skip=start_idx)
        
        if storage_type == 'db':
            session = SessionLocal()
        
        for question_data in questions:
            question_obj = {
                'title': question_data['title'],
                'title_slug': question_data['titleSlug'],
                'difficulty': question_data['difficulty'],
                'frontend_id': question_data['frontendQuestionId'],
                'ac_rate': str(question_data['acRate'])
            }
            
            solutions = client.get_python_solutions(question_data['titleSlug'])
            solution_objects = []
            
            if storage_type == 'db':
                question = Question(**question_obj)
                session.add(question)
                session.flush()
                
                for sol in solutions:
                    solution = Solution(
                        question_id=question.id,
                        summary=sol['summary'],
                        content=sol['content'],
                        author_name=sol['author_name'],
                        created_at=sol['created_at'],
                        updated_at=sol['updated_at']
                    )
                    session.add(solution)
            else:
                solution_objects = [{
                    'summary': sol['summary'],
                    'content': sol['content'],
                    'author_name': sol['author_name'],
                    'created_at': sol['created_at'],
                    'updated_at': sol['updated_at']
                } for sol in solutions]
                
                batch_results.append({
                    'question': question_obj,
                    'solutions': solution_objects
                })
        
        if storage_type == 'db':
            session.commit()
        else:
            import json
            import os
            
            # Create a directory for batch files if it doesn't exist
            os.makedirs('batch_data', exist_ok=True)
            
            # Save batch results to a JSON file
            batch_file = f'batch_data/batch_{start_idx}_{start_idx + batch_size}.json'
            with open(batch_file, 'w') as f:
                json.dump(batch_results, f, indent=2)
            
        return None
    except Exception as e:
        print(f"Error processing batch at index {start_idx}: {str(e)}")
        if storage_type == 'db' and session:
            session.rollback()
        raise Exception(f"Error processing batch at index {start_idx}: {str(e)}")
    finally:
        if session:
            session.close()

def fetch_questions(client, session, total_questions, storage_type='db', batch_size=10):
    """Fetch and store questions from LeetCode using HF datasets for parallel processing"""
    print(f"Total available questions: {total_questions}")
    print(f"Storage type: {storage_type}")
    
    # Configure batching
    num_batches = (total_questions + batch_size - 1) // batch_size
    
    # Create batch data
    batch_data = [
        {
            'start_idx': i * batch_size,
            'batch_size': min(batch_size, total_questions - i * batch_size)
        }
        for i in range(num_batches)
    ]
    
    # Create dataset and enable multiprocessing
    dataset = Dataset.from_list(batch_data)
    
    # Process batches in parallel with progress bar
    num_proc = multiprocessing.cpu_count()
    print(f"Using {num_proc} workers")
    
    results = dataset.map(
        lambda x: process_batch(x, storage_type),
        num_proc=num_proc,
        with_indices=False,
        desc="Fetching questions",    
    )
    
    # Calculate total fetched
    total_fetched = sum(results)
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

def load_json_to_db(session, json_dir):
    """Load data from JSON files into database tables"""
    import json
    import os
    
    try:
        # Get all JSON files in the directory
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        
        if not json_files:
            print(f"No JSON files found in {json_dir}")
            return
        
        total_questions = 0
        total_solutions = 0
        
        for file_name in tqdm(json_files, desc="Processing JSON files"):
            file_path = os.path.join(json_dir, file_name)
            
            with open(file_path, 'r') as f:
                batch_data = json.load(f)
                
                for item in batch_data:
                    # Create Question
                    question = Question(**item['question'])
                    session.add(question)
                    session.flush()  # Get the question ID
                    
                    # Create Solutions
                    for sol_data in item['solutions']:
                        solution = Solution(
                            question_id=question.id,
                            **sol_data
                        )
                        session.add(solution)
                    
                    total_questions += 1
                    total_solutions += len(item['solutions'])
            
            session.commit()
        
        print(f"\nSuccessfully imported {total_questions} questions and {total_solutions} solutions")
        
    except Exception as e:
        print(f"Error loading JSON data: {str(e)}")
        session.rollback()
        raise

def main():
    parser = argparse.ArgumentParser(description='LeetCode Manager')
    parser.add_argument('--init-db', action='store_true', help='Drop and initialize the database')
    parser.add_argument('--fetch', type=int, metavar='N', help='Fetch N number of questions')
    parser.add_argument('--storage-type', choices=['db', 'file'], default='db', help='Storage type (db or file)')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--solutions', action='store_true', help='Show number of solutions per question')
    parser.add_argument('--record-attempt', type=int, metavar='QUESTION_ID', help='Record an attempt for a question')
    parser.add_argument('--difficulty', choices=['EASY', 'MEDIUM', 'HARD'], help='Difficulty rating for the attempt')
    # batch size
    parser.add_argument('--batch-size', type=int, default=1, help='Batch size for fetching questions')
    parser.add_argument('--load-json', type=str, metavar='DIR',
                       help='Load data from JSON files in the specified directory into database')
    
    args = parser.parse_args()
    
    client = LeetCodeClient()
    session = SessionLocal()

    if args.init_db:
        print("Dropping and reinitializing database...")
        drop_and_init_db()

    if args.fetch:
        fetch_questions(client, session, args.fetch, args.storage_type, args.batch_size)

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

    if args.load_json:
        load_json_to_db(session, args.load_json)

    session.close()

if __name__ == "__main__":
    main()