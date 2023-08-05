from setuptools import setup, find_packages


with open("README.md") as fp:
    long_description = fp.read()


setup(
    name="swa_cc.secure_s3_storage_bucket",
    version="1.3.0",

    description="A CDK stack for creating a swa approved s3 bucket",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Seth Dobson",
    author_email="sd0408@gmail.com",

    package_dir={"": "src"},
    packages=["swa_cc.secure_s3_storage_bucket"],

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-s3",
        "aws-cdk.aws_kms",
        "aws-cdk.aws_iam",
        "aws_cdk.aws_events",
        "swa_cc.core"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
