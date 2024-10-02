---
title: Azure OpenAI Exercises
permalink: index.html
layout: home
---

# Develop Generative AI applications with Azure AI Studio

The following exercises are designed to provide you with a hands-on learning experience in which you'll explore common patterns and techniques that developers use to build generative AI applications like chat-based "copilots", and learn how to implement those patterns using Azure AI Services - in particular, Azure OpenAI Service and Azure AI Studio.

While you can complete these exercises on their own, they're designed to complement modules on [Microsoft Learn](https://learn.microsoft.com/training/paths/create-custom-copilots-ai-studio/); in which you'll find a deeper dive into some of the underlying concepts on which these exercises are based.

> **Note**: To complete the exercises, you'll need an Azure subscription in which you have sufficient permissions and quota to provision the Azure resources used by Azure AI Studio and to deploy and use Azure OpenAI GPT models. If you don't already have one, you can sign up for an [Azure account](https://azure.microsoft.com/free). There's a free trial option for new users that includes credits for the first 30 days.

## Exercises

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions'" %}
{% for activity in labs  %}
- [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})
{% endfor %}