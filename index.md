---
title: Azure OpenAI Exercises
permalink: index.html
layout: home
---

# Develop generative AI solutions

The following quickstart exercises are designed to provide you with a hands-on learning experience in which you'll explore the common *jobs to be done* by developers building generative AI solutions like chat-bots and other natural language capable applications on Microsoft Azure.

> **Note**: To complete the exercises, you'll need an Azure subscription in which you have sufficient permissions and quota to provision the necessary Azure resources and generative AI models. If you don't already have one, you can sign up for an [Azure account](https://azure.microsoft.com/free). There's a free trial option for new users that includes credits for the first 30 days.

## Quickstart exercises

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions'" %}
{% for activity in labs  %}
[{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})
activity.lab.description
{% endfor %}

> **Note: While you can complete these exercises on their own, they're designed to complement modules on [Microsoft Learn](https://learn.microsoft.com/training/paths/create-custom-copilots-ai-studio/); in which you'll find a deeper dive into some of the underlying concepts on which these exercises are based.
