Tutorial
Target Prediction
Support Vector Machine
46 models. Metrics for test data:
accuracy 97.59 +/- 2.41
sensitivity 91.9 +/- 8.1
specificity 98.6 +/- 1.4
215/247 87% correct mechanism on independent test set.
======================================
Chembl Target Prediction
Multiclass Classifier
Number of unique targets 560
Ion channel 5
kinase 96
nuclear receptor 21
GPCR 180
Others 258
accuracy .87
auc .92
sensitivity .76
specificity .92
precision .82
225/225 100% correct mechanism on independent test set. Note-- 1 is considered positive and zero is negative for a given target.
======================================
Interpreting output:  For the target predictions, the green represents a positive region for the molecule, the red represents a negative region of the molecule for a tested property, and gray represents no detection. For more on this method please read Similarity maps-- a visualization strategy for molecular fingerprints and machine learning methods.
======================================
Inside the target prediction folder, there should be .png images for each of the smiles in the output folder. Make sure to change the directory to the output directory of the targetprediction folder under the images menu. Since there are 46 models it is best to only use a few smiles at a time.
======================================
Creating your own models:  https://pubchem.ncbi.nlm.nih.gov/#query=interferon&tab=assay, Also see chembl bioassays. These assays must be saved as .txt files with two columns-- the first for the smiles and the next column for either 1 or zero (active and inactive respectively).  The text file with the smiles and 1's and 0's should be in the targetprediction folder.  The text file names should contain the name of the assay.  You want a model with both good sensitivity and specificity (as close to one as possible).  It is important to note that a model can appear highly accurate but if sensitivity is zero, then the model does not detect positives.
======================================
confusion matrix
tn fp
fn tp
It is important to note that column 1, row 1 is NOT true positive as you might expect from stats class.  Sensitive models will not have 0 in the bottom right corner.  If you are not getting good sensitivity and specificity, then you may want to change the penalty C=500000 to some other value.  By default the SVC is set up to use a RBF best fit but this can be changed as per the scikit learn documentation.  The output files will be saved as .pkl files that can later be loaded for future use.
======================================
Pan Assay Interference
See Seven Year Itch: Pan-Assay Interference Compounds (PAINS) in 2017—Utility and Limitations New Substructure Filters for Removal of Pan Assay Interference Compounds (PAINS) from Screening Libraries and for Their Exclusion in Bioassays. Pan Assay Interference Compounds commonly result in false positives in biological screening assays.
Since they bind everything, they are not selective and therefore do not make good drug targets.  We found that the higher the drug score in Data Warrior http://www.openmolecules.org/datawarrior/ the lower the frequency of compounds containing PAINS.  Using data warrior’s evolutionary algorithm (be sure to use the wand tool if you want to fix the scaffold), evolve a few runs by taking the compounds with the top drug scores (macro → run macro → calculate properties) by taking the top 5 scoring compounds as starting points for evolution until you get drug scores greater than .9.  Select based on skelsphere similarity and the algorithm will generate a large number of compounds that have high drug scores, which are oftentimes painless.
The program will tell you what functional groups for each compound were responsible for a positive PAINFUL test result.  The program also tells you the fraction of SP3 hybridized carbons.  Compounds with scores > .47 are more selective binders.  Note that double bonds reduce the fraction of sp3 hybridization, as they make the compound more flat.  See Escape from flatland: increasing saturation as an approach to improving clinical success. Pains are defined as follows:
Doveston R, et al. A Unified Lead-oriented Synthesis of over Fifty Molecular Scaffolds. Org Biomol Chem 13 (2014) 859D65. doi:10.1039/C4OB02287D
Jadhav A, et al, Quantitative Analyses of Aggregation, Autofluorescence, and Reactivity Artifacts in a Screen for Inhibitors of Thiol Protease.  J Med Chem 53 (2009) 37D51. doi:10.1021/jm901070c
======================================
Fragmenter
Input a list of smiles.  These will be recombined into new combinations.  When you take the lowest energy ligands from a docking program and recombine these there may be some compounds that bind with lower energy than the original.
======================================
Make Spreadsheet
Input smiles.  The output will be a spreadsheet called test.xlsx in the target prediction folder that contains images of the molecules.
======================================
Solubility
Predicts log S.  Log S greater than -4 is soluble.
Root mean square error of 1.27 on a scale from -4 to 4.
linear regression
======================================
Build a SAR model
cross entropy- default loss function for binary classification problems. Summarizes the average difference between the actual and predicted probability.
hinge- alternative to cross entropy binary classification developed with SVM models used with support vector machine models
mse-default loss to use for regression problems. calculated as the average of the squared differences between the predicted and actual values
mae-for regression problems.  used in cases where there are outliers. average of the absolute difference between actual and predicted values


