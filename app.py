# app.py
import streamlit as st
import pandas as pd
from sklearn import metrics
import os # To check if the target file exists

st.set_page_config(page_title="Binary Classification Metrics Calculator")

st.title("IDH Mutation Status Classification Metrics")

# --- Streamlit Guidelines for the User ---
st.write("""
Welcome! This app calculates metrics to evaluate your classification model's performance against the TCGA IDH mutation status benchmark data.

To use this app, please upload a CSV file containing your model's predictions.

**Your CSV file must include the following columns:**
-   `slide_id`: A unique identifier for each sample. These IDs must match the samples in our internal target data.
-   `pred`: Your model's predicted binary label for the corresponding `slide_id` (should be 0 or 1).

""")
# --- End of Guidelines ---

# --- Configuration ---
TARGET_DATA_FILENAME = 'target_data.csv'
SUBMISSION_REQUIRED_COLS = ['slide_id', 'pred']
TARGET_REQUIRED_COLS = ['slide_id', 'mIDH']

# --- Load Target Data ---
@st.cache_data # Cache the target data loading
def load_target_data(filename):
    """Loads the target data CSV from a specified file."""
    if not os.path.exists(filename):
        st.error(f"Error: Target data file '{filename}' not found.")
        st.stop() # Stop execution if target file is missing
    try:
        df = pd.read_csv(filename)
        missing = set(TARGET_REQUIRED_COLS).difference(df.columns.tolist())
        if missing:
            st.error(f"Error: Target data file '{filename}' is missing required columns: {', '.join(missing)}")
            st.stop()
        return df[TARGET_REQUIRED_COLS]
    except Exception as e:
        st.error(f"Error loading target data file '{filename}': {e}")
        st.stop()

df_source = load_target_data(TARGET_DATA_FILENAME)


# --- File Uploader for Submission ---
uploaded_file = st.file_uploader("Upload your submission CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Load submission data
        df_submission = pd.read_csv(uploaded_file)

        # Validate submission columns
        missing_submission_cols = set(SUBMISSION_REQUIRED_COLS).difference(df_submission.columns.tolist())
        if missing_submission_cols:
            st.error(f"Error: Submission CSV is missing required columns: {', '.join(missing_submission_cols)}")
        else:
            df_submission = df_submission[SUBMISSION_REQUIRED_COLS]

            # Merge submission with target data
            # Use an inner merge to keep only slide_ids present in both files
            df_merged = df_submission.merge(df_source, on='slide_id', how='inner')

            if df_merged.empty:
                 st.warning("No matching 'slide_id' found between the submission and target data.")
            else:
                # Ensure correct data types
                try:
                    df_merged['mIDH'] = df_merged['mIDH'].astype(int)
                    df_merged['pred'] = df_merged['pred'].astype(int) # Assuming predictions should be integers (0 or 1)
                    if not df_merged['pred'].isin([0, 1]).all():
                         st.warning("Warning: 'pred' column contains values other than 0 or 1. Metrics might be unreliable for binary classification.")
                    if not df_merged['mIDH'].isin([0, 1]).all():
                         st.warning("Warning: 'mIDH' column in target data contains values other than 0 or 1. Metrics might be unreliable for binary classification.")

                except ValueError:
                    st.error("Error: 'mIDH' or 'pred' columns could not be converted to integers. Please check data.")
                    st.stop()


                st.subheader("Results")

                # Calculate and display metrics
                y_true = df_merged['mIDH']
                y_pred = df_merged['pred']

                # Confusion Matrix
                st.write("### Confusion Matrix")
                try:
                    cm = metrics.confusion_matrix(y_true, y_pred)
                    # Display as a dataframe for better readability
                    cm_df = pd.DataFrame(cm, index=['Actual 0', 'Actual 1'], columns=['Predicted 0', 'Predicted 1'])
                    st.dataframe(cm_df)
                    st.write(f"True Positives (TP): {cm[1, 1]}")
                    st.write(f"True Negatives (TN): {cm[0, 0]}")
                    st.write(f"False Positives (FP): {cm[0, 1]}")
                    st.write(f"False Negatives (FN): {cm[1, 0]}")

                except Exception as e:
                     st.error(f"Error calculating Confusion Matrix: {e}")


                # Balanced Accuracy
                st.write("### Balanced Accuracy")
                try:
                    bal_acc = metrics.balanced_accuracy_score(y_true, y_pred)
                    st.write(f"{bal_acc:.4f}")
                except Exception as e:
                     st.error(f"Error calculating Balanced Accuracy: {e}")


                # F1 Score
                st.write("### F1 Score")
                try:
                    f1 = metrics.f1_score(y_true, y_pred)
                    st.write(f"{f1:.4f}")
                except Exception as e:
                     st.error(f"Error calculating F1 Score: {e}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

else:
    st.info("Please upload a submission CSV file to get started.")
