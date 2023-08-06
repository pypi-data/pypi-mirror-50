import setuptools

print(setuptools.find_packages())

setuptools.setup(
    name="novadax",
    version="1.0.0.dev1",
    author="NovaDAX",
    author_email="support@novadax.com",
    description="NovaDAX API SDK",
    url="https://doc.novadax.com/",
    packages=["novadax"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)