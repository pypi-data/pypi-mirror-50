<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install django-storages-s3-env
```

#### Pros
+   compatible with [django-storages S3 settings](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
+   create env with one command

#### How it works
hard-coded environment variables names:
+   `AWS_STORAGE_BUCKET_NAME`
+   `AWS_STORAGE_USER`
+   `AWS_ACCESS_KEY_ID`
+   `AWS_SECRET_ACCESS_KEY`

#### Scripts usage
command|`usage`
-|-
`storages-s3-create-env` |`usage: storages-s3-create-env bucket`

#### Examples
`Makefile`, create env
```bash
MEDIA_BUCKET:=BUCKET_NAME
all:
    test -s .env.prod.media || storages-s3-create-env $(MEDIA_BUCKET) > .env.prod.media
```

#### Links
+   [django-storages](https://django-storages.readthedocs.io/en/latest/index.html)

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>