from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse


alpha = RegexValidator(
  r"^[a-zA-Z]*$",
  "Only alphabetical characters are allowed; no numbers, spaces, symbols etc."
)


class Variant(models.Model):
  # Fields
  name = models.CharField(
    max_length=18,
    unique=True,
    help_text="All species have a 'natural' or 'base' look and feel, but, their physical appearance and colours may vary based on environmental factors. Not all species are available in all variants.",
    validators=[alpha],
  )

  # Metadata
  class Meta:
    ordering = ["id", "name"]
    constraints = [
      models.CheckConstraint(
        name="%(app_label)s_%(class)s_name_not_blank",
        check=~models.Q(name=''),
        violation_error_message="%(app_label)s %(class)s name must not be blank."
      ),
      models.UniqueConstraint(
        Lower("name"),
        name="%(app_label)s_%(class)s_name_case_insensitive_unique",
        violation_error_message="%(app_label)s %(class)s name already exists (case insensitive match)."
      ),
    ]

  # Methods
  def __str__(self):
    return f"#{self.id} {self.name}"


class Pet(models.Model):
  # Fields
  species = models.CharField(
    max_length=18,
    unique=True,
    help_text="What unique term has the great Oneiromancer chosen to refer to this kind of monster?",
    validators=[alpha],
  )
  date_discovered = models.DateTimeField(
    auto_now_add=True,
    help_text="When did the great Oneiromancer learn about the existence of this species?"
  )
  description = models.TextField(
    blank=True,
    help_text="How would the great Oneiromancer describe the behaviours and build of this species? Its nature, its rituals, its way of life?"
  )
  available_variants = models.ManyToManyField(
    to=Variant,
    related_name="species",
    help_text="What variations in physical appearance and colour can this species have?"
  )

  # Metadata
  class Meta:
    ordering = ["species"]
    constraints = [
      models.CheckConstraint(
        name="%(app_label)s_%(class)s_species_not_blank",
        check=~models.Q(species=''),
        violation_error_message="%(app_label)s %(class)s species must not be blank."
      ),
      models.UniqueConstraint(
        Lower("species"),
        name="%(app_label)s_%(class)s_species_case_insensitive_unique",
        violation_error_message="%(app_label)s %(class)s species already exists (case insensitive match)."
      ),
    ]

  # Methods
  def __str__(self):
    return self.species


# class PetInstance(models.Model):
#   # Fields
#   owner = models.ForeignKey()
#
#   # Metadata
#
#   # Methods
