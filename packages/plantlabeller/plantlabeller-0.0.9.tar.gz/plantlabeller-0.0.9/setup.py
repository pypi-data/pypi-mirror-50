from setuptools import setup,find_packages

setup(
        name="plantlabeller",
        version="0.0.9",
        keywords=("pip3","plantlabeller","droneimage","yangh"),
        description="label plants",
        long_description="A pixel-level label plants in drone images\n",

        license = "MIT Licence",

        url="http://css.wsu.edu/people/research-associates/yang-hu/",
        author="yangh",
        author_email="yang.hu@wsu.edu",

        packages=find_packages(),
        include_package_data=True,
        platforms="any",
        install_requires=["pillow","opencv-python","matplotlib","scipy","sklearn","scikit-image"],
        python_requirements='>=3'
        )
