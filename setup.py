from setuptools import setup, find_packages

with open('DOC.md', 'r', encoding='utf-8') as file:
    res = file.read()

setup(
    name='fastdc',
    version='2.2.0',
    author='Arya Wiratama',
    author_email='aryawiratama2401@gmail.com',
    description='A Fast Discord Bot Framework',
    long_description=res,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'discord.py>=2.3.0',
        'groq>=0.3.0',
        'openai>=1.0.0',
        'aiohttp>=3.8.0',
        'python-dotenv>=1.0.0',
        'quart>=0.19.0',
        'hypercorn>=0.17.0',
    ],
    package_data={
        "fastdc": [
            "*.py",
            "dashboard/templates/*.html",
            "dashboard/static/*.css",
            "dashboard/static/*.js",
        ]
    },
    python_requires='>=3.10',
)
