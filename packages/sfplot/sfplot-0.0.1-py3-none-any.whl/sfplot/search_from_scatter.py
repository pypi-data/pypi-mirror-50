# -*- coding:utf-8 -*-
import pandas as pd

from sfplot.search_from_plot import SearchFromPlot
import sfplot.search_core as s_core


class SearchFromScatter(SearchFromPlot):

    def _validation(self, df, x, y, category_list_x, category_list_y):
        """ 個別バリデーションを実装 """
        if not df[x].dtype == 'float' and df[x].dtype == 'int':
            raise Exception('ｘ軸に数値以外のカラムは指定できません')
        if not df[y].dtype == 'float' and df[y].dtype == 'int':
            raise Exception('ｙ軸に数値以外のカラムは指定できません')


    def _draw_figure(self, fig, ax, info):
        """ DataFrameから散布図を作図 """
        # 明示的にinfoから使う変数を取り出す
        df = info.df
        x = info.target_col_x
        y = info.target_col_y

        # 散布図をプロット
        ax.scatter(df[x], df[y], marker='.', color='green', alpha=0.5)
        ax.set_xlim(df[x].min(), df[x].max())
        ax.set_ylim(df[y].min(), df[y].max())


    def _get_data_point(self, info, scale_x, scale_y):
        """ 座標のデータ値を取得 """
        # 明示的にinfoから使う変数を取り出す
        data_x_min = info.x_min
        data_x_max = info.x_max
        data_y_min = info.y_min
        data_y_max = info.y_max

        # データ値を取り出す
        _, data_x = s_core.convert_scaling_point2data_range(0, scale_x, data_x_min, data_x_max)
        _, data_y = s_core.convert_scaling_point2data_range(0, scale_y, data_y_min, data_y_max)

        return data_x, data_y


    def _get_selected_range_df(self, info, scale_x_from, scale_x_to, scale_y_from, scale_y_to):
        """ 選択された範囲内にあるレコードを抽出 """
        # 明示的にinfoから使う変数を取り出す
        df = info.df
        target_col_x = info.target_col_x
        target_col_y = info.target_col_y
        data_x_min = info.x_min
        data_x_max = info.x_max
        data_y_min = info.y_min
        data_y_max = info.y_max

        # 選択範囲をデータ値の範囲に変換する
        data_x_from, data_x_to = s_core.convert_scaling_point2data_range(scale_x_from, scale_x_to,
                                                                         data_x_min, data_x_max)
        data_y_from, data_y_to = s_core.convert_scaling_point2data_range(scale_y_from, scale_y_to,
                                                                         data_y_min, data_y_max)

        # データ値の範囲内のレコードを取得する
        result_df = df[(df[target_col_x] >= data_x_from) &
                       (df[target_col_x] <= data_x_to) &
                       (df[target_col_y] >= data_y_from) &
                       (df[target_col_y] <= data_y_to)]

        return result_df
