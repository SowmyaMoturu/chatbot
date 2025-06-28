from app.db.doctor_service import DoctorService
from app.db.patient_service import PatientService
from app.db.appointment_service import AppointmentService
from datetime import datetime

def dispatch_function_call(function_name, arguments):
    try:
        if function_name == "search_doctors_by_specialization":
            return DoctorService.get_by_specialization(arguments["specialization"])

        if function_name == "search_doctors_by_name":
            return DoctorService.get_doctor_by_name(arguments["doctor_name"])

        if function_name == "check_doctor_slot_availability":
            doctor_name = arguments.get("doctor_name")
            specialization = arguments.get("specialization")
            date_time_str = arguments.get("date_time")
          
           
            if not (doctor_name and specialization and date_time_str):
                return {"available": False, "reason": "Missing required fields"}

            doctor = DoctorService.get_doctor_by_name_and_specialization(doctor_name, specialization)
            if not doctor:
                return {"available": False, "reason": "Doctor not found"}
            doctor_id = doctor["id"]

            try:
                date_time = datetime.fromisoformat(date_time_str)
            except Exception:
                return {"available": False, "reason": f"Invalid datetime format: {date_time_str}"}

            is_available = DoctorService.check_slot_availability(doctor_id, date_time)
            return {"available": is_available, "doctor_name": doctor_name, "date_time": date_time_str}

        if function_name == "book_appointment":
            doctor = DoctorService.get_doctor_by_name_and_specialization(arguments["doctor_name"], arguments["specialization"])
            if not doctor:
                return "Doctor not found."
            doctor_id = doctor["id"]
            

            patient = PatientService.get_patient_details(arguments["patient_phone_number"], arguments["patient_name"])
            print(f"Patient details: {patient}")
            if not patient:
                patient = PatientService.add_patient(arguments["patient_name"], arguments["patient_phone_number"])
                patient_id = patient["id"] 
                print(f"New patient added with ID: {patient_id}")
            else:
                patient_id = patient["id"]

            try:
                date_time = datetime.fromisoformat(arguments["date_time"])
            except Exception:
                return f"Invalid date/time format: {arguments['date_time']}"
            print(f"Booking appointment for {doctor_id} with patient {patient_id} at {date_time}")

            appt = AppointmentService.book_appointment(doctor_id, patient_id, date_time)
            if isinstance(appt, dict):
                return appt
            elif appt is True:
                return f"Appointment booked successfully for {arguments['patient_name']} with {arguments['doctor_name']} on {arguments['date_time']}."
            else:
                return "Appointment booking failed."

        if function_name == "get_next_available_slot":
            doctor_name = arguments.get("doctor_name")
            specialization = arguments.get("specialization")
            date_time_str = arguments.get("date_time")
            print(f"Getting next available slot for {doctor_name} with specialization {specialization} at {date_time_str}")
            doctor = DoctorService.get_doctor_by_name_and_specialization(doctor_name , specialization)
            if not doctor:
                return {"error": "Doctor not found."}
            doctor_id = doctor["id"]

            try:
                date_time = datetime.fromisoformat(arguments["date_time"])
            except Exception:
                return {"error": f"Invalid date/time format: {arguments['date_time']}"}

            return DoctorService.get_next_available_slot(doctor_id, date_time)

    except Exception as e:
        return {"error": str(e)}