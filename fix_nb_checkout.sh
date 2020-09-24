#!/bin/bash

#this fixes the breaking changes that occur to .ipynb files once  a checkout happens
# stolen from https://github.com/fastai/course-v3/issues/64
perl -pi -e 's|execution_count": null|execution_count": 1|g' nbs/*ipynb
