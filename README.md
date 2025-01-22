# LeetCode Data Collector

A tool to fetch LeetCode questions and solutions for training Large Language Models (LLMs) to better solve coding problems.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Arguments](#command-line-arguments)
  - [Examples](#examples)
- [Features](#features)
- [Contributing](#contributing)

## Overview

This project aims to:
1. Collect LeetCode questions and their community solutions systematically
2. Store the data in either a database or JSON files
3. Build a dataset that can be used to fine-tune LLMs for coding tasks
4. Track practice attempts and implement spaced repetition for learning

## Features

- Fetch LeetCode questions with metadata (difficulty, acceptance rate, etc.)
- Collect Python solutions with explanations from the LeetCode community
- Parallel processing for efficient data collection
- Flexible storage options:
  - SQLite database storage
  - JSON file storage
- Track personal practice attempts with spaced repetition:
  - ANKI-style spaced repetition algorithm
  - Customizable review intervals
  - Performance-based difficulty adjustment
  - Review reminders for optimal learning
- View statistics about questions and learning progress
- Smart question selection based on your learning curve

## Usage

### Command Line Arguments

| Argument | Description | Type | Options |
|----------|-------------|------|----------|
| `--init-db` | Drop and initialize the database | flag | - |
| `--fetch N` | Fetch N number of questions | integer | - |
| `--storage-type` | Choose storage method | string | `db`, `file` |
| `--stats` | Show statistics about questions and attempts | flag | - |
| `--solutions` | Show number of solutions per question | flag | - |
| `--record-attempt` | Record an attempt for a question | integer (question_id) | - |
| `--difficulty` | Difficulty rating for the attempt | string | `EASY`, `MEDIUM`, `HARD` |
| `--review` | Start a review session | flag | - |
| `--review-due` | Show questions due for review | flag | - |
| `--set-interval` | Set custom review intervals | string | `1,3,7,14,30,90` |

### Examples

## Initialize the database
```bash
python app.py --init-db
```

## Fetch 100 questions and store in database
```bash
python app.py --fetch 100 --storage-type db
```

## Fetch 50 questions and store in JSON files
```bash
python app.py --fetch 50 --storage-type file
```

## View statistics
```bash
python app.py --stats
```

## Record an attempt for question ID 1 with medium difficulty
```bash
python app.py --record-attempt 1 --difficulty MEDIUM
```

## Show solution counts for all questions
```bash
python app.py --solutions
```

## Review due questions
```bash
python app.py --review-due
```

## Start a review session
```bash
python app.py --review
```

## Set custom review intervals (in days)
```bash
python app.py --set-interval "1,3,7,14,30,90"
```

## Spaced Repetition System

The tool implements an ANKI-style spaced repetition system to help you maintain and improve your problem-solving skills:

- **Review Schedule**: Questions are automatically scheduled for review based on:
  - Your performance on previous attempts
  - The difficulty of the question
  - Time since last review

- **Performance Levels**:
  - Again (1): Review tomorrow
  - Hard (2): Review in 3 days
  - Good (3): Double the previous interval
  - Easy (4): Triple the previous interval

- **Features**:
  - Automatic scheduling of reviews
  - Performance tracking over time
  - Difficulty adjustment based on success rate
  - Review reminders via optional notifications
  - Statistics on learning progress

## Contributing
1. Added a Table of Contents
2. Created a new "Usage" section with detailed command line arguments
3. Added an "Examples" subsection showing common use cases
4. Organized the document with proper markdown headings
5. Added a table for command line arguments with their descriptions
6. Added a Contributing section
7. Maintained all existing content while improving the structure