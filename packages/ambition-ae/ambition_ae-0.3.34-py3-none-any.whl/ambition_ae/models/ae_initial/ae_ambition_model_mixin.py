from django.db import models
from edc_model.validators import datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import UNKNOWN

from ...choices import STUDY_DRUG_RELATIONSHIP


class AeAmbitionModelMixin(models.Model):

    # removed issue #4
    ambisome_relation = models.CharField(
        verbose_name="Relationship to Ambisome:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
        editable=False,
    )

    fluconazole_relation = models.CharField(
        verbose_name="Relationship to Fluconozole:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    # removed issue #4
    amphotericin_b_relation = models.CharField(
        verbose_name="Relationship to Amphotericin B:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
        editable=False,
    )

    flucytosine_relation = models.CharField(
        verbose_name="Relationship to Flucytosine:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    # added issue #4
    amphotericin_relation = models.CharField(
        verbose_name="Amphotericin formulation:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
    )

    details_last_study_drug = models.TextField(
        verbose_name="Details of the last implicated drug (name, dose, route):",
        max_length=1000,
        null=True,
        blank=True,
        editable=False,
    )

    med_administered_datetime = models.DateTimeField(
        verbose_name="Date and time of last implicated study medication administered",
        validators=[datetime_not_future],
        null=True,
        blank=True,
        editable=False,
    )

    ae_cm_recurrence = models.CharField(
        verbose_name="Was the AE a recurrence of CM symptoms?",
        max_length=10,
        choices=YES_NO,
        default=UNKNOWN,
        help_text='If "Yes", fill in the "Recurrence of Symptoms" form',
    )

    tmg_report_datetime = models.DateTimeField(
        verbose_name="Date and time AE reported to TMG",
        blank=True,
        null=True,
        help_text=(
            "AEs ≥ Grade 4 or SAE must be reported to the Trial "
            "Management Group (TMG) within 24 hours"
        ),
    )

    class Meta:
        abstract = True
