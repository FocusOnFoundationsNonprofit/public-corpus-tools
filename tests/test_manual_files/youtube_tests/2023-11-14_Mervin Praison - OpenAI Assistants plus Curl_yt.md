## metadata
last updated: 11-30-2023 Created
link: https://www.youtube.com/watch?v=ZcBJwyCPUHU
youtube transcript source: auto-captions
youtube title: OpenAI Assistants API + Curl 🤯 How to get started? 🚀 EASY way to create Assistants (Full Tutorial)
length: 0:03:02

## content

### youtube chapters

[0:00](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=0) - Introduction to AI Assistant Creation
[0:03](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=3) - Using Curl Commands for Assistants
[0:08](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=8) - Step-by-Step Tutorial Start
[0:15](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=15) - Creating an AI Assistant with Curl
[0:37](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=37) - Setting Up and Using OpenAI API Key
[1:01](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=61) - Initialising Chat Threads
[1:50](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=110) - Adding User Messages and Questions
[2:09](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=129) - Running and Getting Responses from AI Assistant
[2:33](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=153) - Final Results and Example Response
[2:45](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=165) - Integration with Programming Languages
[3:00](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=180) - Conclusion and Thanks

### youtube description

🌟 Master AI Assistant Creation with Curl!
🚀 Dive into an easy, step-by-step tutorial to build your own AI assistant right in your terminal.

🤖 Learn how to:
Set up and export your OpenAI API key.
Use Curl commands to create an AI assistant.
Initialize chat threads and manage user messages.
Seamlessly run and get responses from your AI assistant.
🌍 Example Project: Build a Geography Expert AI!

🔑 Key Benefits:
Gain practical skills in using Curl for AI applications.
Understand the process of building interactive AI assistants.
Enhance your programming knowledge in an engaging way.
🎥 Like & Subscribe for more AI and technology tutorials!
#ArtificialIntelligence #AIAssistant #CurlCommands #Programming #TechTutorial

ChatGPT Tutorials Playlist: https://www.youtube.com/playlist?list=PLYQsp-tXX9w62Lgpvx2JMBvKAAi7rfb_t

ChatGPT Beginners Guide: https://www.youtube.com/watch?v=_E9rqrnPzWI
GPT-4 Assistants API + Python: https://www.youtube.com/watch?v=pZUDEQs89zc
GPT-4 Assistants API +Node: https://www.youtube.com/watch?v=CPlwcY5mQ_4 
OpenAI Assistants API + Retrieval: https://www.youtube.com/watch?v=Wh727dL-Ql4
GPT-4 Turbo: https://www.youtube.com/watch?v=Fo0KEPP7Nt4
GPT-4 Seed: https://www.youtube.com/watch?v=q5o8n1_jQb4
GPT-4 JSON: https://www.youtube.com/watch?v=9FZSA2UzXL0
ChatGPT Text to Speech API: https://www.youtube.com/watch?v=LWfE-j_V2J0
Dall-e 3 API: https://www.youtube.com/watch?v=eKCLFY5_NZI
Whisper API: https://www.youtube.com/watch?v=B9AuQ3jpwrA
GPT-4 Vision API Image: https://www.youtube.com/watch?v=xtdQb7-bv7E
GPT-4 Vision API Video: https://www.youtube.com/watch?v=QyqnR3bBMDs

Code: https://mer.vin/2023/11/assistants-api-curl/

Timestamps
[0:00](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=0) - Introduction to AI Assistant Creation
[0:03](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=3) - Using Curl Commands for Assistants
[0:08](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=8) - Step-by-Step Tutorial Start
[0:15](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=15) - Creating an AI Assistant with Curl
[0:37](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=37) - Setting Up and Using OpenAI API Key
[1:01](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=61) - Initialising Chat Threads
[1:50](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=110) - Adding User Messages and Questions
[2:09](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=129) - Running and Getting Responses from AI Assistant
[2:33](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=153) - Final Results and Example Response
[2:45](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=165) - Integration with Programming Languages
[3:00](https://www.youtube.com/watch?v=ZcBJwyCPUHU&t=180) - Conclusion and Thanks

#openai #assistantsapi #curl #assistants  #api #ai #artificialintelligence #artificial #intelligence #assistant #command #commands #curlcommand  #assistantsapicurl #endpoints #endpoint #terminal #create

### youtube transcript

this is huge is there any way to create your assistance using curl commands is there any easy way to create your assistant in your terminal that's exactly what we're going to see today let's get [Music] started hi everyone I'm really excited to show you about creating assistance using curl commands I'm going to take you through step by step on how to run this in your own computer before going into that I regularly create videos in my YouTube channel about artificial intelligence so do subscribe and stay tuned coming to create your assistance these are the steps first you're creating an assistant then you creating a thread and thirdly you creating a message and fourth you're running that the assistant what we create is a geography expert thread is for initializing the chat and the message is the user which will be the student who is asking question to the geography expert first you're exporting your openi API key like this this and click enter as a first step we are going to create assistants this is the curl command for that I will add all those commands in the description below here using the model gp4 turbo in the instruction you're mentioning you are a expert in geography I'm going to click enter now we have created an assistant with the assistant ID is this now we going to export the assistant ID you can copy the assistant ID from here and paste it in the export command here and then click enter now we have created the first step which is creating our assistant and now we are going to create a thread as a form of initializing the chat SL threads is the end point to create threads we are passing the open a API key and then click enter now thread got created now we're going to export our thread ID we can copy that from the ID provider here and paste and click enter now we created the second point which is thread and thirdly now we're going to create a message by the student asking a question to the geography expert we are passing the thread ID in the URL and slash messages here the user with the role is asking a question what is the capital of France now we're going to click enter we can see the question got created and assigned through the thread now the final step is run this will run the whole execution you are passing the assistant ID and the thread ID here in the URL and I'm going to click enter now we can see it's created at and the assistant ID thread ID and the status is cued now we have created assistant created a thread message and then ran now we need to print out the result to do that you mention slash messages towards the end and click enter now we got the response the initial question was what is the capital of France and you can see the assistant who a geography expert is responding the capital of France is Paris that's it as simple as that the reason why we have curl command is that by understanding this you'll be able to integrate this assistance API in any programming language can't wait to see you create more programs with this I hope you like this video do like sh And subscribe and thanks for watching