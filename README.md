# Scoring IDH Classification models

## Description
This project provides a simple web application built with Streamlit to calculate key binary classification evaluation metrics: Confusion Matrix, Balanced Accuracy, and F1 Score. It processes a user-uploaded CSV file containing predictions and compares them against pre-defined ground truth data included in the application.

The primary goal is to offer a user-friendly interface (specifically for non-technical users like managers) to evaluate model performance without requiring any local software installation or command-line interaction.

## Files
-   `app.py`: The main Streamlit application script that handles file uploads, data processing, metric calculation, and results display.
-   `target_data.csv`: Contains the ground truth labels (`mIDH`) for the corresponding `slide_id`s. **This file is essential and must be deployed alongside `app.py`.**
-   `submission_example.csv`: An example CSV file demonstrating the required format (`slide_id`, `pred`) for user submissions. You can use this as a template.
-   `requirements.txt`: Lists the Python packages required to run the application (`streamlit`, `pandas`, `scikit-learn`).
-   `README.md`: This file providing an overview and instructions.

## Setup (For Local Development and Testing)
1.  Clone this repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```
2.  Ensure you have Python installed (3.7 or higher recommended).
3.  Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
4.  Make sure the `target_data.csv` file is present in the same directory as `app.py`.
5.  Run the Streamlit application from your terminal in the project directory:
    ```bash
    streamlit run app.py
    ```
6.  The app will open in your default web browser.

## CSVs Requirements

### `target_data.csv` (Included in Repository)
This file serves as the ground truth. It must be named `target_data.csv` and placed alongside `app.py`.
Required columns:
-   `slide_id`: A unique identifier for each sample.
-   `mIDH`: The true binary label (integer, 0 or 1).

### User Uploaded CSV (Via App Interface)
This is the file your model's predictions will be evaluated against. It must be a CSV file.
Required columns:
-   `slide_id`: Unique identifier for each sample, matching those in `target_data.csv`.
-   `pred`: The predicted binary label (integer, typically 0 or 1) from the model.

**An example of the expected format, including the required column headers, can be found in the repository as `submission_example.csv`.**

The application will merge the uploaded submission data with the `target_data.csv` based on matching `slide_id`s. Only samples with `slide_id`s present in *both* files will be included in the metric calculations.

## Deployment
This application is designed for easy deployment on platforms that support Streamlit, such as:
-   **Streamlit Cloud (Recommended):** Direct integration with GitHub for easy deployment and updates.
-   Hugging Face Spaces: Another free platform supporting Streamlit apps.
-   Other PaaS providers (Render, Heroku, etc.) or self-hosting with Docker, though these require more configuration.

When deploying, ensure that `app.py`, `target_data.csv`, `submission_example.csv`, and `requirements.txt` are all included in the deployment package/repository.

## How to Use (Deployed Web App)
1.  Navigate to the provided URL of the deployed application.
2.  Read the brief instructions on the page, which explain the required CSV format.
3.  Click the file uploader area or button.
4.  Select your submission CSV file from your computer.
5.  The application will process the file and display the Confusion Matrix, Balanced Accuracy, and F1 Score directly on the page.
