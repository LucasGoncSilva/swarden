from account.models import User
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from secret.models import Card, LoginCredential, SecurityNote


MAIN_COLOR: str = '417690'
SEC_COLOR: str = 'a3aabe'
THIRD_COLOR: str = 'bcc8cc'
DIS_COLOR: str = '777777'


def graph1() -> str:
    return f"""<script>
        new Chart(document.getElementById('graph1'), {{
            type: 'doughnut',
            data: {{
                labels: ['Usuários Ativos', 'Usuários Inativos'],
                datasets: [{{
                    data: [
                        {User.objects.filter(is_active=True).count()},
                        {User.objects.filter(is_active=False).count()},
                    ],
                    backgroundColor: ['#{MAIN_COLOR}', '#{DIS_COLOR}'],
                    borderColor: ['#{MAIN_COLOR}', '#{DIS_COLOR}'],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%'
            }}
        }});
    </script>"""


def graph2() -> str:
    return f"""<script>
        new Chart(document.getElementById('graph2'), {{
            type: 'bar',
            data: {{
                labels: ['Usuários', 'Segredos'],
                datasets: [{{
                    data: [
                        {User.objects.count()},
                        {
        Card.objects.count()
        + LoginCredential.objects.count()
        + SecurityNote.objects.count()
    },
                    ],
                    label: 'Segredos / Usuários',
                    backgroundColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],
                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],
                    borderWidth: 3
                }}]
            }},
            options: {{
                maintainAspectRatio: false,
                title: {{
                    display: false,
                }},
                scales: {{
                    y: {{
                        type: 'logarithmic'
                    }}
                }}
            }}
        }});
    </script>"""


def graph3() -> str:
    return f"""<script>
        new Chart(document.getElementById('graph3'), {{
            type: 'doughnut',
            data: {{
                labels: ['Cards', 'Creds', 'Notas'],
                datasets: [{{
                    data: [
                        {Card.objects.count()},
                        {LoginCredential.objects.count()},
                        {SecurityNote.objects.count()},
                    ],
                    backgroundColor: [
                        '#{MAIN_COLOR}',
                        '#{SEC_COLOR}',
                        '#{THIRD_COLOR}'
                    ],
                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}', '#{THIRD_COLOR}'],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%'
            }}
        }});
    </script>"""


def graph4() -> str:
    return f"""<script>
        new Chart(document.getElementById('graph4'), {{
            type: 'doughnut',
            data: {{
                labels: ['Cards Crédito', 'Cards Débito', 'Cards Pré', 'Cards Co'],
                datasets: [{{
                    data: [
                        {Card.objects.filter(card_type='cred').count()},
                        {Card.objects.filter(card_type='deb').count()},
                        {Card.objects.filter(card_type='pre').count()},
                        {Card.objects.filter(card_type='co').count()},
                    ],
                    backgroundColor: [
                        '#{MAIN_COLOR}',
                        '#{SEC_COLOR}',
                        '#{THIRD_COLOR}',
                        '#{DIS_COLOR}'
                    ],
                    borderColor: [
                        '#{MAIN_COLOR}',
                        '#{SEC_COLOR}',
                        '#{THIRD_COLOR}',
                        '#{DIS_COLOR}'
                    ],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%'
            }}
        }});
    </script>"""


def graph5() -> str:
    return f"""<script>
        new Chart(document.getElementById('graph5'), {{
            type: 'doughnut',
            data: {{
                labels: ['Creds de Login Próprio', 'Creds de Login de 3º'],
                datasets: [{{
                    data: [
                        {LoginCredential.objects.filter(thirdy_party_login=True).count()},
                        {LoginCredential.objects.filter(thirdy_party_login=False).count()},
                    ],
                    backgroundColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],
                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%'
            }}
        }});
    </script>"""


def graph6() -> str:
    lst: list[tuple[str, int]] = [
        ('leg', SecurityNote.objects.filter(note_type='leg').count()),
        ('cmt', SecurityNote.objects.filter(note_type='cmt').count()),
        ('esp', SecurityNote.objects.filter(note_type='esp').count()),
        ('std', SecurityNote.objects.filter(note_type='std').count()),
        ('fml', SecurityNote.objects.filter(note_type='fml').count()),
        ('fin', SecurityNote.objects.filter(note_type='fin').count()),
        ('hlt', SecurityNote.objects.filter(note_type='hlt').count()),
        ('wrk', SecurityNote.objects.filter(note_type='wrk').count()),
        ('trv', SecurityNote.objects.filter(note_type='trv').count()),
        ('vol', SecurityNote.objects.filter(note_type='vol').count()),
        ('oth', SecurityNote.objects.filter(note_type='oth').count()),
    ]

    sorted_lst: list[tuple[str, int]] = list(
        sorted(lst, key=lambda i: i[1], reverse=True)
    )
    return f"""<script>
        new Chart(document.getElementById('graph6'), {{
            type: 'doughnut',
            data: {{
                labels: [
                    'Notas {sorted_lst[0][0].title()}',
                    'Notas {sorted_lst[1][0].title()}',
                    'Notas {sorted_lst[2][0].title()}',
                    'Demais notas',
                ],
                datasets: [{{
                    data: [
                        {sorted_lst[0][1]},
                        {sorted_lst[1][1]},
                        {sorted_lst[2][1]},
                        {sum([i[1] for i in sorted_lst[3:]])},
                    ],
                    backgroundColor: [
                        '#{MAIN_COLOR}',
                        '#{SEC_COLOR}',
                        '#{THIRD_COLOR}',
                        '#{DIS_COLOR}',
                    ],
                    borderColor: [
                        '#{MAIN_COLOR}',
                        '#{SEC_COLOR}',
                        '#{THIRD_COLOR}',
                        '#{DIS_COLOR}',
                    ],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%'
            }}
        }});
    </script>"""


class sWardenAdminSite(AdminSite):
    site_header = 'Administração Geral | sWarden'
    site_title = 'Admin'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['admin_dashboard'] = {
            'range': range(6),
            'graph1': graph1(),
            'graph2': graph2(),
            'graph3': graph3(),
            'graph4': graph4(),
            'graph5': graph5(),
            'graph6': graph6(),
        }

        return super().index(request, extra_context=extra_context)


swarden_admin = sWardenAdminSite(name='customadmin')
swarden_admin.register(Group, GroupAdmin)
