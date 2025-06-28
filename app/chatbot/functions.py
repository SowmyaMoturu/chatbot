functions = [
    {
    "name": "search_doctors_by_specialization",
    "description": (
        "Find doctors with the given specialization. "
        "If more than one doctor is found, always ask the user to pick a doctor and specify a preferred date and time for the appointment. "
    ),
        "parameters": {
            "type": "object",
            "properties": {
                "specialization": {"type": "string"},
                "date_time": {"type": "string", "format": "datetime"}
            },
            "required": ["specialization"],
        },
    },
    {
        "name": "check_doctor_slot_availability",
        "description": "Check if a doctor is available at specified data and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {"type": "string"},
                "date_time": {"type": "string", "format": "datetime"},
                "specialization": {"type": "string"},
                "patient_name": {"type": "string"},
                "patient_phone_number": {"type": "string"},
            },
            "required": ["doctor_name", "date_time", "specialization"],
        },
    },
    {
        "name": "book_appointment",
        "description": "Book an appointment with a doctor.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {"type": "string"},
                "patient_name": {"type": "string"},
                "patient_phone_number": {"type": "string"},
                "date_time": {"type": "string", "format": "datetime"},
                "specialization": {"type": "string"}
            },
            "required": ["doctor_name", "patient_name", "patient_phone_number", "date_time", "specialization"],
        },
    },
    {
    "name": "search_doctors_by_name",
       "description": (
        "Find doctors by their name. Remove title and suffix from the name"
        "If more than one doctor is found, always ask the user to pick a doctor and specify a preferred date and time for the appointment."
        ),
    "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {"type": "string"},
                "date_time": {"type": "string", "format": "datetime"}
            },
            "required": ["doctor_name"],
        },
    },
    {
        "name": "get_appointment_details",
        "description": "Get details of an appointment by patient's phone Number and name",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_phone_number": {"type": "string"},
                "patient_name": {"type": "string"},
            },
            "required": ["patient_phone_number", "patient_name"],
        },
    },
    {
        "name": "get_next_available_slot",
        "description": "Get the next available slot for a doctor.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {"type": "string"},
                "date_time": {"type": "string", "format": "datetime"}
            },
            "required": ["doctor_name", "date"],
        },
    },
    {
        "name": "get_patient_details",
        "description": "Get details of a patient by their phone number and optional name.",
        "parameters": {
            "type": "object",
            "properties": {
                "phone_number": {"type": "string"},
                "name": {"type": "string", "default": None},
            },
            "required": ["phone_number"]
        }
    },
    {
        "name": "add_patient",
        "description": "Add a new patient to the system.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "phone_number": {"type": "string"},
            },
            "required": ["name", "phone_number"],
        },
    },
    {
        "name": "cancel_appointment",
        "description": "Cancel an existing appointment by providing the appointment ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string"},
                "patient_phone_number": {"type": "string"},
                "date_time": {"type": "string", "format": "datetime"},
            },
            "required": ["patient_name", "patient_phone_number", "date_time"],
        }

    }
]
