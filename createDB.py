import argparse
import os
from glob import glob
from tqdm import tqdm
from time import time
from scipy.io import savemat
from utils.extractandenconding import extractFeature

# parsing args from the terminal
parser = argparse.ArgumentParser()
parser.add_argument("--dataset_dir", type=str, default="./Dataset/*",
                    help="Directory of the dataset")
parser.add_argument("--feature_dir", type=str, default="./Feature/",
                    help="Destination of the features database")
args = parser.parse_args()

# time it
start = time()
if not os.path.exists(args.feature_dir):
    print("makedirs", args.feature_dir)
    os.makedirs(args.feature_dir)

files = glob(os.path.join(args.dataset_dir, "*_1_*.jpg"))
n_files = len(files)
print("N# of files which we are extracting features", n_files)

for file in tqdm(files):
    template, mask, _ = extractFeature(file)
    basename = os.path.basename(file)
    out_file = os.path.join(args.feature_dir, "%s.mat" % (basename))
    savemat(out_file, mdict={'template': template, 'mask': mask})

end = time()
print('\nTotal time: {} [s]\n'.format(end-start))