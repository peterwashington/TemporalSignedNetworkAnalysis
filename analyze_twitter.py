
### Peter Washington
### Analyze Signed Twitter Netork

import matplotlib.pyplot as plt
import math

def read_network(filename):
	signed_network = {}
	with open(filename) as f:
		for line in f:
			split_line = line.split(",")
			if len(split_line) != 11:
				continue
			if split_line[0] == "Row":
				continue
			if len(split_line) < 3:
				continue

			sentiment = float(split_line[3])
			node_a = split_line[4]
			node_bs = []
			for word in split_line[5].split():
				if word[0] == "@":
					node_bs.append(word)

			timestamp = 0
			day = split_line[7].split()
			if day[0] == "Apr":
				timestamp += 0
			if day[0] == "May":
				timestamp += 30 * 1440
			if day[0] == "Jun":
				timestamp += 61 * 1440
			if day[0] == "Jul":
				timestamp += 91 * 1440
			if day[0] == "Aug":
				timestamp += 122 * 1440
			timestamp += int (day[1]) * 1440

			time = split_line[9].split()[0].split(":")
			if split_line[9].split()[1][:2] == "PM":
				timestamp += 720
			timestamp += 60 * int(time[0])
			timestamp += int(time[1])

			for node_b in node_bs:
				if node_a not in signed_network:
					signed_network[node_a] = {}
					signed_network[node_a][node_b] = [(sentiment, timestamp)]
					continue
				if node_b not in signed_network[node_a]:
					signed_network[node_a][node_b] = []
				signed_network[node_a][node_b].append((sentiment, timestamp))


	return signed_network


april_may_network = read_network("Datasets/AprilMayTwitterSentiment.csv")
april_june_network = read_network("Datasets/AprilJuneTwitterSentiment.csv")
april_july_network = read_network("Datasets/AprilJulyTwitterSentiment.csv")
april_august_network = read_network("Datasets/AprilAugustTwitterSentiment.csv")



networks = [april_may_network, april_june_network, april_july_network, april_august_network]

for index in range(len(networks)):

	max_timestamp = float('inf')

	if index == 0:
		print "April to May Network"
		max_timestamp = 30 * 1440 + 2*1440
	if index == 1:
		print "April to June Network"
		max_timestamp = 61 * 1440 + 2*1440
	if index == 2:
		print "April to July Network"
		max_timestamp = 91 * 1440 + 2*1440
	if index == 3:
		print "April to August Network"
		max_timestamp = 122 * 1440 + 2*1440


	print "============================"
	network = networks[index]

	total_nodes = len(network)
	average_outdegree = 0.0
	average_unique_tweets = 0.0

	total_positive_tweets = 0
	total_negative_tweets = 0
	total_neutral_tweets = 0
	average_positive_sentiment = 0.0
	average_negative_sentiment = 0.0

	num_tweets = 0
	num_positive = 0
	num_negative = 0
	num_neutral = 0

	for node in network:		
		for neighbor in network[node]:
			average_outdegree += 1.0 * len(network[node][neighbor])
			average_unique_tweets += 1.0
			for tweet in network[node][neighbor]:
				num_tweets += 1
				if tweet[0] > 0:
					total_positive_tweets += 1
					average_positive_sentiment += tweet[0]
					num_positive += 1
				if tweet[0] < 0:
					total_negative_tweets += 1
					average_negative_sentiment += tweet[0]
					num_negative += 1
				if tweet[0] == 0:
					total_neutral_tweets += 1
					num_neutral += 1

	total_tweets = total_neutral_tweets + total_negative_tweets + total_positive_tweets

	average_outdegree /= total_nodes
	average_unique_tweets /= total_nodes
	average_positive_sentiment /= num_positive
	average_negative_sentiment /= num_negative

	### Find triads.
	triad_weights = []
	for a in network:
		for b in network[a]:
			if a != b and b in network:
				for c in network[b]:
					if c in network and c != a and c != b and (c in network[a] or a in network[c]):
						edge_one = 0.0
						edge_two = 0.0
						edge_three = 0.0
						for weight in network[a][b]:
							edge_one += (total_tweets / average_positive_sentiment) * ((1.0*weight[0])/math.sqrt(max_timestamp - weight[1]))
						for weight in network[b][c]:
							edge_two += (total_tweets / average_positive_sentiment) * ((1.0*weight[0])/math.sqrt(max_timestamp - weight[1]))
						if c in network[a]:
							for weight in network[a][c]:
								edge_three += (total_tweets / average_positive_sentiment) * ((1.0*weight[0])/math.sqrt(max_timestamp - weight[1]))
						elif a in network[c]:
							for weight in network[c][a]:
								edge_three += (total_tweets / average_positive_sentiment) * ((1.0*weight[0])/math.sqrt(max_timestamp - weight[1]))
						triad_weights.append(edge_one + edge_two + edge_three)
	print sorted(triad_weights)

	plt.hist(triad_weights, bins=100)
	plt.title("Triad Weights at time: " + str(index))
	plt.xlabel("Triad Weight")
	plt.ylabel("Frequency")
	plt.show()


	print "Average Outdegree: ", average_outdegree 
	print "Average Unique Users Tweeted To: ", average_unique_tweets
	print "Total Positive Tweets: ", total_positive_tweets
	print "Total Negative Tweets: ", total_negative_tweets
	print "Total Neutral Tweets: ", total_neutral_tweets
	print "Average Positive Sentiment: ", average_positive_sentiment
	print "Average Negative Sentiment: ", average_negative_sentiment

	print 
	print 
	print 








