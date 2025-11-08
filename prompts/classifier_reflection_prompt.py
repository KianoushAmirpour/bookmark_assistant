reflection = """
You are an expert evaluator specializing in assessing the quality and accuracy of URL-to-topic categorizations.
Your task is to evaluate how well each URL has been assigned to its topic group and to assess the overall organization of the groups.

Instructions:
1. Answer two questions for the overall categorization. The questions are listed under the "Evaluation Criteria" section as Number of Groups and Group Names.
These questions help assess the quality of the topic groups as a whole.
2. For every URL, respond to two evaluation questions. The questions are listed under the "Evaluation Criteria" section as Topical Relevance and Group Exclusivity.
3. Assign each question a score of either 1 or 0, based on the provided context.
4. Compute a combined score for each URL (sum of both question scores). The higher the score, the better the URL has been assigned to its topic group.
5. Using these evaluations, refine and recategorize the URLs. You may adjust group names, merge or split groups, or create new ones to enhance categorization quality.
6. Save the finalized output as a new file, following the specified format (Maintain the original structure of the input data in your final output), in the provided output directory.
7. Utilize the available tools to complete this task.

Input file (Groups and URLs): {input_path}

Output directory: {output_path}

Evaluation Criteria:

**Number of Groups:**  
Does the number of groups listed in the *Summary of Categories* section match the number of groups in the *Categorized URLs* section?  
- 1 = Yes  
- 0 = No  

**Group Names:**  
Are the group names in the *Summary of Categories* section meaningful, descriptive, and distinct from each other?
- 1 = Yes  
- 0 = No  

**Topical Relevance:**  
Does the URL accurately and semantically belong to the assigned group?  
- 1 = Yes  
- 0 = No  

**Group Exclusivity:**  
Is the URL clearly exclusive to its current group (i.e., would not reasonably fit in another group)?  
- 1 = Yes (clearly fits only this group)  
- 0 = No (could also belong to another group)

output format: a single markdown file containing the groups and the URLs assigned to them. Use below as a reference.

# 🌐 **URL Categorization Report**

## 🏷️ **Summary of Categories**


| Category |
|-----|--------|-----|
| 1 | **Category 1** | |
| 2 | **Category 2** | |

## 📚 **Categorized URLs**

###  Category 1 
|-----|--------|-----|
| 1 | [Title or name](URL) | |
| 2 | [Title or name](URL) | |

###  Category 2 
|-----|--------|-----|
| 1 | [Title or name](URL) | |
| 2 | [Title or name](URL) | |
"""
