# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .managers import CustomUserManager

class Aula(models.Model):
    cod_aula = models.IntegerField(primary_key=True)
    tema_aula = models.CharField(max_length=100, blank=True, null=True)
    cod_hab = models.ForeignKey('Habilidades', models.DO_NOTHING, db_column='cod_hab', blank=True, null=True)
    desc_aula = models.TextField(blank=True, null=True)
    cod_doc = models.ForeignKey('Docente', models.DO_NOTHING, db_column='cod_doc', blank=True, null=True)
    cod_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='cod_turma', blank=True, null=True)
    # disciplina = models.ForeignKey('Disciplina', models.DO_NOTHING, db_column='cod_disc', blank=True, null=True)
    fluxo_aula = models.CharField(max_length=500, blank=True, null=True)
    info_adicionais = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aula'

class Coordenacao(models.Model):
    cod_coord = models.IntegerField(primary_key=True)
    nome_coord = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coordenacao'


class Direcao(models.Model):
    cod_dir = models.IntegerField(primary_key=True)
    nome_dir = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direcao'


class Disciplina(models.Model):
#     def first():
#         return Turma.objects.last().cod_disc + 1
    
    cod_disc = models.AutoField(primary_key=True, default=0)
    nome_disc = models.CharField(max_length=45, blank=True, null=True)
    cod_aula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='cod_aula', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disciplina'


class Docente(models.Model):
    cod_doc = models.IntegerField(primary_key=True)
    nome_doc = models.CharField(max_length=45, blank=True, null=True)
    eventual_doc = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    cod_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='cod_turma', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docente'


class Habilidades(models.Model):
    cod_hab = models.CharField(primary_key=True, max_length=12)
    habilidade = models.CharField(max_length=60, blank=True, null=True)
    desc_habilidade = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habilidades'


class Turma(models.Model):
    cod_turma = models.IntegerField(primary_key=True)
    nome_turma = models.CharField(max_length=45, blank=True, null=True)
    cod_disc = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='cod_disc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turma'

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('O nome do usuário deve ser fornecido'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    nome = models.CharField(max_length=100, blank=False, null=False)
    rg = models.PositiveIntegerField(unique=True)    
    cargo = models.CharField(max_length=20, blank=True, null=True)
    is_temporary_teacher = models.BooleanField(default=False)
    # cod_disc = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    # cod_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'rg'
    REQUIRED_FIELDS = ['nome']
    
    def get_usuario(self):
        return f'{self.nome}'

    def __str__(self):
        return str(self.rg)    
        