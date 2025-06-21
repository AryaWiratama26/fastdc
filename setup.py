from setuptools import setup, find_packages

with open('DOC.md', 'r', encoding='utf-8') as file:
    res = file.read()

setup(
    name='fastdc',
    version='1.6',
    author='Arya Wiratama',
    author_email='aryawiratama2401@gmail.com',
    description='is a library designed to make creating Discord bots easier.',
    long_description=res,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"fastdc": ["*.py"]},
    install_requires=[
        'discord.py>=2.3.0',
        'groq>=0.3.0',
        'openai>=1.0.0',
        'aiohttp>=3.8.0',
        'python-dotenv>=1.0.0',
        'chatterbot>=1.0.0',
        'chatterbot-corpus>=1.2.0',
        'SQLAlchemy>=2.0.0',
        'spacy>=3.0.0', 
    ],
    python_requires='>=3.10',
)
