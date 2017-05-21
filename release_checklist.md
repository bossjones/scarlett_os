# Release checklist ( borrowed from audreyr )

`source: https://gist.github.com/audreyr/5990987`

- [ ] Update HISTORY.rst
- [ ] Commit the changes:
```
git add HISTORY.rst
git commit -m "Changelog for upcoming release 0.1.1."
```
- [ ] Update version number (can also be minor or major)
```
bumpversion patch
```
- [ ] Install the package again for local development, but with the new version number:
```
python setup.py develop
```
- [ ] Run the tests:
```
tox
```
- [ ] Release on PyPI by uploading both sdist and wheel:
```
python setup.py sdist upload
python setup.py bdist_wheel upload
```

- [ ] Test that it pip installs:
```
mktmpenv
pip install my_project
<try out my_project>
deactivate
```

- [ ] Push: `git push`
- [ ] Push tags: `git push --tags`
- [ ] Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.
- [ ] Edit the release on GitHub (e.g. https://github.com/audreyr/cookiecutter/releases). Paste the release notes into the release's release page, and come up with a title for the release.


--------------------------

Awesome checklist. Thanks for this and the wonderful https://github.com/audreyr/cookiecutter-pypackage.
some remarks from the perspective of a pypi noob.

PyPI's own doc is quite comprehensive @ [https://python-packaging-user-guide.readthedocs.org/en/latest/distributing/](Packaging and Distributing Project)

They suggest you can use their test repo https://wiki.python.org/moin/TestPyPI before working on the actual pypi repo. Worked very well for me.
They also advise using twine rather than setup.py upload (or setup.py register for that matter). Reason is cleartext credentials on the wire. Additionally, twine lets you build the dists locally before uploading.

So the workflow is:
python setup.py bdist sdist

Upload to pypitest
twine upload dist/* -r pypitest

Upload to real pypi
twine upload dist/* -r pypi -u -p

Last, this guy had a pretty good write up about packaging https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/. Not sure I am 100% clean yet, but with all of this, and copying from sqlalchemy's setup.py, I am well under way.

Thanks again.


---------------------

- https://github.com/michaeljoseph/changes
- https://pypi.python.org/pypi/ghrelease/0.1.2
- https://github.com/python/release-tools
- https://github.com/aktau/github-release