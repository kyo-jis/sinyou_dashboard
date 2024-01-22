import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# CSVファイルから銘柄情報を読み込む関数
def load_csv_data():
    # CSVファイルをアップロード
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

    if uploaded_file is not None:
        # アップロードされたファイルをPandas DataFrameに読み込む
        df = pd.read_csv(uploaded_file)

        # コード列を整数型に変換
        df['コード'] = pd.to_numeric(df['コード'], errors='coerce').astype('Int64')

        return df
    else:
        return None

# SQLiteデータベースからデータを読み込む関数
def load_database_data():
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect("data.db")  # データベース名は適切に変更してください

        # データを読み込む
        df = pd.read_sql("SELECT * FROM oga", conn)

        # データベース接続を閉じる
        conn.close()

        return df
    except Exception as e:
        st.error(f"データベースからの読み込みエラー: {e}")
        return None

def main():
    # Streamlitアプリのタイトルを設定
    st.title("銘柄情報とデータベースのグラフ表示アプリ")

    # CSVファイルから銘柄情報を読み込む
    csv_df = load_csv_data()

    # データベースからデータを読み込む
    db_df = load_database_data()

    if csv_df is not None and db_df is not None:
        # 銘柄を選択するドロップダウンメニューを表示
        selected_stock_code = st.text_input("銘柄コードを入力してください:")

        # 入力された銘柄コードに基づいて情報を表示
        if selected_stock_code:
            selected_stock_code = int(selected_stock_code)  # 文字列から整数に変換

            # CSVファイルからの情報表示
            selected_stock_info_csv = csv_df[csv_df['コード'] == selected_stock_code]
            if not selected_stock_info_csv.empty:
                st.write("# CSVファイルからの情報:")
                st.write(f"## {selected_stock_info_csv.iloc[0]['銘柄名称']} の情報:")
                for column in ['コード', '市場・商品区分', '33業種区分', '現在値', '出来高', '売買代金',
                               '時価総額', '逆日歩', '信用倍率', '貸借倍率', '決算発表日', 'PER', 'PBR',
                               '配当', '配当落日', '中配落日', '権利落日', '四季報', '株探', 'ミンカブ',
                               '株予報', 'ヤフー']:
                    st.write(f"**{column}**: {selected_stock_info_csv.iloc[0][column]}")

            # データベースからの情報表示
            selected_stock_info_db = db_df[db_df['コード'] == selected_stock_code]
            if not selected_stock_info_db.empty:
                st.write("# データベースからの情報:")
                st.dataframe(selected_stock_info_db)

            # グラフを表示するセクション
            if '制度倍率' in db_df.columns and '一般倍率' in db_df.columns:
                st.write("# グラフの表示")
                fig = px.line(selected_stock_info_db, x='日付', y=['制度倍率', '一般倍率'],
                              labels={'制度倍率': '制度倍率', '一般倍率': '一般倍率', '日付': '日付'},
                              color_discrete_map={'制度倍率': 'blue', '一般倍率': 'orange'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("データベースに '制度倍率' または '一般倍率' の列が存在しません。")

    else:
        st.warning("CSVファイルまたはデータベースが正しく読み込まれていません。")

if __name__ == "__main__":
    main()
