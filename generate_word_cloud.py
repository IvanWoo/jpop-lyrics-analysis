"""
https://github.com/amueller/word_cloud/blob/master/examples/simple.py
"""

from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, "word-cloud-feed.txt")).read()

ebichu_mask = np.array(Image.open(path.join(d, "resources/ebichu-2x.png")))

# Generate a word cloud image
wordcloud = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc', background_color="white", max_words=200, mask=ebichu_mask).generate(text)

# Display the generated image:
# the matplotlib way:
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()
