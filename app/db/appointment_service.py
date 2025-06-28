from datetime import datetime
from typing import List, Dict, Any, Optional
from app.utils.db_utils import execute_query

class AppointmentService:
    @staticmethod
    def _format_appointment(row) -> Dict[str, Any]:
        # Ensure all fields are JSON serializable
        return {
            "id": row["id"],
            "doctor_id": row["doctor_id"],
            "patient_id": row["patient_id"],
            "appointment_time": row["appointment_time"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row["appointment_time"], datetime) else str(row["appointment_time"]),
            "status": row["status"]
        }

    @staticmethod
    def get_appointments_for_patient(phone_number: str, name: str) -> List[Dict[str, Any]]:
        query = """
            SELECT * FROM appointments
            WHERE patient_id = (
                SELECT id FROM patients WHERE phone_number = %s AND name = %s
            )
            ORDER BY appointment_time DESC
        """
        params = (phone_number, name)
        try:
            results = execute_query(query, params, fetchall=True)
            return [AppointmentService._format_appointment(row) for row in results] if results else []
        except Exception as e:
            return [{"error": str(e)}]

    @staticmethod
    def book_appointment(doctor_id: int, patient_id: int, date_time: datetime) -> Any:
        try:
            # Check if slot is already booked
            check_query = """
                SELECT COUNT(*) AS count FROM appointments
                WHERE doctor_id = %s AND appointment_time = %s AND status != 'cancelled'
            """
            check_result = execute_query(check_query, (doctor_id, date_time), fetchone=True)
            if check_result and check_result["count"] > 0:
                return {"error": "Slot already booked."}

            # Book the appointment
            query = """
                INSERT INTO appointments (doctor_id, patient_id, appointment_time, status)
                VALUES (%s, %s, %s, 'booked')
                RETURNING id, doctor_id, patient_id, appointment_time, status
            """
            result = execute_query(query, (doctor_id, patient_id, date_time), fetchone=True)
            if result:
                return AppointmentService._format_appointment(result)
            else:
                return {"error": "Failed to book appointment."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def cancel_appointment(appointment_id: int) -> bool:
        try:
            query = "UPDATE appointments SET status = 'cancelled' WHERE id = %s RETURNING id"
            result = execute_query(query, (appointment_id,), fetchone=True)
            return bool(result)
        except Exception:
            return False

    @staticmethod
    def reschedule_appointment(appointment_id: int, new_date_time: str) -> Optional[Dict[str, Any]]:
        try:
            query = """
                UPDATE appointments
                SET appointment_time = %s, status = 'booked'
                WHERE id = %s
                RETURNING id, doctor_id, patient_id, appointment_time, status
            """
            result = execute_query(query, (new_date_time, appointment_id), fetchone=True)
            if result:
                return AppointmentService._format_appointment(result)
            else:
                return None
        except Exception as e:
            return {"error": str(e)}