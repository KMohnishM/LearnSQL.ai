# Vercel Environment Variables Setup Guide

## Required Environment Variables for Production Deployment

Add these environment variables in your Vercel dashboard:
1. Go to https://vercel.com/dashboard
2. Select your project: learn-sql-ai
3. Go to Settings > Environment Variables
4. Add each variable below:

### Database Configuration
```
DATABASE_URL=postgresql://postgres.ludrzlpwmrcrslbpakah:Kmohnishm%401018@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
```

### LLM API Configuration  
```
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=meta-llama/llama-3.3-8b-instruct:free
GEMINI_API_KEY=AIzaSyDsPJn0wDRGuZCJgsNd9u5qJCx3zvkaN9o
```

### Environment
```
ENVIRONMENT=production
PYTHONPATH=backend
```

## Alternative: Use Vercel CLI to set environment variables

```bash
# Set database URL
vercel env add DATABASE_URL

# Set OpenRouter API key
vercel env add OPENROUTER_API_KEY

# Set OpenRouter model
vercel env add OPENROUTER_MODEL

# Set Gemini API key  
vercel env add GEMINI_API_KEY

# Set environment
vercel env add ENVIRONMENT
```

## After setting environment variables:
1. Redeploy: `vercel --prod`
2. Check logs: `vercel logs`
3. Test API: Visit your production URL + `/api/health`