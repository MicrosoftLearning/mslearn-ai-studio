using System;
using Azure;
using System.IO;
using System.Text;
using System.Collections.Generic;
using Microsoft.Extensions.Configuration;

// Add references


namespace chat_app
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

                // Initialize the project client



                // Get a chat client



                string system_message = "You are an AI assistent in a grocery store that sells fruit.";
                string prompt = "";

                // Loop until the user types 'quit'
                string input_text = "";
                while (input_text.ToLower() != "quit")
                {
                    // Get user input
                    Console.WriteLine("Choose a prompt type (or type 'quit' to exit):\n-1: Text\n-2: Image\n-3: Audio\n");
                    input_text = Console.ReadLine().ToLower();
                    if (input_text != "quit")
                    {
                        switch (input_text)
                        {
                            case "1":
                                Console.WriteLine("Enter the prompt: ");
                                prompt = Console.ReadLine();
                                if (string.IsNullOrEmpty(prompt))
                                {
                                    Console.WriteLine("Please enter a prompt.");
                                }
                                else
                                {
                                    Console.WriteLine("Getting a response to your prompt...");

                                    // Get a response to text input


                                }
                                break;
                            case "2":
                                Console.WriteLine("Enter the prompt to accompany the image: ");
                                prompt = Console.ReadLine();
                                if (string.IsNullOrEmpty(prompt))
                                {
                                    Console.WriteLine("Please enter a prompt.");
                                }
                                else
                                {
                                    Console.WriteLine("Getting a response to your prompt...");

                                    // Get a response to image input


                                }
                                break;
                            case "3":
                                Console.WriteLine("Enter the prompt to accompany an audio recording of 'Me gustaría comprar 2 manzanas.':");
                                prompt = Console.ReadLine();
                                if (string.IsNullOrEmpty(prompt))
                                {
                                    Console.WriteLine("Please enter a prompt.");
                                }
                                else
                                {
                                    Console.WriteLine("Getting a response to your prompt...");

                                    // Get a response to audio input


                                }
                                break;
                            default:
                                Console.WriteLine("Please enter a valid value");
                                break;
                        }
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

