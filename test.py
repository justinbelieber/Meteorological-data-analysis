from pyspark import SparkContext

sc = SparkContext('local', 'test')

lines = sc.textFile("test1.txt")
line3 = sc.parallelize([1, 2, 3, 4])
sumCount = line3.aggregate((0, 0),
                           (lambda acc, value: (acc[0] + value, acc[1] + 1)),
                           (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print(sumCount[0] / float(sumCount[1]))