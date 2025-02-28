/*
Required packages:
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.Identity
dotnet add package Azure.AI.OpenAI --prerelease
*/

using System;
using Azure;
using System.IO;
using System.Text;
using Microsoft.Extensions.Configuration;
using Azure.Identity;
using Azure.AI.Projects;
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
                string project_connection = configuration["PROJECT_CONNECTION"];
                string model_deployment = configuration["MODEL_DEPLOYMENT"];
                string index_name = configuration["INDEX_NAME"];

                // Initialize the project client
                var projectClient = new AIProjectClient(project_connection,
                    new DefaultAzureCredential());
                
                var connectionsClient = projectClient.GetConnectionsClient();

                // Use the AI search service connection to get service details
                ConnectionResponse searchConnection = connectionsClient.GetDefaultConnection(ConnectionType.AzureAISearch, true);
                var searchProperties = searchConnection.Properties as ConnectionPropertiesApiKeyAuth;
                string search_url = searchProperties.Target;
                string search_key = searchProperties.Credentials.Key;

                // Get an Azure OpenAI client
                ConnectionResponse aoaiConnection = connectionsClient.GetDefaultConnection(ConnectionType.AzureAIServices, true);
                var aoaiProperties = aoaiConnection.Properties as ConnectionPropertiesApiKeyAuth;
                AzureOpenAIClient azureOpenAIClient = new(
                    new Uri(aoaiProperties.Target),
                    new AzureKeyCredential(aoaiProperties.Credentials.Key));

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
                        ChatClient chatClient = azureOpenAIClient.GetChatClient(model_deployment);

                        // Additional parameters to apply RAG pattern using the AI Search index
                        // (DataSource is in preview and subject to breaking changes)
                        #pragma warning disable AOAI001

                        ChatCompletionOptions options = new();
                        options.AddDataSource(new AzureSearchChatDataSource()
                        {
                            Endpoint = new Uri(search_url),
                            IndexName = index_name,
                            Authentication = DataSourceAuthentication.FromApiKey(search_key),
                        });

                        ChatCompletion completion = chatClient.CompleteChat(
                            [
                                new SystemChatMessage("You are an AI travel assistant that helps people plan trips."),
                                new UserChatMessage(input_text),
                            ],
                            options);

                        Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
                        
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

