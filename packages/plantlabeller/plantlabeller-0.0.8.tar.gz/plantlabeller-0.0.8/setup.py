from setuptools import setup,find_packages

setup(
        name="plantlabeller",
        version="0.0.8",
        keywords=("pip","plantlabeller","droneimage","yangh"),
        description="label plants",
        long_description="pixel-level label plants in drone images",
        license = "MIT Licence",

        url="http://zzlab.net/yanghu/index.html",
        author="yangh",
        author_email="yang.hu@wsu.edu",

        packages=find_packages(),
        include_package_data=True,
        platforms="any",
        install_requires=["pillow","opencv-python","matplotlib","scipy","sklearn","scikit-image"],
        python_requirements='>=3'
        )
