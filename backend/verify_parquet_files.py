"""
Script to verify Parquet files in S3
"""
import os
from dotenv import load_dotenv
from athena_service import AthenaService

load_dotenv()

def main():
    print("\n" + "="*60)
    print("VERIFYING PARQUET FILES IN S3")
    print("="*60)
    
    try:
        athena = AthenaService()
        result = athena.verify_s3_files()
        
        if result.get('success'):
            print(f"\n✅ S3 Location: {result.get('s3_location', 'N/A')}")
            print(f"✅ Total Parquet Files: {result.get('file_count', 0)}")
            
            total_size_mb = result.get('total_size_bytes', 0) / (1024 * 1024)
            print(f"✅ Total Size: {total_size_mb:.2f} MB")
            
            files = result.get('files', [])
            if files:
                print(f"\n📁 Parquet Files Found:")
                print("-" * 60)
                for i, file_info in enumerate(files, 1):
                    size_kb = file_info['size'] / 1024
                    print(f"{i}. {file_info['key']}")
                    print(f"   Size: {size_kb:.2f} KB")
                    print(f"   Modified: {file_info['last_modified']}")
                    print()
            else:
                print("\n⚠️  No Parquet files found in S3 location!")
                print(f"   Check: {result.get('s3_location', 'N/A')}")
            
            # Also get record count from Athena
            print("\n" + "="*60)
            print("CHECKING ATHENA TABLE")
            print("="*60)
            try:
                stats = athena.get_data_statistics()
                total_records = stats.get('total_records', 0)
                unique_users = stats.get('unique_users', 0)
                unique_patients = stats.get('unique_patients', 0)
                unique_tenants = stats.get('unique_tenants', 0)
                
                # Format numbers safely
                def format_num(n):
                    try:
                        return f"{int(n):,}" if isinstance(n, (int, float)) else str(n)
                    except:
                        return str(n)
                
                print(f"\n✅ Total Records in Table: {format_num(total_records)}")
                print(f"✅ Unique Users: {format_num(unique_users)}")
                print(f"✅ Unique Patients: {format_num(unique_patients)}")
                print(f"✅ Unique Tenants: {format_num(unique_tenants)}")
                
                if stats.get('date_range'):
                    print(f"\n📅 Date Range:")
                    print(f"   Earliest: {stats['date_range'].get('min_date', 'N/A')}")
                    print(f"   Latest: {stats['date_range'].get('max_date', 'N/A')}")
            except Exception as e:
                print(f"\n⚠️  Error getting table statistics: {e}")
            
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            print(f"   S3 Location: {result.get('s3_location', 'N/A')}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

