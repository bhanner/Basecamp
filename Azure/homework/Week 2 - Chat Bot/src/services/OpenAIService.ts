
import { AzureOpenAI } from "openai";
import { ChatCompletionMessageParam } from 'openai/resources/chat/completions';
import { MessageProps } from '../models/MessageProps';

const systemPrompt: ChatCompletionMessageParam = {
  role: 'system',
  content: `
  You are a helpful assistant with a friendly personality. Here is some additional information about Mr. Hugo Biscuits, aka Hugo: Mr. Hugo Biscuits, a lively Brussels Griffon with a heart as big as his eyes, was eagerly wagging his tail as he approached Central Park. It was his third birthday, and the crisp morning air was filled with the promise of fun and celebration. His human had gone all out, setting up a cozy picnic area adorned with colorful balloons and a big banner that read, "Happy Birthday, Mr. Hugo Biscuits!" As they neared the spot, Mr. Hugo Biscuits could already see his best friends, Big Hugo, a gentle Labradoodle, and Caffee, a sprightly brown and white Bernadoodle, waiting for him. Big Hugo had brought along his favorite squeaky toy shaped like a dinosaur, while Caffee had a box of homemade dog treats, each one carefully decorated with tiny paw prints.
  The party was a joyous affair. Mr. Hugo Biscuits bounded around, sniffing the delicious scents of the treats and occasionally stopping to soak in the love from his friends. They played a game of fetch with a bright blue frisbee, which Big Hugo effortlessly caught with his giant paws, much to the delight of everyone. Caffee, ever the entertainer, performed a little dance, spinning in circles and hopping on her hind legs, which earned her a round of applause and a few extra treats. As the sun began to set, casting a golden hue over the park, the friends gathered around a cake made especially for dogs, adorned with peanut butter frosting and carrot candles. Mr. Hugo Biscuits made a wish (though what could a dog wish for other than endless belly rubs and treats?) and blew out the candles with a little help from his human. It was the perfect end to a perfect day, filled with laughter, love, and the kind of memories that last a lifetime.`
};

export async function callOpenAI(chatHistory: MessageProps[]): Promise<AsyncIterable<string>> {
  const endpoint = process.env.REACT_APP_AZURE_OPENAI_ENDPOINT; 
  const apiKey = process.env.REACT_APP_AZURE_OPENAI_API_KEY; 
  const apiVersion = "2024-04-01-preview";
  const deployment = "gpt-4o"; 
  
  console.log('Endpoint:', endpoint);
  console.log('API KEY:', apiKey);
  if (!apiKey) {
    throw new Error('REACT_APP_AZURE_OPENAI_API_KEY is not defined in the environment variables');
  }
  if (!endpoint) {
    throw new Error('REACT_APP_AZURE_OPENAI_ENDPOINT is not defined in the environment variables');
  }
  const client = new AzureOpenAI({ endpoint, apiKey, apiVersion, deployment, dangerouslyAllowBrowser: true });  

  const messages: ChatCompletionMessageParam[] = [
    systemPrompt,
    ...chatHistory.map(({ role, content }) => ({ role, content } as ChatCompletionMessageParam))
  ];

  const stream = await client.chat.completions.create({
    messages: messages,
    model: 'gpt-4o',
    stream: true
  });

  async function* generateStream() {
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      yield content;
    }
  }

  return generateStream();
}