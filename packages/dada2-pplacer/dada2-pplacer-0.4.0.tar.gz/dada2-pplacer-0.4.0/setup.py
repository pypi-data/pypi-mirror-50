from setuptools import setup

setup(
    name='dada2-pplacer',
    version='0.4.0',
    description="""Convert output from dada2 to be compatible with pplacer / guppy / rppr pipelines
      """,
    url='https://github.com/jgolob/dada2-pplacer/',
    author='Jonathan Golob',
    author_email='j-dev@golob.org',
    license='MIT',
    packages=['dada2_pplacer'],
    zip_safe=False,
    install_requires=[
        'numpy>=1.13.3',
        'pandas>=0.20.3'
    ],
    entry_points={
        'console_scripts': [
            'dada2-seqtab-to-sharefile=dada2_pplacer.dada2_seqtab_to_pplacer:main',
            'dada2-seqtab-to-pplacer=dada2_pplacer.dada2_seqtab_to_pplacer:main',
            'dada2-taxonomy-to-tallies-wide=dada2_pplacer.dada2_taxonomy_to_tallies_wide:main'
        ],
    }
)
