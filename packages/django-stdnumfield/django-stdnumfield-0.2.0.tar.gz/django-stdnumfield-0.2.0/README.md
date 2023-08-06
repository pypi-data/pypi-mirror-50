[![CircleCI](https://circleci.com/gh/frnhr/django-stdnumfield/tree/master.svg?style=shield)](https://circleci.com/gh/frnhr/django-stdnumfield/tree/master)
[![codecov](https://codecov.io/gh/frnhr/django-stdnumfield/branch/master/graph/badge.svg)](https://codecov.io/gh/frnhr/django-stdnumfield)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

version: 0.2.0

## What's an stdnum?

See [python-stdnum](https://arthurdejong.org/python-stdnum/doc/1.5/index.html)


## Usage:

    from stdnumfield.models import StdNumField


    class SomeMode(models.Model):
        field = StdNumField(
            'hr.oib',  # stdnum format
        )


    class SampleModelForm(ModelForm):
        class Meta:
            model = SomeModel
            fields = ('field',)
            error_messages = {
                'field': {
                    'stdnum_format':_("Not maching format %(format_list)s"),  # you can override exception message
                },
            }


## Local development and testing

There is a gazillion ways of managing Python versions these days. I prefer 
pip and [pyenv](https://github.com/pyenv/pyenv):
``` bash
pyenv install --skip-existing 3.7.4
pyenv install --skip-existing 3.6.9
pyenv install --skip-existing 3.5.7
pyenv install --skip-existing 2.7.16
pyenv virtualenv 3.7.4 django-stdnumfield
echo 'django-stdnumfield:2.7.16:3.6.9:3.5.7' > .python-version
pip install -e .[dev]
```

Run the test project with:
``` bash
cd testproject
./manage.py migrate
./manage.py runserver
```
Then navigate to:
  * http://localhost:8000/sample_form/
  * http://localhost:8000/model_form/

A valid number to test with: `12345678903` 
