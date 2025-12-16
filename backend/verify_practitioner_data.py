"""Verify that each practitioner has distinct data"""
from database import SessionLocal, SignedNoteItem, PractitionerUsageItem, PatientAccessItem, UnsignedNoteItem, AuditItem

db = SessionLocal()

print('\n=== Practitioner Data Distribution ===\n')

practitioners = ['DR JANE SMITH', 'DR JOHN DOE', 'DR SARAH JOHNSON', 'DR MICHAEL BROWN', 'DR EMILY DAVIS']

for p in practitioners:
    signed = db.query(SignedNoteItem).filter(SignedNoteItem.practitioner == p).count()
    usage = db.query(PractitionerUsageItem).filter(PractitionerUsageItem.practitioner_name == p).first()
    access = db.query(PatientAccessItem).filter(PatientAccessItem.practitioner == p).count()
    unsigned = db.query(UnsignedNoteItem).filter(UnsignedNoteItem.practitioner == p).count()
    audit = db.query(AuditItem).filter(AuditItem.practitioner == p).count()
    
    # Get unique programs and locations
    programs = db.query(SignedNoteItem.program).filter(
        SignedNoteItem.practitioner == p,
        SignedNoteItem.program.isnot(None)
    ).distinct().all()
    locations = db.query(SignedNoteItem.location).filter(
        SignedNoteItem.practitioner == p,
        SignedNoteItem.location.isnot(None)
    ).distinct().all()
    
    print(f'{p}:')
    print(f'  Signed Notes: {signed}')
    print(f'  Unsigned Notes: {unsigned}')
    print(f'  Patient Access: {access}')
    print(f'  Audit Items: {audit}')
    if usage:
        print(f'  Visits: {usage.visits}, Hours: {usage.total_time}')
        print(f'  Primary Program: {usage.program}, Location: {usage.location}')
    print(f'  Programs: {[p[0] for p in programs if p[0]]}')
    print(f'  Locations: {[l[0] for l in locations if l[0]]}')
    print()

db.close()

