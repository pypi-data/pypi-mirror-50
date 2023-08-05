# -*- coding:utf-8 -*-
import pandas as pd

from sfplot.search_from_plot import SearchFromPlot
import sfplot.search_core as s_core


class SearchFromBoxplot(SearchFromPlot):

    def _validation(self, df, x, y, category_list_x, category_list_y):
        """ 個別バリデーションを実装 """
        if df[x].dtype != 'object':
            raise Exception('ｘ軸にobject以外のカラムは指定できません')
        if df[y].dtype != 'float' and df[y].dtype != 'int':
            raise Exception('ｙ軸に数値以外のカラムは指定できません')


    def _draw_figure(self, fig, ax, info):
        """ DataFrameから箱ひげ図を作図 """
        # 明示的にinfoから使う変数を取り出す
        df = info.df
        category_col = info.target_col_x
        target_col = info.target_col_y
        categories = info.category_list_x

        # カテゴリ値毎にデータを取り出す
        category_values = []
        for category in categories:
            category_value = df.loc[df[category_col]==category, target_col].tolist()
            category_values.append(category_value)

        # 箱ひげ図のプロット
        ax.boxplot(category_values,
                   patch_artist=True,  # 細かい設定をできるようにする
                   boxprops=dict(facecolor='green',  # boxの塗りつぶし色の設定
                                 color='black', linewidth=1),  # boxの枠線の設定
                   widths=1,  # boxの幅の設定
                   flierprops=dict(markeredgecolor='lightgreen',
                                   markeredgewidth=1, marker='+'),  # 外れ値の設定
        )
        ax.set_ylim(df[target_col].min(), df[target_col].max())
        ax.set_xticklabels(categories)


    def _get_data_point(self, info, scale_x, scale_y):
        """ 座標のデータ値を取得 """
        # 明示的にinfoから使う変数を取り出す
        categories = info.category_list_x
        data_y_min = info.y_min
        data_y_max = info.y_max

        # データ値を取り出す
        _, data_x_to = s_core.convert_scaling_point2index_range(0, scale_x, len(categories))
        _, data_y_to = s_core.convert_scaling_point2data_range(0, scale_y, data_y_min, data_y_max)

        return categories[data_x_to], data_y_to


    def _get_square_corner_point(self, info):
        """ 選択範囲描画用図形の座標を取得 """
        """ Override """
        # 明示的にinfoから使う変数を取り出す
        canvas_size_x = info.canvas_size_x
        drag_x = info.drag_x
        drag_y = info.drag_y
        drop_x = info.drop_x
        drop_y = info.drop_y
        categories = info.category_list_x

        # X軸を選択カテゴリすべてを覆うように変換
        scale_x_from, scale_x_to = s_core.convert_drag_point2scaling_point(0, canvas_size_x, drag_x, drop_x)
        data_x_from, data_x_to = s_core.convert_scaling_point2index_range(scale_x_from, scale_x_to, len(categories))
        unit_size = canvas_size_x / len(categories)

        return data_x_from * unit_size, drag_y, (data_x_to+1) * unit_size, drop_y


    def _get_selected_range_df(self, info, scale_x_from, scale_x_to, scale_y_from, scale_y_to):
        """ 選択された範囲内にあるレコードを抽出 """
        # 明示的にinfoから使う変数を取り出す
        df = info.df
        target_col_x = info.target_col_x
        target_col_y = info.target_col_y
        categories = info.category_list_x
        data_y_min = info.y_min
        data_y_max = info.y_max

        data_x_from, data_x_to = s_core.convert_scaling_point2index_range(scale_x_from, scale_x_to,
                                                                          len(categories))
        data_y_from, data_y_to = s_core.convert_scaling_point2data_range(scale_y_from, scale_y_to,
                                                                         data_y_min, data_y_max)

        # 選択カテゴリの条件判定を先に行う
        category_condition = None
        for category in categories[data_x_from:data_x_to+1]:
            if category_condition is None:
                category_condition = df[target_col_x]==category
            else:
                category_condition = category_condition | (df[target_col_x]==category)

        # Y軸の判定を加えてデータを取得
        if category_condition is None:
            selected_range_df = df[:0]
        else:
            selected_range_df = df[(category_condition) &
                                   (df[target_col_y] >= data_y_from) &
                                   (df[target_col_y] <= data_y_to)]

        return selected_range_df
