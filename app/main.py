from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from app.ocr_utils import extract_invoice_data
from pymongo import MongoClient
import boto3
import uuid
from bson import ObjectId
from mangum import Mangum

# MongoDB Atlas connection URI
MONGO_URI = "mongodb+srv://akhilkambhatla:akhilkambhatla@invoice-cluster.ucjgb.mongodb.net/invoiceDB?retryWrites=true&w=majority&appName=invoice-cluster"

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["invoiceDB"]
collection = db["invoices"]

# AWS S3 setup
s3_client = boto3.client('s3', region_name='eu-north-1')
S3_BUCKET_NAME = 'invoice-storage-akhil'

# FastAPI setup
app = FastAPI()

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-invoice/")
async def upload_invoice(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Extract data using OCR
        extracted_data = extract_invoice_data(file_location)

        # Upload to S3
        s3_key = f"{uuid.uuid4()}_{file.filename}"
        s3_client.upload_file(file_location, S3_BUCKET_NAME, s3_key)

        # Save to MongoDB
        extracted_data["s3_file_key"] = s3_key  # Add S3 reference
        inserted_result = collection.insert_one(extracted_data)

        # Prepare response
        response_data = extracted_data.copy()
        response_data["_id"] = str(inserted_result.inserted_id)  # Convert ObjectId

        return JSONResponse(content={"invoice_data": response_data}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/invoices/")
async def get_all_invoices():
    try:
        invoices = list(collection.find())
        for invoice in invoices:
            invoice["_id"] = str(invoice["_id"])  # Convert ObjectId to string

        return JSONResponse(content={"invoices": invoices}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
handler = Mangum(app)
