import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
class Word2Vec:
    def __init__(self):
        self.training_epoch = 300 # 학습을 반복할 횟수
        self.learning_rate = 0.1 # 학습률
        self.batch_size = 20 # 한번에 학습할 데이터 크기
        self.embeding_size = 2 # 단어 벡터를 구성할 임베딩 차원의 크기
        self.num_sampled = 15
        # word2vec 모델을 학습시키기 위한 ncs_loss 함수에서 사용하기 위한 샘플링 크기
        # batch_size 보다는 작아야 함 !!!
        self.word_list = []
        self.voc_size = 0


    def show_version(self):
        mpl.rcParams['axes.unicode_minus'] = False
        print('버전: ', mpl.__version__)
        print('설치 위치: ', mpl.__file__)
        print('설정 위치: ', mpl.get_configdir())
        print('캐시 위치: ', mpl.get_cachedir())
        print('설정파일 위치: ', mpl.matplotlib_fname())
        print([(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name])
        from matplotlib import font_manager, rc
        rc('font', family=font_manager
           .FontProperties(fname='C:\\WINDOWS\\Fonts\\나눔고딕코딩.ttf')
           .get_name())

    @staticmethod
    def random_batch(data, size):
        random_inputs = []
        random_labels = []
        print(f'random batch : lenth of data {len(data)}')
        random_index = np.random.choice(range(len(data)), size, replace=False)
        for i in random_index:
            random_inputs.append(data[i][0]) # target
            random_labels.append([data[i][1]]) ### random_labels.append(data[i][1]) 주의 !!
        return random_inputs, random_labels

    def execute(self):
        sentences = ["나 고양이 좋다",
                     "나 강아지 좋다",
                     "나 동물 좋다",
                     "강아지 고양이 동물",
                     "여자친구 고양이 강아지 좋다",
                     "고양이 생선 우유 좋다",
                     "강아지 생선 싫다 우유 좋다",
                     "강아지 고양이 눈 좋다",
                     "나 여자친구 좋다",
                     "여자친구 나 싫다",
                     "여자친구 나 영화 책 음악 좋다",
                     "나 게임 만화 애니 좋다",
                     "고양이 강아지 싫다",
                     "강아지 고양이 좋다"]
        # 1. 문장을 모두 합친 후 , 공백으로 단어를 나누고, 중복된 단어 제거 후 리스트 화 한다
        word_sequnce = " ".join(sentences).split()
        self.word_list = " ".join(sentences).split()
        # self.word_list = list(set(self.word_list)) 중복된 삭제시킴
        self.voc_size = len(self.word_list)  # 총단어의 갯수수
        word_dict = {W: i for i, W in enumerate(self.word_list)}
        skip_grams = []
        for i in range(1, len(word_sequnce) -1):
            target = word_dict[word_sequnce[i]]
            context = [word_dict[word_sequnce[i -1]],
                       word_dict[word_sequnce[i + 1]]
                       ]
            for W in context:
                skip_grams.append([target, W])
            # 스킵그램을 만든 후, 저장은 단어의 인덱스로 한다

        # tf 1.0
        inputs = tf.placeholder(tf.int32, shape=[self.batch_size])
        labels = tf.placeholder(tf.int32, shape=[self.batch_size, 1])
        # tf.nn.nce_loss 를 사용하려면 출력값을 이렇게 [batch_size, 1] 구성해야 함
        embeddings = tf.Variable(tf.random_uniform([self.voc_size, self.embeding_size], -1.0, 1.0))
        # word2vec 모델의 결과 값인 임베딩 벡터를 저장할 변수
        # 총 단어의 갯수와 임베딩 갯수를 크기로 하는 두개의 차원을 갖습니다.
        # embedding vector 의 차원에서 학습할 입력값에 대한 행들을 뽑아옵니다.

        """
        embeddings    input  selected
        [[1,2,3]   -> [2,3] ->[[2,3,4],[3,4,5]]
        [2,3,4]
        [3,4,5]
        [4,5,6]
        ]
        
        """
        selected_embed = tf.nn.embedding_lookup(embeddings, inputs)
        nce_weights = tf.Variable(tf.random_uniform([self.voc_size, self.embeding_size], -1.0, 1.0))
        nce_bias = tf.Variable(tf.zeros([self.voc_size]))
        print(f'nce_weights : {nce_weights}')
        print(f'nce_bias : {nce_bias}')
        print(f'labels : {labels}')
        print(f'num_sampled : {self.num_sampled}')
        print(f'voc_size : {self.voc_size}')
        loss = tf.reduce_mean(
            tf.nn.nce_loss(nce_weights, nce_bias, labels, selected_embed, self.num_sampled, self.voc_size )
        )
        train_op = tf.train.AdamOptimizer(self.learning_rate).minimize(loss)


        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for step in range(1, self.training_epoch + 1):
                batch_inputs, batch_labels = self.random_batch(skip_grams, self.batch_size)
                _, loss_val = sess.run([train_op, loss],
                                       {inputs: batch_inputs,
                                        labels: batch_labels})
                if step % 10 == 0:
                    print(f"loss at step : {step }, loss val: {loss_val}")

            trained_embeddings = embeddings.eval()

        for i, label in enumerate(self.word_list):
            x, y = trained_embeddings[i]
            plt.scatter(x, y)
            plt.annotate(label, xy=(x, y), xytext = (5, 2),
                         textcoords='offset points', ha='right', va='bottom')

        plt.show()


if __name__ == '__main__':
    instance = Word2Vec()
    instance.show_version()
    instance.execute()


