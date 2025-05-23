==============================
README: Sentiment Analysis on Dark Web forums
==============================

Authors: Kyrie-Alysa van IJsselmuide (2136942) & Kim van Kemenade
Assignment: Data Forensics - Scientific Report
Goal: Analyze the sentiment of posts and threads on 4chan and Endchan
Submission: forensics-group3.zip

------------------------------
File Structure in ZIP package:
------------------------------

1. model_training.ipynb          - The main neural network training notebook containing the final model and plotting the loss curve
2. helper.py                     - Contains the neural network class, dataset class, and early stopping class
3. predict_rings.ipynb           - Notebook for running inference on the test dataset
4. best_model.pt                 - Saved model weights from the best model
5. train.csv                     - Original training dataset provided
6. test.csv                      - Original test dataset provided
7. test_with_predictions.csv     - Test set with an added column 'Rings' containing predicted ages
8. DL2025IAreport_2136942.pdf    - Short report summarizing the model
9. README.txt                    - This instruction file

------------------------------
Packages overview:
------------------------------
- Python 3.10.16
- matplotlib         3.10.1
- matplotlib-inline  0.1.7
- numpy              2.1.2
- pandas             2.2.3
- scikit-learn       1.6.1
- scipy              1.15.2
- seaborn            0.13.2
- torch              2.5.1+cu121
- torchaudio         2.5.1+cu121
- torchvision        0.20.1+cu121

------------------------------
Run instructions for test data:
------------------------------

1. Make sure you have the packages and package versions installed as instructed above.

2. Place the following files in the same directory:
   - `helper.py`
   - `best_model.pt`
   - `test.csv`
   - `predict_rings.ipynb`

3. Run the notebook:
   - For notebook (`predict_rings.ipynb`), run all cells in order

4. The notebook will:
   - Load the test dataset and apply the same preprocessing as for the training dataset
   - Load the saved model weights from `best_model.pt`
   - Run inference to predict the number of rings (age) using a multi-classification deep learning model
   - Save a new file `test_with_predictions.csv` with the predictions in the `Rings` column

------------------------------
Notes:
------------------------------
- Make sure you have GPU enabled if using a CUDA environment.
- If any package is missing, install it using pip


