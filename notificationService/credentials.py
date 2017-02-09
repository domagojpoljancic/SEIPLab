#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ as env

def get_creds():
    d = {}
    d['auth_url'] = env['OS_AUTH_URL']
    d['username'] = env['OS_USERNAME']
    d['password'] = env['OS_PASSWORD']
    d['tenant_name'] = env['OS_TENANT_NAME']
    d['region_name'] = env['OS_REGION_NAME']
    return d

def get_nova_creds():
    d = {}
    d['auth_url'] = env['OS_AUTH_URL']
    d['username'] = env['OS_USERNAME']
    d['api_key'] = env['OS_PASSWORD']
    d['project_id'] = env['OS_TENANT_NAME']
    d['region_name'] = env['OS_REGION_NAME']
    return d