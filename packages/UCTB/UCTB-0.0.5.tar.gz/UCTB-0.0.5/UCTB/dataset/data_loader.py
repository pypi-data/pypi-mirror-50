import copy
import datetime
import numpy as np

from dateutil.parser import parse
from sklearn.metrics.pairwise import cosine_similarity

from ..preprocess.time_utils import is_work_day_china, is_work_day_america, is_valid_date
from ..preprocess import MoveSample, SplitData, ST_MoveSample, Normalizer
from ..model_unit import GraphBuilder

from .dataset import DataSet


class GridTrafficLoader(object):

    def __init__(self,
                 dataset,
                 city=None,
                 data_range='all',
                 train_data_length='all',
                 test_ratio=0.1,
                 closeness_len=6,
                 period_len=7,
                 trend_len=4,
                 target_length=1,
                 normalize=True,
                 workday_parser=is_work_day_america,
                 data_dir=None, **kwargs):

        self.dataset = DataSet(dataset, city, data_dir=data_dir)

        self.daily_slots = 24 * 60 / self.dataset.time_fitness

        if type(data_range) is str and data_range.lower() == 'all':
            data_range = [0, len(self.dataset.grid_traffic)]
        elif type(data_range) is float:
            data_range = [0, int(data_range * len(self.dataset.grid_traffic))]
        else:
            data_range = [int(data_range[0] * self.daily_slots), int(data_range[1] * self.daily_slots)]

        num_time_slots = data_range[1] - data_range[0]
        self.traffic_data = self.dataset.grid_traffic[data_range[0]:data_range[1], :].astype(np.float32)

        # external feature
        external_feature = []
        # weather
        if len(self.dataset.external_feature_weather) > 0:
            external_feature.append(self.dataset.external_feature_weather[data_range[0]:data_range[1]])
        # Weekday Feature
        weekday_feature = [[1 if workday_parser(parse(self.dataset.time_range[1])
                                                + datetime.timedelta(hours=e * self.dataset.time_fitness / 60)) else 0] \
                           for e in range(data_range[0], num_time_slots + data_range[0])]
        # Hour Feature
        hour_feature = [[(parse(self.dataset.time_range[1]) +
                          datetime.timedelta(hours=e * self.dataset.time_fitness / 60)).hour / 24.0]
                        for e in range(data_range[0], num_time_slots + data_range[0])]

        external_feature.append(weekday_feature)
        external_feature.append(hour_feature)
        external_feature = np.concatenate(external_feature, axis=-1).astype(np.float32)

        self.height, self.width = self.traffic_data.shape[1], self.traffic_data.shape[2]
        self.external_dim = external_feature.shape[1]

        if test_ratio > 1 or test_ratio < 0:
            raise ValueError('test_ratio ')
        train_test_ratio = [1 - test_ratio, test_ratio]

        self.train_data, self.test_data = SplitData.split_data(self.traffic_data, train_test_ratio)
        self.train_ef, self.test_ef = SplitData.split_data(external_feature, train_test_ratio)

        # Normalize the traffic data
        if normalize:
            self.normalizer = Normalizer(self.train_data)
            self.train_data = self.normalizer.min_max_normal(self.train_data)
            self.test_data = self.normalizer.min_max_normal(self.test_data)

        if train_data_length.lower() != 'all':
            train_day_length = int(train_data_length)
            self.train_data = self.train_data[-int(train_day_length * self.daily_slots):]
            self.train_ef = self.train_ef[-int(train_day_length * self.daily_slots):]

        # expand the test data
        expand_start_index = len(self.train_data) - max(int(self.daily_slots * period_len),
                                                        int(self.daily_slots * 7 * trend_len), closeness_len)

        self.test_data = np.vstack([self.train_data[expand_start_index:], self.test_data])
        self.test_ef = np.vstack([self.train_ef[expand_start_index:], self.test_ef])

        assert type(closeness_len) is int and closeness_len >= 0
        assert type(period_len) is int and period_len >= 0
        assert type(trend_len) is int and trend_len >= 0

        self.closeness_len = closeness_len
        self.period_len = period_len
        self.trend_len = trend_len

        # init move sample obj
        self.st_move_sample = ST_MoveSample(closeness_len=closeness_len,
                                            period_len=period_len,
                                            trend_len=trend_len, target_length=1, daily_slots=self.daily_slots)

        self.train_closeness, \
        self.train_period, \
        self.train_trend, \
        self.train_y = self.st_move_sample.move_sample(self.train_data)

        self.test_closeness, \
        self.test_period, \
        self.test_trend, \
        self.test_y = self.st_move_sample.move_sample(self.test_data)

        self.train_closeness = self.train_closeness.squeeze(-1)
        self.train_period = self.train_period.squeeze(-1)
        self.train_trend = self.train_trend.squeeze(-1)

        self.test_closeness = self.test_closeness.squeeze(-1)
        self.test_period = self.test_period.squeeze(-1)
        self.test_trend = self.test_trend.squeeze(-1)

        self.train_sequence_len = max((len(self.train_closeness), len(self.train_period), len(self.train_trend)))
        self.test_sequence_len = max((len(self.test_closeness), len(self.test_period), len(self.test_trend)))

        # external feature
        self.train_ef = self.train_ef[-self.train_sequence_len - target_length: -target_length]
        self.test_ef = self.test_ef[-self.test_sequence_len - target_length: -target_length]


