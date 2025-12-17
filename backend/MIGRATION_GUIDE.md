# Database Migration Guide: SQLite to PostgreSQL (AWS RDS)

This guide will help you migrate all data from your local SQLite database to AWS RDS PostgreSQL.

## Prerequisites

1. **AWS RDS Database Credentials**
   - Database host: `database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com`
   - Username
   - Password
   - Database name (default: `postgres`)
   - Port (default: `5432`)

2. **Network Access**
   - Your IP address must be allowed in the RDS security group
   - Port 5432 must be open

3. **Python Dependencies**
   - All dependencies from `requirements.txt` must be installed
   - PostgreSQL driver (`psycopg2-binary`) will be installed automatically

## Step-by-Step Migration

### Step 1: Install Dependencies

Make sure you have the latest requirements installed:

```bash
cd backend
pip install -r requirements.txt
```

This will install `psycopg2-binary` and `python-dotenv` if not already installed.

### Step 2: Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` and add your PostgreSQL credentials:

**Option 1: Full Connection URL (Recommended)**
```env
POSTGRES_URL=postgresql://username:password@database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com:5432/database_name
```

**Option 2: Individual Components**
```env
POSTGRES_HOST=database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
USE_POSTGRES=true
```

### Step 3: Verify SQLite Database Exists

Make sure your SQLite database (`dashboard.db`) exists and has data:

```bash
# Check if database exists
ls -lh dashboard.db

# Or on Windows
dir dashboard.db
```

If the database doesn't exist, run the seed script first:

```bash
python seed_data.py
```

### Step 4: Run the Migration

Run the migration script:

```bash
python migrate_to_postgres.py
```

The script will:
1. ✅ Connect to both SQLite (source) and PostgreSQL (destination)
2. ✅ Create all necessary tables in PostgreSQL
3. ✅ Check for existing data and ask for confirmation if found
4. ✅ Migrate all data table by table
5. ✅ Show progress and summary

### Step 5: Verify Migration

After migration, verify the data:

```bash
# The script will show a summary, but you can also verify manually
# by connecting to PostgreSQL and running:
# SELECT COUNT(*) FROM signed_note_items;
```

### Step 6: Switch Application to PostgreSQL

After successful migration, update your `.env` file to use PostgreSQL:

```env
USE_POSTGRES=true
# OR set POSTGRES_URL directly
```

Restart your FastAPI server:

```bash
python main.py
```

The application will now use PostgreSQL instead of SQLite.

## Migration Script Features

- **Automatic Table Creation**: Creates all tables in PostgreSQL automatically
- **Batch Processing**: Migrates data in batches of 1000 records for efficiency
- **Data Safety**: Asks for confirmation before overwriting existing data
- **Progress Tracking**: Shows real-time progress for each table
- **Error Handling**: Handles errors gracefully and provides clear messages
- **Summary Report**: Shows total records migrated per table

## Troubleshooting

### Connection Errors

**Error: "Failed to connect to PostgreSQL"**

**Solutions:**
1. Verify your credentials are correct
2. Check that your IP is allowed in RDS security group
3. Verify the database exists and is accessible
4. Check network connectivity: `ping database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com`

### Authentication Errors

**Error: "password authentication failed"**

**Solutions:**
1. Double-check username and password
2. Ensure username has proper permissions
3. Check if password contains special characters (may need URL encoding)

### Table Already Exists

**Error: "relation already exists"**

**Solutions:**
- The script will detect existing data and ask for confirmation
- Choose "yes" to clear and re-migrate, or "no" to cancel

### Timeout Errors

**Error: "Connection timeout"**

**Solutions:**
1. Check your internet connection
2. Verify RDS instance is running
3. Check security group rules allow your IP
4. Try increasing connection timeout in the script

### Data Type Errors

**Error: "Invalid input syntax"**

**Solutions:**
- The migration script handles most data type conversions automatically
- If you encounter this, check the specific column and data value
- Some SQLite-specific types may need manual conversion

## What Gets Migrated

The following tables are migrated:

1. ✅ `metrics` - Dashboard metrics
2. ✅ `top_users` - Top users data
3. ✅ `active_users` - Active users count
4. ✅ `staff_speaking` - Staff speaking statistics
5. ✅ `times_data` - Time metrics by month
6. ✅ `consents_data` - Consent data
7. ✅ `audit_items` - Audit log entries
8. ✅ `patient_access_items` - Patient access records
9. ✅ `service_usage_items` - Service usage statistics
10. ✅ `recommendation_items` - Recommendation data
11. ✅ `delivery_schedule_items` - Delivery schedules
12. ✅ `signed_note_items` - Signed notes (typically largest table)
13. ✅ `practitioner_usage_items` - Practitioner usage statistics
14. ✅ `sync_issue_items` - Sync issues
15. ✅ `unsigned_note_items` - Unsigned notes

## Rollback

If you need to rollback to SQLite:

1. Update `.env`:
   ```env
   USE_POSTGRES=false
   # Or remove POSTGRES_URL
   ```

2. Restart the application

3. The application will automatically use SQLite again

## Performance Tips

- **Large Databases**: For databases with 100K+ records, the migration may take several minutes
- **Network Speed**: Migration speed depends on your connection to AWS
- **Batch Size**: The script uses batches of 1000 records - you can modify this in the script if needed

## Security Notes

⚠️ **Important Security Reminders:**

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use environment variables** in production instead of `.env` files
3. **Rotate passwords** regularly
4. **Use IAM database authentication** if possible for better security
5. **Restrict RDS security group** to only necessary IP addresses

## Support

If you encounter issues:

1. Check the error message carefully
2. Verify all prerequisites are met
3. Check AWS RDS console for database status
4. Review the troubleshooting section above
5. Check application logs for detailed error messages

## Next Steps After Migration

1. ✅ Test all API endpoints
2. ✅ Verify data appears correctly in the dashboard
3. ✅ Test filtering and search functionality
4. ✅ Monitor application performance
5. ✅ Set up database backups in AWS
6. ✅ Configure connection pooling if needed

---

**Migration Complete!** 🎉

Your data is now in PostgreSQL and ready for production use.

