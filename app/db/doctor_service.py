from datetime import datetime, timedelta, time
from typing import List, Optional, Dict, Any
from app.utils.db_utils import execute_query

class DoctorService:
    @staticmethod
    def get_by_specialization(specialization: str) -> List[Dict[str, Any]]:
        query = """
            SELECT id, name, specialization, start_time, end_time
            FROM doctors
            WHERE LOWER(specialization) = LOWER(%s)
        """
        doctors = execute_query(query, (specialization,), fetchall=True)
        return [DoctorService._format_doctor(row) for row in doctors] if doctors else []

    @staticmethod
    def get_doctor_by_name(doctor_name: str) -> List[Dict[str, Any]]:
        query = """
            SELECT id, name, specialization, start_time, end_time
            FROM doctors
            WHERE LOWER(name) LIKE LOWER(%s)
        """
        doctors = execute_query(query, (f"%{doctor_name}%",), fetchall=True)
        return [DoctorService._format_doctor(row) for row in doctors] if doctors else []

    @staticmethod
    def get_doctor_by_name_and_specialization(doctor_name: str, specialization: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, name, specialization, start_time, end_time
            FROM doctors
            WHERE LOWER(name) LIKE LOWER(%s) AND LOWER(specialization) = LOWER(%s)
            LIMIT 1
        """
        doctor = execute_query(query, (f"%{doctor_name}%", specialization), fetchone=True)
        return DoctorService._format_doctor(doctor) if doctor else None

    @staticmethod
    def get_list_of_specializations() -> List[str]:
        query = "SELECT DISTINCT specialization FROM doctors"
        result = execute_query(query, fetchall=True)
        return [row['specialization'] for row in result] if result else []

    @staticmethod
    def get_available_slots(doctor_id: int, date_obj: datetime) -> List[str]:
        # Get doctor's working hours
        query = "SELECT start_time, end_time FROM doctors WHERE id = %s"
        doctor = execute_query(query, (doctor_id,), fetchone=True)
        if not doctor or not doctor["start_time"] or not doctor["end_time"]:
            return []

        start_time = doctor["start_time"]
        end_time = doctor["end_time"]

        # Build slot times
        slots = []
        current = datetime.combine(date_obj.date(), start_time)
        end = datetime.combine(date_obj.date(), end_time)
        while current < end:
            slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=30)

        # Remove booked slots
        query = """
            SELECT appointment_time FROM appointments
            WHERE doctor_id = %s AND appointment_time::date = %s AND status != 'cancelled'
        """
        booked = execute_query(query, (doctor_id, date_obj.date()), fetchall=True)
        booked_times = {row['appointment_time'].strftime("%H:%M") for row in booked} if booked else set()
        available = [slot for slot in slots if slot not in booked_times]
        return available

    @staticmethod
    def check_slot_availability(doctor_id: int, date_time: datetime) -> bool:
        query = """
            SELECT COUNT(*) AS count FROM appointments
            WHERE doctor_id = %s AND appointment_time = %s AND status != 'cancelled'
        """
        result = execute_query(query, (doctor_id, date_time), fetchone=True)
        return result and result['count'] == 0

    @staticmethod
    def get_next_available_slot(doctor_id: int, date_obj: datetime) -> Optional[dict]:
        for i in range(7):  # Check up to a week ahead
            check_date = date_obj + timedelta(days=i)
            slots = DoctorService.get_available_slots(doctor_id, check_date)
            if slots:
                return {
                "date": check_date.strftime('%Y-%m-%d'),
                "slots": slots
                }
        return None

    @staticmethod
    def _format_doctor(doc: dict) -> dict:
        # Formats a doctor row into a consistent dict
        return {
            "id": doc["id"],
            "name": doc["name"],
            "specialization": doc["specialization"],
            "start_time": doc["start_time"].strftime("%H:%M") if isinstance(doc["start_time"], time) else str(doc["start_time"]),
            "end_time": doc["end_time"].strftime("%H:%M") if isinstance(doc["end_time"], time) else str(doc["end_time"])
        }
    
    @staticmethod
    def get_list_of_specializations() -> list:
        query = "SELECT DISTINCT specialization FROM doctors"
        result = execute_query(query, fetchall=True)
        return [row['specialization'] for row in result] if result else []