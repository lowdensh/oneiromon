from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse


alpha = RegexValidator(
  r"^[a-zA-Z]*$",
  "Only alphabetical characters are allowed; no numbers, spaces, symbols etc."
)
alphanumeric = RegexValidator(
  r"^[0-9a-zA-Z]*$",
  "Only alphanumeric characters are allowed; no spaces, symbols etc."
)


class Species(models.Model):
  # Fields
  name = models.CharField(
    max_length=18,
    unique=True,
    help_text="What unique term has the great Oneiromancer chosen to refer to this species? Letters only.",
    validators=[alpha],
  )
  date_discovered = models.DateTimeField(
    auto_now_add=True,
    help_text="When did the great Oneiromancer learn about the existence of this species?"
  )
  description = models.TextField(
    blank=True,
    help_text="How would the great Oneiromancer describe the behaviours and build of this species? Its attitude, its rituals, its way of life?"
  )

  # Metadata
  class Meta:
    ordering = ["name"]
    verbose_name = "species"
    verbose_name_plural = "species"
    constraints = [
      models.CheckConstraint(
        name="%(app_label)s_%(class)s_name_not_blank",
        check=~models.Q(name=""),
        violation_error_message="Species name must not be blank."
      ),
      models.UniqueConstraint(
        Lower("name"),
        name="%(app_label)s_%(class)s_name_case_insensitive_unique",
        violation_error_message="Species name already exists (case insensitive match)."
      ),
    ]

  # Methods
  def __str__(self):
    return self.name


class Style(models.Model):
  # Fields
  name = models.CharField(
    max_length=18,
    unique=True,
    validators=[alpha],
    help_text="All species have a 'natural' look. Some have different styles i.e. variations in physical appearance and colour. What would you call this style? Letters only.",
  )
  description = models.TextField(
    blank=True,
    help_text="How does this style (variation in physical appearance and colour) deviate from the natural look of the species?",
  )
  valid_species = models.ManyToManyField(
    to=Species,
    through="Combination",
    related_name="valid_styles",
    help_text="What species are available in this style (variation in physical appearance and colour)?"
  )

  # Metadata
  class Meta:
    ordering = ["name", ]
    constraints = [
      models.CheckConstraint(
        name="%(app_label)s_%(class)s_name_not_blank",
        check=~models.Q(name=""),
        violation_error_message="Style name must not be blank."
      ),
      models.UniqueConstraint(
        Lower("name"),
        name="%(app_label)s_%(class)s_name_case_insensitive_unique",
        violation_error_message="Style name already exists (case insensitive match)."
      ),
    ]

  # Methods
  def __str__(self):
    return self.name


class Combination(models.Model):
  # Fields
  species = models.ForeignKey(
    to=Species,
    on_delete=models.CASCADE,
  )
  style = models.ForeignKey(
    to=Style,
    on_delete=models.CASCADE,
  )
  image = models.ImageField(
    upload_to="species_style_combinations",
  )

  # Metadata
  class Meta:
    ordering = ["species", "style", ]
    constraints = [
      models.UniqueConstraint(
        fields=["species", "style", ],
        name="%(app_label)s_%(class)s_species_style_unique_together",
        violation_error_message="Combination of Species and Style is not unique together."
      ),
    ]

  # Methods
  def __str__(self):
    return f"{self.species} species, in {self.style} style"


class PetInstance(models.Model):
  # Fields
  name = models.CharField(
    max_length=18,
    unique=True,
    help_text="What name has been bestowed upon this blessed pet? Must be unique and cannot be changed. Letters and numbers only.",
    validators=[alphanumeric],
  )
  species = models.ForeignKey(
    to=Species,
    on_delete=models.CASCADE,
    help_text="What species is this pet?",
  )
  style = models.ForeignKey(
    to=Style,
    on_delete=models.SET_DEFAULT,
    default=1,
    help_text="What style is the pet?",
  )
  date_hatched = models.DateTimeField(
    auto_now_add=True,
    help_text="When did this pet hatch?",
  )
  owner = models.ForeignKey(
    to=settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    help_text="Who does this pet belong to?",
  )

  # Metadata
  class Meta:
    ordering = ["name"]
    constraints = [
      models.CheckConstraint(
        name="%(app_label)s_%(class)s_name_not_blank",
        check=~models.Q(name=''),
        violation_error_message="PetInstance name must not be blank."
      ),
      models.UniqueConstraint(
        Lower("name"),
        name="%(app_label)s_%(class)s_name_case_insensitive_unique",
        violation_error_message="PetInstance name already exists (case insensitive match)."
      ),
    ]

  # Methods
  def __str__(self):
    return f"{self.name} the {self.style} {self.species}"
