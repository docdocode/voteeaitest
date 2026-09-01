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

    def is_valid_word(self, word: str) -> bool:
        pass


    # then to take the possible words and filter them based on the feedback
    def get_possible_words(self, guess: str, feedback: List[str]) -> List[str]:
        pass


    #then to solve

    def solve(self) -> str:
        pass

