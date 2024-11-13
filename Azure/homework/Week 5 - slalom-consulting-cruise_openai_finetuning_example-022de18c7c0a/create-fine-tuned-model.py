from openai import OpenAI
client = OpenAI()

# Make sure that you have uploaded the training file to the OpenAI Storage are before running the fine tuning job below.
# https://platform.openai.com/storage/files/
# Once the file has been uploaded grab the fileId associated with the file and replace the fileId in the training_file parameter below.
# Make sure you are looking at the correct Project in the OpenAI Platform. The Project should be the same as the one you uploaded the file to.

client.fine_tuning.jobs.create(
  training_file="file-GBFc1KqvdEbavbmk2jv0YCGt",
  model="gpt-4o-mini-2024-07-18",
  suffix="ne-se-gen-ai-boot-camp-2024-11-05"
)