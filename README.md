# Civic Chatbot

## Vercel Deployment Instructions

1. Make sure you have a Vercel account and the Vercel CLI installed.
2. This project uses Flask and is configured for Vercel's Python runtime.
3. The entry point is `app.py` and dependencies are listed in `requirements.txt`.
4. The `vercel.json` file is set up to route all requests to the Flask app.

### Steps:
- Run `vercel login` to log in to your Vercel account.
- Run `vercel` in the project root to deploy.

### Notes & Potential Errors:
- Vercel's Python runtime is designed for serverless functions and may not support all Flask features (e.g., sessions, file uploads, or long-lived processes).
- If you use Flask sessions, ensure the secret key is set via environment variables for production.
- File system writes (e.g., updating faqs.json) may not persist between requests on Vercel. For persistent storage, use an external database or storage service.
- If you see errors about missing modules, check `requirements.txt`.
- If you see errors about unsupported features, consider deploying to a traditional server or use Vercel's recommended frameworks (like Next.js for frontend).

For more, see [Vercel Python docs](https://vercel.com/docs/runtimes#official-runtimes/python).