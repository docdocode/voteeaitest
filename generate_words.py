# generate_words.py
import json

# Expanded list of common 5-letter words (add as many as you can)
words = [
    # A words
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
    "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
    "alike", "alive", "allow", "alone", "along", "alter", "among", "anger",
    "angle", "angry", "apart", "apple", "apply", "arena", "argue", "arise",
    "array", "aside", "asset", "audio", "audit", "avoid", "award", "aware",
    
    # B words
    "badly", "baker", "bases", "basic", "basis", "beach", "began", "begin",
    "begun", "being", "below", "bench", "birth", "black", "blame", "blind",
    "block", "blood", "board", "boost", "booth", "bound", "brain", "brand",
    "bread", "break", "breed", "brief", "bring", "broad", "broke", "brook",
    "brown", "build", "built", "buyer",
    
    # C words
    "cable", "carry", "catch", "cause", "chain", "chair", "cheap", "check",
    "chest", "chief", "child", "china", "claim", "class", "clean", "clear",
    "click", "climb", "clock", "close", "coach", "coast", "could", "count",
    "court", "cover", "craft", "crash", "crazy", "cream", "crime", "cross",
    "crowd", "crown", "curve", "cycle",
    
    # D words
    "daily", "dance", "dated", "dealt", "death", "debut", "delay", "depth",
    "doing", "doubt", "dozen", "draft", "drama", "drank", "drawn", "dream",
    "dress", "drill", "drink", "drive", "drove", "dying",
    
    # E words
    "eager", "early", "earth", "eight", "elite", "empty", "enemy", "enjoy",
    "enter", "entry", "equal", "error", "event", "every", "exact", "exist",
    "extra",
    
    # F words
    "faith", "false", "fault", "fiber", "field", "fifth", "fifty", "fight",
    "final", "first", "fixed", "flash", "fleet", "floor", "fluid", "focus",
    "force", "forth", "forty", "forum", "found", "frame", "frank", "fraud",
    "fresh", "front", "fruit", "fully", "funny",
    
    # G words
    "giant", "given", "glass", "globe", "going", "grace", "grade", "grand",
    "grant", "grass", "great", "green", "gross", "group", "grown", "guard",
    "guess", "guest", "guide",
    
    # H words
    "happy", "harry", "heart", "heavy", "hence", "horse", "hotel", "house",
    "human",
    
    # I words
    "ideal", "image", "index", "inner", "input", "issue",
    
    # J-K words
    "joint", "jones", "judge", "known",
    
    # L words
    "label", "large", "laser", "later", "laugh", "layer", "learn", "lease",
    "least", "leave", "legal", "level", "light", "limit", "links", "lives",
    "local", "logic", "loose", "lower", "lucky", "lunch", "lying",
    
    # M words
    "magic", "major", "maker", "march", "match", "maybe", "mayor", "meant",
    "media", "metal", "might", "minor", "model", "money", "month", "moral",
    "motor", "mount", "mouse", "mouth", "movie", "music",
    
    # N words
    "needs", "never", "newly", "night", "noise", "north", "noted", "novel",
    "nurse",
    
    # O words
    "occur", "ocean", "offer", "often", "order", "other", "ought",
    
    # P words
    "paint", "panel", "paper", "party", "peace", "peter", "phase", "phone",
    "photo", "piano", "piece", "pilot", "pitch", "place", "plain", "plane",
    "plant", "plate", "point", "pound", "power", "press", "price", "pride",
    "prime", "print", "prior", "prize", "proof", "proud", "prove",
    
    # Q-R words
    "queen", "quick", "quiet", "quite", "radio", "raise", "range", "rapid",
    "ratio", "reach", "ready", "refer", "right", "rival", "river", "robin",
    "rough", "round", "route", "royal", "rural",
    
    # S words
    "scale", "scene", "scope", "score", "sense", "serve", "seven", "shall",
    "shape", "share", "sharp", "sheet", "shelf", "shell", "shift", "shine",
    "shirt", "shock", "shoot", "shore", "short", "shown", "sight", "since",
    "sixth", "sixty", "sized", "skill", "sleep", "slide", "small", "smart",
    "smile", "smith", "smoke", "solid", "solve", "sorry", "sound", "south",
    "space", "spare", "speak", "speed", "spend", "spent", "split", "spoke",
    "sport", "staff", "stage", "stake", "stand", "start", "state", "steam",
    "steel", "stick", "still", "stock", "stone", "stood", "store", "storm",
    "story", "strip", "stuck", "study", "stuff", "style", "sugar", "suite",
    "super", "sweet",
    
    # T words
    "table", "taken", "taste", "taxes", "teach", "teeth", "thank", "theft",
    "their", "theme", "there", "these", "thick", "thing", "think", "third",
    "those", "three", "threw", "throw", "tight", "times", "tired", "title",
    "today", "topic", "total", "touch", "tough", "tower", "track", "trade",
    "train", "treat", "trend", "trial", "tried", "tries", "truck", "truly",
    "trust", "truth", "twice",
    
    # U-V words
    "under", "undue", "union", "unity", "until", "upper", "upset", "urban",
    "usage", "usual", "valid", "value", "video", "virus", "visit", "vital",
    "voice",
    
    # W-Y-Z words
    "waste", "watch", "water", "wheel", "where", "which", "while", "white",
    "whole", "whose", "woman", "women", "world", "worry", "worse", "worst",
    "worth", "would", "wound", "write", "wrong", "wrote", "young", "youth",
    "zebra", "zones"
]

# Remove duplicates and save
words = list(set(words))
words.sort()

with open('solution_words.json', 'w') as f:
    json.dump(words, f)

print(f"Saved {len(words)} words to solution_words.json")