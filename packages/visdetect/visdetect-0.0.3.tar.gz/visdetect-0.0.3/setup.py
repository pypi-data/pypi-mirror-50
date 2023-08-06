from setuptools import setup

setup(
    name='visdetect',
    version='0.0.3',
    description='Visual error analysis for detection tasks',
    author='Shiva Pentyala',
    author_email='pk123@tamu.edu',
    packages=['visdetect', 'visdetect/helpers'],
    install_requires=(
            'matplotlib==3.1.1',
            'numpy==1.16.4',
            'opencv-python',
            'pandas==0.25.0',
            'Pillow>=4.0.0',
            'setuptools==41.0.1',
            'tensorflow==1.13.1',
            'tqdm==4.32.2'),
    scripts=['bin/visdetect'],
    zip_safe=False
)