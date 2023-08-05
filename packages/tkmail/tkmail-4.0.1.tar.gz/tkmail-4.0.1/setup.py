import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='tkmail',  
     version='4.0.1',
     author="tuan.dv, nhat.nv",
     author_email="tuan.dv@teko.vn, nhat.nv@teko.vn",
     description="Tool send email via SMTP (with retry)",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://git.teko.vn/data/libs/smtp-mail",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
