minified_data = {}
movies_data = {}
closest_user = []

import pandas as pd
import random

def testing(tolerance=0, min_rating=3, limit = -1):
	nrow = len(minified_data)
	success = 0
	for _ in range(1,101):
		test_idx = random.randrange(1,nrow)
		print("test idx: %d" % test_idx)
		temp = minified_data[test_idx]
		splitted_temp = filter(bool,temp.split(" "))
		minified_data[test_idx] = ''
		documents_test = splitted_temp[::2]
		ratings = splitted_temp[1::2]
		sample_doc = documents_test[::2]
		sample_rating = ratings[::2]
		restructured_video_code = ''
		for i in range(0,len(sample_doc)):
			restructured_video_code = restructured_video_code + " " + sample_doc[i] + " " + sample_rating[i]
		expected_result_wo_ratings = documents_test[1::2]
		rating_filter = ratings[1::2]
		expected_result = set()
		for i in range(0, len(expected_result_wo_ratings)):
			if rating_filter >= min_rating:
				expected_result = expected_result | {expected_result_wo_ratings[i]}
		sim_video_code = set(getSimilarVideoCode(restructured_video_code, limit=limit, min_rating=min_rating))
		if len(sim_video_code - expected_result) == 0:
			success += 1
		else:
			print("added %s" % str(expected_result - sim_video_code))
			print("need %s" % str(sim_video_code - expected_result))
		minified_data[test_idx] = temp 
	print("Success rate: %d %%" % (success * 1.0))



def convertToAlphabet(id):
	if(id < 26):
		return chr(ord('A') + id)
	else:
		return convertToAlphabet(id / 26) + chr(ord('A') + (id % 26))

def convertToNumber(key):
	length = len(key)
	result = 0
	for i in range(0, length):
		base = 26 ** (length - 1 - i)
		c = ord(key[i]) - ord('A')
		result += c * base
	return result

def getSimilarVideoCode(minified_preference, tolerance=0, min_rating=3, limit = 20):
	splitted_minified_preference = filter(bool,minified_preference.split(" "))
	documents = splitted_minified_preference[::2]
	recommendation_bucket = []
	recommendation_video = set()
	point = 0
	for key, value in minified_data.iteritems():
		splitted_test_preference = filter(bool,value.split(" "))
		test_documents = splitted_test_preference[::2]
		diff = set(documents) - set(test_documents)
		if(len(diff) > tolerance):
			continue			
		tmp_point = 0
		for document in documents:
			index_pref = splitted_minified_preference.index(document)
			index_test = splitted_test_preference.index(document)
			rating_pref = float(splitted_minified_preference[index_pref + 1])
			rating_test = float(splitted_test_preference[index_test + 1])
			rating_diff = abs(rating_pref - rating_test)
			if(rating_diff >= 2):
				tmp_point -= 1
			elif(rating_diff > 0):
				tmp_point += 0.5
			else:
				tmp_point += 1
		reco_for_flag = False
		if(tmp_point > point):
			dist_videos = list(set(test_documents) - set(documents))
			proven_videos = []
			for video in dist_videos:
				idx_test = splitted_test_preference.index(video)
				if(float(splitted_test_preference[idx_test + 1]) >= min_rating):
					proven_videos.append(video)
					reco_for_flag = True
			recommendation_video = set(proven_videos)
		elif(tmp_point == point):
			dist_videos = list(set(test_documents) - set(documents))
			proven_videos = []
			for video in dist_videos:
				idx_test = splitted_test_preference.index(video)
				if(float(splitted_test_preference[idx_test + 1]) >= min_rating):
					proven_videos.append(video)
					reco_for_flag = True
			recommendation_video |= set(proven_videos)
		if reco_for_flag:
			recommendation_bucket.append(key)
	# print(recommendation_bucket)
	if limit == -1:
		return filter(bool,recommendation_video)
	else:
		return random.sample(filter(bool,recommendation_video), limit)

def videoIdListToCode(video_id_list):
	codes = []
	for video_id in video_id_list:
		codes.append(convertToAlphabet(video_id))
	return codes

def codeListToVideoId(code_list):
	video_ids = []
	for codes in code_list:
		video_ids.append(convertToNumber(codes))
	return video_ids

def showRecommendationFromPreference(preference, tolerance=0, min_rating=3, limit = 20):
	splitted_preference = preference.split(' ')
	video_ids = splitted_preference[::2]
	ratings = splitted_preference[1::2]
	preference_string = ''
	code_list = videoIdListToCode(video_ids)
	for i in range(0, len(video_ids)):
		preference_string = preference_string + code_list[i] + " " + ratings[i] + " "
	similar_video_code = getSimilarVideoCode(preference_string, tolerance=tolerance, min_rating=min_rating, limit=limit)
	return codeListToVideoId(similar_video_code)

raw_data_ratings = pd.read_csv('/home/liqrgv/Workspace/hackaton/kudo/ml-20m/ratings.csv')
raw_data_movies = pd.read_csv('/home/liqrgv/Workspace/hackaton/kudo/ml-20m/movies.csv')

row_num_ratings = 500000
row_num_movies = raw_data_movies.shape[0]

for i in range(0, row_num_ratings):
	row_data = raw_data_ratings.iloc[i]
	user_id = row_data[0]
	movie_id = row_data[1]
	rating = row_data[2]
	if user_id in minified_data:
		minified_data[int(user_id)] = minified_data[int(user_id)] + convertToAlphabet(int(movie_id)) + " " + str(rating) + " "
	else:
		minified_data[int(user_id)] = convertToAlphabet(int(movie_id)) + " " + str(rating) + " "
	print("Processing user: %d" % int(user_id))

for i in range(0, row_num_movies):
	row_data = raw_data_movies.iloc[i]
	movie_id = row_data[0]
	title = row_data[1]
	movies_data[int(movie_id)] = title
	print("Processing movies: %d" % int(movie_id))