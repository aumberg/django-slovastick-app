from setuptools import setup, find_packages

setup(
    name='django-slovastick-app',
    description=\
        'Research in the perception of sound information based on the Braille',
    version="0.0.1",
    packages=find_packages(),
    author='Alexander Umberg',
    author_email='slovastick@mail.ru',
    url='https://github.com/aumberg/django-slovastick-app',
    license='GPL v2',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)

print "all ok :)"