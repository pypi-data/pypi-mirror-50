from edc_list_data import PreloadData
from edc_constants.constants import OTHER


list_data = {
    "ambition_ae.antibiotictreatment": [
        ("amoxicillin", "Amoxicillin"),
        ("flucloxacillin", "Flucloxacillin"),
        ("doxycycline", "Doxycycline"),
        ("ceftriaxone", "Ceftriaxone"),
        ("erythromycin", "Erythromycin"),
        ("ciprofloxacin", "Ciprofloxacin"),
        ("no_treatment", "- No treatment"),
        (OTHER, "- Other, specify"),
    ],
    "ambition_ae.meningitissymptom": [
        ("headache", "Headache"),
        ("vomiting", "Vomiting"),
        ("fever", "Fever"),
        ("seizures", "Seizures"),
        ("neck_pain", "Neck pain"),
        ("no_symptoms", "- No symptoms"),
        (OTHER, "- Other, specify"),
    ],
    "ambition_ae.neurological": [
        ("meningism", "Meningism"),
        ("papilloedema", " Papilloedema"),
        ("focal_neurologic_deficit", "Focal neurologic deficit"),
        ("CN_VI_palsy", "Cranial Nerve VI palsy"),
        ("CN_III_palsy", "Cranial Nerve III palsy"),
        ("CN_IV_palsy", "Cranial Nerve IV palsy"),
        ("CN_VII_palsy", "Cranial Nerve VII palsy"),
        ("CN_VIII_palsy", "Cranial Nerve VIII palsy"),
        ("no_symptoms", "- No symptoms"),
        (OTHER, "- Other CN palsy"),
    ],
    "edc_adverse_event.aeclassification": [
        ("anaemia", "Anaemia"),
        ("bacteraemia/sepsis", "Bacteraemia/Sepsis"),
        ("CM_IRIS", "CM IRIS"),
        ("diarrhoea", "Diarrhoea"),
        ("hypokalaemia", "Hypokalaemia"),
        ("neutropaenia", "Neutropaenia"),
        ("pneumonia", "Pneumonia"),
        ("renal_impairment", "Renal impairment"),
        ("respiratory_distress", "Respiratory distress"),
        ("TB", "TB"),
        ("thrombocytopenia", "Thrombocytopenia"),
        ("thrombophlebitis", "Thrombophlebitis"),
        (OTHER, "Other"),
    ],
}

preload_data = PreloadData(list_data=list_data, model_data={}, unique_field_data=None)
