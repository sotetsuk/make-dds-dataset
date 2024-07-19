from tqdm import tqdm
from typing import Tuple
import numpy as np


def to_value(sample: list) -> np.ndarray:
    """Convert sample to value
    >>> sample = ['0', '1', '0', '4', '0', '13', '12', '13', '9', '13', '0', '1', '0', '4', '0', '13', '12', '13', '9', '13']
    >>> to_value(sample)
    Array([  4160, 904605,   4160, 904605], dtype=int32)
    """
    np_sample = np.array([int(s) for s in sample], dtype=np.int8).reshape(
        4, 5
    )
    return to_binary(np_sample)


def to_binary(x) -> np.ndarray:
    """Convert dds information to value
    >>> np.array([16**i for i in range(5)], dtype=np.int32)[::-1]
    Array([65536,  4096,   256,    16,     1], dtype=int32)
    >>> x = np.arange(20, dtype=np.int32).reshape(4, 5) % 14
    >>> to_binary(x)
    Array([  4660, 354185, 703696,  74565], dtype=int32)
    """
    bases = np.array([16**i for i in range(5)], dtype=np.int32)[::-1]
    return (x * bases).sum(axis=1)  # shape = (4, )


def make_hash_table(
    tsv_path: str,
) -> Tuple[np.ndarray, np.ndarray]:
    """make key and value of hash from samples
    [start, end)
    """
    keys = []
    values = []
    with open(tsv_path, "r") as f:
        for line in tqdm(f):
            pbn, dds = line.split("\t")
            dds = dds.split(',')
            keys.append(_pbn_to_key(pbn))
            values.append(to_value(dds))
    return np.array(keys, dtype=np.int32), np.array(values, dtype=np.int32)


def _pbn_to_key(pbn: str) -> np.ndarray:
    """Convert pbn to key of dds table"""
    key = np.zeros(52, dtype=np.int8)
    hands = pbn[2:]
    for player, hand in enumerate(list(hands.split())):  # for each player
        for suit, cards in enumerate(list(hand.split("."))):  # for each suit
            for card in cards:  # for each card
                card_num = _card_str_to_int(card) + suit * 13
                # key = key.at[card_num].set(player)
                key[card_num] = (player)
    key = key.reshape(4, 13)
    return _to_binary(key)


def _to_binary(x: np.ndarray) -> np.ndarray:
    bases = np.array([4**i for i in range(13)], dtype=np.int32)[::-1]
    return (x * bases).sum(axis=1)  # shape = (4, )


def _card_str_to_int(card: str) -> int:
    if card == "K":
        return 12
    elif card == "Q":
        return 11
    elif card == "J":
        return 10
    elif card == "T":
        return 9
    elif card == "A":
        return 0
    else:
        return int(card) - 1


def main(fname):
    keys, values = make_hash_table(fname)

    fname = f"{fname.split(".")[0]}.npy"
    np.save(fname, arr=(keys, values))

    keys, values = np.load(fname)
    for i in range(5):
        print(keys[i], values[i])


def test():
    fname = "test.tsv"
    main(fname)
    
    expected_keys = np.int32([[24494087, 53250751, 4828063 , 22552142],
                              [49254891, 38345158, 3793117 , 54415393],
                              [38001191, 61321396, 37835372, 28705279], 
                              [31565552, 43246604, 52788853, 55340170], 
                              [18868003, 33931363, 55738086, 37984138]])
    expected_vals = np.int32([[213810, 694955, 148274, 629419],
                              [554870, 353639, 489318, 353639],
                              [288101, 620407, 222565, 616295],
                              [674181, 234584, 674181, 234584],
                              [616808, 291956, 616808, 291956]])

    # first 5 itesm
    keys, values = np.load("test.npy")
    assert np.allclose(keys[:5], expected_keys)
    assert np.allclose(values[:5], expected_vals)
 

if __name__ == '__main__':
    test()
    # import sys
    # fname = sys.argv[1]
    # main(fname)
    


