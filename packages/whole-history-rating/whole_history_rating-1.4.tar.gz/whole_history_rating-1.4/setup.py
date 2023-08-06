import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whole_history_rating",
    version="1.4",
    author="Pierre-François MONVILLE",
    author_email="p_fmonville@hotmail.fr",
    description="A python implementation of the whole-history-rating algorythm by Rémi Coulom (based on the ruby implementation at https://github.com/goshrine/whole_history_rating)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pfmonville/whole_history_rating",
    packages=["whr"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)