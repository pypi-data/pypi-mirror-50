<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install find-python-packages
```

#### Scripts usage
command|`usage`
-|-
`find-python-packages` |`usage: find-python-packages path`

#### Examples
```
apps/__init__.py
apps/app1/__init__.py
apps/app2/__init__.py
settings/__init__.py
```

```bash
$ find-python-packages . | grep apps
apps
apps.app1
apps.app2
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>