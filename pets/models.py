from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.html import mark_safe


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
    help_text="What unique term has the great Oneiromancer chosen to refer to this monster species? Letters only.",
    validators=[alpha],
  )
  date_discovered = models.DateTimeField(
    auto_now_add=True,
    help_text="When did the great Oneiromancer learn about the existence of this monster species?"
  )
  description = models.TextField(
    blank=True,
    help_text="How would the great Oneiromancer describe the behaviours and build of this particular monster species? Its attitude, its rituals, its way of life?"
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

  def count_pet_instances(self):
    return PetInstance.objects.filter(species=self).count()

  def count_themes(self):
    return self.valid_themes.all().count()

  def has_theme(self, theme):
    if theme in self.valid_themes.all():
      return True
    return False


class Theme(models.Model):
  # Fields
  name = models.CharField(
    max_length=18,
    unique=True,
    validators=[alpha],
    help_text="Some monster species have different themes i.e. variations in physical appearance and colour. What would you call this theme? Letters only.",
  )
  description = models.TextField(
    blank=True,
    help_text="Describe this theme (variation in physical appearance and colour).",
  )
  valid_species = models.ManyToManyField(
    to=Species,
    through="Combination",
    related_name="valid_themes",
    help_text="What monster species are available in this theme (variation in physical appearance and colour)?"
  )

  # Metadata
  class Meta:
    ordering = ["name", ]
    constraints = [
      models.CheckConstraint(
        name="%(app_label)s_%(class)s_name_not_blank",
        check=~models.Q(name=""),
        violation_error_message="Theme name must not be blank."
      ),
      models.UniqueConstraint(
        Lower("name"),
        name="%(app_label)s_%(class)s_name_case_insensitive_unique",
        violation_error_message="Theme name already exists (case insensitive match)."
      ),
    ]

  # Methods
  def __str__(self):
    return self.name

  def count_pet_instances(self):
    return PetInstance.objects.filter(theme=self).count()

  def count_species(self):
    return self.valid_species.all().count()

  def has_species(self, species):
    if species in self.valid_species.all():
      return True
    return False


class Combination(models.Model):
  # Fields
  species = models.ForeignKey(
    to=Species,
    on_delete=models.CASCADE,
  )
  theme = models.ForeignKey(
    to=Theme,
    on_delete=models.CASCADE,
  )
  image = models.ImageField(
    upload_to="combinations",
  )

  # Metadata
  class Meta:
    ordering = ["species", "theme", ]
    constraints = [
      models.UniqueConstraint(
        fields=["species", "theme", ],
        name="%(app_label)s_%(class)s_species_theme_unique_together",
        violation_error_message="Combination of Species and Theme is not unique together."
      ),
    ]

  # Methods
  def __str__(self):
    return f"{self.species} species, in {self.theme} theme"

  def image_tag(self):
    return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)


class PetInstance(models.Model):
  # Fields
  name = models.CharField(
    max_length=18,
    unique=True,
    help_text="What name has been bestowed upon this beloved monster? Must be unique and cannot be changed. Letters and numbers only.",
    validators=[alphanumeric],
  )
  species = models.ForeignKey(
    to=Species,
    on_delete=models.CASCADE,
    help_text="What species (type of monster) is this pet?",
  )
  theme = models.ForeignKey(
    to=Theme,
    on_delete=models.SET_DEFAULT,
    default=1,
    help_text="What theme (variation in physical appearance and colour) is this pet?",
  )
  date_hatched = models.DateTimeField(
    auto_now_add=True,
    help_text="When did this beloved monster hatch?",
  )
  owner = models.ForeignKey(
    to=settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    help_text="Who does this beloved monster belong to?",
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
    return f"{self.name} the {self.theme} {self.species}"

  def has_combination(self):
    if self.theme in self.species.valid_themes.all():
      return True
    else:
      print(f"Combination of '{self.species}' species, in '{self.theme}' theme does not exist (for PetInstance '{self.name}').")
      return False

  def get_combination(self):
    if self.has_combination():
      return Combination.objects.get(
        Q(species=self.species) &
        Q(theme=self.theme)
      )
    else:
      return None

  def image_tag(self):
    if self.has_combination():
      return self.get_combination().image_tag()
    else:
      return None

