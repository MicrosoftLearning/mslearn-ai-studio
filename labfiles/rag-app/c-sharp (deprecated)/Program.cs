using System;
using Azure;
using System.IO;
using System.Text;
using System.Collections.Generic;
using Microsoft.Extensions.Configuration;
using Azure.AI.OpenAI;
using System.ClientModel;
using Azure.AI.OpenAI.Chat;
using OpenAI.Chat;

namespace rag_app
{
    class Program
    {
        static void Main(string[] args)
        {
            // Clear the console
            Console.Clear();

            try
            {
                // Get config settings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string open_ai_endpoint = configuration["OPEN_AI_ENDPOINT"];
                string open_ai_key = configuration["OPEN_AI_KEY"];
                string chat_model = configuration["CHAT_MODEL"];
                string embedding_model = configuration["EMBEDDING_MODEL"];
                string search_url = configuration["SEARCH_ENDPOINT"];
                string search_key = configuration["SEARCH_KEY"];
                string index_name = configuration["INDEX_NAME"];

                // Get an Azure OpenAI chat client
                AzureOpenAIClient azureClient = new(
                    new Uri(open_ai_endpoint),
                    new AzureKeyCredential(open_ai_key));
                ChatClient chatClient = azureClient.GetChatClient(chat_model);


                // Initialize prompt with system message
                var prompt = new List<ChatMessage>()
                {
                    new SystemChatMessage("You are a travel assistant that provides information on travel services available from Margie's Travel.")
                };

                // Loop until the user types 'quit'
                string input_text = "";
                while (input_text.ToLower() != "quit")
                {
                    // Get user input
                    Console.WriteLine("Enter the prompt (or type 'quit' to exit):");
                    input_text = Console.ReadLine();

                    if (input_text.ToLower() != "quit")
                    {
                        // Add the user input message to the prompt
                        prompt.Add(new UserChatMessage(input_text));

                        // (DataSource is in preview and subject to breaking changes)
                        #pragma warning disable AOAI001

                        // Additional parameters to apply RAG pattern using the AI Search index
                        ChatCompletionOptions options = new();
                        options.AddDataSource(new AzureSearchChatDataSource()
                        {
                            // The following params are used to search the index
                            Endpoint = new Uri(search_url),
                            IndexName = index_name,
                            Authentication = DataSourceAuthentication.FromApiKey(search_key),
                            // The following params are used to vectorize the query
                            QueryType = "vector",
                            VectorizationSource = DataSourceVectorizer.FromDeploymentName(embedding_model),
                        });

                        // Submit the prompt with the data source options and display the response
                        ChatCompletion completion = chatClient.CompleteChat(prompt, options);
                        var completionText = completion.Content[0].Text;
                        Console.WriteLine(completionText);

                        // Add the response to the chat history
                        prompt.Add(new AssistantChatMessage(completionText));

                        #pragma warning restore AOAI001
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}