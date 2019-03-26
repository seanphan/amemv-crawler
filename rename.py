#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import glob
import os
import shutil
from optparse import OptionParser
import time
import json

from six.moves import input

def run_translate(text,target):
	# [START translate_quickstart]
	# Imports the Google Cloud client library
	from google.cloud import translate

	# Instantiates a client
	translate_client = translate.Client()

	# Translates some text into Russian
	translation = translate_client.translate(
		text,
		target_language=target)
	print(u'Text: {}'.format(text))
	print(u'Translation: {}'.format(translation['translatedText']))
	# [END translate_quickstart]
	return translation['translatedText']

def get_dir_files(dir_path, patterns):
	"""Get all absolute paths for pattern matched files in a directory.

	Args:
		dir_path (str): The path to of the directory containing media assets.
		patterns (list of str): The list of patterns/file extensions to match.

	Returns:
		(list of str): A list of all pattern-matched files in a directory.
	"""
	if not patterns or type(patterns) != list:
		print('No patterns list passed to get_dir_files, defaulting to patterns.')
		patterns = ['*.mp4', '*.avi', '*.mov', '*.flv']

	files = []
	for pattern in patterns:
		dir_path = os.path.abspath(dir_path) + '/' + pattern
		files.extend(glob.glob(dir_path))
	return files

def get_tiktok_caption(uri, metadata_path):
	with open(metadata_path) as f:
		metadata = json.load(f)
	for item in metadata:
		if item['video']['play_addr']['uri'] ==  uri:
			share_info = item.get('share_info', {})
			share_desc = share_info.get('share_desc', uri)
			return share_desc
	# caption = [item["edge_media_to_caption"]["edges"][0]["node"]["text"] for item in metadata
	# 			if item['video']['play_addr']['uri'] ==  uri]
	

if __name__ == '__main__':

	status = 'Failed!'
	parser = OptionParser(version='%prog 1.0.0')
	parser.add_option('-p', '--path', action='store', dest='dir_path',
					  default='.', type='string',
					  help='the path of the directory of assets, defaults to .')
	parser.add_option('-i', '--id', action='store', dest='user_id',
					  default='.', type='string',
					  help='user_id')
	# parser.add_option('-t', '--target', action='store', dest='target',
	# 				  default='.', type='string',
	# 				  help='target folder')
	# parser.add_option('-n', '--niche', action='store', dest='niche',
	# 				  default='.', type='string',
	# 				  help='niche')
	parser.add_option('-m', '--max', action='store', dest='max',
					  default='1', type='int',
					  help='max')

	options, args = parser.parse_args()
	# with open() as f:
	# 	data = json.load(f)
	# with open("config.json") as f:
	# 	data = json.load(f)
	user_id=options.user_id

	metadata_path = user_id+".json"
	dir_path = os.path.normpath(options.dir_path)
	# audio_path = os.path.normpath(data[0]["audio_path"]) + os.sep
	# dir_used_path = os.path.normpath(data[0]["video-used_path"]) + os.sep + options.niche + os.sep
	# final_cut_path = os.path.normpath(data[0]["final-cut_path"]) + os.sep
	# metadata_path = os.path.normpath(data[0]["metadata_path"])  + os.sep + options.target  + os.sep + options.target + ".json" 

	# logo_path = [item["logo_path"] for item in data[0]["target"]
	# 			if item["niche"] ==  options.niche]
	# print(logo_path)
	# page_name = [item["page_name"] for item in data[0]["target"]
	# 			if item["niche"] ==  options.niche]
	print('Running against directory path: {}'.format(dir_path))
	path_correct = input('Is that correct?').lower()
	print(path_correct)

	if path_correct.startswith('y'):
		for i in range(0,options.max):
			timestr = time.strftime("%Y%m%d-%H%M%S")
			dir_paths = get_dir_files(dir_path,patterns=None)
			# print(dir_paths)
			d = {}
			n=0
			for item in dir_paths:
				arrays = item.split(os.sep)
				fileName = item.split(os.sep)[len(arrays)-1]
				likes_count = fileName.split("_")[0]
				d[fileName] = int(likes_count)
			for key, value in sorted(d.items(), key=lambda kv: (kv[1], kv[0]),reverse=True):
				n = n + 1
				uri=key[key.find("_")+len("_"):key.rfind(".")]
				# likecounts = int(value)
				# print(u'key: {}'.format(key))
				# print(u'value: {}'.format(value))
				# print(likecounts)
				# print(key)
				# print(value)
				# print(uri)
				caption = get_tiktok_caption(uri,metadata_path)
				# print(caption)
				# The text to translate
				# text = u'这个小老弟你在干啥#家有萌宠 #柯基柯基柯基'
				# text = caption
				# # text.replace('～', ' ')
				# textList = text.split(' ')
				# translateList = []
				# # print(textList)
				# for item in textList:
				# 	# print(item)
				# 	# print(item.find("#"))
				# 	# print(item.find("@"))
				# 	if (item.find("#") == -1) and (item.find("@") == -1):
				# 		translateList.append(item)
				# 	elif (item.find("#") > 0):
				# 		item=item.partition("#")[0]
				# 		translateList.append(item)
				# 	elif (item.find("@") > 0):
				# 		item=item.partition("@")[0]
				# 		translateList.append(item)
				# # print('translateList: {}'.format(translateList))
				# # print(translateList)
				# revisedCaption = ' '
				# revisedCaption = revisedCaption.join(translateList)
				# target = 'en'
				# translation = run_translate(text=revisedCaption,target=target)
				# # print(translation)
				originalDirectory = dir_path + "/" + key
				# string = key
				# print(u'originalDirectory: {}'.format(originalDirectory))
				st = str(value) + "_" + uri + "_" + caption + ".mp4"
				# print(u'st: {}'.format(st))
				targetDirectory = dir_path + "/revised/" + st
				print(u'originalDirectory: {}'.format(originalDirectory))
				print(u'targetDirectory: {}'.format(targetDirectory))
				# print(caption)
				# The target language
				if (os.path.isfile(originalDirectory)):
					# os.remove(directory)
					# print("Remove:" + directory)
					# originalDirectory = directory
					# arrays = directory.split(os.sep)
					# fileName = directory.split(os.sep)[len(arrays)-1]
					# print(fileName)
					# targetDirectory = os.path.normpath(dir_used_path)  + os.sep  + output  
					if not os.path.exists(dir_path + "/revised/"):
						os.makedirs(dir_path + "/revised/")
					shutil.move(originalDirectory, targetDirectory)	


