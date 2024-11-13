import json

# This file converts the legacy FAQ data format to the new format expected by OpenAI

input_file = 'faq_data_before_prep.jsonl'
output_file = 'faq_data_after_prep.jsonl'

# Define the system message
system_message = {
    "role": "system",
    "content": "You are an assistant providing information about Norwegian Cruise Line services."
}

# Read the input file and process each line
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        data = json.loads(line)
        prompt = data['prompt'].strip()
        completion = data['completion'].strip()
        
        # Create the new format
        messages = [
            system_message,
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": completion}
        ]
        
        # Write the new format to the output file
        json.dump({"messages": messages}, outfile)
        outfile.write('\n')

print(f"Data has been converted and saved to {output_file}")