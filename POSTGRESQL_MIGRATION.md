# PostgreSQL Migration Guide

## Database Migration from SQLite to PostgreSQL

The application has been migrated from SQLite to PostgreSQL for better production reliability and scalability.

### Prerequisites

1. **Install PostgreSQL dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Option 1: Local PostgreSQL Setup

1. **Install PostgreSQL:**
   - Windows: Download from https://www.postgresql.org/download/windows/
   - Mac: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql postgresql-contrib`

2. **Create Database:**
   ```sql
   createdb sql_learning
   ```

3. **Update Environment Variables:**
   Edit `backend/.env`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/sql_learning
   ```

### Option 2: Supabase (Recommended for Production)

1. **Create Supabase Account:**
   - Go to https://supabase.com
   - Create new project
   - Note down your database URL

2. **Get Connection String:**
   - Go to Settings > Database
   - Copy the connection string
   - Replace `[YOUR-PASSWORD]` with your actual password

3. **Update Environment Variables:**
   Edit `backend/.env`:
   ```
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

### Option 3: Other Cloud PostgreSQL Providers

**Neon (Free Tier):**
- Website: https://neon.tech
- Offers generous free tier with serverless PostgreSQL

**Railway:**
- Website: https://railway.app
- Simple PostgreSQL deployment

**ElephantSQL:**
- Website: https://www.elephantsql.com
- Managed PostgreSQL service

### Database Schema Initialization

The application will automatically create all necessary tables on first run using the PostgreSQL schema in `database_postgresql.sql`.

### Key Changes Made

1. **Database Connection:**
   - Replaced SQLite with asyncpg for PostgreSQL
   - Added connection pooling with SQLAlchemy
   - Asynchronous database operations with sync wrappers

2. **Schema Conversion:**
   - `INTEGER PRIMARY KEY AUTOINCREMENT` → `SERIAL PRIMARY KEY`
   - `REAL` → `DECIMAL`
   - Added proper foreign key constraints
   - Added performance indexes

3. **Query Compatibility:**
   - Updated parameter placeholders from `?` to `$1, $2, etc.`
   - Modified INSERT queries to use `RETURNING id`
   - Added proper error handling

### Testing the Migration

1. **Start the Application:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Verify Database Connection:**
   - Check logs for "Database initialized successfully!"
   - Test API endpoints at http://localhost:8000/docs

3. **Test Analytics Storage:**
   - Try practice questions and check if progress is saved
   - Visit analytics page to verify data persistence

### Troubleshooting

**Connection Issues:**
- Verify DATABASE_URL format
- Check firewall settings
- Ensure PostgreSQL service is running

**Permission Issues:**
- Verify user has CREATE/INSERT/UPDATE permissions
- Check database exists and is accessible

**Migration Errors:**
- Check PostgreSQL version compatibility (9.6+)
- Verify all dependencies are installed
- Review logs for specific error messages

### Benefits of PostgreSQL Migration

1. **Production Reliability:** No more readonly database errors
2. **Scalability:** Better handling of concurrent users
3. **Data Integrity:** Proper foreign key constraints
4. **Performance:** Optimized indexes and query planning
5. **Features:** Full-text search, JSON operations, advanced analytics

### Rollback Plan

If needed, you can temporarily rollback to SQLite by:
1. Changing DATABASE_URL to SQLite format in `.env`
2. Reverting database.py imports to original SQLite functions
3. Using the original `database_simple.sql` schema

However, PostgreSQL is strongly recommended for production use.