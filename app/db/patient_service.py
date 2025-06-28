from typing import Optional, Dict, Any, List
from app.utils.db_utils import execute_query

class PatientService:
    @staticmethod
    def add_patient(name: str, phone_number: str) -> Optional[Dict[str, Any]]:
        query = """
            INSERT INTO patients (name, phone_number)
            VALUES (%s, %s)
            RETURNING id, name, phone_number
        """
        patient = execute_query(query, (name, phone_number), fetchone=True)
        return PatientService._format_patient(patient) if patient else None

    @staticmethod
    def get_patient_details(phone_number: str, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if name:
            query = """
                SELECT id, name, phone_number
                FROM patients
                WHERE phone_number = %s AND LOWER(name) = LOWER(%s)
                LIMIT 1
            """
            params = (phone_number, name)
        else:
            query = """
                SELECT id, name, phone_number
                FROM patients
                WHERE phone_number = %s
                LIMIT 1
            """
            params = (phone_number,)
        patient = execute_query(query, params, fetchone=True)
        return PatientService._format_patient(patient) if patient else None

    @staticmethod
    def get_all_patients() -> List[Dict[str, Any]]:
        query = "SELECT id, name, phone_number FROM patients"
        patients = execute_query(query, fetchall=True)
        return [PatientService._format_patient(p) for p in patients] if patients else []

    @staticmethod
    def _format_patient(patient: dict) -> Dict[str, Any]:
        return {
            "id": patient.get("id"),
            "name": patient.get("name"),
            "phone_number": patient.get("phone_number"),
        }