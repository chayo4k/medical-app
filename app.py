from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Моделі бази даних
class MedicalFacility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('medical_facility.id'), nullable=False)
    facility = db.relationship('MedicalFacility', backref='doctors')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('medical_facility.id'), nullable=False)
    facility = db.relationship('MedicalFacility', backref='services')  # Додаємо зв’язок

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    appointment_date = db.Column(db.String(20), nullable=False)

    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    service = db.relationship('Service', backref='appointments')

# Головна сторінка
@app.route('/')
def index():
    facilities = MedicalFacility.query.all()
    return render_template('index.html', facilities=facilities)

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        new_facility = MedicalFacility(name=name, address=address, phone=phone)
        db.session.add(new_facility)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_facility.html')

@app.route('/edit_facility/<int:id>', methods=['GET', 'POST'])
def edit_facility(id):
    facility = MedicalFacility.query.get_or_404(id)

    if request.method == 'POST':
        facility.name = request.form['name']
        facility.address = request.form['address']
        facility.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_facility.html', facility=facility)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_facility(id):
    facility = MedicalFacility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return redirect(url_for('index'))

# ====== Маршрути для лікарів ======
@app.route('/doctors')
def doctors():
    doctors_list = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors_list)

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        facility_id = request.form['facility_id']
        new_doctor = Doctor(name=name, specialization=specialization, facility_id=facility_id)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctors'))
    facilities = MedicalFacility.query.all()
    return render_template('add_doctor.html', facilities=facilities)

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('doctors'))

# ====== Маршрути для пацієнтів ======
@app.route('/patients')
def patients():
    patients_list = Patient.query.all()
    return render_template('patients.html', patients=patients_list)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        new_patient = Patient(name=name, birth_date=birth_date, phone=phone)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patients'))

# ====== Маршрути для послуг ======
@app.route('/services')
def services():
    services_list = Service.query.all()
    return render_template('services.html', services=services_list)

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        facility_id = request.form['facility_id']
        new_service = Service(name=name, price=price, facility_id=facility_id)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('services'))
    facilities = MedicalFacility.query.all()
    return render_template('add_service.html', facilities=facilities)

@app.route('/delete_service/<int:id>')
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('services'))

@app.route('/edit_service/<int:id>', methods=['GET', 'POST'])
def edit_service(id):
    service = Service.query.get_or_404(id)
    facilities = MedicalFacility.query.all()

    if request.method == 'POST':
        service.name = request.form['name']
        service.price = request.form['price']
        service.facility_id = request.form['facility_id']
        db.session.commit()
        return redirect(url_for('services'))

    return render_template('edit_service.html', service=service, facilities=facilities)

# ====== Маршрути для записів на прийом ======
@app.route('/appointments')
def appointments():
    appointments_list = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments_list)

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        service_id = request.form['service_id']
        appointment_date = request.form['appointment_date']
        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, service_id=service_id, appointment_date=appointment_date)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('appointments'))
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    services = Service.query.all()
    return render_template('add_appointment.html', patients=patients, doctors=doctors, services=services)

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('appointments'))

@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    services = Service.query.all()

    if request.method == 'POST':
        appointment.patient_id = request.form['patient_id']
        appointment.doctor_id = request.form['doctor_id']
        appointment.service_id = request.form['service_id']
        appointment.appointment_date = request.form['appointment_date']
        db.session.commit()
        return redirect(url_for('appointments'))

    return render_template('edit_appointment.html', appointment=appointment, patients=patients, doctors=doctors, services=services)

@app.route('/debug_facilities')
def debug_facilities():
    facilities = MedicalFacility.query.all()
    return "<br>".join([f"{facility.id}. {facility.name} - {facility.address} ({facility.phone})" for facility in facilities])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
