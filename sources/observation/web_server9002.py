#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__title__ = ''
__author__ = 'yangzl31'
__mtime__ = '2018/12/13'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

from typing import List, Any, Union

import tornado.ioloop
import tornado.web
import json
import os
import sys
import jieba
import numpy as np
# from ir.search import Search
# from ir.config import Config
import logging
import time
import pandas as pd

# from infer_spec import prepare, inference, infer_prob

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curdir))


now_date = time.strftime("%Y_%m_%d")
print(now_date)
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	filename= curdir + '/web_server/%s' % (now_date + '_dl.log'),
	filemode='a'
)


def chinese_tokenizer(documents):
	"""
	:param documents:
	:return:
	"""
	for document in documents:
		yield list(jieba.cut(document))


# set config
# config = Config()

# search = Search()
# vocab_processor, model, session = prepare()


# with open('../data/primary_question_dict.json', encoding='utf-8') as primary_dict_f:
# 	primary_question_dict = json.loads(primary_dict_f.readline())

def temp_file(path_in, path_out):
	df = pd.read_csv(path_in)
	df.to_csv(path_out)
	return df

def temp_str(str_in):
	str0=str_in
	str1=str_in
	str2=str_in
	str3=str_in
	str4=str_in
	str5=str_in
	str6=str_in
	str7=str_in
	str8=str_in
	str9=str_in
	return str0,str1,str2,str3,str4,str5,str6,str7,str8,str9

class PrimaryQuestionFindHandler(tornado.web.RequestHandler):

	def get(self, *args, **kwargs):
		params = {
			"module_name": 'find_primary.html',
			"type": self.get_query_argument('type', 'single')
		}
		self.render('frame.html', params=params)

	def post(self, *args, **kwargs):
		self.post_request()

	def download(self, *args, **kwargs):
		filename = self.get_query_argument('filename', '')
		if len(filename) < 1:
			self.set_status(404)
			self.finish("File not found");
		else:
			buf_size = 4096
			self.set_header('Content-Type', 'application/octet-stream')
			self.set_header('Content-Disposition', 'attachment; filename')
			with open('data/' + filename, 'r') as f:
				while True:
					data = f.read(bug_size)
					if not data:
						break
					self.write(data)
			self.finish()

	def post_request(self):
		type = self.get_argument('type')
		params = {
			'type': type,
			'module_name': 'find_primary.html'
		}
		if type == 'single':
			diagnose_text = self.get_argument('diagnose_text')
			params['diagnose_text'] = diagnose_text

			params['diagnose_result'] = temp_str(str_in=diagnose_text)
			self.render('frame.html', params=params)
		elif type == 'batch':
			file = self.request.files['file'][0]
			original_fname = file['filename']
			extension = os.path.splitext(original_fname)[1]
			output_file = open('uploads/' + original_fname, 'wb')
			output_file.write(file['body'])
			if extension == 'csv':
				temp_file(path_in='uploads/' + original_fname, path_out='data/' + original_fname)
				params['downloadUrl'] = '/download?filename=' + original_fname;
			self.render('frame.html', params=params)

def make_app():
	setting = dict(
		template_path=os.path.join(os.path.dirname(__file__), 'templates'),
		static_path=os.path.join(os.path.dirname(__file__), 'static')
	)
	return tornado.web.Application(
		[(r'/FindPrimary', PrimaryQuestionFindHandler)],
		**setting
	)


if __name__ == '__main__':
	app = make_app()
	app.listen(9002)
	tornado.ioloop.IOLoop.current().start()
