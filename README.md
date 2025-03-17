# Medical Invoice Processor

This project is a **Medical Invoice Processor** that extracts information from medical invoices, stores the data in **MongoDB**, and uploads the invoice images to **Amazon S3**. It runs on an **EC2 instance** in an AWS environment.

## Features

- **OCR Extraction**: Extracts text from medical invoices using Optical Character Recognition (OCR).
- **MongoDB Integration**: Stores extracted data in **MongoDB** for easy retrieval and management.
- **S3 Storage**: Uploads invoice images to **Amazon S3** for cloud storage and accessibility.
- **FastAPI Backend**: A RESTful API built with **FastAPI** for handling HTTP requests and processing invoices.
- **AWS EC2**: The application runs on an **AWS EC2 instance** for hosting the backend and interacting with AWS services.

## Technologies Used

- **FastAPI**: The web framework for building APIs with Python.
- **MongoDB**: A NoSQL database used for storing invoice data.
- **Tesseract OCR**: An OCR tool used to extract text from images (invoices).
- **Amazon S3**: Cloud storage for storing invoice images.
- **AWS EC2**: Virtual machine in the cloud to host and run the application.
- **Boto3**: AWS SDK for Python to interact with S3 and EC2 services.

## Setup Instructions

### Prerequisites

Before setting up the project, ensure the following tools are installed:

- **Python 3.9+**
- **MongoDB** (local or MongoDB Atlas)
- **AWS CLI** (for interacting with AWS services)
- **AWS EC2 Instance** (with the appropriate IAM role for S3 and MongoDB access)
- **pip** (for installing dependencies)

### 1. Clone the Repository

```bash
git clone https://github.com/Akhil-Kambhatla/Medical-Invoice-Processor.git
cd Medical-Invoice-Processor
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. MongoDB Configuration
To store invoice data, configure the MongoDB database:
- Ensure your MongoDB is running (either locally or on MongoDB Atlas).
- Set the connection string in your **config.py** or environment variables.

```bash
MONGO_URI = "mongodb://localhost:27017"
```

### 4. S3 Configuration
To upload invoice images to Amazon S3, you’ll need to configure your AWS credentials.
- Set up IAM roles and policies in AWS for EC2 to interact with S3 and MongoDB.
- Ensure your EC2 instance has the necessary IAM permissions to interact with S3.
- Set the bucket name in your **config.py** or environment variables:

```bash
S3_BUCKET_NAME = "your-s3-bucket-name"
```

### 5. Run the FastAPI Application
1. Run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```
This will start the API server on http://127.0.0.1:8000.  

2. Test the OCR and File Upload Process
- You can upload invoice images via the FastAPI endpoints.
- The invoice image will be processed, and the extracted data will be stored in MongoDB.
- The image will be uploaded to your specified S3 bucket.


### 6. Deploying on EC2
To run this application on an EC2 instance:

1. SSH into the EC2 instance:
```bash
ssh -i "your-key.pem" ec2-user@<your-ec2-public-ip>
```
2. Install dependencies on the EC2 instance:
```bash
git clone https://github.com/Akhil-Kambhatla/Medical-Invoice-Processor.git
cd Medical-Invoice-Processor
pip install -r requirements.txt
```
3. Run the FastAPI app on the EC2 instance:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
4. Ensure your EC2 instance security group allows incoming traffic on port 8000 (or any other port you choose).
