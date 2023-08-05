# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sfplot.search_core as s_core

class SearchFromPlot:

    class Info:
        """ 検索に必要な情報をまとめる """
        def __init__(self, sfp_class):
            self.canvas_size_x = sfp_class.canvas_size_x
            self.canvas_size_y = sfp_class.canvas_size_y
            self.drag_x = 0
            self.drag_y = 0
            self.drop_x = 0
            self.drop_y = 0

            self.df = None
            self.target_col_x = ''
            self.target_col_y = ''
            self.category_list_x = []
            self.category_list_y = []


        def set_drag_point(self, x, y):
            self.drag_x = x
            self.drag_y = y


        def set_drop_point(self, x, y):
            self.drop_x = x
            self.drop_y = y


        def set_df(self, df, x, y, category_list_x, category_list_y):
            self.df = df
            self.target_col_x = x
            self.target_col_y = y
            if category_list_x:
                self.category_list_x = category_list_x
            else:
                self.category_list_x = df[x].unique()
            if category_list_y:
                self.category_list_y = category_list_y
            else:
                self.category_list_y = df[y].unique()
            if df[x].dtype == 'float' or df[x].dtype == 'int':
                self.x_min = df[x].min()
                self.x_max = df[x].max()
            else:
                self.x_min = 0
                self.x_max = 0
            if df[y].dtype == 'float' or df[y].dtype == 'int':
                self.y_min = df[y].min()
                self.y_max = df[y].max()
            else:
                self.y_min = 0
                self.y_max = 0


    def __init__(self, canvas_size_x, canvas_size_y, dpi):
        self.canvas_size_x = canvas_size_x
        self.canvas_size_y = canvas_size_y
        self._dpi = dpi


    def __call__(self, df, x='', y='', category_list_x=[], category_list_y=[], return_debbug_info=False):

        self._abstract_validation(df, x, y, category_list_x, category_list_y)

        info = SearchFromPlot.Info(self)
        info.set_df(df, x, y, category_list_x, category_list_y)

        dnd_flg = False
        result_df = df[:0]

        root = tk.Tk()
        root.title('SFPlot')

        # 画面中央に表示
        root.geometry('%dx%d+%d+%d' % (self.canvas_size_x,
                                       self.canvas_size_y + 45,
                                       root.winfo_screenwidth()/2 - self.canvas_size_x/2,
                                       root.winfo_screenheight()/2 - self.canvas_size_y/2))
        root.resizable(0,0)

        ## 画像を配置
        def on_canvas_mouse_click(event):
            nonlocal dnd_flg
            # ドラッグ中でない場合、ドラッグアンドドロップフラグを有効化
            # 座標取得・選択範囲表示用の図形を配置
            if not dnd_flg:
                dnd_flg = True
                info.set_drag_point(event.x, event.y)
                canvas_widget.create_rectangle(info.drag_x, info.drag_y,
                                               info.drag_x, info.drag_y,
                                               outline='#FB8072', tags='rect')


        def on_canvas_mouse_drag(event):
            # 座標取得
            info.set_drop_point(event.x, event.y)
            # マウスが載ってる座標の情報をラベルに表示
            under_label_var.set(self._abstract_get_data_point(info))
            # ドラッグ中の場合、選択範囲表示用の図形のサイズを変更
            if dnd_flg:
                x1, y1, x2, y2 = self._get_square_corner_point(info)
                canvas_widget.coords('rect', x1, y1, x2, y2)


        def on_canvas_mouse_release(event):
            nonlocal dnd_flg, result_df
            if dnd_flg:
                # 座標取得
                info.set_drop_point(event.x, event.y)
                # 選択範囲表示用の図形を削除
                canvas_widget.delete('rect')
                # 選択履歴用の図形を配置
                x1, y1, x2, y2 = self._get_square_corner_point(info)
                canvas_widget.create_rectangle(x1, y1, x2, y2, outline='#8DD3C7')
                # 情報から選択範囲のdfを取得
                result_df = self._abstract_get_selected_range_df(info, result_df)
                # 検索終了ボタンに選択中のデータ件数を表示
                data_count = len(result_df)
                if data_count > 100:
                    finish_button.configure(text='100件以上取得')
                else:
                    finish_button.configure(text=str(data_count)+'件取得')
                # ドラッグアンドドロップフラグを無効化
                dnd_flg = False


        fig = self._abstract_get_figure(info)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=0, y=0)
        canvas_widget.bind('<Button-1>', on_canvas_mouse_click)
        canvas_widget.bind('<Motion>', on_canvas_mouse_drag)
        canvas_widget.bind('<ButtonRelease-1>', on_canvas_mouse_release)

        ## ラベルを配置
        under_label_font = font.Font(family='ＭＳ ゴシック', weight='bold')
        under_label_var = tk.StringVar()
        under_label = tk.Label(root,
                               textvariable=under_label_var,
                               font=under_label_font,
                               justify='left',)
        under_label.place(x=0, y=self.canvas_size_y)

        ## N件取得ボタンを配置
        finish_button_width = 90
        finish_button = tk.Button(root,
                                  text='0件取得',
                                  width=11,
                                  height=2,
                                  command=root.destroy)
        finish_button.place(x=self.canvas_size_x-finish_button_width, y=self.canvas_size_y+2)

        root.mainloop()

        if return_debbug_info:
            return result_df, info
        else:
            return result_df


    def _abstract_validation(self, df, x, y, category_list_x, category_list_y):
        """ 共通バリデーションを実装 """
        if not x or not y:
            raise Exception('ｘまたはｙカラムの入力がありません')
        cols = df.columns.tolist()
        if x not in cols or y not in cols:
            raise Exception('指定したカラムがDataFrame内に存在しません')

        self._validation(df, x, y, category_list_x, category_list_y)


    def _validation(self, df, x, y, category_list_x, category_list_y):
        """ abstract method """
        """ 個別バリデーションを実装 """
        raise Exception('not abstracted...')


    def _abstract_get_figure(self, info):
        """ DataFrameから作図 """
        figsize=(self.canvas_size_x/self._dpi, self.canvas_size_y/self._dpi)
        fig = plt.figure(figsize=figsize, dpi=self._dpi)
        ax = fig.add_subplot(111)
        self._draw_figure(fig, ax, info)
        ax.tick_params(bottom=False,
                       left=False,
                       right=False,
                       top=False,
                       labelbottom=False,
                       labelleft=False,
                       labelright=False,
                       labeltop=False)
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('none')
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.close()
        return fig


    def _draw_figure(self, fig, ax, info):
        """ abstract method """
        """ DataFrameから作図 """
        raise Exception('not abstracted...')


    def _abstract_get_data_point(self, info):
        """ 座標のデータ値を取得 """
        canvas_size_x = info.canvas_size_x
        canvas_size_y = info.canvas_size_y
        x = info.drop_x
        y = info.drop_y
        x_label = info.target_col_x
        y_label = info.target_col_y

        _, scale_x = s_core.convert_drag_point2scaling_point(0, canvas_size_x, 0, x)
        _, scale_y = s_core.convert_drag_point2scaling_point(0, canvas_size_y, 0, y)

        x_value, y_value = self._get_data_point(info, scale_x, 1-scale_y)

        return '横軸 {0:<15}...：{1:<15} \n縦軸 {2:<15}...：{3:<15}'.format(
            x_label, str(x_value), y_label, str(y_value))


    def _get_data_point(self, info, scale_x, scale_y):
        """ 座標のデータ値を取得 """
        """ abstract method """
        raise Exception('not abstracted...')


    def _get_square_corner_point(self, info):
        """ 選択範囲描画用図形の座標を取得 """
        """ 必要であれば書き換える """
        return info.drag_x, info.drag_y, info.drop_x, info.drop_y

    def _abstract_get_selected_range_df(self, info, result_df):
        """ 選択された範囲内にあるレコードを抽出 """
        canvas_size_x = info.canvas_size_x
        canvas_size_y = info.canvas_size_y
        drag_x = info.drag_x
        drop_x = info.drop_x
        drag_y = info.drag_y
        drop_y = info.drop_y

        # 選択範囲のデータ取得
        x_from, x_to = s_core.convert_drag_point2scaling_point(0, canvas_size_x, drag_x, drop_x)
        y_from, y_to = s_core.convert_drag_point2scaling_point(0, canvas_size_y, drag_y, drop_y)
        selected_range_df = self._get_selected_range_df(info, x_from, x_to, 1-y_to, 1-y_from)

        # 選択済みのDataFrameと統合
        result_df = pd.concat([result_df, selected_range_df], axis=0).drop_duplicates()

        return result_df


    def _get_selected_range_df(self, info, scale_x_from, scale_x_to, scale_y_from, scale_y_to):
        """ 選択された範囲内にあるレコードを抽出 """
        """ abstract method """
        raise Exception('not abstracted...')
