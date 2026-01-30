#!/usr/bin/env python3
"""
Example: Full exploration workflow

1. Generate a random concept
2. Print it for the agent to explore
3. (Agent does its thing - research, connect, discover)
4. Log results to a file
"""
import sys
import os
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.random_concept import get_model, random_concept

# Seed words to rotate through (vary the exploration space)
SEED_WORDS = [
    'science', 'consciousness', 'mythology', 'technology', 
    'biology', 'philosophy', 'art', 'mathematics', 'ecology',
    'language', 'music', 'evolution', 'quantum', 'emergence'
]

def main():
    import random
    
    print("Loading model...")
    model = get_model()
    
    # Pick a random seed word
    seed = random.choice(SEED_WORDS)
    
    # Generate concept
    concept = random_concept(model, method='walk', seed_word=seed, noise_scale=0.6)
    
    print(f"\n{'='*50}")
    print(f"EXPLORATION SEED: {concept}")
    print(f"(walked from: {seed})")
    print(f"{'='*50}")
    print()
    print("Instructions for the agent:")
    print(f"1. Research '{concept}' - what is it? why is it interesting?")
    print("2. Follow tangents that catch your attention")
    print("3. Connect it to things you already know")
    print("4. Note what surprises you")
    print("5. Log your findings")
    print()
    
    # Log the seed for later reference
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'exploration_seeds.txt')
    with open(log_file, 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}\t{seed}\t{concept}\n")
    
    print(f"Seed logged to: {log_file}")

if __name__ == "__main__":
    main()
