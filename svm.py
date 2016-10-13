# Combine twitter and weather data to produce tweets labeled by weather
import helper
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from nltk.classify.scikitlearn import SklearnClassifier


class SVMLearner():

	def __init__(self):
		self.classifier = SklearnClassifier(LinearSVC())
		#self.classifier = SklearnClassifier(LinearSVC(multi_class='crammer_singer'))
		#self.classifier = SklearnClassifier(SVC())

	def train(self, data):
		self.classifier.train(data)
		return self

	def classify(self, element):
		return self.classifier.classify_many(element)[0]

if __name__ == "__main__":
	# Get observed weather in formatted time ranges
	observed_weather = helper.format_observed_weather()
	# Assign tweets to their respective time range and weather
	tweets_by_weather = helper.find_tweets_weather(observed_weather)

	# Compute features (words) and their labels
	final_data = helper.compute_features(tweets_by_weather)

	helper.cross_validate(final_data, 5, SVMLearner())


	