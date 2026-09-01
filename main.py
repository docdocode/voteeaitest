import requests
import json
from typing import List, Dict, Optional


class VoteeWordleSolver:
    def __init__(self, base_url: str = "https://wordle.votee.dev:8000/redoc"):
        self.base_url = base_url
        self.session = requests.Session()

        #these are the optimal starting words pre-comupted
        self.optimal_guesses = ["lares", "rales", "tares", "soare", "reais", 
                                "stoae", "toeas", "aloes", "aeons", "arise",
                                "raise", "irate", "arose", "alter", "alone"]

        #then we load the word list

        try: 
            with open("wordle_words.json", "r") as f:
                self.word_list = json.load(f)

        #this except catch will be to fallback to the common words
        except: 
            self.word_list = ["crane", "slate", "audio", "stone", "train", "raise", 
                         "cloud", "price", "round", "tales", "apple", "beach"]


    # next should be about making a guess

    def make_guess(self, guess: str, mode: str = "daily", size: int = 5
                   ,seed: Optional[int] = None
                   ,target_word: Optional[str] = None) -> Dict:

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
        
        response = self.session.get(url, params=params)
        return response.json()



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
                    guess = possible[0]  # take the first possible word
                else:
                    break  # no possible words left


            print(f"Attempt {attempt + 1}: Guessing '{guess}'")

            #then doing the api call

            results = self.make_guess(guess, mode=mode, size=size, seed=seed, target_word=target_word)

            feedback_str = self.feedback_to_string(results, guess)

            guesses.append(guess)
            feedback.append(feedback_str)

            print(f"Feedback: {feedback_str}")

            if feedback_str == '1' * size:
                print(f"Solved! The word is '{guess}'")
                return guess  # solved


            possible = self.get_possible_words(guesses, feedback)
            if len(possible) <= 5:
                print(f"Possible words left: {possible}")

        print("Failed to solve the Wordle.")
        return None  # failed to solve

    

