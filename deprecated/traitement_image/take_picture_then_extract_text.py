from text_extractor import TextExtractor
import time

text_extractor = TextExtractor()
start = time.time()
text_extractor.analyse_image_silently("test")
end = time.time()
print(end - start)