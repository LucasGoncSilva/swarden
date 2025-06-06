
# File: `0001_initial.py`
Path: `SWARDEN.secret.migrations`



---

## Imports

### `#!py import django.core.validators`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.core.validators
    ```

### `#!py import django.db.models.deletion`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.db.models.deletion
    ```

### `#!py import secret.month.models`

Path: `#!py None`

Category: Local

??? example "SNIPPET"

    ```py
    import secret.month.models
    ```

### `#!py import uuid`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import uuid
    ```

### `#!py import settings`

Path: `#!py django.conf`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.conf import settings
    ```

### `#!py import migrations`

Path: `#!py django.db`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db import migrations
    ```

### `#!py import models`

Path: `#!py django.db`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db import models
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class Migration`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Migration(migrations.Migration):
        initial = True
        dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
        operations = [migrations.CreateModel(name='Card', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('name', models.CharField(max_length=40, validators=[django.core.validators.MaxLengthValidator(40)], verbose_name='Apelido (ex: Cartão da Família)')), ('card_type', models.CharField(choices=[('deb', 'Débito'), ('cred', 'Crédito'), ('pre', 'Pré-pago'), ('co', 'Co-branded')], max_length=4, validators=[django.core.validators.MaxLengthValidator(4)], verbose_name='Tipo (débito, crédito, ...)')), ('number', models.CharField(max_length=19, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.MaxLengthValidator(19)], verbose_name='Número do Cartão')), ('expiration', secret.month.models.MonthField(verbose_name='Data de Expiração')), ('cvv', models.CharField(max_length=4, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(4)], verbose_name='cvv')), ('bank', models.CharField(choices=[('nao-listado--', 'NÃO LISTADO'), ('original--', 'Banco Original'), ('banco-do-brasil--', 'Banco do Brasil'), ('bradesco--', 'Bradesco'), ('caixa--', 'Caixa'), ('itau--', 'Itaú'), ('next--', 'Next'), ('nubank--', 'Nubank'), ('pagseguro--', 'PagSeguro'), ('paypal--', 'PayPal'), ('pao-de-acucar--', 'Pão de Açúcar'), ('santander--', 'Santander'), ('ticket--', 'Ticket')], max_length=64, verbose_name='Banco')), ('brand', models.CharField(choices=[('nao-listado--', 'NÃO LISTADO'), ('american-express--', 'American Express'), ('diners-club-international--', 'Diners Club International'), ('elo--', 'Elo'), ('hipercard--', 'Hipercard'), ('mastercard--', 'Mastercard'), ('visa--', 'Visa')], max_length=64, verbose_name='Bandeira')), ('owners_name', models.CharField(max_length=64, validators=[django.core.validators.MaxLengthValidator(64)], verbose_name='Nome do Titular (como no cartão)')), ('note', models.TextField(blank=True, max_length=128, null=True, validators=[django.core.validators.MaxLengthValidator(128)], verbose_name='Anotação Particular')), ('slug', models.SlugField(max_length=128, validators=[django.core.validators.MaxLengthValidator(128)])), ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')), ('updated', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')), ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL, verbose_name='Dono'))], options={'verbose_name': 'Cartão', 'verbose_name_plural': 'Cartões', 'ordering': ['-created']}), migrations.CreateModel(name='LoginCredential', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('service', models.CharField(choices=[('nao-listado--', 'NÃO LISTADO'), ('aws--', 'AWS'), ('adobe--', 'Adobe'), ('airbnb--', 'Airbnb'), ('amazon--', 'Amazon'), ('prime-video--', 'Amazon Prime Video'), ('american-express--', 'American Express'), ('amil--', 'Amil'), ('apple--', 'Apple'), ('atari--', 'Atari'), ('original--', 'Banco Original'), ('banco-do-brasil--', 'Banco do Brasil'), ('blizzard--', 'Blizzard Entertainment'), ('booking--', 'Booking'), ('bradesco--', 'Bradesco'), ('cma--', 'CMA Vantagens'), ('caixa--', 'Caixa'), ('deezer--', 'Deezer'), ('diners-club-international--', 'Diners Club International'), ('discord--', 'Discord'), ('disney-plus--', 'Disney+'), ('elo--', 'Elo'), ('epic-games--', 'Epic Games'), ('facebook--', 'Facebook'), ('github--', 'Github'), ('glassdoor--', 'Glassdoor'), ('google--', 'Google'), ('gov-br--', 'Gov BR'), ('hapvida--', 'Hapvida'), ('heroku--', 'Heroku'), ('hipercard--', 'Hipercard'), ('indeed--', 'Indeed'), ('instagram--', 'Instagram'), ('itau--', 'Itaú'), ('kayak--', 'Kayak'), ('lg--', 'LG'), ('linkedin--', 'LinkedIn'), ('magalu--', 'Magazine Luiza'), ('mastercard--', 'Mastercard'), ('mercado-livre--', 'Mercado Livre'), ('motorola--', 'Motorola'), ('netflix--', 'Netflix'), ('next--', 'Next'), ('nintendo--', 'Nintendo'), ('notion--', 'Notion'), ('notredame-intermedica--', 'Notredame Intermédica'), ('nu-invest--', 'Nu Invest'), ('nubank--', 'Nubank'), ('outlook--', 'Outlook'), ('pagseguro--', 'PagSeguro'), ('paypal--', 'PayPal'), ('pinterest--', 'Pinterest'), ('playstation--', 'PlayStation'), ('porto-seguro--', 'Porto Seguro'), ('prevent-senior--', 'Prevent Senior'), ('pao-de-acucar--', 'Pão de Açúcar'), ('reddit--', 'Reddit'), ('revelo--', 'Revelo'), ('riot-games--', 'Riot Games'), ('samsung--', 'Samsung'), ('santander--', 'Santander'), ('skype--', 'Skype'), ('slack--', 'Slack'), ('spotify--', 'Spotify'), ('steam--', 'Steam'), ('stripe--', 'Stripe'), ('submarino--', 'Submarino'), ('sulamerica--', 'Sulamerica'), ('supercell--', 'Supercell'), ('ticket--', 'Ticket'), ('trello--', 'Trello'), ('trip-advisor--', 'Trip Advisor'), ('twitch--', 'Twitch'), ('twitter--', 'Twitter'), ('unimed--', 'Unimed'), ('vercel--', 'Vercel'), ('visa--', 'Visa'), ('wargaming--', 'Wargaming'), ('wordpress--', 'Wordpress'), ('xbox--', 'Xbox'), ('yahoo--', 'Yahoo')], max_length=64, validators=[django.core.validators.MaxLengthValidator(64)], verbose_name='Serviço')), ('name', models.CharField(max_length=40, validators=[django.core.validators.MaxLengthValidator(40)], verbose_name='Apelido (ex: Conta Principal)')), ('thirdy_party_login', models.BooleanField(verbose_name='Login com serviço de terceiro?')), ('thirdy_party_login_name', models.CharField(max_length=40, validators=[django.core.validators.MaxLengthValidator(40)], verbose_name='Apelido do serviço de terceiro')), ('login', models.CharField(max_length=200, validators=[django.core.validators.MaxLengthValidator(200)], verbose_name='Login')), ('password', models.CharField(max_length=200, validators=[django.core.validators.MaxLengthValidator(200)], verbose_name='Senha')), ('note', models.TextField(blank=True, max_length=128, null=True, validators=[django.core.validators.MaxLengthValidator(128)], verbose_name='Anotação particular')), ('slug', models.SlugField(max_length=128, validators=[django.core.validators.MaxLengthValidator(128)])), ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')), ('updated', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')), ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials', to=settings.AUTH_USER_MODEL, verbose_name='Dono'))], options={'verbose_name': 'Credencial', 'verbose_name_plural': 'Credenciais', 'ordering': ['-created']}), migrations.CreateModel(name='SecurityNote', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('title', models.CharField(max_length=40, validators=[django.core.validators.MaxLengthValidator(40)], verbose_name='Título')), ('content', models.TextField(max_length=300, validators=[django.core.validators.MaxLengthValidator(300)], verbose_name='Conteúdo')), ('note_type', models.TextField(choices=[('leg', 'Assuntos Legais'), ('cmt', 'Compromisso'), ('esp', 'Espiritualidade'), ('std', 'Estudo'), ('fml', 'Família'), ('fin', 'Finança'), ('hlt', 'Saúde'), ('wrk', 'Trabalho'), ('trv', 'Viagem'), ('vol', 'Voluntariado'), ('oth', 'Outro')], max_length=3, validators=[django.core.validators.MaxLengthValidator(3), django.core.validators.MinLengthValidator(3)], verbose_name='Classificação')), ('slug', models.SlugField(validators=[django.core.validators.MaxLengthValidator(50)])), ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')), ('updated', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')), ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL, verbose_name='Dono'))], options={'verbose_name': 'Nota de Segurança', 'verbose_name_plural': 'Notas de Segurança', 'ordering': ['-created']})]
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
