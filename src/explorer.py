#!/usr/bin/env python3
"""
Balanced exploration: alternate between pure randomness and interest-based walks.

Maintains a list of "interests" that grows as you explore.
Each exploration either:
- Dives deeper into an existing interest (walk)
- Discovers something completely new (pure random)
"""
import numpy as np
import json
import os
from pathlib import Path
from datetime import datetime

from .random_concept import get_model, random_concept, is_good_word

DEFAULT_INTERESTS = [
    'consciousness', 'emergence', 'fractals', 'bioluminescence',
    'philosophy', 'networks', 'evolution', 'linguistics'
]

class Explorer:
    def __init__(self, interests_file=None):
        self.model = None
        self.interests_file = interests_file or Path.home() / '.creativity-engine' / 'interests.json'
        self.interests = self._load_interests()
        
    def _load_interests(self):
        """Load interests from file or use defaults."""
        if os.path.exists(self.interests_file):
            with open(self.interests_file) as f:
                data = json.load(f)
                return data.get('interests', DEFAULT_INTERESTS.copy())
        return DEFAULT_INTERESTS.copy()
    
    def _save_interests(self):
        """Save interests to file."""
        os.makedirs(os.path.dirname(self.interests_file), exist_ok=True)
        with open(self.interests_file, 'w') as f:
            json.dump({
                'interests': self.interests,
                'updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def add_interest(self, word):
        """Add a new interest discovered during exploration."""
        if word not in self.interests and is_good_word(word):
            self.interests.append(word)
            self._save_interests()
            return True
        return False
    
    def get_model(self):
        """Lazy load the model."""
        if self.model is None:
            self.model = get_model()
        return self.model
    
    def explore(self, random_chance=0.3):
        """
        Generate next exploration seed.
        
        Args:
            random_chance: Probability of pure random vs interest walk (default 30%)
        
        Returns:
            tuple: (concept, method, seed_word_if_walk)
        """
        model = self.get_model()
        
        if np.random.random() < random_chance:
            # Pure random - discover something completely new
            concept = random_concept(model, method='pure_random')
            return concept, 'random', None
        else:
            # Walk from an interest - go deeper
            seed = np.random.choice(self.interests)
            concept = random_concept(model, method='walk', seed_word=seed, noise_scale=0.6)
            return concept, 'walk', seed


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Balanced exploration')
    parser.add_argument('--random-chance', type=float, default=0.3,
                        help='Chance of pure random vs interest walk (default: 0.3)')
    parser.add_argument('--add-interest', type=str, help='Add a new interest')
    parser.add_argument('--list-interests', action='store_true', help='List current interests')
    parser.add_argument('-n', type=int, default=1, help='Number of concepts')
    args = parser.parse_args()
    
    explorer = Explorer()
    
    if args.list_interests:
        print("Current interests:")
        for i in explorer.interests:
            print(f"  - {i}")
        return
    
    if args.add_interest:
        if explorer.add_interest(args.add_interest):
            print(f"Added interest: {args.add_interest}")
        else:
            print(f"Already exists or invalid: {args.add_interest}")
        return
    
    print("Loading model...", file=__import__('sys').stderr)
    
    for _ in range(args.n):
        concept, method, seed = explorer.explore(random_chance=args.random_chance)
        if method == 'random':
            print(f"{concept} (pure random)")
        else:
            print(f"{concept} (walked from: {seed})")


if __name__ == "__main__":
    main()
