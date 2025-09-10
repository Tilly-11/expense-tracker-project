# **Backend Engineering Assessment – AI-Powered Expense Tracker API**

<aside>
🎯 In this assessment, you are tasked with implementing an AI-powered expense tracking API using Django and any AI/ML framework of your choice.

The goal is to extend a standard expense tracker with **AI capabilities** that help users automatically classify and analyze their expenses.

</aside>

## **Requirements**

Your application should:

1. **Core Expense Tracking API**
    - Implement endpoints for adding, updating, deleting, and retrieving expenses (amount, description, category, date).
    - Follow RESTful design with proper request/response formats.
    - Include user authentication and error handling.
2. **AI-Powered Features**
    - **Expense Categorization:**
        
        You can make use of any pretrained model (Langchain, RAG, mcp etc)
        
        The user should be able to override AI’s prediction manually.
        
    - **Insights & Summaries:**
        
        Implement an endpoint that provides personalized insights such as:
        
        - Monthly/weekly spending summary
        - Top categories
        - AI-detected anomalies (e.g., unusual spending compared to historical patterns)
3. **Testing**
    - Write unit and integration tests for all endpoints, including AI endpoints.
    - Ensure deterministic tests even if using AI models (e.g., fix random seeds).
4. **Documentation**
    - Document your API using **Swagger/OpenAPI 3.0**.
    - Include details about AI endpoints (input, output, possible errors).

## **Evaluation Criteria**

Your submission will be evaluated on:

- **Completeness** – Have you implemented both the core tracker and AI-powered features?
- **Correctness** – Do endpoints and AI predictions work as expected?
- **Design** – Is your solution modular and scalable (e.g., AI pipeline can be swapped/upgraded)?
- **Documentation** – Is your Swagger/OpenAPI spec clear and aligned with the code?
- **Code Quality** – Is the code readable, well-structured, and follows best practices?

## **Submission**

Please submit:

- The code for your API implementation
- Model artifacts or scripts for training/loading AI models
- Instructions for running your code and setting up the AI features