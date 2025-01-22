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
- Track personal practice attempts with spaced repetition
- View statistics about questions and learning progress

## Installation

// ... existing code ...

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

## Contributing
1. Added a Table of Contents
2. Created a new "Usage" section with detailed command line arguments
3. Added an "Examples" subsection showing common use cases
4. Organized the document with proper markdown headings
5. Added a table for command line arguments with their descriptions
6. Added a Contributing section
7. Maintained all existing content while improving the structure