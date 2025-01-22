notes: list[tuple[str, str]] = [
    ('wrk', 'Trabalho'),
    ('std', 'Estudo'),
    ('cmt', 'Compromisso'),
    ('fml', 'Família'),
    ('hlt', 'Saúde'),
    ('fin', 'Finança'),
    ('trv', 'Viagem'),
    ('vol', 'Voluntariado'),
    ('esp', 'Espiritualidade'),
    ('leg', 'Assuntos Legais'),
]

banks: list[tuple[str, str]] = [
    ('banco-do-brasil--', 'Banco do Brasil'),
    ('original--', 'Banco Original'),
    ('bradesco--', 'Bradesco'),
    ('caixa--', 'Caixa'),
    ('itau--', 'Itaú'),
    ('next--', 'Next'),
    ('nubank--', 'Nubank'),
    ('pao-de-acucar--', 'Pão de Açúcar'),
    ('pagseguro--', 'PagSeguro'),
    ('paypal--', 'PayPal'),
    ('santander--', 'Santander'),
    ('ticket--', 'Ticket'),
]

brands: list[tuple[str, str]] = [
    ('american-express--', 'American Express'),
    ('diners-club-international--', 'Diners Club International'),
    ('elo--', 'Elo'),
    ('hipercard--', 'Hipercard'),
    ('mastercard--', 'Mastercard'),
    ('visa--', 'Visa'),
]

cards_types: list[tuple[str, str]] = [
    ('deb', 'Débito'),
    ('cred', 'Crédito'),
    ('pre', 'Pré-pago'),
    ('co', 'Co-branded'),
]

services: list[tuple[str, str]] = (
    [
        ('aws--', 'AWS'),
        ('adobe--', 'Adobe'),
        ('airbnb--', 'Airbnb'),
        ('amazon--', 'Amazon'),
        ('prime-video--', 'Amazon Prime Video'),
        ('apple--', 'Apple'),
        ('booking--', 'Booking'),
        ('deezer--', 'Deezer'),
        ('discord--', 'Discord'),
        ('disney-plus--', 'Disney+'),
        ('epic-games--', 'Epic Games'),
        ('facebook--', 'Facebook'),
        ('github--', 'Github'),
        ('google--', 'Google'),
        ('gov-br--', 'Gov BR'),
        ('heroku--', 'Heroku'),
        ('instagram--', 'Instagram'),
        ('kayak--', 'Kayak'),
        ('linkedin--', 'LinkedIn'),
        ('magalu--', 'Magazine Luiza'),
        ('mercado-livre--', 'Mercado Livre'),
        ('netflix--', 'Netflix'),
        ('notion--', 'Notion'),
        ('nu-invest--', 'Nu Invest'),
        ('outlook--', 'Outlook'),
        ('pinterest--', 'Pinterest'),
        ('reddit--', 'Reddit'),
        ('spotify--', 'Spotify'),
        ('steam--', 'Steam'),
        ('stripe--', 'Stripe'),
        ('submarino--', 'Submarino'),
        ('ticket--', 'Ticket'),
        ('trello--', 'Trello'),
        ('trip-advisor--', 'Trip Advisor'),
        ('twitch--', 'Twitch'),
        ('twitter--', 'Twitter'),
        ('vercel--', 'Vercel'),
        ('wordpress--', 'Wordpress'),
        ('yahoo--', 'Yahoo'),
        ('atari--', 'Atari'),
        ('blizzard--', 'Blizzard Entertainment'),
        ('lg--', 'LG'),
        ('motorola--', 'Motorola'),
        ('nintendo--', 'Nintendo'),
        ('playstation--', 'PlayStation'),
        ('riot-games--', 'Riot Games'),
        ('samsung--', 'Samsung'),
        ('skype--', 'Skype'),
        ('slack--', 'Slack'),
        ('supercell--', 'Supercell'),
        ('wargaming--', 'Wargaming'),
        ('xbox--', 'Xbox'),
        ('amil--', 'Amil'),
        ('cma--', 'CMA Vantagens'),
        ('glassdoor--', 'Glassdoor'),
        ('hapvida--', 'Hapvida'),
        ('indeed--', 'Indeed'),
        ('notredame-intermedica--', 'Notredame Intermédica'),
        ('porto-seguro--', 'Porto Seguro'),
        ('prevent-senior--', 'Prevent Senior'),
        ('revelo--', 'Revelo'),
        ('sulamerica--', 'Sulamerica'),
        ('unimed--', 'Unimed'),
    ]
    + banks
    + brands
)


cards_banks: list[tuple[str, str]] = sorted(set(banks), key=lambda x: x[1])
cards_brands: list[tuple[str, str]] = sorted(set(brands), key=lambda x: x[1])
credentials_services: list[tuple[str, str]] = sorted(set(services), key=lambda x: x[1])
notes_types: list[tuple[str, str]] = sorted(set(notes), key=lambda x: x[1])

cards_banks.insert(0, ('nao-listado--', 'NÃO LISTADO'))
cards_brands.insert(0, ('nao-listado--', 'NÃO LISTADO'))
credentials_services.insert(0, ('nao-listado--', 'NÃO LISTADO'))
notes_types.append(('oth', 'Outro'))
