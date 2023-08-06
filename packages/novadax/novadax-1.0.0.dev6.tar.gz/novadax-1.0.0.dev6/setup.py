import setuptools

print(setuptools.find_packages())

setuptools.setup(
    name="novadax",
    version="1.0.0.dev6",
    author="NovaDAX",
    author_email="support@novadax.com",
    description="NovaDAX API SDK",
    url="https://doc.novadax.com/",
    packages=["novadax", "novadax.impl"],
    install_requires=['requests']
)