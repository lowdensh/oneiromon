from .models import Species, Theme, Combination, PetInstance
from django.contrib import admin
from django.utils.html import mark_safe


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("name", "count_pet_instances", "count_themes", "description", "date_discovered", )
  list_display_links = ("name", )
  search_fields = ("name", "description",)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("name", "count_pet_instances", "count_species", "description", )
  list_display_links = ("name", )
  search_fields = ("name", "description",)


@admin.register(PetInstance)
class PetInstanceAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("image_tag", "name", "theme", "species", "date_hatched", "owner", )
  list_display_links = ("name", )
  list_filter = ("theme", "species", "owner", )
  ordering = ("owner", "name", )
  search_fields = ("name", )

  # Specific instance
  readonly_fields = ["date_hatched", "image_tag", ]


@admin.register(Combination)
class CombinationAdmin(admin.ModelAdmin):
  # Main list of all objects
  list_display = ("image_tag", "__str__", "theme", "species", )
  list_display_links = ("image_tag", "__str__", )
  list_filter = ("theme", "species", )

  # Specific instance
  readonly_fields = ["image_tag", ]

