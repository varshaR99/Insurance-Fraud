# Insurance-Fraud
Automatic Vehicle Fraud Insurance Claim Detection System

Key Components of the System:
Machine Learning Algorithm – XGBoost: The core of the system is built around the XGBoost algorithm, a powerful machine learning technique known for its speed and performance, particularly in classification tasks. This algorithm will be trained on a dataset of legitimate and fraudulent vehicle insurance claims, learning patterns that help distinguish between the two. Once trained, it will be able to accurately predict whether a newly submitted insurance claim is fraudulent or legitimate.
Secure Data Handling with AES Encryption: Given the sensitive nature of insurance data, security is a top priority. To ensure that customer data, including personal and financial information, is protected, the system uses AES (Advanced Encryption Standard) encryption. This encryption system secures the data at rest, meaning any customer data stored in the database is encrypted to prevent unauthorized access.

Fraud Detection Workflow:

A user uploads their claim document via the website.
The document is analyzed to extract essential information and keywords.
The extracted data is fed into the XGBoost model, which predicts whether the claim is fraudulent or legitimate.
If the claim is flagged as potentially fraudulent, it may be escalated for further review.
Real-Time Decision Making: The system is designed to work efficiently, providing real-time analysis of insurance claims. This helps insurance companies save time by automatically filtering out fraudulent claims, allowing legitimate ones to be processed faster.

Advantages:
Increased Efficiency: Automates the process of claim verificat![Screenshot (552)](https://github.com/user-attachments/assets/7098f3d6-b169-46c4-ab64-aeb0496b752a)
ion, reducing the workload for human auditors.
Enhanced Accuracy: Machine learning models like XGBoost provide high accuracy, minimizing false positives and negatives.
Data Security: AES encryption ensures that sensitive customer information remains secure throughout the process.
Cost Savings: By detecting fraud early, the system helps reduce financial losses for insurance companies.
![Screenshot (554)](https://github.com/user-attachments/assets/f3755efc-ed8b-4e5b-b6ef-0fb7a8cea455)

![Screenshot (555)](https://github.com/user-attachments/assets/eae75c4c-1c48-4c27-be3f-82f02a65cae4)

![Capture12](https://github.com/user-attachments/assets/5b18df4c-0ce8-4677-bf1c-bb14d5a84bd4)

