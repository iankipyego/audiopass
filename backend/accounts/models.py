import zoneinfo

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Hospital(models.Model):
    """A hospital tenant.

    Every tenant-owned record (children, screenings, ...) will be scoped to a
    Hospital, and every user belongs to a Hospital so that one hospital can
    never see another hospital's data (CLAUDE.md, rule 2).
    """

    name = models.CharField(max_length=200)
    # IANA timezone string, e.g. "Africa/Nairobi". Stored as plain text so we
    # can compute due dates and display times in each hospital's local time.
    # Validated in clean() to catch typos like "Afric/Nairobi".
    timezone = models.CharField(max_length=64, default="Africa/Nairobi")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()
        try:
            zoneinfo.ZoneInfo(self.timezone)
        except Exception as exc:  # invalid or unknown IANA key
            raise ValidationError({"timezone": f"Invalid timezone: {self.timezone!r}"}) from exc


class User(AbstractUser):
    """Custom user tied to a Hospital with a screening role.

    Roles (per CLAUDE.md):
      - admin:      hospital administrator
      - supervisor: oversees screeners and reviews referrals
      - screener:   performs OAE screenings (default, least privilege)

    Note: `role` is the application-level screening role and is separate from
    Django's `is_staff` (admin-site access) and `is_superuser` (all
    permissions, cross-hospital). A site-wide superuser may have no hospital.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        SUPERVISOR = "supervisor", "Supervisor"
        SCREENER = "screener", "Screener"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SCREENER,
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"

    def clean(self) -> None:
        super().clean()
        # Multi-tenant integrity: every real user must belong to a hospital.
        # Only a site-wide superuser (bootstrap / cross-hospital oversight) may
        # have a null hospital.
        if not self.is_superuser and not self.hospital_id:
            raise ValidationError(
                {"hospital": "Non-superuser users must be assigned to a hospital."}
            )
