import sys
import numpy as np
from tqdm import tqdm
import argparse

from ddstable import get_ddstable  # https://gitlab.com/xrgopher/ddstable


# カードと数字の対応
# 0~12 spade, 13~25 heart, 26~38 diamond, 39~51 club
# それぞれのsuitにおいて以下の順で数字が並ぶ
TO_CARD = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]


def random_to_pbn() -> str:
    """Convert state to pbn format"""
    statehand = np.arange(0, 52)
    np.random.shuffle(statehand)
    pbn = "N:"
    for i in range(4):  # player
        hand = np.sort(statehand[i * 13 : (i + 1) * 13])
        for j in range(4):  # suit
            card = [
                TO_CARD[i % 13] for i in hand if j * 13 <= i < (j + 1) * 13
            ][::-1]
            if card != [] and card[-1] == "A":
                card = card[-1:] + card[:-1]
            pbn += "".join(card)
            if j == 3:
                if i != 3:
                    pbn += " "
            else:
                pbn += "."
    return pbn


def main(num):
    players = ["N", "E", "S", "W"]
    denominations = ["C", "D", "H", "S", "NT"]
    for i in tqdm(range(num)):
        pbn = random_to_pbn()
        dds_results = get_ddstable(pbn.encode('utf-8'))
        dds = []
        for player in players:
            for denomination in denominations:
                trick = dds_results[player][denomination]
                dds.append(trick)

        print(pbn + "\t" + ",".join([str(x) for x in dds]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--num", type=int, default=10_000_000)
    args = parser.parse_args()

    if args.seed is None:
        seed = np.random.randint(0, 2**32 - 1)
        print(f"Randomly generated seed: {seed}", file=sys.stderr)

    np.random.seed(seed=args.seed)
    main(args.num)
