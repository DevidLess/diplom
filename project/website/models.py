from datetime import datetime

import django
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser


def validate_file_extension(value):
    if not value.name.endswith(".docx"):
        raise ValidationError(u"Необходим файл в формате Word (*.docx)")


class UserType(models.Model):
    """Роли пользователя"""

    title = models.CharField("Название", "title", max_length=255)
    """Название"""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип пользователя"
        verbose_name_plural = "Типы пользователя"


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь"""

    db_table = "auth_user"

    middle_name = models.CharField("Отчество", max_length=50, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=255, null=True, blank=True)
    address = models.CharField("Адрес", max_length=255, null=True, blank=True)
    user_type = models.ForeignKey(
        "UserType",
        on_delete=models.SET_NULL,
        verbose_name="Тип пользователя",
        null=True,
        blank=True,
    )
    report_date_1 = models.DateField("Начало периода", null=True, blank=True)
    report_date_2 = models.DateField("Окончание периода", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def title_short(self):
        short = ""
        if self.first_name:
            short += self.first_name[0] + "."
        if self.middle_name:
            short += self.middle_name[0] + "."
        if short:
            short = " " + short
        return f"{self.last_name}{short}"

    def title_long(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class CourtDistrict(models.Model):
    """Судебный участок"""

    title = models.CharField("Название", "title", max_length=255)
    """Название"""
    address = models.CharField("Адрес", "address", max_length=255)
    """Адрес"""
    phone = models.CharField("Телефон", "phone", max_length=255)
    """Телефон"""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Судебный участок"
        verbose_name_plural = "Судебные участки"


class CourtOrderStatus(models.Model):
    """Статус судебного приказа"""

    title = models.CharField("Название", "title", max_length=255)
    """Название предмета"""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус судебного приказа"
        verbose_name_plural = "Статусы судебного приказа"


class Template(models.Model):
    """Шаблон документа"""

    title = models.CharField("Название", "title", max_length=255)
    """Название"""
    description = models.TextField("Описание", "description", null=True, blank=True)
    """Описание"""
    file = models.FileField(
        "Файл шаблона (docx)",
        "file",
        null=True,
        blank=True,
        upload_to="templates/",
        validators=[validate_file_extension],
    )
    """Файл шаблона (docx)"""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Шаблон документа"
        verbose_name_plural = "Шаблоны документов"


class CourtOrderCategory(models.Model):
    """Категория судебного приказа"""

    title = models.CharField("Название", "title", max_length=255)
    """Название"""
    templates = models.ManyToManyField("Template", verbose_name="Шаблоны", blank=True)
    """Шаблоны"""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория судебного приказа"
        verbose_name_plural = "Категории судебных приказов"


class CourtOrder(models.Model):
    registration_date = models.DateTimeField(
        "Дата регистрации",
        help_text="дата регистрации",
        default=django.utils.timezone.now,
    )
    """Дата регистрации"""
    date = models.DateField("Дата", "date")
    """Дата"""
    number = models.CharField("Номер", "number", max_length=255)
    """Номер"""
    claimant = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        verbose_name="Истец",
        related_name="claimant",
        null=True,
        blank=True,
    )
    """Истец"""
    defendant = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        verbose_name="Ответчик",
        related_name="defendant",
        null=True,
        blank=True,
    )
    """Ответчик"""
    content = models.TextField("Содержание", "content", null=True, blank=True)
    """Содержание"""
    court_district = models.ForeignKey(
        "CourtDistrict",
        on_delete=models.RESTRICT,
        verbose_name="Судебный участок",
        null=True,
        blank=True,
    )
    """Судебный участок"""
    author = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        verbose_name="Автор",
        related_name="author",
        null=True,
        blank=True,
    )
    """Автор"""
    status = models.ForeignKey(
        "CourtOrderStatus",
        on_delete=models.RESTRICT,
        verbose_name="Статус",
        related_name="status",
        null=True,
        blank=True,
    )
    """Статус"""
    category = models.ForeignKey(
        "CourtOrderCategory",
        on_delete=models.RESTRICT,
        verbose_name="Категория",
        null=True,
        blank=True,
    )
    """Категория"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_id_ = self.status_id

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.status_id != self.status_id_:
            self.status_id_ = self.status_id
            history = CourtOrderHistory()
            history.registration_date = datetime.now()
            history.court_order = self
            history.user = self.author
            history.status = self.status
            history.save()
            print(self.id)

    def __str__(self):
        return (
            "Приказ № "
            + self.number.__str__()
            + " от "
            + self.registration_date.__format__("%d.%m.%Y")
        )

    class Meta:
        verbose_name = "Судебный приказ"
        verbose_name_plural = "Судебные приказы"


