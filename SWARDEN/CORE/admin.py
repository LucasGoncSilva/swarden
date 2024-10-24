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
                    backgroundColor: ['#{MAIN_COLOR}aa', '#{DIS_COLOR}aa'],
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
                    backgroundColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}aa'],
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
                        '#{SEC_COLOR}aa',
                        '#{THIRD_COLOR}aa'
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
                        '#{SEC_COLOR}aa',
                        '#{THIRD_COLOR}aa',
                        '#{DIS_COLOR}aa'
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
                    backgroundColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}aa'],
                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%'
            }}
        }});
    </script>"""


class sWardenAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['admin_dashboard'] = {
            'range': range(5),
            'graph1': graph1(),
            'graph2': graph2(),
            'graph3': graph3(),
            'graph4': graph4(),
            'graph5': graph5(),
        }

        return super().index(request, extra_context=extra_context)


swarden_admin = sWardenAdminSite(name='customadmin')
swarden_admin.register(Group, GroupAdmin)
