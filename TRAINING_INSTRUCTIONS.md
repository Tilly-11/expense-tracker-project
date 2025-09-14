# Using the AI Model

The AI-powered expense tracker uses a pre-trained zero-shot classification model that doesn't require training. This approach provides immediate, accurate categorization without the need for user-specific model training.

## How the AI Works

1. **Pre-trained Model**: The system uses the `facebook/bart-large-mnli` model, which is pre-trained on a large corpus of text and can classify new text into any categories without prior training.

2. **Zero-Shot Classification**: When you create an expense without specifying a category, the AI analyzes the description and classifies it into one of the default categories:
   - Food & Drink
   - Groceries
   - Transport
   - Entertainment
   - Utilities
   - Rent
   - Healthcare
   - Shopping
   - Other

3. **Confidence Scoring**: Each prediction comes with a confidence score between 0 and 1. If the confidence is below 0.7, the category is marked as "Uncertain".

4. **Fallback Mechanism**: If the AI model fails for any reason, a rule-based fallback system categorizes the expense based on keywords in the description.

## Manual Override

Even though the model doesn't require training, you can still override any AI prediction:

```bash
curl -X POST http://127.0.0.1:8000/api/expenses/{expense_id}/override/ \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer {your_access_token}" \\
     -d '{"category": "Correct Category Name"}'
```

Replace `{expense_id}` with the actual ID of the expense and `{your_access_token}` with your JWT access token.

## Benefits of This Approach

1. **No Training Required**: The model works immediately without any training period.
2. **Consistent Performance**: All users benefit from the same high-quality pre-trained model.
3. **Lower Maintenance**: No need to maintain user-specific models or handle model updates.
4. **Better Accuracy**: Pre-trained models are typically more robust than custom-trained models on limited data.
5. **Lighter Storage**: No model files need to be stored or managed.

## When to Override Predictions

You should override predictions when:
1. The AI categorizes an expense incorrectly
2. The AI marks an expense as "Uncertain" and you want to provide the correct category
3. You want to use a category that's not in the default list (though the model can still attempt to classify it)

## Monitoring AI Performance

You can monitor the AI's performance by:
1. Checking the `ai_confidence` value in expense responses
2. Noting how often you need to override predictions
3. Observing if the AI correctly categorizes new expenses without manual intervention

## Troubleshooting

If you notice issues with AI categorization:
1. Ensure your expense descriptions are clear and descriptive
2. Check that the AI confidence threshold (0.7) is appropriate for your needs
3. Report consistent misclassifications as potential improvements to the system

The pre-trained model approach provides a simpler, more reliable experience while maintaining high accuracy for expense categorization.