from setuptools import setup, find_packages


setup(
    name             = 'KoreanInput',
    version          = '1.0',
    description      = 'Korean Input for Pygame',
    author           = 'Jaesuk Lim',
    author_email     = 'flight0454@gmail.com',
    #url              = 'https://github.com/flight0454/KorInput',
    #download_url     = 'https://github.com/rampart81/pyquibase/archive/1.2.tar.gz',
    install_requires = ['hgtk','pygame','text-to-image','Pillow' ],
    packages         = find_packages(exclude = ['docs', 'tests*']),
    keywords         = ['Korean', 'KoreanKeyboard'],
    python_requires  = '>=3',
    package_data     =  {
        'KorInput' : [
            'NanumSquareRoundB.ttf'

        ]},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
