import openai
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open('train_data.jsonl', 'rb') as file:
    upload_response = client.files.create(
        file=file,
        purpose="fine-tune"
    )

file_id = upload_response.id

job_response = client.fine_tuning.jobs.create(
    training_file=file_id,  # File ID obtained from the upload
    model="gpt-4o-mini-2024-07-18"  # Choose the model you want to fine-tune
)


status_response = client.fine_tuning.jobs.retrieve(job_response.id)
#print(f"Fine-tuning job status: {status_response.status}")
#while True:
#    status_response = client.fine_tuning.jobs.retrieve(job_response.id)
#    print(f"Fine-tuning job status: {status_response.status}")
#
#    if status_response.status == 'succeeded':
#        print("Fine-tuning completed successfully!")
#        job_details = client.fine_tuning.jobs.retrieve("ftjob-zEBkVawFybZqPEp64AwVdcEI")
#        print(job_details)
#        break
#   elif status_response.status == 'failed':
#        print("Fine-tuning job failed.")
#        break
#    elif status_response.status == 'validating_files':
#    elif status_response.status == 'training':
#        print("Training in progress...")
#     # Wait for 30 seconds before checking the status again
#    time.sleep(30)
