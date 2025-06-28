# Doctor Assistant Chatbot

## Overview
The Doctor Assistant Chatbot is an intelligent system designed to assist users in finding doctors, checking appointment availability, and booking appointments. It leverages OpenAI's GPT model and integrates with a backend database to manage doctors, patients, and appointments.

---

## Features
- **Search for Doctors**: Find doctors by name or specialization.
- **Check Slot Availability**: Verify if a doctor is available at a specific date and time.
- **Book Appointments**: Schedule appointments with doctors.
- **Suggest Alternate Slots**: If a preferred slot is unavailable, suggest the next available slot.
- **Manage Patient Information**: Add new patients and retrieve existing patient details.

---

## Technologies Used
- **Backend**:
  - Python
  - Flask
  - SQLAlchemy
  - PostgreSQL
- **AI Integration**:
  - OpenAI GPT-4o
- **Frontend**:
  - Streamlit (optional for UI)
- **Other Libraries**:
  - FastAPI
  - Pydantic
  - psycopg2

---

## Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database
- OpenAI API key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/doctor-assistant-chatbot.git
   cd doctor-assistant-chatbot