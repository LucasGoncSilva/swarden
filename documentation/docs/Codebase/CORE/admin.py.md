
# File: `admin.py`
Path: `SWARDEN.CORE`



---

## Imports

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```

### `#!py import AdminSite`

Path: `#!py django.contrib.admin`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.admin import AdminSite
    ```

### `#!py import GroupAdmin`

Path: `#!py django.contrib.auth.admin`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.admin import GroupAdmin
    ```

### `#!py import Group`

Path: `#!py django.contrib.auth.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.models import Group
    ```

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import SecurityNote
    ```



---

## Consts

### `#!py MAIN_COLOR`

Type: `#!py str`

Value: `#!py '417690'`

??? example "SNIPPET"

    ```py
    MAIN_COLOR: str = '417690'
    ```

### `#!py SEC_COLOR`

Type: `#!py str`

Value: `#!py 'a3aabe'`

??? example "SNIPPET"

    ```py
    SEC_COLOR: str = 'a3aabe'
    ```

### `#!py THIRD_COLOR`

Type: `#!py str`

Value: `#!py 'bcc8cc'`

??? example "SNIPPET"

    ```py
    THIRD_COLOR: str = 'bcc8cc'
    ```

### `#!py DIS_COLOR`

Type: `#!py str`

Value: `#!py '777777'`

??? example "SNIPPET"

    ```py
    DIS_COLOR: str = '777777'
    ```



---

## Classes

### `#!py class sWardenAdminSite`

