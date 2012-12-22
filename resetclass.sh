#!/bin/bash

rm data/classlist
rm -rf data/$1
touch data/classlist
chown www-data data/classlist
chgrp www-data data/classlist
