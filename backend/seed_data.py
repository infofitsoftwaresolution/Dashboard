"""
Script to seed the database with initial data
"""
from database import (
    SessionLocal, init_db,
    Metric, TopUser, ActiveUser, StaffSpeaking, TimesData, ConsentsData,
    AuditItem, PatientAccessItem, ServiceUsageItem, RecommendationItem,
    DeliveryScheduleItem, SignedNoteItem, PractitionerUsageItem,
    SyncIssueItem, UnsignedNoteItem
)
from datetime import datetime, timedelta
import random

def seed_database():
    """Seed the database with initial data"""
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Metric).delete()
        db.query(TopUser).delete()
        db.query(ActiveUser).delete()
        db.query(StaffSpeaking).delete()
        db.query(TimesData).delete()
        db.query(ConsentsData).delete()
        db.query(AuditItem).delete()
        db.query(PatientAccessItem).delete()
        db.query(ServiceUsageItem).delete()
        db.query(RecommendationItem).delete()
        db.query(DeliveryScheduleItem).delete()
        db.query(SignedNoteItem).delete()
        db.query(PractitionerUsageItem).delete()
        db.query(SyncIssueItem).delete()
        db.query(UnsignedNoteItem).delete()
        
        # Seed Metrics
        metrics = [
            Metric(label="Visits", value="80", change=300.0, trend="up"),
            Metric(label="Notes from Scribe", value="13", change=160.0, trend="up"),
            Metric(label="Notes without Scribe", value="8", change=700.0, trend="up"),
            Metric(label="Note Content from Scribe", value="0.0", change=-10.2, trend="down"),
            Metric(label="Total Time", value="5 hr 9 min", change=618.6, trend="up")
        ]
        db.add_all(metrics)
        
        # Seed Top Users
        top_users = [
            TopUser(name="PA PAUL ALLWIN", visits=2, total_time=""),
            TopUser(name="DR JANE SMITH", visits=5, total_time="2 hr 15 min"),
            TopUser(name="DR JOHN DOE", visits=3, total_time="1 hr 30 min"),
            TopUser(name="DR SARAH JOHNSON", visits=4, total_time="1 hr 45 min"),
            TopUser(name="DR MICHAEL BROWN", visits=3, total_time="1 hr 20 min"),
            TopUser(name="DR EMILY DAVIS", visits=2, total_time="45 min"),
            TopUser(name="DR ROBERT WILSON", visits=4, total_time="2 hr 5 min"),
            TopUser(name="DR LISA ANDERSON", visits=3, total_time="1 hr 10 min")
        ]
        db.add_all(top_users)
        
        # Seed Active Users
        enabled = random.randint(150, 200)
        active = random.randint(int(enabled * 0.6), int(enabled * 0.85))
        db.add(ActiveUser(active=active, enabled=enabled))
        
        # Seed Staff Speaking
        non_staff = random.randint(65, 85)
        staff = random.randint(15, 35)
        db.add(StaffSpeaking(staff=staff, non_staff=non_staff))
        
        # Seed Times Data - One year of monthly data
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        base_recording = 2.0
        base_processing = 3.0
        base_created = 5.0
        for i, month in enumerate(month_names):
            # Create variation that trends slightly upward over the year
            variation = (i - 6) * 0.2
            db.add(TimesData(
                month=month,
                recording=round(max(1.0, base_recording + variation + random.uniform(-0.5, 0.5)), 1),
                processing=round(max(2.0, base_processing + variation + random.uniform(-0.5, 0.5)), 1),
                created_to_sign=round(max(3.0, base_created + variation + random.uniform(-0.8, 0.8)), 1)
            ))
        
        # Seed Consents
        listening = random.randint(82, 92)
        dictation = random.randint(8, 18)
        db.add(ConsentsData(listening=listening, dictation=dictation))
        
        # Seed Audit Items - One year of data with distinct practitioner patterns
        actions = ["Login", "Data Access", "Note Creation", "Note Modification", "Report Generation", "Settings Change"]
        users = ["DR JANE SMITH", "DR JOHN DOE", "PA PAUL ALLWIN", "DR SARAH JOHNSON", "ADMIN USER"]
        practitioners = ["DR JANE SMITH", "DR JOHN DOE", "DR SARAH JOHNSON", "DR MICHAEL BROWN", "DR EMILY DAVIS"]
        practitioner_profiles_audit = {
            "DR JANE SMITH": {"programs": ["Cardiology", "Primary Care"], "locations": ["Main Clinic", "Downtown Office"], "activity": 4},
            "DR JOHN DOE": {"programs": ["Pediatrics", "Primary Care"], "locations": ["North Branch", "Main Clinic"], "activity": 3},
            "DR SARAH JOHNSON": {"programs": ["Orthopedics", "Neurology"], "locations": ["South Branch", "Emergency Dept"], "activity": 5},
            "DR MICHAEL BROWN": {"programs": ["Dermatology", "Primary Care"], "locations": ["Downtown Office", "North Branch"], "activity": 2},
            "DR EMILY DAVIS": {"programs": ["Neurology", "Cardiology"], "locations": ["Main Clinic", "Emergency Dept"], "activity": 3}
        }
        statuses = ["Success", "Failed", "Warning"]
        base_date = datetime.now()
        # Generate data for the past year
        for day in range(365):
            date = base_date - timedelta(days=day)
            # Each practitioner has different activity levels
            for practitioner, profile in practitioner_profiles_audit.items():
                entries_for_practitioner = random.randint(1, profile["activity"])
                for entry in range(entries_for_practitioner):
                    hour = random.randint(8, 18)  # Business hours
                    minute = random.randint(0, 59)
                    entry_date = date.replace(hour=hour, minute=minute)
                    db.add(AuditItem(
                        date=entry_date.strftime("%Y-%m-%d %H:%M"),
                        action=random.choice(actions),
                        user=practitioner,
                        practitioner=practitioner,
                        program=random.choice(profile["programs"]) if random.random() > 0.2 else None,
                        location=random.choice(profile["locations"]) if random.random() > 0.2 else None,
                        status=random.choice(statuses),
                        details=f"Action performed on {entry_date.strftime('%Y-%m-%d')}"
                    ))
        
        # Seed Patient Access - One year of data with distinct practitioner patterns
        patient_access_profiles = {
            "DR JANE SMITH": {"programs": ["Cardiology", "Primary Care"], "locations": ["Main Clinic", "Downtown Office"], "patients": ["John Smith", "Mary Johnson", "Robert Williams"], "daily_access": (4, 10)},
            "DR JOHN DOE": {"programs": ["Pediatrics", "Primary Care"], "locations": ["North Branch", "Main Clinic"], "patients": ["Michael Brown", "Sarah Wilson", "David Lee"], "daily_access": (3, 7)},
            "DR SARAH JOHNSON": {"programs": ["Orthopedics", "Neurology"], "locations": ["South Branch", "Emergency Dept"], "patients": ["Christopher Brown", "Amanda Taylor", "James Anderson"], "daily_access": (5, 12)},
            "DR MICHAEL BROWN": {"programs": ["Dermatology", "Primary Care"], "locations": ["Downtown Office", "North Branch"], "patients": ["Lisa Martinez", "Emily Davis", "David Lee"], "daily_access": (2, 6)},
            "DR EMILY DAVIS": {"programs": ["Neurology", "Cardiology"], "locations": ["Main Clinic", "Emergency Dept"], "patients": ["Sarah Wilson", "Robert Williams", "Amanda Taylor"], "daily_access": (3, 8)}
        }
        access_types = ["Portal Login", "Record View", "Appointment Schedule", "Message Access"]
        patient_counter = 1000
        # Generate data for the past year
        for day in range(365):
            date = base_date - timedelta(days=day)
            # Each practitioner has different patient access patterns
            for practitioner, profile in patient_access_profiles.items():
                events_for_practitioner = random.randint(*profile["daily_access"])
                for event in range(events_for_practitioner):
                    hour = random.randint(6, 22)  # Extended hours
                    minute = random.randint(0, 59)
                    event_date = date.replace(hour=hour, minute=minute)
                    db.add(PatientAccessItem(
                        patient_id=f"PAT{patient_counter}",
                        patient_name=random.choice(profile["patients"]),
                        practitioner=practitioner,
                        program=random.choice(profile["programs"]) if random.random() > 0.1 else None,
                        location=random.choice(profile["locations"]) if random.random() > 0.1 else None,
                        access_date=event_date.strftime("%Y-%m-%d %H:%M"),
                        access_type=random.choice(access_types),
                        duration=f"{random.randint(5, 45)} min"
                    ))
                    patient_counter += 1
        
        # Seed Service Usage
        services = ["Virtual Scribe", "Telemedicine", "Patient Portal", "Messaging", "Appointment Booking"]
        for service in services:
            db.add(ServiceUsageItem(
                service_name=service,
                usage_count=random.randint(50, 500),
                total_time=f"{random.randint(10, 100)} hours",
                last_used=(base_date - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
            ))
        
        # Seed Recommendations - One year of data
        types = ["Clinical", "Administrative", "Quality", "Compliance"]
        priorities = ["High", "Medium", "Low"]
        rec_statuses = ["Pending", "In Progress", "Completed", "Dismissed"]
        rec_counter = 2000
        # Generate data for the past year (2-4 recommendations per week)
        for week in range(52):
            week_start = base_date - timedelta(weeks=week)
            recommendations_per_week = random.randint(2, 4)
            for rec in range(recommendations_per_week):
                day_offset = random.randint(0, 6)
                date = week_start - timedelta(days=day_offset)
                db.add(RecommendationItem(
                    rec_id=f"REC{rec_counter}",
                    type=random.choice(types),
                    priority=random.choice(priorities),
                    status=random.choice(rec_statuses),
                    created_date=date.strftime("%Y-%m-%d")
                ))
                rec_counter += 1
        
        # Seed Delivery Schedules
        reports = ["Daily Summary", "Weekly Report", "Monthly Analytics", "Audit Report", "Usage Report"]
        frequencies = ["Daily", "Weekly", "Monthly", "Quarterly"]
        schedule_statuses = ["Active", "Paused", "Completed"]
        for report in reports:
            next_delivery = base_date + timedelta(days=random.randint(1, 7))
            db.add(DeliveryScheduleItem(
                report_name=report,
                frequency=random.choice(frequencies),
                next_delivery=next_delivery.strftime("%Y-%m-%d %H:%M"),
                status=random.choice(schedule_statuses)
            ))
        
        # Seed Signed Notes - One year of data with distinct practitioner data
        # Assign specific programs and locations to each practitioner for distinct data
        practitioner_profiles = {
            "DR JANE SMITH": {
                "programs": ["Cardiology", "Primary Care"],
                "locations": ["Main Clinic", "Downtown Office"],
                "patients": ["John Smith", "Mary Johnson", "Robert Williams", "Emily Davis"],
                "daily_notes_range": (8, 18),  # Busier practitioner
                "status_preference": {"Signed": 0.7, "Pending Review": 0.2, "Archived": 0.1}
            },
            "DR JOHN DOE": {
                "programs": ["Pediatrics", "Primary Care"],
                "locations": ["North Branch", "Main Clinic"],
                "patients": ["Michael Brown", "Sarah Wilson", "David Lee", "Jennifer White"],
                "daily_notes_range": (5, 12),  # Moderate
                "status_preference": {"Signed": 0.6, "Pending Review": 0.3, "Archived": 0.1}
            },
            "DR SARAH JOHNSON": {
                "programs": ["Orthopedics", "Neurology"],
                "locations": ["South Branch", "Emergency Dept"],
                "patients": ["Christopher Brown", "Amanda Taylor", "James Anderson"],
                "daily_notes_range": (10, 20),  # Very busy
                "status_preference": {"Signed": 0.8, "Pending Review": 0.15, "Archived": 0.05}
            },
            "DR MICHAEL BROWN": {
                "programs": ["Dermatology", "Primary Care"],
                "locations": ["Downtown Office", "North Branch"],
                "patients": ["Lisa Martinez", "John Smith", "Emily Davis", "David Lee"],
                "daily_notes_range": (4, 10),  # Less busy
                "status_preference": {"Signed": 0.5, "Pending Review": 0.35, "Archived": 0.15}
            },
            "DR EMILY DAVIS": {
                "programs": ["Neurology", "Cardiology"],
                "locations": ["Main Clinic", "Emergency Dept"],
                "patients": ["Sarah Wilson", "Robert Williams", "Amanda Taylor", "Jennifer White"],
                "daily_notes_range": (6, 14),  # Moderate
                "status_preference": {"Signed": 0.65, "Pending Review": 0.25, "Archived": 0.1}
            }
        }
        
        note_counter = 3000
        # Generate data for the past year with distinct practitioner patterns
        for day in range(365):
            date = base_date - timedelta(days=day)
            # Each practitioner gets their own data pattern
            for practitioner, profile in practitioner_profiles.items():
                notes_for_practitioner = random.randint(*profile["daily_notes_range"])
                for note in range(notes_for_practitioner):
                    # Use weighted random for status based on practitioner preference
                    rand_val = random.random()
                    cumulative = 0
                    status = "Signed"
                    for stat, prob in profile["status_preference"].items():
                        cumulative += prob
                        if rand_val <= cumulative:
                            status = stat
                            break
                    
                    db.add(SignedNoteItem(
                        note_id=f"NOTE{note_counter}",
                        patient_name=random.choice(profile["patients"]),
                        practitioner=practitioner,
                        program=random.choice(profile["programs"]) if random.random() > 0.05 else None,
                        location=random.choice(profile["locations"]) if random.random() > 0.05 else None,
                        signed_date=date.strftime("%Y-%m-%d"),
                        status=status
                    ))
                    note_counter += 1
        
        # Seed Practitioner Usage with distinct data for each practitioner
        practitioner_usage_data = {
            "DR JANE SMITH": {"visits": 185, "hours": 42, "program": "Cardiology", "location": "Main Clinic"},
            "DR JOHN DOE": {"visits": 142, "hours": 28, "program": "Pediatrics", "location": "North Branch"},
            "DR SARAH JOHNSON": {"visits": 210, "hours": 48, "program": "Orthopedics", "location": "South Branch"},
            "DR MICHAEL BROWN": {"visits": 98, "hours": 18, "program": "Dermatology", "location": "Downtown Office"},
            "DR EMILY DAVIS": {"visits": 165, "hours": 35, "program": "Neurology", "location": "Main Clinic"},
            "DR ROBERT WILSON": {"visits": 120, "hours": 25, "program": "Primary Care", "location": "North Branch"}
        }
        
        for practitioner, data in practitioner_usage_data.items():
            db.add(PractitionerUsageItem(
                practitioner_name=practitioner,
                program=data["program"],
                location=data["location"],
                visits=data["visits"],
                total_time=f"{data['hours']} hours",
                last_active=(base_date - timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d")
            ))
        
        # Seed Sync Issues - One year of data
        sync_types = ["Data Sync", "File Upload", "API Connection", "Database Sync", "Authentication"]
        severities = ["Critical", "High", "Medium", "Low"]
        sync_statuses = ["Open", "In Progress", "Resolved", "Closed"]
        sync_counter = 4000
        # Generate data for the past year (1-3 issues per week)
        for week in range(52):
            week_start = base_date - timedelta(weeks=week)
            issues_per_week = random.randint(1, 3)
            for issue in range(issues_per_week):
                day_offset = random.randint(0, 6)
                hour = random.randint(8, 20)
                minute = random.randint(0, 59)
                date = (week_start - timedelta(days=day_offset)).replace(hour=hour, minute=minute)
                db.add(SyncIssueItem(
                    issue_id=f"SYNC{sync_counter}",
                    type=random.choice(sync_types),
                    severity=random.choice(severities),
                    status=random.choice(sync_statuses),
                    reported_date=date.strftime("%Y-%m-%d %H:%M")
                ))
                sync_counter += 1
        
        # Seed Unsigned Notes - One year of data with distinct practitioner patterns
        unsigned_note_counter = 5000
        # Use the same practitioner profiles for consistency
        for day in range(365):
            date = base_date - timedelta(days=day)
            days_pending = (base_date - date).days
            if days_pending > 0:  # Only create notes that are actually pending
                # Each practitioner has different unsigned note patterns
                for practitioner, profile in practitioner_profiles.items():
                    # Some practitioners have more unsigned notes than others
                    unsigned_range_map = {
                        "DR JANE SMITH": (1, 4),  # Fewer unsigned
                        "DR JOHN DOE": (2, 5),     # Moderate
                        "DR SARAH JOHNSON": (3, 7), # More unsigned (busy)
                        "DR MICHAEL BROWN": (1, 3), # Fewer
                        "DR EMILY DAVIS": (2, 4)    # Moderate
                    }
                    unsigned_count = random.randint(*unsigned_range_map[practitioner])
                    for note in range(unsigned_count):
                        db.add(UnsignedNoteItem(
                            note_id=f"NOTE{unsigned_note_counter}",
                            patient_name=random.choice(profile["patients"]),
                            practitioner=practitioner,
                            program=random.choice(profile["programs"]) if random.random() > 0.05 else None,
                            location=random.choice(profile["locations"]) if random.random() > 0.05 else None,
                            created_date=date.strftime("%Y-%m-%d"),
                            days_pending=days_pending
                        ))
                        unsigned_note_counter += 1
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

