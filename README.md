# Votee Wordle Solver

A Python-based solver for the Votee Wordle API challenge. The solver uses optimal starting words and feedback-based filtering to solve Wordle puzzles in minimal attempts.

## Objective

Connect to the Votee Wordle API and solve daily, random, and specific-word puzzles using an algorithmic approach with optimal word selection strategies.

## Tools & Libraries

- **Python 3.x** - Core programming language
- **requests** - HTTP client for API interaction
- **json** - Word list data handling
- **typing** - Type hints for better code clarity

## Approach

### 1. Word Selection Strategy
- Uses pre-computed optimal starting words (e.g., "lares", "tares", "arise")
- Scores candidate words based on English letter frequency
- Prioritizes words with common letters (E, A, R, S, T)

### 2. Feedback Processing
- Converts API responses to internal feedback format:
  - `1` = correct position (green)
  - `2` = present but wrong position (yellow)
  - `3` = absent (grey)

### 3. Word Filtering
- Eliminates impossible words based on feedback
- Validates candidates against all previous guesses
- Falls back to unguessed words when list is exhausted

## Challenges

1. **API Rate Limits** - Needed to handle timeouts and errors gracefully
2. **Word List Size** - Solution space depends on comprehensive word list
3. **Optimal First Guess** - Finding the best starting word to maximize information gain
4. **Edge Cases** - Handling repeated letters, invalid words, and no-solution scenarios

## Solution

The solver implements:
- Pre-computed optimal starters from information theory analysis
- Letter frequency scoring for intelligent word selection
- Iterative filtering to narrow down possibilities
- Fallback strategies when candidate list is empty
- Error handling with timeout and retry logic

## Limitations

- **Word List Dependency**: Success rate depends on having the target word in the local dictionary
- **Daily Puzzle**: May fail if the word is uncommon or not in word list
- **Simple Scoring**: Letter frequency heuristic isn't as optimal as full entropy calculation
- **Fixed Attempts**: Limited to 6 attempts like traditional Wordle

## Usage

```bash
# Run the solver
python main.py

# Or use specific modes
python -c "from main import quick_solve; quick_solve('daily')"
python -c "from main import quick_solve; quick_solve('random', seed=42)"
python -c "from main import quick_solve; quick_solve('word', target_word='apple')"