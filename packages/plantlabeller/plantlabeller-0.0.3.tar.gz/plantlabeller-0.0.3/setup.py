from setuptools import setup,find_packages

setup(
        name="plantlabeller",
        version="0.0.3",
        keywords=("pip","plantlabeller","droneimage","yangh"),
        description="label plants",
        long_description="label plants in drone images",
        license = "MIT Licence",

        url="http://zzlab.net/yanghu/index.html",
        author="yangh",
        author_email="yang.hu@wsu.edu",

        packages=find_packages(),
        include_package_data=True,
        platforms="any",
        install_requires=["tkinter","PIL","cv2","csv","gdal","matplotlib","scipy","sklearn","functools","time","skimage"],
        python_requirements='>=3'
        )