Parents: `AdminSite`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class sWardenAdminSite(AdminSite):
        site_header = 'Administração Geral | sWarden'
        site_title = 'Admin'

        def index(self, request, extra_context=None):
            extra_context = extra_context or {}
            extra_context['admin_dashboard'] = {'range': range(6), 'graph1': graph1(), 'graph2': graph2(), 'graph3': graph3(), 'graph4': graph4(), 'graph5': graph5(), 'graph6': graph6()}
            return super().index(request, extra_context=extra_context)
    ```



---

## Functions

### `#!py def graph1`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def graph1() -> str:
        return f"<script>\n        new Chart(document.getElementById('graph1'), {{\n            type: 'doughnut',\n            data: {{\n                labels: ['Usuários Ativos', 'Usuários Inativos'],\n                datasets: [{{\n                    data: [\n                        {User.objects.filter(is_active=True).count()},\n                        {User.objects.filter(is_active=False).count()},\n                    ],\n                    backgroundColor: ['#{MAIN_COLOR}', '#{DIS_COLOR}'],\n                    borderColor: ['#{MAIN_COLOR}', '#{DIS_COLOR}'],\n                    borderWidth: 3\n                }}]\n            }},\n            options: {{\n                cutout: '60%'\n            }}\n        }});\n    </script>"
    ```

### `#!py def graph2`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def graph2() -> str:
        return f"<script>\n        new Chart(document.getElementById('graph2'), {{\n            type: 'bar',\n            data: {{\n                labels: ['Usuários', 'Segredos'],\n                datasets: [{{\n                    data: [\n                        {User.objects.count()},\n                        {Card.objects.count() + LoginCredential.objects.count() + SecurityNote.objects.count()},\n                    ],\n                    label: 'Segredos / Usuários',\n                    backgroundColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],\n                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],\n                    borderWidth: 3\n                }}]\n            }},\n            options: {{\n                maintainAspectRatio: false,\n                title: {{\n                    display: false,\n                }},\n                scales: {{\n                    y: {{\n                        type: 'logarithmic'\n                    }}\n                }}\n            }}\n        }});\n    </script>"
    ```

### `#!py def graph3`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def graph3() -> str:
        return f"<script>\n        new Chart(document.getElementById('graph3'), {{\n            type: 'doughnut',\n            data: {{\n                labels: ['Cards', 'Creds', 'Notas'],\n                datasets: [{{\n                    data: [\n                        {Card.objects.count()},\n                        {LoginCredential.objects.count()},\n                        {SecurityNote.objects.count()},\n                    ],\n                    backgroundColor: [\n                        '#{MAIN_COLOR}',\n                        '#{SEC_COLOR}',\n                        '#{THIRD_COLOR}'\n                    ],\n                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}', '#{THIRD_COLOR}'],\n                    borderWidth: 3\n                }}]\n            }},\n            options: {{\n                cutout: '60%'\n            }}\n        }});\n    </script>"
    ```

### `#!py def graph4`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def graph4() -> str:
        return f"<script>\n        new Chart(document.getElementById('graph4'), {{\n            type: 'doughnut',\n            data: {{\n                labels: ['Cards Crédito', 'Cards Débito', 'Cards Pré', 'Cards Co'],\n                datasets: [{{\n                    data: [\n                        {Card.objects.filter(card_type='cred').count()},\n                        {Card.objects.filter(card_type='deb').count()},\n                        {Card.objects.filter(card_type='pre').count()},\n                        {Card.objects.filter(card_type='co').count()},\n                    ],\n                    backgroundColor: [\n                        '#{MAIN_COLOR}',\n                        '#{SEC_COLOR}',\n                        '#{THIRD_COLOR}',\n                        '#{DIS_COLOR}'\n                    ],\n                    borderColor: [\n                        '#{MAIN_COLOR}',\n                        '#{SEC_COLOR}',\n                        '#{THIRD_COLOR}',\n                        '#{DIS_COLOR}'\n                    ],\n                    borderWidth: 3\n                }}]\n            }},\n            options: {{\n                cutout: '60%'\n            }}\n        }});\n    </script>"
    ```

### `#!py def graph5`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def graph5() -> str:
        return f"<script>\n        new Chart(document.getElementById('graph5'), {{\n            type: 'doughnut',\n            data: {{\n                labels: ['Creds de Login Próprio', 'Creds de Login de 3º'],\n                datasets: [{{\n                    data: [\n                        {LoginCredential.objects.filter(third_party_login=True).count()},\n                        {LoginCredential.objects.filter(third_party_login=False).count()},\n                    ],\n                    backgroundColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],\n                    borderColor: ['#{MAIN_COLOR}', '#{SEC_COLOR}'],\n                    borderWidth: 3\n                }}]\n            }},\n            options: {{\n                cutout: '60%'\n            }}\n        }});\n    </script>"
    ```

### `#!py def graph6`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def graph6() -> str:
        lst: list[tuple[str, int]] = [('leg', SecurityNote.objects.filter(note_type='leg').count()), ('cmt', SecurityNote.objects.filter(note_type='cmt').count()), ('esp', SecurityNote.objects.filter(note_type='esp').count()), ('std', SecurityNote.objects.filter(note_type='std').count()), ('fml', SecurityNote.objects.filter(note_type='fml').count()), ('fin', SecurityNote.objects.filter(note_type='fin').count()), ('hlt', SecurityNote.objects.filter(note_type='hlt').count()), ('wrk', SecurityNote.objects.filter(note_type='wrk').count()), ('trv', SecurityNote.objects.filter(note_type='trv').count()), ('vol', SecurityNote.objects.filter(note_type='vol').count()), ('oth', SecurityNote.objects.filter(note_type='oth').count())]
        sorted_lst: list[tuple[str, int]] = list(sorted(lst, key=lambda i: i[1], reverse=True))
        return f"<script>\n        new Chart(document.getElementById('graph6'), {{\n            type: 'doughnut',\n            data: {{\n                labels: [\n                    'Notas {sorted_lst[0][0].title()}',\n                    'Notas {sorted_lst[1][0].title()}',\n                    'Notas {sorted_lst[2][0].title()}',\n                    'Demais notas',\n                ],\n                datasets: [{{\n                    data: [\n                        {sorted_lst[0][1]},\n                        {sorted_lst[1][1]},\n                        {sorted_lst[2][1]},\n                        {sum([i[1] for i in sorted_lst[3:]])},\n                    ],\n                    backgroundColor: [\n                        '#{MAIN_COLOR}',\n                        '#{SEC_COLOR}',\n                        '#{THIRD_COLOR}',\n                        '#{DIS_COLOR}',\n                    ],\n                    borderColor: [\n                        '#{MAIN_COLOR}',\n                        '#{SEC_COLOR}',\n                        '#{THIRD_COLOR}',\n                        '#{DIS_COLOR}',\n                    ],\n                    borderWidth: 3\n                }}]\n            }},\n            options: {{\n                cutout: '60%'\n            }}\n        }});\n    </script>"
    ```

### `#!py def index`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, request: Unknown, extra_context: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['admin_dashboard'] = {'range': range(6), 'graph1': graph1(), 'graph2': graph2(), 'graph3': graph3(), 'graph4': graph4(), 'graph5': graph5(), 'graph6': graph6()}
        return super().index(request, extra_context=extra_context)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
