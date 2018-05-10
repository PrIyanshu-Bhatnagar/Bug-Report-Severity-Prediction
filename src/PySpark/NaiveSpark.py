from __future__ import print_function
from pyspark.sql import SparkSession
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.feature import Word2Vec
from pyspark.sql import Row
from pyspark.mllib.linalg import DenseVector
import sys
import time

spark = SparkSession\
        .builder\
        .config("spark.executor.memory","1g")\
        .config("spark.cores.max","1")\
        .appName("PythonNaiveBayes")\
        .getOrCreate()

def get_label_point(label):
    if label == "major":
        return 2
    elif label == "minor":
        return 3
    elif label == "normal":
        return 4
    elif label == "trivial":
        return 5
    elif label == "enhancement":
        return 6
    elif label == "blocker":
        return 7
    elif label == "critical":
        return 8
    else:
        return 1


def parseLine(line):
    # Get Values
    label = line.severity
    # print('label: ', label)
    features = DenseVector(line.result)
    # print(features)
    return LabeledPoint(get_label_point(label), features)


def preprocess_vector(line):
    for v in line.result:
        if v < 0:
            return False
    return True


if __name__ == "__main__":
    # Spark Context Object
    sc = spark.sparkContext
    start_time = time.time()
    # Upload Raw data
    path = sys.argv[1].split("hdfs://master-virtualbox:9000")[1]
    raw_data = sc.textFile(sys.argv[1])
    # filter data
    filter_data = raw_data.filter(lambda l: len(l.strip().split("\t\t"))%3 == 0)
    # Preparing features
    row_data = filter_data.map(lambda l: l.strip().split("\t\t"))
    # split data bug_id, text & severity
    text_data = row_data.map(lambda r: Row(text=r[1].split(" "), severity=r[2]) )
    # text_data dataframe
    documentDF = spark.createDataFrame(text_data)
    # Learn a mapping from words to Vectors.
    word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol="text", outputCol="result")
    # model training
    model = word2Vec.fit(documentDF)
    # result vector
    result = model.transform(documentDF)
    # Preprocess negative vectors
    pre_data = result.rdd.filter(lambda l: preprocess_vector(l))
    # parse dataframe to labelled point
    data = pre_data.map(parseLine)
    # Naive Bayes implementation
    # Split data aproximately into training (60%) and test (40%)
    training, test = data.randomSplit([0.6, 0.4], seed=0)
    # Train a naive Bayes model.
    model = NaiveBayes.train(training, 1.0)
    # Make prediction and test accuracy.
    predictionAndLabel = test.map(lambda p: (model.predict(p.features), p.label))
    accuracy = 1.0 * predictionAndLabel.filter(lambda pl: pl[0] == pl[1]).count() / test.count()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Accuracy: ', accuracy*100, "%")
    print('Time: ', elapsed_time)
    # Save and load model
    inputname, ext = path.split(".")
    model.save(sc, "Target/{}-{}".format(inputname, time.time()))
    # sameModel = NaiveBayesModel.load(sc, "Target/myNaiveBayesModel-{}"format(sys.argv[1]))
