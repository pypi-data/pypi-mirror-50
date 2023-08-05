#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Creation: 8/1/19 2:15 AM
@Author: liang
@File: tests.py
"""
from bottle import Bottle

from bottle_resource import BottleResource, api, api_get, api_post, api_put, api_patch, api_delete


class DemoResource(BottleResource):

    @api('/demos')
    def get_demo_list(self):
        return {'demos': [1, 2, 3, 4, 5]}

    @api_get('/demos/<demo_id>')
    def get_demo_detail(self, demo_id):
        return {'name': 'demo', 'id': demo_id}

    @api_post('/demos')
    def create_demo(self):
        return {'status': 'ok', 'msg': 'created success'}

    @api_put('/demos/<demo_id>')
    def update_demo(self, demo_id):
        return {'status': 'ok', 'msg': 'updated success', 'id': demo_id}

    @api_patch('/demos/<demo_id>')
    def patch_demo(self, demo_id):
        return {'status': 'ok', 'msg': 'patch success', 'id': demo_id}

    @api_delete('/demos/<demo_id>')
    def delete_demo(self, demo_id):
        return {'status': 'ok', 'msg': 'delete success', 'id': demo_id}


if __name__ == '__main__':
    app = Bottle()
    app.install(DemoResource())
    app.run(host='0.0.0.0', port=8000, debug=True, reloader=True)
