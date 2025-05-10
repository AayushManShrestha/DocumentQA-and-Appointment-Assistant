# DocumentQA and Appointment Assistant

This application offers two main features:

1. **Document Question Answering (DocumentQA)**: Allows users to upload documents (PDF, TXT, DOCX) and query specific information.
2. **Appointment Booking**: Guides users through booking appointments by collecting details such as name, email, phone number, and preferred date.

---

## Setup

### Prerequisites

* Python 3.9+
* Streamlit
* Langchain
* Other dependencies in `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/documentqa-appointment-assistant.git
   cd documentqa-appointment-assistant
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Run the app with:

```bash
streamlit run app.py
```

---

## File Structure

* **app.py**: Main entry point of the app.
* **pages**:

  * **document\_qa.py**: Handles document uploading and QA.
  * **appointment\_booking.py**: Manages appointment booking flow.
* **data**:

  * **appointments.json**: Stores appointment details.
  * **documents**: Stores uploaded documents.
* **utils**:

  * **document\_processor.py**: Processes uploaded documents.
  * **booking\_utils.py**: Utilities for managing appointments.
  * **date\_utils.py**: Handles date parsing and validation.
  * **validator.py**: Validates user inputs (e.g., email, phone number).
* **config**:

  * **llm.py**: LLM configuration.
* **requirements.txt**: Project dependencies.

---

## Usage

### Document QA Flow:

1. Upload documents (PDF, DOCX, TXT).
2. Ask questions about the document.
3. The assistant responds with relevant answers.

### Appointment Booking Flow:

1. Provide your name to start.
2. The assistant collects contact details and preferred appointment date.
3. Once completed, the appointment is confirmed.

---

## License

MIT License - see the [LICENSE](LICENSE) file for details.