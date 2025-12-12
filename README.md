# nhs-length-of-stay-prediction

Group Project 10 – Predicting a Patient’s Length of Stay (WWL NHS)

Structure:

- data
  - processed - our columns after data cleaning
  - raw
  - data.csv - merged cleaned columns
  - data_reduced.csv - data after feature selection
- notebooks
  - EDA
  - feature_selection
    - correlation.ipynb - file Sophie presented on the 2nd December, see description below
  - merge_data
    - merge.ipynb - code to merge all columns into data.csv file
  - model
    - model.ipynb - file Sophie presented on the 2nd December, see description below

Feature selection:

1 Features were categorized by type to apply appropriate analysis methods:
Continuous Numerical - Spearman/Pearson correlation
Reason: Spearman method is Non-parametric (Does not assume linear relationships or normal distributions)
Robust to outliers: Uses rank-based calculations
Appropriate for ordinal data: Works well with scores and categorical ordinals

Binary Numerical - Pearson correlation

2 Feature Selection Algorithms:
Method 1: DropCorrelatedFeatures
Algorithm: Drops one feature from each correlated pair

Parameters:
Method: Spearman
Threshold: 0.7
Selection criterion: Drops feature with lower variance

Method 2: SmartCorrelatedSelection
Algorithm: Intelligent selection considering target correlation

Parameters:
Method: Spearman
Threshold: 0.7
Selection method: Variance

Considers correlation with target variable when choosing which feature to drop
Among correlated features, retains the one most predictive of length of stay
Balances multicollinearity reduction with predictive performance

Decision Logic:
For correlated feature pair (A, B):

- If corr(A, target) > corr(B, target): Keep A, drop B
- Else: Keep B, drop A
- If equal: Keep feature with higher variance

3 Feature Grouping
Features were organized into logical clinical groups for interpretable analysis.

Modeling:

Evaluation Metrics:
Mean Absolute Error (MAE) - Primary metric
Interpretable: "Average prediction error in hours"
Robust to outliers compared to MSE
Directly meaningful to clinicians

Root Mean Squared Error (RMSE) - Secondary metric
Penalizes large errors more heavily
Standard in regression problems

R² Score - Model fit metric
Proportion of variance explained
Allows comparison across models
Range: [0, 1] with higher being better

A) Random Forest Regressor
Configuration
n_estimators=200 # Fewer trees, faster training
max_depth=8 # Shallower trees, less complexity
min_samples_split=30 # Requires more samples to split
min_samples_leaf=15 # Larger leaf nodes
max_features=0.5 # Even more feature randomness
max_samples=0.7 # Less data per tree

B) XGBoost
Configuration
n_estimators=200 # Fewer rounds
learning_rate=0.03 # Even slower learning
max_depth=4 # Shallower trees
min_child_weight=5 # Stronger constraint
subsample=0.7 # More subsampling
colsample_bytree=0.7 # Less features per tree
gamma=1.0 # Higher split threshold
reg_alpha=0.1 # More L1 regularization
reg_lambda=2.0 # More L2 regularization

2 Cross-Validation Strategy
Method: 5-Fold Cross-Validation with KFold

1. Shuffle training data
2. Split into 5 equal folds
3. For each fold:
   - Train on 4 folds (80% of training)
   - Validate on 1 fold (20% of training)
4. Average metrics across 5 folds
5. Report mean ± standard deviation

Metrics Tracked:
CV MAE (mean ± std)
CV RMSE (mean ± std)
CV R² (mean ± std)

3 Overfitting Detection & Prevention

Detection Methods:

1. Train-Test Gap Analysis

MAE Gap = Test MAE - Train MAE
R² Gap = Train R² - Test R²
Interpretation:

MAE Gap < 3 hours: Excellent generalization
MAE Gap 3-5 hours: Good generalization
MAE Gap 5-8 hours: Mild overfitting
MAE Gap > 8 hours: Significant overfitting
R² Gap < 0.05: Excellent
R² Gap 0.05-0.10: Good
R² Gap 0.10-0.15: Acceptable
R² Gap > 0.15: Overfitting

2. CV-Test Gap Analysis
   CV-Test Gap = Test MAE - CV MAE
   Reasoning:
   If test performance is much worse than CV, model doesn't generalize
   Small gaps indicate consistent performance across different data splits

Ensemble Strategy:

Approach: Simple averaging of predictions from all models
Reasoning:
Wisdom of crowds: Different models capture different patterns
Reduces variance: Averaging smooths individual model errors
Improves robustness: Less sensitive to any single model's weaknesses
Often reduces overfitting: Combined predictions generalize better

Implementation:
Ensemble Prediction = Mean([RF, RF_Cons, XGB, XGB_Cons, CB, CB_Cons])

Rationale:
Simple average gives equal weight to all models
More sophisticated weighting could be explored (e.g., weighted by CV performance)
Ensemble often outperforms individual models in practice
