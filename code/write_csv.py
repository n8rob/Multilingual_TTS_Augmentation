import argparse
import os
import pickle as pkl

def pkl2csv(no2voice, no2prompt, out_csv):
    with open(out_csv, 'w') as f:
        for no in no2voice:
            f.write(f"{no}, {no2voice[no]}, {no2prompt[no]}\n")
    return

def main(args):

    with open(args.in_pkl, 'rb') as f:
        no2voice, no2prompt = pkl.load(f)

    csv_dir = os.path.split(args.out_csv)[0]
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    pkl2csv(no2voice, no2prompt, args.out_csv)
    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--in-pkl", type=str, required=True,\
            help="Path to mappings pickle")
    parser.add_argument("--out-csv", type=str, required=True,\
            help="Path to output csv")

    args = parser.parse_args()

    main(args)