class NodeTrafficLoader(object):
    """The data loader that extracts and processes data from a :obj:`DataSet` object.

    Args:
        dataset (str): A string containing path of the dataset pickle file or a string of name of the dataset.
        city (:obj:`str` or ``None``): ``None`` if dataset is file path, or a string of name of the city.
            Default: ``None``
        data_range: The range of data extracted from ``self.dataset`` to be further used. If set to ``'all'``, all data in
            ``self.dataset`` will be used. If set to a float between 0.0 and 1.0, the relative former proportion of data in
            ``self.dataset`` will be used. If set to a list of two integers ``[start, end]``, the data from *start* day to
            (*end* - 1) day of data in ``self.dataset`` will be used. Default: ``'all'``
        train_data_length: The length of train data. If set to ``'all'``, all data in the split train set will be used.
            If set to int, the latest ``train_data_length`` days of data will be used as train set. Default: ``'all'``
        test_ratio (float): The ratio of test set as data will be split into train set and test set. Default: 0.1
        closeness_len (int): The length of closeness data history. The former consecutive ``closeness_len`` time slots
            of data will be used as closeness history. Default: 6
        period_len (int): The length of period data history. The data of exact same time slots in former consecutive
            ``period_len`` days will be used as period history. Default: 7
        trend_len (int): The length of trend data history. The data of exact same time slots in former consecutive
            ``trend_len`` weeks (every seven days) will be used as trend history. Default: 4
        target_length (int): The numbers of steps that need prediction by one piece of history data. Have to be 1 now.
            Default: 1
        graph (str): Types of graphs used in neural methods. Graphs should be a subset of { ``'Correlation'``,
            ``'Distance'``, ``'Interaction'``, ``'Line'``, ``'Neighbor'``, ``'Transfer'`` } and concatenated by ``'-'``,
            and *dataset* should have data of selected graphs. Default: ``'Correlation'``
        threshold_distance (float): Used in building of distance graph. If distance of two nodes in meters is larger
            than ``threshold_distance``, the corresponding position of the distance graph will be 1 and otherwise
            0.the corresponding Default: 1000
        threshold_correlation (float): Used in building of correlation graph. If the Pearson correlation coefficient is
            larger than ``threshold_correlation``, the corresponding position of the correlation graph will be 1
            and otherwise 0. Default: 0
        threshold_interaction (float): Used in building of interatction graph. If in the latest 12 months, the number of
            times of interaction between two nodes is larger than ``threshold_interaction``, the corresponding position
            of the interaction graph will be 1 and otherwise 0. Default: 500
        normalize (bool): If ``True``, do min-max normalization on data. Default: ``True``
        workday_parser: Used to build external features to be used in neural methods. Default: ``is_work_day_america``
        with_lm (bool): If ``True``, data loader will build graphs according to ``graph``. Default: ``True``
        with_tpe (bool): If ``True``, data loader will build time position embeddings. Default: ``False``
        data_dir (:obj:`str` or ``None``): The dataset directory. If set to ``None``, a directory will be created. If
            ``dataset`` is file path, ``data_dir`` should be ``None`` too. Default: ``None``

    Attributes:
        dataset (DataSet): The DataSet object storing basic data.
        daily_slots (int): The number of time slots in one single day.
        station_number (int): The number of nodes.
        external_dim (int): The number of dimensions of external features.
        train_closeness (np.ndarray): The closeness history of train set data. When ``with_tpe`` is ``False``,
            its shape is [train_time_slot_num, ``station_number``, ``closeness_len``, 1].
            On the dimension of ``closeness_len``, data are arranged from earlier time slots to later time slots.
            If ``closeness_len`` is set to 0, train_closeness will be an empty ndarray.
            ``train_period``, ``train_trend``, ``test_closeness``, ``test_period``, ``test_trend`` have similar shape
            and construction.
        train_y (np.ndarray): The train set data. Its shape is [train_time_slot_num, ``station_number``, 1].
            ``test_y`` has similar shape and construction.
        LM (list): If ``with_lm`` is ``True``, the list of Laplacian matrices of graphs listed in ``graph``.
    """
    def __init__(self,
                 dataset,
                 city=None,
                 data_range='all',
                 train_data_length='all',
                 test_ratio=0.1,
                 closeness_len=6,
                 period_len=7,
                 trend_len=4,
                 target_length=1,
                 graph='Correlation',
                 threshold_distance=1000,
                 threshold_correlation=0,
                 threshold_interaction=500,
                 normalize=True,
                 workday_parser=is_work_day_america,
                 with_lm=True,
                 with_tpe=False,
                 data_dir=None, **kwargs):

        self.dataset = DataSet(dataset, city, data_dir=data_dir)

        self.daily_slots = 24 * 60 / self.dataset.time_fitness

        self.closeness_len = int(closeness_len)
        self.period_len = int(period_len)
        self.trend_len = int(trend_len)

        assert type(self.closeness_len) is int and self.closeness_len >= 0
        assert type(self.period_len) is int and self.period_len >= 0
        assert type(self.trend_len) is int and self.trend_len >= 0

        if type(data_range) is str and data_range.lower() == 'all':
            data_range = [0, len(self.dataset.node_traffic)]
        elif type(data_range) is float:
            data_range = [0, int(data_range * len(self.dataset.node_traffic))]
        else:
            data_range = [int(data_range[0] * self.daily_slots), int(data_range[1] * self.daily_slots)]

        num_time_slots = data_range[1] - data_range[0]

        # traffic feature
        traffic_data_index = np.where(np.mean(self.dataset.node_traffic, axis=0) * self.daily_slots > 1)[0]

        self.traffic_data = self.dataset.node_traffic[data_range[0]:data_range[1], traffic_data_index].astype(
            np.float32)

        # external feature
        external_feature = []
        # weather
        if len(self.dataset.external_feature_weather) > 0:
            external_feature.append(self.dataset.external_feature_weather[data_range[0]:data_range[1]])
        # Weekday Feature
        weekday_feature = [[1 if workday_parser(parse(self.dataset.time_range[1])
                                                + datetime.timedelta(hours=e * self.dataset.time_fitness / 60)) else 0] \
                           for e in range(data_range[0], num_time_slots + data_range[0])]
        # Hour Feature
        hour_feature = [[(parse(self.dataset.time_range[1]) +
                          datetime.timedelta(hours=e * self.dataset.time_fitness / 60)).hour / 24.0]
                        for e in range(data_range[0], num_time_slots + data_range[0])]

        external_feature.append(weekday_feature)
        external_feature.append(hour_feature)
        external_feature = np.concatenate(external_feature, axis=-1).astype(np.float32)

        self.station_number = self.traffic_data.shape[1]
        self.external_dim = external_feature.shape[1]

        if test_ratio > 1 or test_ratio < 0:
            raise ValueError('test_ratio ')
        train_test_ratio = [1 - test_ratio, test_ratio]

        self.train_data, self.test_data = SplitData.split_data(self.traffic_data, train_test_ratio)
        self.train_ef, self.test_ef = SplitData.split_data(external_feature, train_test_ratio)

        # Normalize the traffic data
        if normalize:
            self.normalizer = Normalizer(self.train_data)
            self.train_data = self.normalizer.min_max_normal(self.train_data)
            self.test_data = self.normalizer.min_max_normal(self.test_data)

        if train_data_length.lower() != 'all':
            train_day_length = int(train_data_length)
            self.train_data = self.train_data[-int(train_day_length * self.daily_slots):]
            self.train_ef = self.train_ef[-int(train_day_length * self.daily_slots):]

        # expand the test data
        expand_start_index = len(self.train_data) - \
                             max(int(self.daily_slots * self.period_len),
                                 int(self.daily_slots * 7 * self.trend_len),
                                 self.closeness_len)

        self.test_data = np.vstack([self.train_data[expand_start_index:], self.test_data])
        self.test_ef = np.vstack([self.train_ef[expand_start_index:], self.test_ef])

        # init move sample obj
        self.st_move_sample = ST_MoveSample(closeness_len=self.closeness_len,
                                            period_len=self.period_len,
                                            trend_len=self.trend_len, target_length=1, daily_slots=self.daily_slots)

        self.train_closeness, \
        self.train_period, \
        self.train_trend, \
        self.train_y = self.st_move_sample.move_sample(self.train_data)

        self.test_closeness, \
        self.test_period, \
        self.test_trend, \
        self.test_y = self.st_move_sample.move_sample(self.test_data)

        self.train_sequence_len = max((len(self.train_closeness), len(self.train_period), len(self.train_trend)))
        self.test_sequence_len = max((len(self.test_closeness), len(self.test_period), len(self.test_trend)))

        # external feature
        self.train_ef = self.train_ef[-self.train_sequence_len - target_length: -target_length]
        self.test_ef = self.test_ef[-self.test_sequence_len - target_length: -target_length]

        if with_tpe:

            # Time position embedding
            self.closeness_tpe = np.array(range(1, self.closeness_len + 1), dtype=np.float32)
            self.period_tpe = np.array(range(1 * int(self.daily_slots),
                                             self.period_len * int(self.daily_slots) + 1,
                                             int(self.daily_slots)), dtype=np.float32)
            self.trend_tpe = np.array(range(1 * int(self.daily_slots) * 7,
                                            self.trend_len * int(self.daily_slots) * 7 + 1,
                                            int(self.daily_slots) * 7), dtype=np.float32)

            self.train_closeness_tpe = np.tile(np.reshape(self.closeness_tpe, [1, 1, -1, 1]),
                                               [len(self.train_closeness), len(traffic_data_index), 1, 1])
            self.train_period_tpe = np.tile(np.reshape(self.period_tpe, [1, 1, -1, 1]),
                                            [len(self.train_period), len(traffic_data_index), 1, 1])
            self.train_trend_tpe = np.tile(np.reshape(self.trend_tpe, [1, 1, -1, 1]),
                                           [len(self.train_trend), len(traffic_data_index), 1, 1])

            self.test_closeness_tpe = np.tile(np.reshape(self.closeness_tpe, [1, 1, -1, 1]),
                                              [len(self.test_closeness), len(traffic_data_index), 1, 1])
            self.test_period_tpe = np.tile(np.reshape(self.period_tpe, [1, 1, -1, 1]),
                                           [len(self.test_period), len(traffic_data_index), 1, 1])
            self.test_trend_tpe = np.tile(np.reshape(self.trend_tpe, [1, 1, -1, 1]),
                                          [len(self.test_trend), len(traffic_data_index), 1, 1])

            self.tpe_dim = self.train_closeness_tpe.shape[-1]

            # concat temporal feature with time position embedding
            self.train_closeness = np.concatenate((self.train_closeness, self.train_closeness_tpe,), axis=-1)
            self.train_period = np.concatenate((self.train_period, self.train_period_tpe,), axis=-1)
            self.train_trend = np.concatenate((self.train_trend, self.train_trend_tpe,), axis=-1)

            self.test_closeness = np.concatenate((self.test_closeness, self.test_closeness_tpe,), axis=-1)
            self.test_period = np.concatenate((self.test_period, self.test_period_tpe,), axis=-1)
            self.test_trend = np.concatenate((self.test_trend, self.test_trend_tpe,), axis=-1)

        else:

            self.tpe_dim = None

        if with_lm:

            self.LM = []
            self.AM = []

            for graph_name in graph.split('-'):

                if graph_name.lower() == 'distance':

                    # Default order by date
                    order_parser = parse
                    try:
                        for key, value in self.dataset.node_station_info.items():
                            if is_valid_date(value[0]) is False:
                                order_parser = lambda x: x
                                print('Order by string')
                                break
                    except:
                        order_parser = lambda x: x
                        print('Order by string')

                    lat_lng_list = \
                        np.array([[float(e1) for e1 in e[1][1:3]] for e in
                                  sorted(self.dataset.node_station_info.items(),
                                         key=lambda x: order_parser(x[1][0]), reverse=False)])
                    self.AM.append(GraphBuilder.distance_adjacent(lat_lng_list[traffic_data_index], threshold=float(threshold_distance)))
                    self.LM.append(GraphBuilder.adjacent_to_laplacian(self.AM[-1]))

                if graph_name.lower() == 'interaction':
                    monthly_interaction = self.dataset.node_monthly_interaction[:, traffic_data_index, :][:, :,
                                          traffic_data_index]

                    monthly_interaction, _ = SplitData.split_data(monthly_interaction, train_test_ratio)

                    annually_interaction = np.sum(monthly_interaction[-12:], axis=0)
                    annually_interaction = annually_interaction + annually_interaction.transpose()

                    self.AM.append(GraphBuilder.interaction_adjacent(annually_interaction,
                                                                     threshold=float(threshold_interaction)))

                    self.LM.append(GraphBuilder.adjacent_to_laplacian(self.AM[-1]))

                if graph_name.lower() == 'correlation':
                    self.AM.append(GraphBuilder.correlation_adjacent(self.train_data[-30 * int(self.daily_slots):],
                                                                     threshold=float(threshold_correlation)))
                    self.LM.append(GraphBuilder.adjacent_to_laplacian(self.AM[-1]))

                if graph_name.lower() == 'neighbor':
                    self.LM.append(
                        GraphBuilder.adjacent_to_laplacian(
                            self.dataset.data.get('contribute_data').get('graph_neighbors')))

                if graph_name.lower() == 'line':
                    self.LM.append(
                        GraphBuilder.adjacent_to_laplacian(self.dataset.data.get('contribute_data').get('graph_lines')))

                if graph_name.lower() == 'transfer':
                    self.LM.append(
                        GraphBuilder.adjacent_to_laplacian(
                            self.dataset.data.get('contribute_data').get('graph_transfer')))

            self.LM = np.array(self.LM, dtype=np.float32)

    def st_map(self, zoom=11, style='light'):

        if self.dataset.node_station_info is None or len(self.dataset.node_station_info) == 0:
            raise ValueError('No station information found in dataset')

        import numpy as np
        import plotly
        from plotly.graph_objs import Scattermapbox, Layout

        mapboxAccessToken = "pk.eyJ1Ijoicm1ldGZjIiwiYSI6ImNqN2JjN3l3NjBxc3MycXAzNnh6M2oxbGoifQ.WFNVzFwNJ9ILp0Jxa03mCQ"

        order_parser = parse
        try:
            for key, value in self.dataset.node_station_info.items():
                if is_valid_date(value[0]) is False:
                    order_parser = lambda x: x
                    print('Order by string')
                    break
        except:
            order_parser = lambda x: x
            print('Order by string')

        lat_lng_name_list = [e[1][1:] for e in
                             sorted(self.dataset.node_station_info.items(), key=lambda x: order_parser(x[1][0]),
                                    reverse=False)]
        build_order = list(range(len(lat_lng_name_list)))

        lng = [float(e[1]) for e in lat_lng_name_list]
        lat = [float(e[0]) for e in lat_lng_name_list]
        text = [e[-1] for e in lat_lng_name_list]

        file_name = self.dataset.dataset + '-' + self.dataset.city + '.html'

        bikeStations = [Scattermapbox(
            lon=lng,
            lat=lat,
            text=text,
            mode='markers',
            marker=dict(
                size=6,
                color=['rgb(%s, %s, %s)' % (255,
                                            195 - e * 195 / max(build_order),
                                            195 - e * 195 / max(build_order)) for e in build_order],
                opacity=1,
            ))]

        layout = Layout(
            title='Bike Station Location & The latest built stations with deeper color',
            autosize=True,
            hovermode='closest',
            showlegend=False,
            mapbox=dict(
                accesstoken=mapboxAccessToken,
                bearing=0,
                center=dict(
                    lat=np.median(lat),
                    lon=np.median(lng)
                ),
                pitch=0,
                zoom=zoom,
                style=style
            ),
        )

        fig = dict(data=bikeStations, layout=layout)
        plotly.offline.plot(fig, filename=file_name)

    def make_concat(self, node='all', is_train=True):
        """A function to concatenate all closeness, period and trend history data to use as inputs of models.

        Args:
            node (int or ``'all'``): To specify the index of certain node. If set to ``'all'``, return the concatenation
                result of all nodes. If set to an integer, it will be the index of the selected node. Default: ``'all'``
            is_train (bool): If set to ``True``, ``train_closeness``, ``train_period``, and ``train_trend`` will be
                concatenated. If set to ``False``, ``test_closeness``, ``test_period``, and ``test_trend`` will be
                concatenated. Default: True

        Returns:
            np.ndarray: Function returns an ndarray with shape as
            [time_slot_num, ``station_number``, ``closeness_len`` + ``period_len`` + ``trend_len``, 1],
            and time_slot_num is the temporal length of train set data if ``is_train`` is ``True``
            or the temporal length of test set data if ``is_train`` is ``False``.
            On the second dimension, data are arranged as
             ``earlier closeness -> later closeness -> earlier period -> later period -> earlier trend -> later trend``.
        """

        if is_train:
            length = len(self.train_y)
            closeness = self.train_closeness
            period = self.train_period
            trend = self.train_trend
        else:
            length = len(self.test_y)
            closeness = self.test_closeness
            period = self.test_period
            trend = self.test_trend
        if node == 'all':
            node = list(range(self.station_number))
        else:
            node = [node]
        history = np.zeros([length, len(node), self.closeness_len + self.period_len + self.trend_len])
        for i in range(len(node)):
            for c in range(self.closeness_len):
                history[:, i, c] = closeness[:, node[i], c, -1]
            for p in range(self.period_len):
                history[:, i, self.closeness_len + p] = period[:, node[i], p, -1]
            for t in range(self.trend_len):
                history[:, i, self.closeness_len + self.period_len + t] = trend[:, node[i], t, -1]
        history = np.expand_dims(history, 3)
        return history


