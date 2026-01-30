#!/usr/bin/env python3
"""
Generate random concepts by sampling semantic embedding space.

Uses Word2Vec trained on Google News (3M words, 300 dimensions).
First run downloads ~1.6GB model, cached after that.

Methods:
- walk: Random walk from a seed word (recommended)
- interpolate: Blend two random common words  
- pure_random: Random point in embedding space (weird results)
"""
import numpy as np
import sys

_model = None

def get_model():
    """Load Word2Vec model (cached after first load)."""
    global _model
    if _model is None:
        import gensim.downloader as api
        _model = api.load("word2vec-google-news-300")
    return _model

def is_good_word(word):
    """Filter out proper nouns, multi-word phrases, etc."""
    if '_' in word:  # Skip multi-word phrases like "New_York"
        return False
    if word[0].isupper():  # Skip proper nouns
        return False
    if len(word) < 3:  # Skip very short words
        return False
    if not word.isalpha():  # Skip words with numbers/symbols
        return False
    return True

def random_concept(model, method='walk', seed_word='science', noise_scale=0.5):
    """
    Generate a random concept using specified method.
    
    Args:
        model: Loaded Word2Vec model
        method: 'walk', 'interpolate', or 'pure_random'
        seed_word: Starting point for walk method
        noise_scale: How far to drift in walk method (0.1=close, 1.0=far)
    
    Returns:
        A single word (string)
    """
    
    if method == 'pure_random':
        # Pure random vector - tends to give weird/proper noun results
        random_vec = np.random.randn(300)
        random_vec = random_vec / np.linalg.norm(random_vec)
        candidates = model.similar_by_vector(random_vec, topn=50)
        
    elif method == 'walk':
        # Random walk from a seed - more controlled exploration
        if seed_word not in model:
            seed_word = 'science'
        base_vec = model[seed_word]
        noise = np.random.randn(300) * noise_scale
        random_vec = base_vec + noise
        random_vec = random_vec / np.linalg.norm(random_vec)
        candidates = model.similar_by_vector(random_vec, topn=50)
        
    elif method == 'interpolate':
        # Interpolate between two random common words
        common_words = [w for w in list(model.key_to_index.keys())[:5000] if is_good_word(w)]
        w1, w2 = np.random.choice(common_words, 2, replace=False)
        alpha = np.random.uniform(0.3, 0.7)
        random_vec = model[w1] * alpha + model[w2] * (1 - alpha)
        candidates = model.similar_by_vector(random_vec, topn=50)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Filter for good words (no proper nouns, phrases, etc.)
    good_candidates = [(w, s) for w, s in candidates if is_good_word(w)]
    
    if good_candidates:
        # Return a random one from top filtered results (adds variety)
        idx = np.random.randint(0, min(5, len(good_candidates)))
        return good_candidates[idx][0]
    else:
        return candidates[0][0]  # fallback to unfiltered

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate random concept from embedding space',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --method walk --seed science -n 5
  %(prog)s --method interpolate -n 10
  %(prog)s --method pure_random
        """
    )
    parser.add_argument('--method', choices=['pure_random', 'walk', 'interpolate'], 
                        default='walk', help='Generation method (default: walk)')
    parser.add_argument('--seed', default='science', 
                        help='Seed word for walk method (default: science)')
    parser.add_argument('--noise', type=float, default=0.5,
                        help='Noise scale for walk method (default: 0.5)')
    parser.add_argument('-n', type=int, default=1, 
                        help='Number of concepts to generate (default: 1)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress loading messages')
    args = parser.parse_args()
    
    if not args.quiet:
        print("Loading model...", file=sys.stderr)
    model = get_model()
    
    if not args.quiet:
        print("Generating...", file=sys.stderr)
    
    for _ in range(args.n):
        concept = random_concept(
            model, 
            method=args.method, 
            seed_word=args.seed,
            noise_scale=args.noise
        )
        print(concept)

if __name__ == "__main__":
    main()
