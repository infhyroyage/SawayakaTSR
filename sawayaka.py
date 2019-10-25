# coding: utf-8

from datetime import datetime
import folium as flm
from googlemaps import Client


class Sawayaka(object):
    """
    さわやかの各店舗の情報を管理するクラス

    Attributes
    ----------
    _directions : list
        各店舗間の経路情報の行列
        対角成分はNoneとする
    """

    # 各店舗の住所
    _ADDRESSES = [
        "〒412-0026 静岡県御殿場市東田中984−1",             # 御殿場インター店
        "〒419-0122 静岡県田方郡函南町上沢130−1",           # 函南店
        "〒411-0942 静岡県駿東郡長泉町中土狩340−5",         # 長泉店
        "〒410-0042 静岡県沼津市神田町6番26号",             # 沼津学園通り店
        "〒417-0045 静岡県富士市錦町1丁目11-16",            # 富士錦店
        "〒419-0202 静岡県富士市久沢847-11",                # 富士鷹岡店
        "〒420-0913 静岡県静岡市葵区瀬名川2丁目39番37号",   # 静岡瀬名川店
        "〒420-8508 静岡県静岡市葵区鷹匠一丁目1番1号",      # 新静岡セノバ店
        "〒422-8005 静岡県静岡市駿河区池田634-1",           # 静岡池田店
        "〒422-8051 静岡県静岡市駿河区中野新田387-1",       # 静岡インター店
        "〒425-0035 静岡県焼津市東小川7-17-12",             # 焼津店
        "〒426-0031 静岡県藤枝市築地520-1",                 # 藤枝築地店
        "〒427-0058 静岡県島田市祇園町8912-2",              # 島田店
        "〒421-0301 静岡県榛原郡吉田町住吉696-1",           # 吉田店
        "〒439-0031 静岡県菊川市加茂6088",                  # 菊川本店
        "〒436-0020 静岡県掛川市矢崎町3-15",                # 掛川インター店
        "〒436-0043 静岡県掛川市大池3001-1",                # 掛川本店
        "〒437-0064 静岡県袋井市川井70-1",                  # 袋井本店
        "〒438-0071 静岡県磐田市今之浦4丁目4-6",            # 磐田本店
        "〒438-0834 静岡県磐田市森下1002-3",                # 豊田店
        "〒435-0042 静岡県浜松市東区篠ケ瀬町1232",          # 浜松篠ヶ瀬店
        "〒435-0057 静岡県浜松市東区中田町126-1",           # 浜松中田店
        "〒431-3122 静岡県浜松市東区有玉南町547-1",         # 浜松有玉店
        "〒434-0041 静岡県浜松市浜北区平口2926-1",          # 浜北店
        "〒431-1304 静岡県浜松市北区細江町中川5443-1",      # 細江本店
        "〒433-8125 静岡県浜松市中区和合町193-14",          # 浜松和合店
        "〒433-8118 静岡県浜松市中区高丘西3丁目46-12",      # 浜松高丘店
        "〒432-8002 静岡県浜松市中区富塚町439-1",           # 浜松富塚店
        "〒432-8023 静岡県浜松市中区鴨江3-10-1",            # 浜松鴨江店
        "〒430-8588 静岡県浜松市中区砂山町320-2",		   # 浜松遠鉄店
        "〒430-0846 静岡県浜松市南区白羽町636-1",           # 浜松白羽店
        "〒432-8065 静岡県浜松市南区高塚町4888-11",         # 浜松高塚店
        "〒431-0301 静岡県湖西市新居町中之郷4007-1"         # 新居湖西店
    ]


    # folium.PolyLine()でセットする線の色
    _LINE_COLORS = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]


    def __init__(self, apiKey: str):
        """
        コンストラクタ

        Parameters
        ----------
        apiKey : str
            Google Mapsクライアントに接続するAPI key

        Notes
        -----
        (32 + 31 + ... + 2 + 1)回Google Maps APIを実行して通信を行う
        """

        # 各店舗間の経路情報の行列の初期化
        self._directions = []

        # Google Mapsクライエントの初期化
        client = Client(key=apiKey)

        # Google Maps APIを用いて、各店舗間の経路情報の行列をセット
        for i in range(len(Sawayaka._ADDRESSES)):
            directions_tmp = []

            for j in range(len(Sawayaka._ADDRESSES)):
                if i < j:
                    # 上三角成分の場合は、Google Maps APIを実行して追加
                    result = client.directions(
                                origin=Sawayaka._ADDRESSES[i],
                                destination=Sawayaka._ADDRESSES[j],
                                mode="driving",
                                alternatives=False
                            )
                    directions_tmp.append(result[0]['legs'][0])
                elif i > j:
                    # 下三角成分の場合は、上三角成分をそのままコピー
                    directions_tmp.append(self._directions[j][i])
                else:
                    # 対角成分の場合は、Noneを追加
                    directions_tmp.append(None)
            
            self._directions.append(directions_tmp)
    

    def get_cost_matrix(self):
        """
        各店舗間の移動時間(単位:秒)で表わされたコスト行列を取得する

        Returns
        -------
        costMatrix : list
            コスト行列
            対角成分はNoneとする
        """

        return  [[self._directions[i][j]['duration']['value']
                    if self._directions[i][j] is not None
                    else None
                    for j in range(len(self._directions[i]))]
                for i in range(len(self._directions))]
    

    def draw_map(self, route: list, fileName: str):
        """
        指定された巡回ルートを地図上にhtml形式で出力する

        Parameters
        ----------
        route : list
            さわやか33店舗の巡回ルート
        fileName : str
            pngファイル名(拡張子除く)
        """

        # 静岡県を俯瞰したマップインスタンスの初期化
        foliumMap = flm.Map(location=[35.1199454,138.0443639], zoom_start=10)

        # 各店舗間をマーカーでマップインスタンスに追加
        flm.Marker([self._directions[0][1]['start_location']['lat'], self._directions[0][1]['start_location']['lng']]).add_to(foliumMap)
        for i in range(1, len(self._directions)):
            flm.Marker([self._directions[0][i]['end_location']['lat'], self._directions[0][i]['end_location']['lng']]).add_to(foliumMap)

        # 各店舗間のルートを線でマップインスタンスに追加
        for i in range(len(route) - 1):
            # 出発地の店舗のインデックスを取得
            start = route[i]
            # 到着地の店舗のインデックスを取得
            goal = route[i + 1]

            # 各店舗間のルートにおける曲がり角の位置リストを取得
            locations = [[step['start_location']['lat'], step['start_location']['lng']] for step in self._directions[start][goal]['steps']]
            locations.append([self._directions[start][goal]['end_location']['lat'], self._directions[start][goal]['end_location']['lng']])

            # 曲がり角の位置を描いた線を追加
            color = Sawayaka._LINE_COLORS[i % len(Sawayaka._LINE_COLORS)]
            flm.PolyLine(locations, color=color).add_to(foliumMap)
        
        # html形式で出力
        foliumMap.save(str(fileName) + ".html")
