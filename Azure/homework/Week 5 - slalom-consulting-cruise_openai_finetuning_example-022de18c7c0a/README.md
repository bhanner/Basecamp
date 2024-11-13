
# Cruise FAQ Scraper and Fine-Tuning

This repository contains Python scripts for scraping Frequently Asked Questions (FAQs) from the NCL website and generating a JSONL data file for fine-tuning a language model using OpenAI.

**Please note**: The example provided is for demonstration purposes and uses publicly available data from the NCL website (<https://www.ncl.com/faq>). This is provided as a learning lab and is not appropriate for customer demos.

## Repository Contents

1. `scraper.py` - Python script to scrape FAQ data from the NCL website and save it in JSONL format.
1. `dataset-preparer.py` - Converts the `faq_data_before_prep.jsonl` file into the new format expected by OpenAI for training.
1. `create-find-tuned-model.py` - Kicks off the job that begins the fine tuning job.
1. `completions.py` - Python script to interact with the fine-tuned model and generate responses to user prompts.
1. `create-fine-tuned-model.py` - Python script to initiate the fine tuning job.
1.

## Usage

### Scraping Data

1. Run the `scraper.py` script to scrape the FAQ data and save it in the `faq_data.jsonl` file.

   ```terminal
   python scraper.py
   ```

### Fine-Tuning

1. Follow the instructions in the [OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning) to validate the generated data file and perform fine-tuning using the OpenAI platform.
2. Upload the `faq_data.jsonl` file to the OpenAI platform and validate it.
3. Follow the fine-tuning steps provided in the guide to train the model.
4. Please be aware that fine-tuning has associated costs. Check the OpenAI pricing details for more information.

### Using the Fine-Tuned Model

1. Replace the `model` parameter in the `completions.py` script with the name of the fine-tuned model.
2. Run the script to generate responses to user prompts using the fine-tuned model.

   ```terminal
   python completions.py
   ```

## Example Output

```terminal
Question: Are babysitters available?
Answer: Yes, babysitting services are available on board. However, charges may apply, and availability is subject to certain conditions. Please check with the guest services desk on the ship for more information.
```

## License

This repository is provided under the MIT License. Please see the `LICENSE` file for more information.

Please be aware of the potential legal and ethical implications of web scraping. Ensure that you have the proper permission and consent to scrape and use data from websites.

---

You can adapt this template to your specific needs and include additional details if required. It covers the main parts of the repository, usage, and important notices.
