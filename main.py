from newsreaderfile import newsreader

url = "https://edition.cnn.com/"

nr =newsreader(url)

# Print all sentiments
print(nr.current_date)

for i, sentiment in enumerate(nr.sentiments):
    print("Sentiment: {:.2f} \t| {}".format(sentiment, nr.headlines[i]))