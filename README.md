## AI Agents for Managing Chrome Bookmarks
This repository explores using AI agents to enhance the management of Chrome bookmarks.  
It contains two main agent workflows—**one for classification and one for recency ranking**—along with supporting utilities, evaluation data, and a reflection-based improvement loop.  

## Overview
This project implements AI agents designed to:  
* Classify bookmark URLs into meaningful groups with descriptive category names.  
* Rank bookmarks based on when they were added, enabling recency-based organization.  

## Utilities & Tools
* Converting WebKit timestamps to standard datetime formats.
* Sorting lists by key.
* Formatting timestamps into human-readable strings.
* Reading and writing JSON and Markdown files.

## Reflection Pattern
Both agents employ the reflection pattern, where the model receives feedback— **LLM-as-judge or from tools**.  
Classification Agent: Reflection via rubric-based grading. [prompt for reflection](https://github.com/KianoushAmirpour/bookmark_assistant/blob/main/prompts/classifier_reflection_prompt.py)   
Recency Agent: Reflection powered by external, tool-assisted feedback. 

## Evaluation
A dedicated evaluation dataset has been created to test the recency ranking agent.

## Tech stack
* pydantic-ai and logfire

## to do
* support for mac and linux
* prompt versioning
* add logging
* eval dataset for classifier agent



