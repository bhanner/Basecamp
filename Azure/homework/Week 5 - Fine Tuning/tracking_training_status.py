# Track training status

from IPython.display import clear_output
from openai import AzureOpenAI
import os
import time

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),
  api_version = "2024-08-01-preview"  # This API version or later is required to access seed/events/checkpoint features
)

job_id = "<JOB ID>" # Replace with the JOB ID from the previous step
start_time = time.time()

# Get the status of our fine-tuning job.
response = client.fine_tuning.jobs.retrieve(job_id)

status = response.status

# If the job isn't done yet, poll it every 10 seconds.
while status not in ["succeeded", "failed"]:
    time.sleep(10)

    response = client.fine_tuning.jobs.retrieve(job_id)
    print(response.model_dump_json(indent=2))
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    status = response.status
    print(f'Status: {status}')
    clear_output(wait=True)

print(f'Fine-tuning job {job_id} finished with status: {status}')

print("\n---------------------------------------------------------------------------")
print("Fine-tuning job details:")
print("---------------------------------------------------------------------------")

# List all fine-tuning jobs for this resource.
print('Checking other fine-tune jobs for this resource.')
response = client.fine_tuning.jobs.list()
print(f'Found {len(response.data)} fine-tune jobs.')

# List fine-tuning job events
print("\n---------------------------------------------------------------------------")
print("Fine-tuning job events:")
print("---------------------------------------------------------------------------")

response = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=10)
print(response.model_dump_json(indent=2))

# List checkpoints
print("\n---------------------------------------------------------------------------")
print("Checkpoints:")
print("---------------------------------------------------------------------------")

response = client.fine_tuning.jobs.checkpoints.list(job_id)
print(response.model_dump_json(indent=2))

# Retrieve fine_tuned_model name

response = client.fine_tuning.jobs.retrieve(job_id)

print("\n---------------------------------------------------------------------------")
print("fine_tuned_model name:")
print("---------------------------------------------------------------------------")

print(response.model_dump_json(indent=2))
fine_tuned_model = response.fine_tuned_model