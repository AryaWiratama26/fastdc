from setuptools import setup, find_packages

setup(
    name='fastdc',
    version='1.0',
    author='Arya Wiratama',
    author_email='aryawiratama2401@gmail.com',
    description='FastDC: A fast, modular, and AI-integrated Discord bot framework.',
    packages=find_packages(),
    package_data={"fastdc": ["*.py"]},
    install_requires=[
        'discord.py',
        'chatterbot',
        'spacy',
        'python-dotenv',
        'groq',
    ],
    python_requires='>=3.10',
)
