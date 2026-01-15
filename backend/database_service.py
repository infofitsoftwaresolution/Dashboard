"""
PostgreSQL Database Service
Connects to RDS PostgreSQL and provides data access methods
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class DatabaseService:
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.table_name = os.getenv('TABLE_NAME', 'audittrail_firehose')
        
        # Validate required environment variables
        if not all([self.db_host, self.db_name, self.db_user, self.db_password]):
            raise ValueError(
                "Missing required database environment variables. "
                "Please set DB_HOST, DB_NAME, DB_USER, and DB_PASSWORD in your .env file. "
                "See env.example for reference."
            )
    
    def get_connection(self):
        """Create and return a PostgreSQL database connection"""
        return psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
    
    def get_all_data(self, limit: Optional[int] = None, 
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None,
                    status: Optional[str] = None,
                    user_id: Optional[str] = None) -> List[Dict]:
        """Get all data from audit_trail_data table"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = f"SELECT * FROM {self.table_name} WHERE 1=1"
            params = []
            
            if start_date:
                query += f" AND audit_datetime >= %s"
                params.append(start_date)
            if end_date:
                query += f" AND audit_datetime <= %s"
                params.append(end_date)
            if status:
                query += f" AND status = %s"
                params.append(status)
            if user_id:
                query += f" AND user_id = %s"
                params.append(user_id)
            
            query += " ORDER BY audit_datetime DESC"
            
            if limit:
                query += f" LIMIT %s"
                params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error getting data: {e}")
            return []
    
    def get_count(self) -> int:
        """Get total count of records"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting count: {e}")
            return 0
    
    def get_metrics(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> List[Dict]:
        """Get dashboard metrics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = f"""
                SELECT 
                    COUNT(*) as total_visits,
                    COUNT(DISTINCT patient_id) as unique_patients,
                    COUNT(DISTINCT user_id) as unique_users,
                    SUM(CASE WHEN status = 'completed' OR status = 'FINALIZED' THEN 1 ELSE 0 END) as completed_notes,
                    AVG(CAST(audio_duration AS FLOAT)) as avg_duration
                FROM {self.table_name}
                WHERE 1=1
            """
            params = []
            
            if start_date:
                query += " AND audit_datetime >= %s"
                params.append(start_date)
            if end_date:
                query += " AND audit_datetime <= %s"
                params.append(end_date)
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return [dict(result)]
            return []
        except Exception as e:
            print(f"Error getting metrics: {e}")
            return []
    
    def get_recent_data(self, limit: int = 100) -> List[Dict]:
        """Get recent data"""
        return self.get_all_data(limit=limit)