class CourtOrderHistory(models.Model):
    """История статусов приказа"""

    registration_date = models.DateTimeField("Дата", "registration_date", default=datetime.now())
    """Дата"""
    court_order = models.ForeignKey(
        "CourtOrder",
        on_delete=models.RESTRICT,
        verbose_name="Судебный приказ",
        null=True,
        blank=True,
    )
    """Судебный приказ"""
    user = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    """Пользователь"""
    status = models.ForeignKey(
        "CourtOrderStatus",
        on_delete=models.RESTRICT,
        verbose_name="Статус",
        null=True,
        blank=True,
    )
    """Статус"""

    def __str__(self):
        return "#" + self.id.__str__() + " от " + self.registration_date.__format__("%d.%m.%Y")

    class Meta:
        verbose_name = "История статусов приказа"
        verbose_name_plural = "История статусов приказа"


class CancellationRequestStatus(models.Model):
    """Статус заявления"""

    title = models.CharField("Название", "title", max_length=255)
    """Название предмета"""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус заявления об отмене судебного приказа"
        verbose_name_plural = "Статусы заявления об отмене судебного приказа "


class CancellationRequest(models.Model):
    """Заявление об отмене судебного приказа"""

    registration_date = models.DateTimeField("Дата", "registration_date", default=datetime.now())
    """Дата"""
    court_order = models.ForeignKey(
        "CourtOrder",
        on_delete=models.RESTRICT,
        verbose_name="Судебный приказ",
        null=True,
        blank=True,
    )
    """Судебный приказ"""
    user = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    """Пользователь"""
    content = models.TextField("Содержание", "content", null=True, blank=True)
    """Содержание"""
    status = models.ForeignKey(
        "CancellationRequestStatus",
        on_delete=models.RESTRICT,
        verbose_name="Статус",
        null=True,
        blank=True,
    )
    """Статус"""

    def status_history(self):
        return CancellationRequestHistory.objects.filter(cancellation_request=self).all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_id_ = self.status_id

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert, force_update, using, update_fields)

        if self.status_id != self.status_id_:
            self.status_id_ = self.status_id
            history = CancellationRequestHistory()
            history.registration_date = datetime.now()
            history.cancellation_request = self
            history.user = self.user
            history.status = self.status
            history.save()
            print(self.id)

    def __str__(self):

        return (
            "Заявление № "
            + self.id.__str__()
            + " от "
            + self.registration_date.__format__("%d.%m.%Y")
        )

    class Meta:
        verbose_name = "Заявление об отмене судебного приказа"
        verbose_name_plural = "Заявления об отмене судебных приказов"


class CancellationRequestHistory(models.Model):
    """История статусов заявления об отмене судебного приказа"""

    registration_date = models.DateTimeField("Дата", "registration_date", default=datetime.now())
    """Дата"""
    cancellation_request = models.ForeignKey(
        "CancellationRequest",
        on_delete=models.CASCADE,
        verbose_name="Заявление",
        null=True,
        blank=True,
    )
    """Судебный приказ"""
    user = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    """Пользователь"""
    status = models.ForeignKey(
        "CancellationRequestStatus",
        on_delete=models.RESTRICT,
        verbose_name="Статус",
        null=True,
        blank=True,
    )
    """Статус"""

    def __str__(self):
        return "#" + self.id.__str__() + " от " + self.registration_date.__format__("%d.%m.%Y")

    class Meta:
        verbose_name = "История статусов заявления"
        verbose_name_plural = "История статусов заявления"
