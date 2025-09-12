# Training the AI Model

The AI-powered expense tracker uses user-specific models that improve over time through your interactions. Here's how to effectively train the model for better categorization accuracy.

## How the AI Learning Works

1. **Initial State**: When you first start using the app, the AI uses a global model trained on general expense data.
2. **User-Specific Models**: As you use the app, a personalized model is created for your account.
3. **Learning from Feedback**: Every time you manually override an AI prediction, that feedback is used to improve your personal model.
4. **Confidence Threshold**: The AI will indicate when it's uncertain about a prediction (confidence < 70%), allowing you to provide corrections.

## Best Practices for Training

### 1. Provide Consistent Category Names
- Use consistent naming for your expense categories (e.g., always use "Groceries" instead of alternating between "Food" and "Groceries").
- Avoid creating too many similar categories (e.g., "Entertainment", "Fun", "Leisure" could all be consolidated).

### 2. Correct Uncertain Predictions Promptly
- When the AI returns "Uncertain" as the category, make sure to use the override endpoint to provide the correct category.
- The more examples you provide for uncertain predictions, the faster your personal model will improve.

### 3. Be Specific with Descriptions
- Use descriptive expense entries that clearly indicate the nature of the expense.
- Instead of "Bought stuff", use "Bought new shoes at Nike store".
- The more context in the description, the better the AI can learn patterns.

### 4. Override Incorrect Predictions
- Even if the AI prediction is wrong but not marked as "Uncertain", you should still override it.
- Every correction helps improve the model's accuracy.

### 5. Provide Examples for New Categories
- When you start using a new category that the AI hasn't seen before, provide several examples.
- For instance, if you're adding "Pet Expenses" for the first time, add a few different examples like "Dog food", "Vet visit", "Pet toys".

## Using the Override Endpoint

To train the model effectively, use the override endpoint whenever an expense is misclassified:

```bash
curl -X POST http://127.0.0.1:8000/api/expenses/{expense_id}/override/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer {your_access_token}" \
     -d '{"category": "Correct Category Name"}'
```

Replace `{expense_id}` with the actual ID of the expense and `{your_access_token}` with your JWT access token.

## Monitoring Model Performance

You can monitor how well your personal model is performing by:

1. Checking the `ai_confidence` value in expense responses.
2. Noting how often you need to override predictions.
3. Observing if the AI correctly categorizes new expenses without manual intervention.

## Tips for Optimal Results

1. **Be Patient**: The AI needs time to learn your patterns. Significant improvements are typically seen after 20-30 corrections.
2. **Regular Maintenance**: Periodically review your expenses to ensure categories are consistent.
3. **Handle Edge Cases**: Pay special attention to expenses that the AI consistently gets wrong and provide corrections for them.
4. **Seasonal Patterns**: The AI will learn seasonal spending patterns (e.g., holiday shopping, vacation expenses) over time.

## Troubleshooting

If you notice the AI isn't improving:
1. Check that you're consistently using the override endpoint for corrections.
2. Ensure you're providing clear, descriptive expense entries.
3. Verify that you're using consistent category names.
4. Make sure you have enough examples (at least 10-15 per category) for the AI to learn effectively.

With consistent feedback and clear expense descriptions, your personal AI model will become increasingly accurate at categorizing your expenses automatically.