#!/usr/bin/env sh
#
pants package ::
terraform -chdir=src/infra apply -auto-approve
