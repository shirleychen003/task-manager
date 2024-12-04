from setuptools import setup, find_packages

setup(
    name="task_manager",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # List any third-party dependencies here. Tkinter usually comes with Python.
    ],
    entry_points={
        'console_scripts': [
            'task-manager=main:main',
        ],
    },
    author="David Dimalanta",
    author_email="david.dimalanta@mail.utoronto.ca",
    description="An accessible task management application developed in Python.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shirleychen003/task-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 