class TransferDataLoader(object):

    def __init__(self, sd_params, td_params, model_params, td_data_length=None):

        if td_data_length:
            td_params.update({'train_data_length': td_data_length})

        self.sd_loader = NodeTrafficLoader(**sd_params, **model_params)
        self.td_loader = NodeTrafficLoader(**td_params, **model_params)

        # fake td data_loader
        # td_params.update({'train_data_length': str(int(td_data_length) + 30)})
        td_params.update({'train_data_length': '1'})
        self.fake_td_loader = NodeTrafficLoader(**td_params, **model_params)

    def traffic_sim(self):

        assert self.sd_loader.daily_slots == self.td_loader.daily_slots

        similar_record = []

        for i in range(0, self.sd_loader.train_data.shape[0] - self.td_loader.train_data.shape[0],
                       int(self.sd_loader.daily_slots)):

            sim = cosine_similarity(self.td_loader.train_data.transpose(),
                                    self.sd_loader.train_data[i:i + self.td_loader.train_data.shape[0]].transpose())

            max_sim, max_index = np.max(sim, axis=1), np.argmax(sim, axis=1)

            if len(similar_record) == 0:
                similar_record = [[max_sim[e], max_index[e], i, i + self.td_loader.train_data.shape[0]]
                                  for e in range(len(max_sim))]
            else:
                for index in range(len(similar_record)):
                    if similar_record[index][0] < max_sim[index]:
                        similar_record[index] = [max_sim[index], max_index[index], i,
                                                 i + self.td_loader.train_data.shape[0]]

        return similar_record

    def traffic_sim_fake(self):

        assert self.sd_loader.daily_slots == self.td_loader.daily_slots

        similar_record = []

        for i in range(0, self.sd_loader.train_data.shape[0] - self.fake_td_loader.train_data.shape[0],
                       int(self.sd_loader.daily_slots)):

            sim = cosine_similarity(self.fake_td_loader.train_data.transpose(),
                                    self.sd_loader.train_data[
                                    i:i + self.fake_td_loader.train_data.shape[0]].transpose())

            max_sim, max_index = np.max(sim, axis=1), np.argmax(sim, axis=1)

            if len(similar_record) == 0:
                similar_record = [[max_sim[e], max_index[e], i, i + self.fake_td_loader.train_data.shape[0]]
                                  for e in range(len(max_sim))]
            else:
                for index in range(len(similar_record)):
                    if similar_record[index][0] < max_sim[index]:
                        similar_record[index] = [max_sim[index], max_index[index], i,
                                                 i + self.fake_td_loader.train_data.shape[0]]

        for i in range(len(similar_record)):
            similar_record[i][2] = similar_record[i][3] - self.td_loader.train_data.shape[0]

        return similar_record
