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


class FindAnswerHandler(tornado.web.RequestHandler):

	def data_received(self, chunk):
		pass

	def get(self, *args, **kwargs):
		self.render('find_answer.html')

	def post(self, *args, **kwargs):
		self.use_write()

	def use_write(self):
		question = self.get_argument('question')
		top_n = int(self.get_argument('top_n'))
		original = self.get_argument('original')
		try:
			# results = search.search4answer(question, top_n=top_n, config=config, original=original)
			# question_list = [question for _ in range(len(results))]
			# retrievaled_questions = [temp[1] for temp in results]
			# probs, _ = infer_prob(question_list, retrievaled_questions, vocab_processor, model, session)
			# positive_probs = probs[:, 1]
			# alternative_answers = [temp[2] for temp in results]

			# json_data = {
			# 	'question': str(question),
			# 	'retrieval_question': '|||'.join(retrievaled_questions),
			# 	'probabilities': '|||'.join(str(prob) for prob in positive_probs),
			# 	'answer': str(alternative_answers)
			# }
			json_data = {
			    'question': 'question',
			    'retrieval_question': 'retrieval_question',
			    'probabilities': '|||',
			    'answer': 'answer'
			}
			# print(json_data)
			self.write(json.dumps(json_data, ensure_ascii=False))
		except Exception as e:
			print(e)
			json_data = {
				'question': str(question),
				'retrieval_question': 'unknown',
				'probabilities': 'unknown',
				'answer': 'unknown'
			}
			self.write(json.dumps(json_data, ensure_ascii=False))


class PrimaryQuestionFindHandler(tornado.web.RequestHandler):
	def data_received(self, chunk):
		pass

	def get(self, *args, **kwargs):
		self.render('find_primary.html')

	def post(self, *args, **kwargs):
		self.use_write()

	def use_write(self):
		question = self.get_argument('question')
		topn = int(self.get_argument('top_n'))
		original = self.get_argument('original')

		try:
			# results = search.search_by_question(question, top_n=topn, config=config, original=original)
			# question_list = [question for _ in range(len(results))]
			# retrievaled_questions = [temp[1] for temp in results]
			# probs, _ = infer_prob(question_list, retrievaled_questions, vocab_processor, model, session)
			# positive_probs = probs[:, 1]

			# alternative_primary_questions = []
			# for result in results:
			# 	alternative_primary_questions.append(result[2])
			# 	json_data = {
			# 		'alternative': '|||'.join(alternative_primary_questions),
			# 		'sub_question': '|||'.join(retrievaled_questions),
			# 		'match_score': '|||'.join([str(prob) for prob in positive_probs]),
			# 		'user_query': str(question)
			# 	}
			# print(json_data)
			json_data = {
				'question': question,
				'topn': topn,
				'original': original
			}
			self.write(json.dumps(json_data, ensure_ascii=False))

		except Exception as e:
			print(e)
			json_data = {
				'alternative': 'Unknown',
				'match_score': '0',
				'user_query': str(question)
			}
			self.write(json.dumps(json_data, ensure_ascii=False))


def make_app():
	setting = dict(
		template_path=os.path.join(os.path.dirname(__file__), 'templates'),
		static_path=os.path.join(os.path.dirname(__file__), 'static')
	)
	return tornado.web.Application(
		[(r'/FindAnswer', FindAnswerHandler), (r'/FindPrimary', PrimaryQuestionFindHandler)],
		**setting
	)


if __name__ == '__main__':
	app = make_app()
	app.listen(9002)
	tornado.ioloop.IOLoop.current().start()
