(1)程式的原理與功能：
 原理
  運算-增減百分比
  邏輯-取得清單交集
 功能
  1.給定一定區間之歷史價格資料，利用歷史價格進行運算獲得符合條件之時間，登錄為訂單。
  2.訂單自動測試不同TP-SL的比例，獲得每個特定比例的盈利/虧損數據。

(2)使用方式
A‧ 使用者須準備、輸入以下數據：
1.歷史數據的excel(.xlsx)文檔、名稱
2.NC：與上漲/下跌程度有關，數字越小程度越猛烈
3.NCC：與判定訂單有關，數字越大越嚴格判定
4.Margin：初始投資金額
5.leverage：槓桿倍數
6.ratio_max：TP-SL的最大比例(SL/TP)
7.ratio_min：最小
8.tp_max：最大單一單TP百分比
9.tp_min：最小
10.tim：每單最大等待時間
B‧ 獲得結果：
不同TP-SL比例的結果(金額、勝率)

(3)程式的架構
#1_Import：載入所需Python資料庫
#2_Read data [Day,Time,Open,High,Low,Close]：讀取歷史數據
#3 By data find order condition：獲得訂單在歷史數據中的編號(運算、取得交集)
#4 Order to TP/SL, no more margin, certain period：決定訂單情形與不同盈利率、比例的計算

(4)開發過程
困難：將交易方法量化
 解決方法-用另一個.py檔案的function(非本project裡)，測試出現delta的比例，進而調整#3中的delta等。

(5)參考資料來源
-計算機程式課程簡報
-Tradinghero圖表
-交易平臺開發之Metatrader 4 excel檔案
-Chatgpt 指令(如(6))

(6)程式修改或增強的內容
指定排除特定時段：該時段內只進不出(2-9 GMT+8)-
Chatgpt 指令：我需要找到在原本清單中datetime在(2,0)~(9,0)中的order，並從最後獲得的long_final_indices and short_final_indices 剔除。