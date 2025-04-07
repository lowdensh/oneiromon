from .models import Species, Style, Combination, PetInstance
from django.contrib import admin


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("name", "date_discovered", "description", )
  list_display_links = ("name", )
  search_fields = ("name", "description",)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("name", "description", )
  list_display_links = ("name", )
  search_fields = ("name", "description",)


@admin.register(PetInstance)
class PetInstanceAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("name", "style", "species", "date_hatched", "owner", )
  list_display_links = ("name", )
  list_filter = ("style", "species", "owner", )
  ordering = ("owner", "name", )
  search_fields = ("name", )

  # Specific object instance
  readonly_fields = ["date_hatched", ]


@admin.register(Combination)
class CombinationAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("__str__", "style", "species", )
  list_display_links = ()
  list_filter = ("style", "species", )

