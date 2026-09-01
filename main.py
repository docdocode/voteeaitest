import requests
import json
from typing import List, Dict, Optional


class VoteeWordleSolver:
    def __init__(self, base_url: str = "https://wordle.votee.dev:8000"):
        self.base_url = base_url
        self.session = requests.Session()

        #these are the optimal starting words pre-comupted
        self.optimal_guesses = ["lares", "rales", "tares", "soare", "reais", 
                                "stoae", "toeas", "aloes", "aeons", "arise",
                                "raise", "irate", "arose", "alter", "alone"]

        #then we load the word list

        try: 
            with open("solution_words.json", "r") as f:
                self.word_list = json.load(f)
            print(f"Loaded {len(self.word_list)} words from solution_words.json")

        #this except catch will be to fallback to the common words
        except: 
            self.word_list = ["crane", "slate", "audio", "stone", "train", "raise", 
                         "cloud", "price", "round", "tales", "apple", "beach",
                         "brain", "chair", "dance", "dream", "earth", "flame",
                         "grace", "heart", "light", "music", "ocean", "peace"]
            print(f"Using fallback word list with {len(self.word_list)} words")


    # next should be about making a guess

    def make_guess(self, guess: str, mode: str = "daily", size: int = 5
                   ,seed: Optional[int] = None
                   ,target_word: Optional[str] = None) -> List[Dict]:

        #have to make an api call to guess the word

        params = {
            "guess": guess
        }

        if mode == "daily":
            params['size'] = size
            url = f"{self.base_url}/daily"
        elif mode == "random":
            params['size'] = size
            if seed:
                params['seed'] = seed
            url = f"{self.base_url}/random"
        elif mode == "word" and target_word:
            url = f"{self.base_url}/word/{target_word}"

        else:
            raise ValueError(f"Invalid mode {mode}. Choose from 'daily', 'random', or 'word'.")
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise



    # next should be the feedback part

    def feedback_to_string(self, results: List[Dict], guess:str) -> str:

        #here basically I take the api response to feedback string based on 1 = green, 2 = yellow, 3 =grey
        feedback = ['3'] * len(guess) #this is the default, all absent

        for result in results:
            slot = result['slot']
            status = result['result']

            if status == "correct":
                feedback[slot] = '1'  # green
            if status == "present":
                feedback[slot] = '2'  # yellow

        return ''.join(feedback)




    # next should be to check if the word is valid

    def is_valid_word(self, word: str, guesses: List[str],feedback: List[str]) -> bool:

        # have to check if wrd matches all the prev feedbacks"

        if word in guesses:
            return False  # already guessed

        #loop
        for i in range(len(guesses)):
            for j in range(len(guesses[i])):
                if feedback[i][j] == '1' and guesses[i][j] != word[j]:
                    return False  # green mismatch
                if feedback[i][j] == '2' and (guesses[i][j] == word[j] or guesses[i][j] not in word):
                    return False  # yellow mismatch
                if feedback[i][j] == '3' and guesses[i][j] in word:
                    return False  # grey mismatch
        return True
    

        


        #pass


    # then to take the possible words and filter them based on the feedback
    def get_possible_words(self, guesses: List[str], feedback: List[str]) -> List[str]:
        return [wo for wo in self.word_list if self.is_valid_word(wo, guesses, feedback)]
    

    # then to choose the best guess from possible words
    def choose_best_guess(self, possible_words: List[str]) -> Optional[str]:
        #here we score words based on letter frequency to pick the best guess
        
        if not possible_words:
            return None
        
        # letter frequency in English (percentage)
        letter_frequency = {
            'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0,
            'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3,
            'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4, 'w': 2.4,
            'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5,
            'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15, 'q': 0.1, 'z': 0.07
        }
        
        best_word = None
        best_score = -1
        
        for word in possible_words:
            # score based on unique letters (avoid repeated letters)
            unique_letters = set(word)
            score = sum(letter_frequency.get(letter, 0) for letter in unique_letters)
            
            if score > best_score:
                best_score = score
                best_word = word
        
        return best_word


    #then to solve

    def solve(self, mode: str = "daily", size: int = 5, seed: Optional[int] = None
              ,target_word: Optional[str] = None) -> Optional[str]:

        #here we solve using optimal guesses and feedback

        guesses = []
        feedback = []

        for attempt in range(6):
            if attempt == 0:
                guess = self.optimal_guesses[0]  # first optimal guess
            elif len(feedback) == 1 and feedback[0] == '33333':
                guess = self.optimal_guesses[attempt] if attempt < len(self.optimal_guesses) else "crane"

            else:
                possible = self.get_possible_words(guesses, feedback)
                if not possible:
                    possible = [wo for wo in self.word_list if wo not in guesses]  # fallback to any word
                if possible:
                    guess = self.choose_best_guess(possible)  # pick the best word
                else:
                    break  # no possible words left


            print(f"Attempt {attempt + 1}: Guessing '{guess}'")

            #then doing the api call

            try:
                results = self.make_guess(guess, mode=mode, size=size, seed=seed, target_word=target_word)

                feedback_str = self.feedback_to_string(results, guess)

                guesses.append(guess)
                feedback.append(feedback_str)

                print(f"Feedback: {feedback_str}")

                if feedback_str == '1' * size:
                    print(f"Solved! The word is '{guess}'")
                    return guess  # solved


                possible = self.get_possible_words(guesses, feedback)
                print(f"Remaining candidates: {len(possible)}")
                if len(possible) <= 5:
                    print(f"Possible words left: {possible}")

            except Exception as e:
                print(f"Error during attempt: {e}")
                break

        print("Failed to solve the Wordle.")
        return None  # failed to solve

    
    def close(self):
        #close the session
        self.session.close()


