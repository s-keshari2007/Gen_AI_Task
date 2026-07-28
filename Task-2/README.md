# Project Sentinel — Eyes of the Highway Reserve
**ACM BPHC GenAI Induction 2026 — Task 2**

Land-cover classification on satellite imagery, built as a stand-in for the reserve's new
satellite feed. Every patch of the reserve-highway corridor gets tagged as one of 10 EuroSAT
classes (AnnualCrop, Forest, HerbaceousVegetation, Highway, Industrial, Pasture, PermanentCrop,
Residential, River, SeaLake) — the real-world equivalents of forest / river / highway / farmland /
residential the brief asks for.

## What's inside

`Project_Sentinel_EuroSAT.ipynb` trains and compares **four models**:

| # | Model | Augmentation |
|---|-------|--------------|
| 1 | TinyVGG (CNN from scratch) | No |
| 2 | TinyVGG (CNN from scratch) | Yes |
| 3 | ResNet18 (fine-tuned, ImageNet-pretrained) | No |
| 4 | ResNet18 (fine-tuned, ImageNet-pretrained) | Yes |

For each: training/validation loss & accuracy curves, final test accuracy, and a confusion matrix.
The last section of the notebook lays out the side-by-side comparison and a field-report write-up.

## Architecture details

- **TinyVGG**: 2 conv blocks (Conv→ReLU→Conv→ReLU→MaxPool), trained from random init.
- **ResNet18 fine-tune**: ImageNet-pretrained backbone, frozen except `layer4`; final FC layer
  replaced with a fresh `Linear(512, 10)` and trained.
- **Augmentation**: random horizontal/vertical flip, random rotation (±15°), light color jitter.
  Applied to training data only — validation/test always use the un-augmented pipeline so
  numbers stay comparable across the four runs.

## How to run

1. Open `Project_Sentinel_EuroSAT.ipynb` in **Google Colab** (recommended — pick a T4 GPU runtime
   via Runtime → Change runtime type) or run locally with `torch` + `torchvision` installed.
2. Run all cells top to bottom. `torchvision.datasets.EuroSAT(download=True)` fetches the RGB/JPEG
   dataset automatically — no manual download needed.
   - If the automatic download is blocked in your environment, grab the RGB zip from the
     [Kaggle link](https://www.kaggle.com/datasets/apollo2506/eurosat-dataset) in the task brief,
     extract it, and point `DATA_ROOT` at the folder instead.
3. Training runs for `EPOCHS = 10` per model by default — adjust in the "Train Model 1" cell if
   you need it faster (CPU) or want to push accuracy further (GPU).
4. The final cells produce the comparison table, bar chart, and confusion matrices used in the
   field report.

## Field report

See the last markdown cell of the notebook for the write-up template covering:
- Scratch-CNN vs. fine-tuned convergence speed and final accuracy
- Whether augmentation helped more for TinyVGG or ResNet18
- Which land-cover classes get confused with each other
- Deployment recommendation for the actual satellite pipeline

*(Fill in final accuracy numbers + a confusion matrix screenshot here after running the notebook.)*

## Colab link

*(paste your Colab link here if you ran it there, per the task's "alternatively" option)*
