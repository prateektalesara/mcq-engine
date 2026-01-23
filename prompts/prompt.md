Act as a quiz generator. I need a JSON file compatible with a specific MCQ engine schema. 

Please generate a JSON object for a quiz about: [INSERT TOPIC HERE].

The JSON must follow this exact schema structure:

{
  "id": "unique-id-string",
  "title": "Title of the Quiz",
  "description": "Short description of the quiz content.",
  "durationMinutes": 10,
  "questions": [
    {
      "id": 1,
      "text": "Question text here?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correctIndices": [0], 
      "hint": "A short hint for the user.",
      "explanation": "Detailed explanation of why the answer is correct."
    }
  ]
}

**Strict Rules:**
1. "correctIndices" must be an array of integers (0-based index).
2. If there are multiple correct answers, include all indices (e.g., [0, 2]).
3. "durationMinutes" should be an integer representing the estimated time to complete.
4. "id" should be kebab-case (e.g., "python-basics-01").
5. Provide at least 5 questions.
6. Return ONLY the raw JSON code, inside a code block.