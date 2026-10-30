"""Accuracy of the predictions written by the ResNet-20/110 executables.

Usage: python3 score.py resnet20_bundle*.txt
"""
import re
import sys
from pathlib import Path

LABEL_DIR = Path(__file__).resolve().parent / "label"
NUM_LABEL_FILES = 313  # label_1.txt ... label_313.txt: 32 labels each, 16 in label_313.txt
NUM_TEST_IMAGES = 10000
BUNDLE_SIZE = 512  # one run = 16 image packs x 32 images
NUM_BUNDLES = 20


def load_labels():
    labels = []
    for p in range(1, NUM_LABEL_FILES + 1):
        labels += [int(float(t)) for t in (LABEL_DIR / f"label_{p}.txt").read_text().split()]
    if len(labels) != NUM_TEST_IMAGES:
        sys.exit(f"{LABEL_DIR}: expected {NUM_TEST_IMAGES} labels, found {len(labels)}")
    return labels


def bundle_number(path):
    m = re.search(r"bundle(\d+)\.txt$", path)
    if not m or not 1 <= int(m.group(1)) <= NUM_BUNDLES:
        sys.exit(f"{path}: expected a file named *bundle<1-{NUM_BUNDLES}>.txt")
    return int(m.group(1))


def main(paths):
    if not paths:
        sys.exit(__doc__.strip())
    bundles = sorted((bundle_number(path), path) for path in paths)
    numbers = [b for b, _ in bundles]
    if len(set(numbers)) != len(numbers):
        sys.exit("each bundle may be given only once")
    labels = load_labels()
    correct = total = 0
    for b, path in bundles:
        preds = [int(t) for t in re.findall(r"\d+", Path(path).read_text())]
        if len(preds) != BUNDLE_SIZE:
            sys.exit(f"{path}: expected {BUNDLE_SIZE} predictions, found {len(preds)}")
        # Bundle 20 holds the last 272 test images; the rest of it is zero padding.
        ref = labels[BUNDLE_SIZE * (b - 1):BUNDLE_SIZE * b]
        hits = sum(p == r for p, r in zip(preds, ref))
        print(f"bundle {b:2d}: {hits}/{len(ref)}")
        correct += hits
        total += len(ref)
    print(f"accuracy: {correct}/{total} = {100 * correct / total:.2f}%")


if __name__ == "__main__":
    main(sys.argv[1:])
