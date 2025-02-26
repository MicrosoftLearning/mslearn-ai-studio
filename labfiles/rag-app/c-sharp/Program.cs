using System;
using System.Text.Json;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Json;
using Azure;

// Add Azure OpenAI package
using Azure.AI.Projects;
using Azure.Identity;
using OpenAI.Chat;
using Azure.AI.OpenAI;

namespace rag_app
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Get config settings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string project_connection = configuration["PROJECT_CONNECTION"];
                string model_deployment = configuration["MODEL_DEPLOYMENT"];
                string search_index = configuration["SEARCH_INDEX"];

                // Initialize the project client
                var projectClient = new AIProjectClient(project_connection,
                        new DefaultAzureCredential());

                // Get a connections client
                var projectConnections = projectClient.GetConnectionsClient();


                // Get an OpenAI chat client
                ConnectionResponse aoaiConnection = projectConnections.GetDefaultConnection(ConnectionType.AzureOpenAI, withCredential: true);
                var aoaiProperties = aoaiConnection.Properties as ConnectionPropertiesApiKeyAuth;
                AzureOpenAIClient aoaiClient = new(
                    new Uri(aoaiProperties.Target),
                    new AzureKeyCredential(aoaiProperties.Credentials.Key));

                ChatClient chat = aoaiClient.GetChatClient(model_deployment);

                // Configure Azure Search data source
                ConnectionResponse searchConnection = projectConnections.GetDefaultConnection(ConnectionType.AzureAISearch, withCredential: true).Value;
                var searchProperties = searchConnection.Properties as ConnectionPropertiesApiKeyAuth;
                ChatCompletionOptions chatOptions = new();
                chatOptions.AddDataSource(new AzureSearchChatDataSource()
                {
                    Endpoint = new Uri(searchProperties.Target),
                    IndexName = search_index,
                    Authentication = DataSourceAuthentication.FromApiKey(searchProperties.Credentials.Key),
                });


                // Loop until the user types 'quit'
                string input_text = "";
                while (input_text.ToLower() != "quit")
                {
                    // Get user input
                    Console.WriteLine("Enter the prompt (or type 'quit' to exit):");
                    input_text = Console.ReadLine();
                    if (input_text.ToLower() != "quit")
                    {
                        // Get a chat completion
                        ChatCompletion completion = chatClient.CompleteChat(
                            [
                                new SystemChatMessage("You are a helpful AI assistant that answers questions about travel."),
                                new UserChatMessage(input_text),
                            ],
                            chatOptions);
                         Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");

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


