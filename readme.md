This program will translate any markdown file using the openai gpt3.5. gpt3.5 works really well for most uses. You could change to gpt4 if it's for professional needs. 

Estimating cost: paste your markdown content into here: https://www.chatsplitter.com/?m=1. check your total tokens against the below openAI pricing (as of March 25, 2024). About $0.10 for a 100 page book.

Model	Input	Output
gpt-3.5-turbo-0125	$0.50 / 1M tokens	$1.50 / 1M tokens

To translate your markdown file:

- download the repo
- create a .env file in root with your api key.  OPENAI_API_KEY= XYZ 
- find the markdown file you want to translate
- run the program while specifying the location of input file, starting language, and translation language.

example preloaded that you can run immediately in command line:

python translate.py ./input/peter-pan-abridged.md English Spanish

Note: costs $0.01 to run the above translation of chapter 1 of peter pan from english into spanish. 

Please respect copyright laws. 
