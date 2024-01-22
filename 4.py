import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

def load_data():
    # SQLiteデータベースに接続
    conn = sqlite3.connect("data.db")  # データベース名は適切に変更してください

    # データを読み込む
    df = pd.read_sql("SELECT * FROM oga", conn)

    # データベース接続を閉じる
    conn.close()

    return df

def main():
    # 画面をワイドに設定
    st.set_page_config(layout="wide")

    # データを読み込む
    df = load_data()

    # データフレームの表示
    # st.write("### データフレームの表示")
    # st.dataframe(df)

    # 銘柄コードでのフィルター
    selected_code = st.selectbox("銘柄コードを選択してください", df['銘柄コード'].unique())

    # ここで選択された銘柄コードを表示
    st.write(f"選択された銘柄コード: {selected_code}")

    # フィルタリングされたデータフレームを表示
    # st.write("### 銘柄コードでフィルター前")
    # st.dataframe(df)

    # フィルタリング
    filtered_df = df[df['銘柄コード'] == selected_code]

    # フィルタリングされたデータフレームを表示
    st.write("### 銘柄コードでフィルター後")
    st.dataframe(filtered_df)

    # グラフの表示
    st.write("### グラフの表示")
    fig = px.line(filtered_df, x='日付', y=['制度倍率', '一般倍率'],
                  labels={'制度倍率': '倍率', '一般倍率': '一般倍率', '日付': '日付'},
                  color_discrete_map={'制度倍率': 'blue', '一般倍率': 'orange'})

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