# Simplified version for quick testing
def quick_solve(mode="daily", seed=None, target_word=None):
    """Minimal solver function"""
    base_url = "https://wordle.votee.dev:8000"
    session = requests.Session()
    
    # Load words
    try:
        with open('solution_words.json') as f:
            words = json.load(f)
        print(f"Loaded {len(words)} words from solution_words.json")
    except:
        words = ["crane", "slate", "audio", "stone", "train", "raise", 
                 "cloud", "price", "round", "tales", "apple", "beach",
                 "brain", "chair", "dance", "dream", "earth", "flame",
                 "grace", "heart", "light", "music", "ocean", "peace"]
        print(f"Using fallback word list with {len(words)} words")
    
    guesses = []
    feedbacks = []
    
    # Optimal starters
    starters = ["lares", "rales", "tares", "soare", "reais", "arise", "raise"]
    
    # letter frequency for scoring
    letter_freq = {'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0,
                  'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3,
                  'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4, 'w': 2.4,
                  'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5,
                  'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15, 
                  'q': 0.1, 'z': 0.07}
    
    for attempt in range(6):
        if attempt == 0:
            guess = starters[0]
        else:
            # Filter possible words
            possible = []
            for word in words:
                if word in guesses:
                    continue
                
                valid = True
                for i in range(len(guesses)):
                    for j in range(len(guesses[i])):
                        if feedbacks[i][j] == '1' and guesses[i][j] != word[j]:
                            valid = False
                            break
                        if feedbacks[i][j] == '2' and (guesses[i][j] == word[j] or 
                                                       guesses[i][j] not in word):
                            valid = False
                            break
                        if feedbacks[i][j] == '3' and guesses[i][j] in word:
                            valid = False
                            break
                    if not valid:
                        break
                
                if valid:
                    possible.append(word)
            
            if not possible:
                possible = [w for w in words if w not in guesses]
            
            # Choose best word based on letter frequency
            if possible:
                guess = max(possible, key=lambda w: sum(letter_freq.get(c, 0) 
                                                        for c in set(w)))
            else:
                guess = "crane"
        
        # Make API call
        params = {"guess": guess}
        if mode == "daily":
            params["size"] = 5
            url = f"{base_url}/daily"
        elif mode == "random":
            params["size"] = 5
            if seed:
                params["seed"] = seed
            url = f"{base_url}/random"
        elif mode == "word" and target_word:
            url = f"{base_url}/word/{target_word}"
        
        try:
            response = session.get(url, params=params, timeout=10)
            results = response.json()
        except Exception as e:
            print(f"API error: {e}")
            break
        
        # Convert to feedback string
        feedback = ['3'] * len(guess)
        for result in results:
            if result["result"] == "correct":
                feedback[result["slot"]] = '1'
            elif result["result"] == "present":
                feedback[result["slot"]] = '2'
        feedback_str = ''.join(feedback)
        
        guesses.append(guess)
        feedbacks.append(feedback_str)
        
        print(f"Attempt {attempt + 1}: {guess} -> {feedback_str}")
        
        if feedback_str == '1' * len(guess):
            print(f"Solved: {guess}")
            return guess
    
    print("Failed")
    return None


if __name__ == "__main__":
    # Test all three modes
    print("For the Daily")
    quick_solve("daily")
    
    print("\n For Random (seed=42)")
    quick_solve("random", seed=42)
    
    print("\n For Specific Word (apple)")
    quick_solve("word", target_word="apple")