---
title: Develop generative AI solutions in Azure
permalink: index.html
layout: home
---

<button id="theme-toggle" aria-label="Toggle dark mode">🌓</button>
<link rel="stylesheet" href="{{ '/assets/css/theme.css' | relative_url }}">
<script src="{{ '/assets/js/theme.js' | relative_url }}"></script>

The following exercises are designed to provide you with a hands-on learning experience in which you'll explore common tasks that developers do when building generative AI solutions on Microsoft Azure.

> **Note**: To complete the exercises, you'll need an Azure subscription in which you have sufficient permissions and quota to provision the necessary Azure resources and generative AI models. If you don't already have one, you can sign up for an [Azure account](https://azure.microsoft.com/free). There's a free trial option for new users that includes credits for the first 30 days.

## Exercises

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions'" %}
{% for activity in labs  %}
<hr>
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

{% endfor %}

> **Note**: While you can complete these exercises on their own, they're designed to complement modules on [Microsoft Learn](https://learn.microsoft.com/training/paths/create-custom-copilots-ai-studio/); in which you'll find a deeper dive into some of the underlying concepts on which these exercises are based.
