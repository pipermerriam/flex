python setup.py sdist
python setup.py bdist_wheel --universal
ARTIFACT_BUCKET=s3://artifact-monetate-dev
aws s3 cp dist/flex-*.tar.gz $ARTIFACT_BUCKET/python/source/
aws s3 cp dist/flex-*-py2.py3-none-any.whl $ARTIFACT_BUCKET/python/wheelhouse/amzn/2014.09/
aws s3 cp dist/flex-*-py2.py3-none-any.whl $ARTIFACT_BUCKET/python/wheelhouse/amzn/2015.09/
aws s3 cp dist/flex-*-py2.py3-none-any.whl $ARTIFACT_BUCKET/python/wheelhouse/amzn/2016.03/

