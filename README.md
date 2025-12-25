(1)程式的原理與功能：
 原理
  運算-增減百分比
  邏輯-取得清單交集
 功能
  1.給定一定區間之歷史價格資料，利用歷史價格進行運算獲得符合條件之時間，登錄為訂單。
  2.訂單自動測試不同TP-SL的比例，獲得每個特定比例的盈利/虧損數據與圖表。

(2)使用方式
A‧ 使用者須準備、輸入以下數據：
1.歷史數據的excel(.xlsx)文檔、名稱('Enter name of the data file: ')
2.NC：與上漲/下跌程度有關，數字越小程度越猛烈('Bars for checking: ')
3.NCC：與判定訂單有關，數字越大越嚴格判定('Bars for oscillate: ')
B‧ 獲得結果：
1.交易方法在此區間的勝率
2.不同TP-SL比例的結果、最好比例、盈利/虧損程度圖表

(3)程式的架構
#1_Import：載入所需Python資料庫
#2_Read data [Day,Time,Open,High,Low,Close]：讀取歷史數據
#3 By data find order condition：獲得訂單在歷史數據中的編號

(4)開發過程
困難：將交易方法量化
 解決方法-用另一個.py檔案的function(非本project裡)，測試出現delta的比例，進而調整#3中的delta等。

(5)參考資料來源
-計算機程式課程簡報
-Tradinghero圖表
-交易平臺開發之Metatrader 4 excel檔案

(6)程式修改或增強的內容
1.指定排除特定時段：該時段內只進不出(2~9 GMT+8)-Chatgpt 指令：我需要找到在原本清單中datetime在(2,0)~(9,0)中的order，並從最後獲得的long_final_indices and short_final_indices 剔除。