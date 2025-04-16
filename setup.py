from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    res = file.read()

setup(
    name='fastdc',
    version='1.2',
    author='Arya Wiratama',
    author_email='aryawiratama2401@gmail.com',
    description='FastDC: A fast, modular, and AI-integrated Discord bot framework.',
    # long_description=res,
    # long_description_content_type="text/markdown",
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
