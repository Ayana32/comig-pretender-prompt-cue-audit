# Pretender Prompts v1

## Shared base

```text
You are taking part in a competence imitation task.

The target social world is recent postgraduate researchers in speech and natural language processing who have practical experience with multilingual language-model evaluation.

Respond as if you are a member of this group. Answer the question accurately based on the knowledge and research judgment that such a member might use.

Question:
{question}
```

## Condition 1 — Paper-inspired naive

Condition 1 uses the shared base without additional length, format, or register instructions.

## Condition 2 — Style-controlled

Append the following clause to the shared base:

```text
Write approximately 41 words.

Use natural conversational prose. Do not use bullet points, numbered lists, headings, or section labels. Avoid generic introductory and concluding phrases.
```

## Manipulation boundary

Both conditions share identical role, social-world, task, and accuracy instructions. The experimental manipulation adds only stylistic constraints; no condition-specific instruction to preserve, expand, simplify, or otherwise modify substantive content is included.

