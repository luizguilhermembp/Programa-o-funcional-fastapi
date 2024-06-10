from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

app = FastAPI()

engine = create_engine('postgresql://postgres:root@localhost:5432/provafinal')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patient'
    patientid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)

class Vaccine(Base):
    __tablename__ = 'vaccine'
    vaccineID = Column(Integer, primary_key=True, index=True)
    patientID = Column(Integer, ForeignKey('patient.patientid'))
    vaccinename = Column(String)
    dosedate = Column(String)  # Alteração aqui para usar string em vez de DateTime
    dosenumber = Column(Integer)
    vaccinetype = Column(String)
    patient = relationship("Patient")

class Dose(Base):
    __tablename__ = 'dose'
    doseID = Column(Integer, primary_key=True, index=True)
    vaccineID = Column(Integer, ForeignKey('vaccine.vaccineID'))
    typedose = Column(String)
    dosedate = Column(String)  # Alteração aqui para usar string em vez de DateTime
    dosenumber = Column(Integer)
    applicationtype = Column(String)
    vaccine = relationship("Vaccine")

Base.metadata.create_all(bind=engine)

# CRUD PACIENTES
@app.get("/api/patients")
def get_patients():
    return session.query(Patient).all()

@app.post("/api/patients")
def create_patient(name: str, lastname: str):
    patient = Patient(name=name, lastname=lastname)
    session.add(patient)
    session.commit()
    return patient

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: int):
    return session.query(Patient).filter(Patient.patientid == patient_id).first()

@app.put("/api/patients/{patient_id}")
def update_patient(patient_id: int, name: str, lastname: str):
    patient = session.query(Patient).filter(Patient.patientid == patient_id).first()
    if patient:
        patient.name = name
        patient.lastname = lastname
        session.commit()
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: int):
    patient = session.query(Patient).filter(Patient.patientid == patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        return {"message": "Patient deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

# CRUD VACINAS
@app.get("/api/vaccines")
def get_vaccines():
    return session.query(Vaccine).all()

@app.post("/api/vaccines")
def create_vaccine(patientID: int, vaccinename: str, dosedate: str, dosenumber: int, vaccinetype: str):  # Alteração aqui para usar string em vez de DateTime
    vaccine = Vaccine(patientID=patientID, vaccinename=vaccinename, dosedate=dosedate, dosenumber=dosenumber, vaccinetype=vaccinetype)
    session.add(vaccine)
    session.commit()
    return vaccine

@app.get("/api/vaccines/{vaccine_id}")
def get_vaccine(vaccine_id: int):
    return session.query(Vaccine).filter(Vaccine.vaccineID == vaccine_id).first()

@app.put("/api/vaccines/{vaccine_id}")
def update_vaccine(vaccine_id: int, patientID: int, vaccinename: str, dosedate: str, dosenumber: int, vaccinetype: str):  # Alteração aqui para usar string em vez de DateTime
    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == vaccine_id).first()
    if vaccine:
        vaccine.patientID = patientID
        vaccine.vaccinename = vaccinename
        vaccine.dosedate = dosedate
        vaccine.dosenumber = dosenumber
        vaccine.vaccinetype = vaccinetype
        session.commit()
        return vaccine
    else:
        raise HTTPException(status_code=404, detail="Vaccine not found")

@app.delete("/api/vaccines/{vaccine_id}")
def delete_vaccine(vaccine_id: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccineID == vaccine_id).first()
    if vaccine:
        session.delete(vaccine)
        session.commit()
        return {"message": "Vaccine deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Vaccine not found")

# CRUD DOSES
@app.get("/api/doses")
def get_doses():
    return session.query(Dose).all()

@app.post("/api/doses")
def create_dose(vaccineID: int, typedose: str, dosedate: str, dosenumber: int, applicationtype: str):  # Alteração aqui para usar string em vez de DateTime
    dose = Dose(vaccineID=vaccineID, typedose=typedose, dosedate=dosedate, dosenumber=dosenumber, applicationtype=applicationtype)
    session.add(dose)
    session.commit()
    return dose

@app.get("/api/doses/{dose_id}")
def get_dose(dose_id: int):
    return session.query(Dose).filter(Dose.doseID == dose_id).first()

@app.put("/api/doses/{dose_id}")
def update_dose(dose_id: int, vaccineID: int, typedose: str, dosedate: str, dosenumber: int, applicationtype: str):  # Alteração aqui para usar string em vez de DateTime
    dose = session.query(Dose).filter(Dose.doseID == dose_id).first()
    if dose:
        dose.vaccineID = vaccineID
        dose.typedose = typedose
        dose.dosedate = dosedate
        dose.dosenumber = dosenumber
        dose.applicationtype = applicationtype
        session.commit()
        return dose
    else:
        raise HTTPException(status_code=404, detail="Dose not found")

@app.delete("/api/doses/{dose_id}")
def delete_dose(dose_id: int):
    dose = session.query(Dose).filter(Dose.doseID == dose_id).first()
    if dose:
        session.delete(dose)
        session.commit()
        return {"message": "Dose deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Dose not found")

