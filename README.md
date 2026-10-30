# HEaaN-CBC-ResNet

Encrypted batch inference of ResNet-20 and ResNet-110 on the CIFAR-10 test set with
channel-by-channel (CBC) packing, implemented with the HEaaN library (RNS-CKKS). This is the code of

> J. H. Cheon, M. Kang, T. Kim, J. Jung, and Y. Yeo, "Batch Inference on Deep Convolutional Neural
> Networks With Fully Homomorphic Encryption Using Channel-By-Channel Convolutions,"
> *IEEE Transactions on Dependable and Secure Computing*, vol. 22, no. 2, pp. 1674–1685, 2025.
> doi:[10.1109/TDSC.2024.3448406](https://doi.org/10.1109/TDSC.2024.3448406)

## Requirements

- **HEaaN.** HEaaN is proprietary software of CryptoLab and is not included in this repository
  (see https://heaan.it). The experiments in the paper ran in a HEaaN Docker image (Ubuntu 20.04)
  provided by CryptoLab. The code uses the HEaaN API of that release
  (`HomEvaluator::bootstrap`, `makeBootstrappable`, parameter preset `FGb`); other HEaaN versions
  may need changes.
- **GCC with OpenMP.** The code uses `auto` function parameters, which GCC accepts before C++20
  but Clang does not.
- CMake 3.13 or later.
- Python 3 for scoring (standard library only; it can also be run outside the container).
- **Hardware.** The paper used 2× Intel Xeon Gold 6248 (40 cores in total) with 1 TB of RAM.
  Peak memory was about 370 GB, and one run of 512 images took about 8,068 s for ResNet-20 and
  44,850 s for ResNet-110.

## Build

Inside the HEaaN container (or another environment with that HEaaN release installed):

```sh
git clone https://github.com/mskang0503/HEaaN-CBC-ResNet.git
cd HEaaN-CBC-ResNet
cmake -B build
cmake --build build
```

This builds `build/bin/20` (ResNet-20) and `build/bin/110` (ResNet-110). The location of the
repository is compiled in, so the executables read `image/` and `kernel/` from any working
directory; rebuild after moving the repository.

## Run

The 10,000 test images are split into 20 bundles of 512 images: bundle *b* consists of
`image/image_<16(b-1)+1>.txt` … `image/image_<16b>.txt`. Each run reads the bundle number from
standard input and writes the 512 predicted classes to `resnet20_bundle<b>.txt`
(`resnet110_bundle<b>.txt` for ResNet-110) in the current directory.

```sh
export OMP_NUM_THREADS=40 OMP_PROC_BIND=true OMP_PLACES=cores
cd build/bin
echo 1 | ./20                                    # ResNet-20, bundle 1
for b in $(seq 1 20); do echo $b | ./20; done    # ResNet-20, all 10,000 images
```

## Score

```sh
python3 ../../score.py resnet20_bundle*.txt
```

prints the accuracy of each bundle and the total against `label/`. Over all 20 bundles the paper
reports 91.96% for ResNet-20 and 93.65% for ResNet-110 (Table VI). CKKS is approximate and
encryption is randomized, so a few predictions close to a decision boundary can differ between runs.

## Data

| Path | Contents |
| --- | --- |
| `image/image_<p>.txt`, p = 1 … 320 | CIFAR-10 test images 32(p−1) … 32p−1 in test-set order, normalized; 32 × 3 × 32 × 32 values, one per line. `image_313.txt` holds the last 16 images followed by zeros, and `image_314.txt` … `image_320.txt` are zero padding, so that 20 bundles × 512 = 10,240 slots. |
| `label/label_<p>.txt`, p = 1 … 313 | Labels of the images in `image_<p>.txt` (16 labels in `label_313.txt`). |
| `kernel/ResNet20/`, `kernel/ResNet110/` | Pre-trained weights with batch normalization folded into the convolutions: weights in `multiplicands/`, biases in `summands/`. |

## Citation

```bibtex
@article{CKK+25,
  author  = {Cheon, Jung Hee and Kang, Minsik and Kim, Taeseong and Jung, Junyoung and Yeo, Yongdong},
  title   = {Batch Inference on Deep Convolutional Neural Networks With Fully Homomorphic Encryption Using Channel-By-Channel Convolutions},
  journal = {IEEE Transactions on Dependable and Secure Computing},
  volume  = {22},
  number  = {2},
  pages   = {1674--1685},
  year    = {2025},
  doi     = {10.1109/TDSC.2024.3448406}
}
```
