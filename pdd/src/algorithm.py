
import json
import datetime
import numpy as np

from sklearn.metrics import plot_roc_curve
from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.datasets import load_digits
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.model_selection import ShuffleSplit
import matplotlib.pyplot as plt
from io import StringIO
from scipy.io import arff
from traceback import format_exc
from domain_parser import domain_parser
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

from ns_log import NsLog
from json2arff import json2arff
from rule_extraction import rule_extraction


class machine_learning_algorithm():

    def __init__(self, algorithm, train_data_name="gsb.arff"):

        self.logger = NsLog("log")

        self.path_output_arff = "../output/arff/"
        self.path_test_output = ""

        self.json2arff_object = json2arff()
        self.parser_object = domain_parser()
        self.train_data_name = train_data_name
        self.rule_calculation = rule_extraction()

        self.train, self.test, self.train_label, self.test_label = self.split_test_and_train_data()

        self.time_now = str(datetime.datetime.now())[0:19].replace(" ", "_")

        if algorithm == 'NB':
            self.model = self.create_model_NB()
            self.active_model = self.active_create_model_NB()
        elif algorithm == 'RF':
            self.model = self.create_model_RF()
            self.active_model = self.active_create_model_RF()
        elif algorithm == 'GB':
            self.model = self.create_model_GB()
            self.active_model = self.active_create_model_GB()

    def txt_to_list(self, txt_object):

        lst = []

        for line in txt_object:
            lst.append(line.strip())

        txt_object.close()

        return lst

    def split_test_and_train_data(self):
        try:
            data , label = self.preparing_train_data()
            train,test,train_label,test_label = train_test_split(data,label,test_size=0.25,random_state=42)
        except:
            self.logger.debug(file_name+" ile train ve test ayırma sırasında hata")
            self.logger.error("Error : {0}".format(format_exc()))

        return train,test,train_label,test_label

    def preparing_train_data(self, file_name="gsb.arff"):

        train = []
        target = []

        try:
            train_dataset, train_meta = arff.loadarff(open("{0}{1}".format(self.path_output_arff, file_name), "r"))

            train = train_dataset[train_meta.names()[:-1]]  # everything but the last column
            target = train_dataset[train_meta.names()[len(train_meta.names()) - 1]]  # last column

            train = np.asarray(train.tolist(), dtype=np.float32)  # olay burda
        except:
            self.logger.debug(file_name+" ile eğitim sırasında hata")
            self.logger.error("Error : {0}".format(format_exc()))

        return train, target

    def preparing_test_data(self, test_dataset_list):
        try:
            feat_json = open("../output/test-output/json-"+self.time_now+".txt", "w")
            feat_arff = open("../output/test-output/arff-"+self.time_now+".arff", "w")

            "domain_parsed to json without class"
            self.test_parsed_domains = self.parser_object.parse_nonlabeled_samples(test_dataset_list)

            "rule calculation for test samples without class information -- output json format"
            test_features = self.rule_calculation.extraction(self.test_parsed_domains)

            "test sampleları için oluşturulan json -> arff e dönüştür. Class yok."
            arff_test_str = self.json2arff_object.convert_for_test(test_features, '')

            feat_json.write(json.dumps(test_features))
            feat_arff.write(arff_test_str)

            feat_arff.close()
            feat_json.close()

            arff_raw = StringIO(arff_test_str)

            test_dataset, test_meta = arff.loadarff(arff_raw)

            test = test_dataset[test_meta.names()]
            test = np.asarray(test.tolist(), dtype=np.float32)
        except:
            self.logger.error("Test verisi ayarlanırken hata  /  Error : {0}".format(format_exc()))
        return test, self.test_parsed_domains

    def create_model_NB(self):

        #train, target = self.preparing_train_data()
        train, target = self.train, self.train_label#self.preparing_train_data()
        gnb = GaussianNB()
        #model = gnb.fit(train, target)
        model = gnb.fit(self.train, self.train_label)

        return model

    def create_model_RF(self):
        #train, target = self.preparing_train_data()
        train, target = self.train, self.train_label#self.preparing_train_data()
        clf = GradientBoostingClassifier(n_estimators=10, max_depth=7,random_state=0, verbose=0)
        #model = clf.fit(train, target)
        model = clf.fit(self.train, self.train_label)

        return model

    def create_model_GB(self):
        train, target = self.train, self.train_label#self.preparing_train_data()
        clf = GradientBoostingClassifier(n_estimators=10, max_depth=7,random_state=0, verbose=0)
        #clf = GradientBoostingClassifier(n_estimators=10, max_depth=7, random_state=0, verbose=0, max_features=50, min_samples_split=50, min_samples_leaf=50)

        model = clf.fit(self.train, self.train_label)


        return model

    def active_create_model_NB(self):

        train, target = self.preparing_train_data()
        gnb = GaussianNB()
        model = gnb.fit(train, target)

        return model

    def active_create_model_RF(self):
        train, target = self.preparing_train_data()
        clf = GradientBoostingClassifier(n_estimators=10, max_depth=7,random_state=0, verbose=0)
        model = clf.fit(train, target)

        return model

    def active_create_model_GB(self):
        #train, target = self.preparing_train_data()
        train, target = self.train, self.train_label#self.preparing_train_data()

        clf = GradientBoostingClassifier(n_estimators=10, max_depth=7, random_state=0, verbose=0)
        model = clf.fit(train, target)

        return model

    def model_run(self, test):

        model = self.model
        model_pre = model.predict(test)
        model_probability = model.predict_proba(test)

        model_pre_list = []
        for p in model_pre:
            model_pre_list.append(str(p).replace("b'", "").replace("'", ""))

        model_probability = model_probability.tolist()

        return model_pre_list, model_probability

    def active_model_run(self, test):

        model = self.active_model
        model_pre = model.predict(test)
        model_probability = model.predict_proba(test)

        model_pre_list = []
        for p in model_pre:
            model_pre_list.append(str(p).replace("b'", "").replace("'", ""))

        model_probability = model_probability.tolist()

        return model_pre_list, model_probability

    def output(self, test_data):

        test= self.test
        #self.test_parsed_domains = self.parser_object.parse_nonlabeled_samples(test_data)

        model_pre, model_probability = self.model_run(test)
        #test_parsed_domain = self.test_parsed_domains
        result_list = []

        for test_domain in range(len(self.test)):#test_parsed_domain:
            result = {}
            result['id'] = test_domain
            result['class'] = model_pre[test_domain]
            result_list.append(result)

        test_result = open("../output/test-output/result-"+self.time_now+".txt", "w")
        test_result.write(json.dumps(result_list))
        test_result.close()

        return result_list

    def active_output(self, test_data):

        test, test_parsed_domains = self.preparing_test_data(test_data)
        model_pre, model_probability = self.active_model_run(test)

        test_parsed_domain = self.test_parsed_domains
        result_list = []
        #print(model_pre, model_probability)

        for test_domain in test_parsed_domain:
            result = {}
            result['domain'] = test_domain['url']
            result['id'] = test_domain['id']
            result['predicted_class'] = model_pre[test_domain['id']]
            result['probability_phish'] = (model_probability[test_domain['id']][1] / sum(model_probability[test_domain['id']])) * 100
            result['probability_legitimate'] = (model_probability[test_domain['id']][0] / sum(model_probability[test_domain['id']])) * 100
            result_list.append(result)

        test_result = open("../output/test-output/result-"+self.time_now+".txt", "w")
        test_result.write(json.dumps(result_list))
        test_result.close()

        return result_list


    def accuracy(self):
        model = self.model
        test_data, test_label = self.preparing_train_data()
        scores = cross_val_score(model, test_data, test_label, cv=10)

        return scores

    def test_accuracy(self):
        test_file = self.txt_to_list( (open("../output/features/dp29114.txt",'r')))

        self.result_list = self.output(test_file)
        count = 0
        print("Starting...\n")
        for i in range(len(self.test)):

            if self.test_label[i].decode('utf-8') == self.result_list[i]['class']:
                count = count + 1

        acc = ( count / len(self.test) ) * 100

        return acc,count


    def confusion_matrix(self, name):
        """
        train dataseti gsb.arff model içerisinde bu dataset var.
        confisioun matris çıkarmayı istediğimiz datayı preparing_train_data fonksiyonu ile arff formatı okunur.
        okunan dosya data ve label olarak bölünür.
        data model üzerinde çalıştırılır.
        elde edilen tahmin sonuçlarına ilişkin labellar model_preye atılır.

        test_label--bytes array formatında unicode formatına dönüştürülür

        ardından confusion matrix çalıştırılır.
        :param name:
        :return:
        """

        test, test_label = self.preparing_train_data(file_name=name)
        model_pre, model_pro = self.model_run(test)

        test_label_unicode = []

        for t in test_label:
            test_label_unicode.append(str(t, 'utf-8'))
        active = confusion_matrix(test_label_unicode, model_pre, labels=['phish', 'legitimate'])

        test = self.train
        test_label = self.train_label

        model_pre, model_pro = self.model_run(test)

        test_label_unicode = []

        for t in test_label:
            test_label_unicode.append(str(t, 'utf-8'))

        return confusion_matrix(test_label_unicode, model_pre, labels=['phish', 'legitimate']), active
def main():
    testResult = machine_learning_algorithm('GB')
   #test_data = testResult.txt_to_list( (open("../output/features/dp29114.txt",'r')))
    #test_data = testResult.txt_to_list( (open("../data/testdp.txt",'r')))

   #print(testResult.active_output(test_data))
   #print(testResult.confusion_matrix("gsb.arff"))

    print(testResult.test_accuracy())

if __name__=="__main__":
    main()
